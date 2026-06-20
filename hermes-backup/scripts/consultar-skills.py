#!/usr/bin/env python3
"""
Consultar skills relevantes en ChromaDB por similitud semántica.
Usa qwen3-embedding vía API NaN + cliente Python chromadb (API v2).

Uso: python3 consultar-skills.py "texto de la consulta" [--top N] [--json]
"""

import os
import sys
import json
import requests

# Config
CHROMA_URL = "http://localhost:8000"
NAN_API_KEY = os.environ.get("NAN_API", "")
NAN_EMBEDDING_MODEL = "qwen3-embedding"
COLLECTION_NAME = "mastermind-skills"

def get_embedding(text):
    """Generar embedding vía API NaN."""
    if not NAN_API_KEY:
        print("ERROR: NAN_API no configurada", file=sys.stderr)
        sys.exit(1)
    
    resp = requests.post(
        "https://api.nan.builders/v1/embeddings",
        headers={
            "Authorization": f"Bearer {NAN_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": NAN_EMBEDDING_MODEL,
            "input": text
        },
        timeout=30
    )
    
    if resp.status_code != 200:
        print(f"ERROR embedding: {resp.status_code} {resp.text}", file=sys.stderr)
        return None
    
    data = resp.json()
    return data["data"][0]["embedding"]

def query_skills(query_text, n_results=5):
    """Buscar skills relevantes en ChromaDB usando cliente Python."""
    import chromadb
    
    # Obtener embedding de la consulta
    embedding = get_embedding(query_text)
    if not embedding:
        return None
    
    # Conectar con ChromaDB usando cliente Python (API v2)
    client = chromadb.HttpClient(host="localhost", port=8000)
    
    try:
        collection = client.get_collection(COLLECTION_NAME)
    except Exception as e:
        print(f"ERROR: colección no encontrada: {e}", file=sys.stderr)
        return None
    
    # Query
    result = collection.query(
        query_embeddings=[embedding],
        n_results=n_results,
        include=["metadatas", "distances", "documents"]
    )
    
    # Formatear resultados
    results = []
    ids = result["ids"][0]
    distances = result["distances"][0]
    metadatas = result["metadatas"][0]
    documents = result["documents"][0]
    
    for i in range(len(ids)):
        # Convertir distancia a score de similitud (1 - distance)
        similarity = 1.0 - distances[i]
        results.append({
            "name": ids[i],
            "score": round(similarity, 4),
            "category": metadatas[i].get("category", ""),
            "tags": metadatas[i].get("tags", ""),
            "description": metadatas[i].get("description", ""),
            "version": metadatas[i].get("version", ""),
            "document_preview": documents[i][:200] if documents[i] else ""
        })
    
    return results

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 consultar-skills.py 'texto de consulta' [--top N] [--json]", file=sys.stderr)
        sys.exit(1)
    
    query_text = sys.argv[1]
    n_results = 5
    
    if "--top" in sys.argv:
        idx = sys.argv.index("--top")
        if idx + 1 < len(sys.argv):
            n_results = int(sys.argv[idx + 1])
    
    # Si es modo JSON, imprimir solo JSON
    json_mode = "--json" in sys.argv
    
    results = query_skills(query_text, n_results)
    
    if not results:
        print(json.dumps({"error": "No se encontraron resultados"}))
        sys.exit(1)
    
    if json_mode:
        print(json.dumps({"results": results, "query": query_text}, ensure_ascii=False))
    else:
        print(f"\n🔍 Consulta: \"{query_text}\"")
        print(f"📊 Top {len(results)} skills relevantes:\n")
        for r in results:
            bar = "█" * int(r["score"] * 20) + "░" * (20 - int(r["score"] * 20))
            print(f"  {r['name']}")
            print(f"  [{bar}] {r['score']:.1%}")
            print(f"  📂 {r['category']}  |  🏷️  {r['tags'][:60]}")
            print(f"  {r['description'][:120]}")
            print()

if __name__ == "__main__":
    main()
