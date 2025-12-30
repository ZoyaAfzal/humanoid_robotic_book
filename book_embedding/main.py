import requests
import xml.etree.ElementTree as ET
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import trafilatura
import cohere
import re
import os

# -------------------------------------
# CONFIG
# Your Deployment Link:
SITEMAP_URL = "https://zoyaafzal.github.io/humanoid_robotic_book/sitemap.xml"
COLLECTION_NAME = "humanoid_robotic_book"

cohere_client = cohere.Client("QVVViq3UKczgO0P7QZ302I7xk8JsUmWfrsiEbw4o")
EMBED_MODEL = "embed-english-v3.0"

# Connect to Qdrant Cloud
qdrant = QdrantClient(
    url="https://fd51812c-3541-4d56-aa03-7db87f4beba4.us-east4-0.gcp.cloud.qdrant.io:6333", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.ha03izlu7nPCmVy74eZr20UOmEVQiCIQ3TaFx03zhNQ",
)


# -------------------------------------
# Step 1 — URL → Markdown candidates
# -------------------------------------
def markdown_candidates(url):
    prefix = "https://zoyaafzal.github.io/humanoid_robotic_book"
    raw_base = "https://raw.githubusercontent.com/ZoyaAfzal/humanoid_robotic_book/main"

    if not url.startswith(prefix):
        return []

    path = url.replace(prefix, "").strip("/")
    if not path:
        return []

    return [
        f"{raw_base}/{path}.md",
        f"{raw_base}/{path}/README.md",
        f"{raw_base}/{path}/index.md",
    ]

# -------------------------------------
# Step 2 — Fetch Markdown
# -------------------------------------
import os

def fetch_markdown_local(url):
    """
    Convert GitHub Pages URL to local Markdown path
    """
    prefix = "https://zoyaafzal.github.io/humanoid_robotic_book"
    path = url.replace(prefix, "").strip("/")
    candidates = [
        f"./docs/{path}.md",
        f"./docs/{path}/README.md",
        f"./docs/{path}/index.md",
    ]
    for c in candidates:
        if os.path.exists(c):
            with open(c, "r", encoding="utf-8") as f:
                return f.read()
    return None



def fetch_text_from_html(url):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        html = resp.text
        text = trafilatura.extract(html)
        if text:
            return text.strip()
    except requests.exceptions.Timeout:
        print(f"  ⚠️ Timeout fetching HTML: {url}")
    except Exception as e:
        print(f"  ⚠️ Error fetching HTML: {url}: {e}")
    return None

import requests

def fetch_markdown_github(url):
    for candidate in markdown_candidates(url):
        try:
            resp = requests.get(candidate, timeout=15)
            if resp.status_code == 200:
                return resp.text
        except Exception:
            continue
    return None


# -------------------------------------
# Step 3 — Clean Markdown
# -------------------------------------
def clean_markdown(md):
    md = re.sub(r"^---.*?---", "", md, flags=re.DOTALL)  # frontmatter
    md = re.sub(r"```.*?```", "", md, flags=re.DOTALL)    # code blocks
    md = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", md)      # links
    return md.strip()

# -------------------------------------
# Step 4 — Chunk text
# -------------------------------------
def chunk_text(text, max_chars=1200):
    chunks = []
    text = text.strip()
    while len(text) > max_chars:
        split = text.rfind("\n\n", 0, max_chars)
        if split == -1:
            split = text.rfind(". ", 0, max_chars)
            if split == -1:
                split = max_chars
        chunks.append(text[:split].strip())
        text = text[split:].strip()
    if text:
        chunks.append(text)
    return chunks

# -------------------------------------
# Step 5 — Embed
# -------------------------------------
def embed(text):
    try:
        text = text[:3000]  # Cohere safe limit
        response = cohere_client.embed(
            model=EMBED_MODEL,
            input_type="search_document",
            texts=[text],
        )
        return response.embeddings[0]
    except Exception as e:
        print(f"  ❌ Embedding failed: {e}")
        return None

# -------------------------------------
# Step 6 — Qdrant collection
# -------------------------------------
def create_collection():
    try:
        if qdrant.collection_exists(COLLECTION_NAME):
            print("✔️ Qdrant collection exists")
            return
        print("🆕 Creating Qdrant collection...")
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
        )
    except Exception as e:
        print(f"  ❌ Failed to create collection: {e}")

# -------------------------------------
# Step 7 — Save chunk
# -------------------------------------
def save_chunk_to_qdrant(chunk, chunk_id, url):
    vector = embed(chunk)
    if vector is None:
        print(f"  ⚠️ Skipping chunk {chunk_id} due to embedding failure")
        return
    try:
        qdrant.upsert(
            collection_name=COLLECTION_NAME,
            points=[PointStruct(id=chunk_id, vector=vector, payload={"url": url, "text": chunk})]
        )
    except Exception as e:
        print(f"  ❌ Failed to save chunk {chunk_id}: {e}")

# -------------------------------------
# Step 8 — Sitemap fetch
# -------------------------------------
def get_all_urls(sitemap_url):
    try:
        resp = requests.get(sitemap_url, timeout=15)
        resp.raise_for_status()
        root = ET.fromstring(resp.text)
        urls = [child.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text.strip()
                for child in root if child.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc") is not None]
        print(f"\nFOUND {len(urls)} URLS")
        return urls
    except Exception as e:
        print(f"❌ Failed to fetch sitemap: {e}")
        return []

# -------------------------------------
# Step 9 — Main ingestion pipeline
# -------------------------------------
def ingest_book():
    urls = get_all_urls(SITEMAP_URL)
    create_collection()
    global_id = 1

    for url in urls:
        print(f"\n🔗 Processing: {url}")
        # Use local Markdown only
        md = fetch_markdown_github(url)
        if not md:
            print(f"  ⚠️ No markdown found for {url}, skipping")
            continue

        clean_text = clean_markdown(md)
        chunks = chunk_text(clean_text)
        print(f"  📦 {len(chunks)} chunks")

        for ch in chunks:
            save_chunk_to_qdrant(ch, global_id, url)
            print(f"  ✅ Saved chunk {global_id}")
            global_id += 1

    print(f"\n🎉 Markdown ingestion completed! Total chunks stored: {global_id-1}")



# -------------------------------------
# RUN
# -------------------------------------
if __name__ == "__main__":
    ingest_book()
