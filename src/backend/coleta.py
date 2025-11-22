import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

RSS_URL = "https://g1.globo.com/rss/g1/economia/"


def baixar_rss(url=RSS_URL):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "xml")
    items = soup.find_all("item")
    return items


def extrair_texto_noticia(url):
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        paragraphs = soup.select("div.mc-body p")
        texto = "\n".join([p.get_text(strip=True) for p in paragraphs])

        if not texto:
            paragraphs = soup.find_all("p")
            texto = "\n".join([p.get_text(strip=True) for p in paragraphs])

        return texto

    except Exception as e:
        print(f"Falha ao baixar notícia: {url} -> {e}")
        return ""


def coletar_noticias(limit=None):
    items = baixar_rss()
    noticias = []

    if limit:
        items = items[:limit]

    for item in items:
        titulo = item.title.text
        link = item.link.text
        data_pub = item.pubDate.text if item.pubDate else ""
        descricao = item.description.text if item.description else ""

        print(f" Baixando: {titulo}")

        texto = extrair_texto_noticia(link)

        noticias.append({
            "titulo": titulo,
            "data": data_pub,
            "descricao": descricao,
            "link": link,
            "texto": texto
        })

        time.sleep(1)

    df = pd.DataFrame(noticias)
    return df


if __name__ == "__main__":
    df = coletar_noticias(limit=5)
    print(df.head())
