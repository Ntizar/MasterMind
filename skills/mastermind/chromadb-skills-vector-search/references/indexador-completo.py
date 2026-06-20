#!/usr/bin/env python3
"""
Indexador completo de skills en ChromaDB.
Lee todos los SKILL.md de /hermes-home/skills/, extrae frontmatter,
genera embeddings con qwen3-embedding (NaN API) y los guarda en ChromaDB.

Uso:
  python3 indexador-completo.py [--dry-run] [--force]

Requiere:
  - $NAN_API en entorno
  - ChromaDB expuesto públicamente
  - pip install chromadb requests pyyaml
"""

import os
import sys
import json
import time
import hashlib
from pathlib import Path

import yaml
import requests
import chromadb

# Configuración
NAN_API = os.environ.get("NAN_API")
if not NAN_API:
    print("ERROR: $NAN_API no está definida")
    sys.exit(1)

CHROMA_HOST = os.environ.get("CHROMA_HOST", "chromadb-ntizar.apps.nan.builders")
CHROMA_PORT = int(os.environ.get("CHROMA_PORT", "80"))
SKILLS_DIR = Path(os.environ.get("SKILLS_DIR", "/hermes-home/skills"))
COLLECTION_NAME = "mastermind-skills"
EMBEDDING_MODEL = "qwen3-embedding"
BATCH_SIZE = 10  # skills por lote para evitar rate limits

# Cache de embeddings para no repetir llamadas API
EMBEDDING_CACHE = {}


def get_embedding(text, max_retries=3):
    """Genera embedding de un texto usando qwen3-embedding."""
    # Truncar si es muy largo (~8K tokens ≈ 32000 chars)
    if len(text) > 30000:
        text = text[:30000]
    
    cache_key = hashlib.md5(text.encode()).hexdigest()
    if cache_key in EMBEDDING_CACHE:
        return EMBEDDING_CACHE[cache_key]
    
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
            embedding = data["data"][0]["embedding"]
            EMBEDDING_CACHE[cache_key] = embedding
            return embedding
        except Exception as e:
            if attempt < max_retries - 1:
                wait = 2 ** attempt
                print(f"  ⚠️  Error en embedding (intento {attempt+1}): {e}. Esperando {wait}s...")
                time.sleep(wait)
            else:
                print(f"  ❌ Error en embedding tras {max_retries} intentos: {e}")
                return None


def extract_skill_info(skill_path):
    """Lee un SKILL.md y extrae frontmatter + contenido relevante."""
    content = Path(skill_path).read_text(encoding="utf-8")
    
    # Parsear frontmatter YAML
    frontmatter = {}
    body = content
    
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                frontmatter = yaml.safe_load(parts[1]) or {}
                body = parts[2].strip()
            except yaml.YAMLError:
                frontmatter = {}
    
    nombre = frontmatter.get("name", skill_path.parent.name)
    descripcion = frontmatter.get("description", "")
    tags = frontmatter.get("tags", [])
    version = frontmatter.get("version", "unknown")
    categoria = skill_path.parent.parent.name if skill_path.parent.parent.name != "skills" else "general"
    
    # Construir documento para embedding: nombre + descripción + tags + contenido relevante
    documento = f"{nombre}\n{descripcion}\n{' '.join(tags)}\n{body[:5000]}"
    
    metadata = {
        "nombre": nombre,
        "categoria": categoria,
        "tags": ",".join(tags) if isinstance(tags, list) else str(tags),
        "version": version,
        "descripcion": descripcion[:500] if descripcion else "",
        "ruta": str(skill_path),
        "prioridad": "HIGH" if categoria in ("mastermind", "multi-agent") else "MEDIUM"
    }
    
    return {
        "id": nombre,
        "embedding_text": documento,
        "metadata": metadata,
        "documento": body[:2000]  # documento de búsqueda más corto
    }


def index_all_skills(dry_run=False, force=False):
    """Indexa todos los skills en ChromaDB."""
    print(f"🔍 Escaneando skills en {SKILLS_DIR}...")
    
    # Encontrar todos los SKILL.md
    skill_files = list(SKILLS_DIR.rglob("SKILL.md"))
    print(f"📚 Encontrados {len(skill_files)} skills")
    
    if dry_run:
        print("\n🏃 Dry-run: mostrando lo que se indexaría")
        for sf in sorted(skill_files):
            info = extract_skill_info(sf)
            print(f"  • {info['id']} ({info['metadata']['categoria']})")
        print(f"\nTotal: {len(skill_files)} skills")
        return
    
    # Conectar a ChromaDB
    print(f"🔗 Conectando a ChromaDB en {CHROMA_HOST}:{CHROMA_PORT}...")
    try:
        client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        client.heartbeat()  # Verificar conexión
        print("✅ Conexión establecida")
    except Exception as e:
        print(f"❌ No se pudo conectar a ChromaDB: {e}")
        print("   ¿Está expuesto públicamente?")
        sys.exit(1)
    
    # Obtener o crear colección
    if force:
        try:
            client.delete_collection(COLLECTION_NAME)
            print(f"🗑️  Colección '{COLLECTION_NAME}' eliminada (force=True)")
        except:
            pass
    
    coleccion = client.get_or_create_collection(COLLECTION_NAME)
    
    # Obtener skills ya indexados
    existing = set(coleccion.get()["ids"]) if coleccion.count() > 0 else set()
    print(f"📊 Skills ya indexados: {len(existing)}")
    
    # Indexar en lotes
    nuevos = 0
    actualizados = 0
    errores = 0
    
    for i, sf in enumerate(sorted(skill_files)):
        info = extract_skill_info(sf)
        
        if info["id"] in existing and not force:
            continue  # Ya indexado, saltar
        
        print(f"  [{i+1}/{len(skill_files)}] {info['id']}...", end=" ", flush=True)
        
        embedding = get_embedding(info["embedding_text"])
        if embedding is None:
            print("❌")
            errores += 1
            continue
        
        try:
            if info["id"] in existing:
                # Actualizar
                coleccion.update(
                    ids=[info["id"]],
                    embeddings=[embedding],
                    metadatas=[info["metadata"]],
                    documents=[info["documento"]]
                )
                actualizados += 1
                print("🔄")
            else:
                # Añadir
                coleccion.add(
                    ids=[info["id"]],
                    embeddings=[embedding],
                    metadatas=[info["metadata"]],
                    documents=[info["documento"]]
                )
                nuevos += 1
                print("✅")
        except Exception as e:
            print(f"❌ {e}")
            errores += 1
        
        # Rate limiting
        if (i + 1) % BATCH_SIZE == 0:
            time.sleep(1)
    
    # Resumen
    total = coleccion.count()
    print(f"\n📊 Resumen:")
    print(f"  • Nuevos: {nuevos}")
    print(f"  • Actualizados: {actualizados}")
    print(f"  • Errores: {errores}")
    print(f"  • Total en colección: {total}")
    
    # Mostrar distribución por categoría
    all_meta = coleccion.get()["metadatas"]
    cats = {}
    for m in all_meta:
        c = m.get("categoria", "unknown")
        cats[c] = cats.get(c, 0) + 1
    print(f"\n📂 Distribución por categoría:")
    for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  • {cat}: {count}")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    force = "--force" in sys.argv
    
    index_all_skills(dry_run=dry_run, force=force)