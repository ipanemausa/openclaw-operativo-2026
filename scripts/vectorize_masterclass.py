"""
vectorize_masterclass.py — OpenClaw RAG Indexer for Masterclass Video
======================================================================
Reads all .ASS subtitle files from the 30-minute masterclass render,
extracts clean text per module, generates 768-dim embeddings via
Google text-embedding-004, and upserts into Qdrant for semantic search.

Run BEFORE Firebase deploy for full RAG-ready content at deploy time.
Usage:
    python scripts/vectorize_masterclass.py
"""

import os
import re
import sys
import logging
import uuid
from pathlib import Path

import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, UpdateStatus

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [VECTORIZER] %(message)s"
)
logger = logging.getLogger("vectorizer")

# ── Config ─────────────────────────────────────────────────────────────────
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
COLLECTION = "masterclass_30min_2026"
EMBEDDING_DIM = 768
EMBEDDING_MODEL = "models/text-embedding-004"

OUT_DIR = Path(r"C:\openclaw\hb-jewelry\public\videos\youtube_30min_masterclass")

# ── Helpers ─────────────────────────────────────────────────────────────────


def extract_text_from_ass(ass_path: Path) -> str:
    """Strip ASS formatting tags and return clean dialogue text."""
    text_lines = []
    with open(ass_path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("Dialogue:"):
                # Extract text after the 9th comma
                parts = line.split(",", 9)
                if len(parts) == 10:
                    raw = parts[9].strip()
                    # Remove ASS override tags {\\pos(...)} {\\k...} etc.
                    clean = re.sub(r'\{[^}]*\}', '', raw)
                    text_lines.append(clean.strip())
    return " ".join(text_lines)


def chunk_text(text: str, max_tokens: int = 200) -> list[str]:
    """Chunk text by word count approximation."""
    words = text.split()
    chunks = []
    current = []
    for word in words:
        current.append(word)
        if len(current) >= max_tokens:
            chunks.append(" ".join(current))
            current = []
    if current:
        chunks.append(" ".join(current))
    return chunks


def get_embedding(text: str) -> list[float]:
    """Generate 768-dim embedding using Google text-embedding-004."""
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text,
        task_type="RETRIEVAL_DOCUMENT"
    )
    return result["embedding"]


def ensure_collection(client: QdrantClient):
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION not in existing:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE)
        )
        logger.info(f"Collection '{COLLECTION}' created in Qdrant.")
    else:
        logger.info(f"Collection '{COLLECTION}' already exists — upserting.")


def main():
    print("=" * 65)
    print("OPENCLAW MASTERCLASS VECTORIZER — 768-dim RAG Indexing")
    print("=" * 65)

    if not GOOGLE_API_KEY:
        logger.error("GEMINI_API_KEY not set. Check .openclaw-master.env")
        sys.exit(1)

    genai.configure(api_key=GOOGLE_API_KEY)

    # Connect to Qdrant
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    ensure_collection(client)

    # Firebase Hosting base URL for video links
    base_video_url = "https://hb-jewelry-cloud-2026-2dff9.web.app/videos/youtube_30min_masterclass"

    points = []
    total_chunks = 0

    for lang in ["es", "en"]:
        for mod_id in range(1, 7):
            ass_file = OUT_DIR / f"mod_{mod_id}_{lang}.ass"
            if not ass_file.exists():
                logger.warning(f"[SKIP] {ass_file.name} not found.")
                continue

            text = extract_text_from_ass(ass_file)
            if not text.strip():
                logger.warning(f"[SKIP] {ass_file.name} has no dialogue text.")
                continue

            chunks = chunk_text(text, max_tokens=200)
            logger.info(f"Module {mod_id} ({lang.upper()}): {len(chunks)} chunk(s) — generating embeddings...")

            for chunk_idx, chunk in enumerate(chunks):
                try:
                    embedding = get_embedding(chunk)
                    point = PointStruct(
                        id=str(uuid.uuid4()),
                        vector=embedding,
                        payload={
                            "lang": lang,
                            "module_id": mod_id,
                            "chunk_index": chunk_idx,
                            "text": chunk,
                            "source": "masterclass_30min_2026",
                            "video_url": f"{base_video_url}/youtube_30min_masterclass_{'full_1080p' if lang == 'es' else 'en_1080p'}.mp4",
                            "ass_file": ass_file.name,
                        }
                    )
                    points.append(point)
                    total_chunks += 1
                except Exception as e:
                    logger.error(f"  Embedding failed for chunk {chunk_idx}: {e}")

    # Upsert all points to Qdrant
    if points:
        result = client.upsert(collection_name=COLLECTION, points=points)
        if result.status == UpdateStatus.COMPLETED:
            logger.info(f"[OK] {total_chunks} chunks indexed in Qdrant collection '{COLLECTION}'.")
        else:
            logger.error(f"[FAIL] Qdrant upsert status: {result.status}")
    else:
        logger.warning("No points generated. Check ASS files.")

    print("=" * 65)
    print(f"VECTORIZATION COMPLETE: {total_chunks} semantic chunks indexed.")
    print(f"Collection: {COLLECTION} | Qdrant: {QDRANT_HOST}:{QDRANT_PORT}")
    print("=" * 65)


if __name__ == "__main__":
    main()
