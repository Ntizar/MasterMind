#!/usr/bin/env python3
"""
Indexar skills en ChromaDB v2 — usa el cliente Python chromadb (API v2).
Usa qwen3-embedding vía API NaN.

Uso: python3 indexar-skills.py [--reset]
"""

import os
import sys
import json
import glob
import time
import requests
import logging
from pathlib import Path

# Config
CHROMA_URL = "http://localhost:8000"
NAN_API_KEY = os.environ.get("NAN_API", "")
NAN_EMBEDDING_MODEL = "qwen3-embedding"
SKILLS_DIR = "agent/skills"
COLLECTION_NAME = "mastermind-skills"
LOG_FILE = "/tmp/indexar-skills.log"

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
log = logging.getLogger(__name__)


def get_embedding(text):
    """Generar embedding vía API NaN."""
    if not NAN_API_KEY:
        log.error("NAN_API no configurada")
        return None
    
    for attempt in range(3):
        try:
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
            
            if resp.status_code == 200:
                data = resp.json()
                return data["data"][0]["embedding"]
            elif resp.status_code == 429:
                wait = 2 ** attempt
                log.warning(f"Rate limit (429), esperando {wait}s...")
                time.sleep(wait)
            else:
                log.error(f"Error {resp.status_code}: {resp.text[:200]}")
                return None
        except Exception as e:
            log.error(f"Excepción: {e}")
            if attempt < 2:
                time.sleep(2)
    
    return None


def extract_skill_info(skill_dir):
    """Extraer info de un skill desde su SKILL.md."""
    skill_path = Path(skill_dir) / "SKILL.md"
    if not skill_path.exists():
        return None
    
    content = skill_path.read_text(encoding="utf-8", errors="replace")
    
    name = skill_path.parent.name
    description = ""
    tags = ""
    version = ""
    category = ""
    
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]
            
            for line in frontmatter.split("\n"):
                line = line.strip()
                if line.startswith("name:"):
                    name = line.split(":", 1)[1].strip().strip('"').strip("'")
                elif line.startswith("description:"):
                    desc = line.split(":", 1)[1].strip().strip('"').strip("'")
                    if desc:
                        description = desc
                elif line.startswith("tags:"):
                    tags_part = line.split(":", 1)[1].strip()
                    if tags_part.startswith("["):
                        try:
                            tags_list = json.loads(tags_part)
                            tags = ",".join(tags_list)
                        except:
                            tags = tags_part.strip("[]").replace('"', '').replace("'", '')
                    else:
                        tags = tags_part
                elif line.startswith("version:"):
                    version = line.split(":", 1)[1].strip().strip('"').strip("'")
                elif line.startswith("category:"):
                    category = line.split(":", 1)[1].strip().strip('"').strip("'")
    
    if not description:
        body_lines = content.split("\n")
        for line in body_lines:
            line = line.strip()
            if line and not line.startswith("---") and not line.startswith("#"):
                description = line[:200]
                break
    
    if not category:
        parent_dir = Path(skill_dir).parent.name
        category = parent_dir if parent_dir != "skills" else "general"
    
    embed_text = f"{name} {description} {tags}"
    
    body = content
    if "---" in content:
        parts = content.split("---", 2)
        if len(parts) >= 3:
            body = parts[2]
    
    sections = []
    current_section = ""
    for line in body.split("\n"):
        if line.startswith("## "):
            if current_section:
                sections.append(current_section)
            current_section = line
        elif current_section:
            if len(current_section) < 500:
                current_section += " " + line.strip()
    
    if current_section:
        sections.append(current_section)
    
    for s in sections[:5]:
        if len(embed_text) < 2000:
            embed_text += " " + s[:300]
    
    # Usar path relativo como ID único para evitar colisiones por nombre duplicado
    rel_path = str(Path(skill_dir).relative_to(SKILLS_DIR))
    unique_id = rel_path.replace("/", "--")
    
    return {
        "id": unique_id,
        "name": name,
        "description": description[:500],
        "tags": tags[:500],
        "version": version or "1.0.0",
        "category": category,
        "embed_text": embed_text[:3000],
        "content_preview": body[:1000],
        "path": str(skill_path),
        "unique_id": unique_id
    }


def main():
    import chromadb
    
    reset = "--reset" in sys.argv
    
    log.info("=" * 50)
    log.info("🔍 INDEXADOR DE SKILLS v2 (chromadb client)")
    log.info("=" * 50)
    
    log.info(f"Buscando skills en {SKILLS_DIR}...")
    skill_files = sorted(glob.glob(f"{SKILLS_DIR}/**/SKILL.md", recursive=True))
    log.info(f"  → {len(skill_files)} SKILL.md encontrados")
    
    skills = []
    for sf in skill_files:
        info = extract_skill_info(os.path.dirname(sf))
        if info:
            skills.append(info)
    
    log.info(f"  → {len(skills)} skills válidos")
    
    # Conectar con ChromaDB usando el cliente Python (API v2)
    log.info("\n📦 Conectando con ChromaDB...")
    client = chromadb.HttpClient(host="localhost", port=8000)
    
    if reset:
        log.info("\n🔄 Reset: eliminando colección existente...")
        try:
            client.delete_collection(COLLECTION_NAME)
            log.info("  → Colección eliminada")
        except Exception as e:
            log.info(f"  → No existía: {e}")
    
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )
    log.info(f"  → Colección: {COLLECTION_NAME} (actual: {collection.count()} docs)")
    
    # Verificar qué IDs ya existen
    existing = set()
    if collection.count() > 0:
        try:
            existing_data = collection.get(include=[])
            existing = set(existing_data["ids"])
            log.info(f"  → {len(existing)} IDs ya indexados")
        except:
            pass
    
    # Filtrar skills nuevos o modificados
    new_skills = [s for s in skills if s["id"] not in existing]
    log.info(f"  → {len(new_skills)} skills nuevos por indexar")
    
    if not new_skills:
        log.info("\n✅ Todo ya indexado. Nada nuevo.")
        return
    
    log.info(f"\n🧠 Generando embeddings con {NAN_EMBEDDING_MODEL}...")
    skills_with_embeddings = []
    
    for i, skill in enumerate(new_skills):
        log.info(f"  [{i+1}/{len(new_skills)}] {skill['name']}...")
        
        if i > 0:
            time.sleep(1.5)
        
        embedding = get_embedding(skill["embed_text"])
        if embedding:
            skill["embedding"] = embedding
            skills_with_embeddings.append(skill)
            log.info(f"    ✅ ({len(embedding)} dims)")
        else:
            log.warning(f"    ❌ Falló embedding")
    
    log.info(f"\n  → {len(skills_with_embeddings)}/{len(new_skills)} skills con embedding")
    
    if not skills_with_embeddings:
        log.error("No se generó ningún embedding")
        sys.exit(1)
    
    # Añadir en lotes
    log.info("\n💾 Guardando en ChromaDB...")
    batch_size = 10
    for i in range(0, len(skills_with_embeddings), batch_size):
        batch = skills_with_embeddings[i:i+batch_size]
        
        ids = [s["id"] for s in batch]
        embeddings = [s["embedding"] for s in batch]
        metadatas = [{
            "name": s["name"],
            "category": s["category"],
            "tags": s["tags"],
            "version": s["version"],
            "description": s["description"][:500]
        } for s in batch]
        documents = [s["embed_text"] for s in batch]
        
        collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents
        )
        
        log.info(f"  Lote {i//batch_size + 1}: {len(batch)} skills añadidos")
    
    log.info(f"\n✅ Indexación completada: {collection.count()} skills en ChromaDB")


if __name__ == "__main__":
    main()
