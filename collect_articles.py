import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.myvala.com"

response = requests.get(BASE_URL + "/knowledgebase")
soup = BeautifulSoup(response.text, "html.parser")


links = set()

for a in soup.find_all("a", href=True):
    href = a["href"]

    if href.startswith("https://www.myvala.com/info/"):
        links.add(href)

print(f"Nombre d'articles trouvés : {len(links)}")

articles = []

for url in links:
    print("Collecte :", url)

    page = requests.get(url)
    article = BeautifulSoup(page.text, "html.parser")

    title = article.title.text.strip()

    content = article.find("div", class_="sayfacontent")

    if content:
        text = content.get_text("\n", strip=True)

        articles.append({
            "title": title,
            "url": url,
            "content": text
        })

with open("articles.json", "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)

print(f"\nTerminé ! {len(articles)} articles sauvegardés.")