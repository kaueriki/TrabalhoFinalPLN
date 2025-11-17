import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

RSS_URL = "https://g1.globo.com/rss/g1/economia/"

def get_rss_items(url):
    """Baixa e lê o RSS."""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "xml")
    items = soup.find_all("item")
    return items

def extract_article_text(url):
    """Baixa o texto principal da notícia no G1."""
    try:
        html = requests.get(url, timeout=8)
        soup = BeautifulSoup(html.text, "html.parser")

        paragraphs = soup.select("div.mc-body p")
        text = "\n".join([p.get_text(strip=True) for p in paragraphs])

        if not text:

            paragraphs = soup.find_all("p")
            text = "\n".join([p.get_text(strip=True) for p in paragraphs])

        return text
    except Exception as e:
        print("Erro ao baixar notícia:", url, e)
        return ""

def scrape_g1_economia():
    data = []

    items = get_rss_items(RSS_URL)
    print(f"Encontradas {len(items)} notícias no RSS.")

    for item in items:
        title = item.title.text
        link = item.link.text
        pub_date = item.pubDate.text if item.pubDate else None
        description = item.description.text if item.description else None

        print("Baixando:", title)
        full_text = extract_article_text(link)

        data.append({
            "title": title,
            "date": pub_date,
            "description": description,
            "link": link,
            "text": full_text
        })

        time.sleep(1)  # respeitar o servidor

    df = pd.DataFrame(data)
    df.to_csv("g1_economia_noticias.csv", index=False, encoding="utf-8")

    print("\nFinalizado! Arquivo salvo como g1_economia_noticias.csv")

if __name__ == "__main__":
    scrape_g1_economia()
