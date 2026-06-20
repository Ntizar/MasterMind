#!/usr/bin/env python3
"""
Consultor de skills en ChromaDB.
Recibe una consulta en texto, la vectoriza con qwen3-embedding,
busca en ChromaDB y devuelve los skills más relevantes.

Uso:
  python3 consultor-completo.py "haz un informe del mercado eléctrico"
  python3 consultor-completo.py --json "texto de búsqueda"
  python3 consultor-completo.py --top 10 "texto"

Requiere:
  - $NAN_API en entorno
  - ChromaDB expuesto públicamente
  - pip install chromadb requests
"""

import os
import sys
import json
import time
import hashlib
from pathlib import Path

import requests
import chromadb

# Configuración
NAN_API = os.environ.get("NAN_API")
if not NAN_API:
    print("ERROR: $NAN_API no está definida", file=sys.stderr)
    sys.exit(1)

CHROMA_HOST = os.environ.get("CHROMA_HOST", "chromadb-ntizar.apps.nan.builders")
CHROMA_PORT = int(os.environ.get("CHROMA_PORT", "80"))
COLLECTION_NAME = "mastermind-skills"
EMBEDDING_MODEL = "qwen3-embedding"
DEFAULT_TOP_K = 5
SCORE_THRESHOLD = 0.3  # Ignorar resultados por debajo de este score


def get_embedding(text, max_retries=3):
    """Genera embedding de un texto usando qwen3-embedding."""
    if len(text) > 30000:
        text = text[:30000]
    
    for attempt in range(max_retries):
        try:
            resp = requests.post(
                "https://api.nan.builders/v1/embeddings",
                headers={
                    "Authorization": f"Bearer {NAN_API}",
                    "Content-Type": "application/json"
                },
                json={"model": EMBEDDING_MODEL, "input": text},
                timeout=30
            )
            resp.raise_for_status()
            data = resp.json()
            return data["data"][0]["embedding"]
        except Exception as e:
            if attempt < max_retries - 1:
                wait = 2 ** attempt
                time.sleep(wait)
            else:
                print(f"Error en embedding: {e}", file=sys.stderr)
                return None


def search_skills(query, n_results=DEFAULT_TOP_K):
    """Busca skills relevantes para una consulta."""
    # Conectar a ChromaDB
    try:
        client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        client.heartbeat()
    except Exception as e:
        print(f"Error conectando a ChromaDB: {e}", file=sys.stderr)
        return []
    
    # Obtener colección
    try:
        coleccion = client.get_collection(COLLECTION_NAME)
    except Exception:
        print(f"Colección '{COLLECTION_NAME}' no encontrada", file=sys.stderr)
        return []
    
    # Generar embedding de la consulta
    query_embedding = get_embedding(query)
    if query_embedding is None:
        return []
    
    # Buscar
    try:
        results = coleccion.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
    except Exception as e:
        print(f"Error en query: {e}", file=sys.stderr)
        return []
    
    # Formatear resultados
    skills = []
    if results["ids"] and results["ids"][0]:
        for i in range(len(results["ids"][0])):
            score = 1 - results["distances"][0][i]  # Convertir distancia a similitud
            if score < SCORE_THRESHOLD:
                continue
            
            meta = results["metadatas"][0][i]
            skills.append({
                "nombre": results["ids"][0][i],
                "categoria": meta.get("categoria", "unknown"),
                "score": round(score, 4),
                "tags": meta.get("tags", ""),
                "version": meta.get("version", "unknown"),
                "descripcion": meta.get("descripcion", ""),
                "prioridad": meta.get("prioridad", "MEDIUM")
            })
    
    return skills


def format_results(skills, query=""):
    """Formatea resultados para mostrar al usuario."""
    if not skills:
        return "❌ No se encontraron skills relevantes para esta consulta."
    
    lines = [f"🔍 Resultados para: \"{query}\"", ""]
    
    for i, s in enumerate(skills, 1):
        bar = "█" * int(s["score"] * 20) + "░" * (20 - int(s["score"] * 20))
        lines.append(f"  {i}. {s['nombre']}")
        lines.append(f"     [{bar}] {s['score']:.2f}")
        lines.append(f"     📂 {s['categoria']}  |  🏷️  {s['tags']}")
        if s["descripcion"]:
            desc = s["descripcion"][:120]
            lines.append(f"     {desc}")
        lines.append("")
    
    return "\n".join(lines)


if __name__ == "__main__":
    args = sys.argv[1:]
    
    output_json = "--json" in args
    if output_json:
        args.remove("--json")
    
    top_k = DEFAULT_TOP_K
    if "--top" in args:
        idx = args.index("--top")
        if idx + 1 < len(args):
            top_k = int(args[idx + 1])
            args = args[:idx] + args[idx+2:]
    
    if not args:
        print("Uso: consultor-completo.py [--json] [--top N] \"texto de búsqueda\"")
        sys.exit(1)
    
    query = " ".join(args)
    skills = search_skills(query, n_results=top_k)
    
    if output_json:
        print(json.dumps(skills, indent=2, ensure_ascii=False))
    else:
        print(format_results(skills, query))