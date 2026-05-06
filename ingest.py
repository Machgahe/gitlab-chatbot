import chromadb
from sentence_transformers import SentenceTransformer
from scraper import scrape_all

# Load a free embedding model (downloads automatically first time, ~90MB)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Set up ChromaDB (saves locally in a folder called 'db')
client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection(name="gitlab_handbook")

def chunk_text(text, chunk_size=500):
    """Split text into chunks of ~500 words"""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def ingest():
    print("Scraping pages...")
    pages = scrape_all()

    all_chunks = []
    all_ids = []
    all_metadata = []

    for page in pages:
        chunks = chunk_text(page["text"])
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_ids.append(f"{page['url']}__chunk{i}")
            all_metadata.append({"url": page["url"]})

    print(f"Total chunks created: {len(all_chunks)}")
    print("Creating embeddings and storing in ChromaDB...")

    embeddings = model.encode(all_chunks).tolist()

    collection.add(
        documents=all_chunks,
        embeddings=embeddings,
        ids=all_ids,
        metadatas=all_metadata
    )

    print("Done! All data stored in ./db folder")

if __name__ == "__main__":
    ingest()