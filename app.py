from flask import Flask, render_template, request
import chromadb
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# Charger le modèle d'embedding
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connexion à la base ChromaDB
client = chromadb.PersistentClient(path="db")
collection = client.get_collection("myvala")


@app.route("/", methods=["GET", "POST"])
def home():

    answer = ""
    question = ""

    if request.method == "POST":

        question = request.form.get("question", "").strip()

        if question:

            embedding = model.encode(question).tolist()

            results = collection.query(
                query_embeddings=[embedding],
                n_results=1
            )

            if results["documents"] and len(results["documents"][0]) > 0:

                article = results["documents"][0][0]
                metadata = results["metadatas"][0][0]

                title = metadata["title"]
                url = metadata["url"]

                answer = f"""
<h2>{title}</h2>

<p>{article}</p>

<br>

<a href="{url}" target="_blank">
📄 Voir l'article original
</a>
"""

            else:

                answer = """
Désolé, je n'ai trouvé aucune réponse dans la base de connaissances.
"""

    return render_template(
        "index.html",
        answer=answer,
        question=question
    )


if __name__ == "__main__":
    app.run(debug=True)