import json
from sentence_transformers import SentenceTransformer
from scraper import scrape_all

model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def ingest():
    print("Scraping pages...")
    pages = scrape_all()

    all_data = []
    for page in pages:
        chunks = chunk_text(page["text"])
        for chunk in chunks:
            embedding = model.encode([chunk])[0].tolist()
            all_data.append({
                "text": chunk,
                "url": page["url"],
                "embedding": embedding
            })

    with open("data.json", "w") as f:
        json.dump(all_data, f)

    print(f"Done! Saved {len(all_data)} chunks to data.json ✅")

if __name__ == "__main__":
    ingest()