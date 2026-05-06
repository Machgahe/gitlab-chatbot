import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
model = SentenceTransformer("all-MiniLM-L6-v2")
client_db = chromadb.PersistentClient(path="./db")
collection = client_db.get_or_create_collection(name="gitlab_handbook")

def ask(question):
    # Step 1: Convert question to embedding
    question_embedding = model.encode([question]).tolist()

    # Step 2: Find top 3 most relevant chunks from ChromaDB
    results = collection.query(
        query_embeddings=question_embedding,
        n_results=3
    )

    chunks = results["documents"][0]
    sources = [m["url"] for m in results["metadatas"][0]]

    # Step 3: Build prompt with context
    context = "\n\n".join(chunks)
    prompt = f"""You are a helpful assistant for GitLab employees.
Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't have information on that."

Context:
{context}

Question: {question}

Answer:"""

    # Step 4: Ask Groq (using Llama 3)
    response = client_groq.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": list(set(sources))
    }

if __name__ == "__main__":
    print("GitLab Chatbot — type 'quit' to exit\n")
    while True:
        question = input("You: ")
        if question.lower() == "quit":
            break
        result = ask(question)
        print(f"\nBot: {result['answer']}")
        print(f"Sources: {result['sources']}\n")