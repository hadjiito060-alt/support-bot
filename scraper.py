import requests
from bs4 import BeautifulSoup

url = "https://www.myvala.com/info/installer-wordpress"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

content = soup.find("div", class_="sayfacontent")

if content:
    print(content.get_text("\n", strip=True))
else:
    print("Content not found")