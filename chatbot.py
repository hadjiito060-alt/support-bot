import chromadb
from sentence_transformers import SentenceTransformer

# تحميل نموذج الـ Embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# فتح قاعدة البيانات
client = chromadb.PersistentClient(path="db")
collection = client.get_collection("myvala")

print("=== MyVala Support Bot ===")

while True:
    question = input("\nVous : ")

    if question.lower() == "exit":
        break

    embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=1
    )

    article = results["documents"][0][0]
    title = results["metadatas"][0][0]["title"]
    url = results["metadatas"][0][0]["url"]

    print("\nBot :")
    print(title)
    print("-" * 50)
    print(article[:1200])  # عرض أول 1200 حرف
    print("\nSource :", url)