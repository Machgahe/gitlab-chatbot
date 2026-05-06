import json
import numpy as np
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
model = SentenceTransformer("all-MiniLM-L6-v2")

with open("data.json", "r") as f:
    data = json.load(f)

texts = [d["text"] for d in data]
urls = [d["url"] for d in data]
embeddings = np.array([d["embedding"] for d in data])

def cosine_similarity(a, b):
    return np.dot(b, a) / (np.linalg.norm(b, axis=1) * np.linalg.norm(a))

def ask(question):
    question_embedding = model.encode([question])[0]
    scores = cosine_similarity(question_embedding, embeddings)
    top_indices = np.argsort(scores)[-3:][::-1]

    chunks = [texts[i] for i in top_indices]
    sources = list(set([urls[i] for i in top_indices]))

    context = "\n\n".join(chunks)
    prompt = f"""You are a helpful assistant for GitLab employees.
Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't have information on that."

Context:
{context}

Question: {question}

Answer:"""

    response = client_groq.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": sources
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