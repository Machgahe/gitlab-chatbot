File Job
scraper.py Goes to GitLab's handbook website and downloads the text
ingest.py Splits that text into chunks, converts to embeddings, saves to ChromaDB
chatbot.py Takes a user question, finds relevant chunks, asks Gemini to answer
app.py The chat window UI built with Streamlit