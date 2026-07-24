import json
import chromadb
from sentence_transformers import SentenceTransformer

with open("articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="db")
collection = client.get_or_create_collection("myvala")

for i, article in enumerate(articles):
    embedding = model.encode(article["content"]).tolist()

    collection.add(
        ids=[str(i)],
        documents=[article["content"]],
        metadatas=[{
            "title": article["title"],
            "url": article["url"]
        }],
        embeddings=[embedding]
    )

print("Base créée avec succès !")