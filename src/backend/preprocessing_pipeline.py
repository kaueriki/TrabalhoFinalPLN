import re
import unicodedata

STOPWORDS = set([
    "a", "o", "os", "as", "de", "da", "do", "das", "dos", "em", "um", "uma",
    "para", "com", "que", "por", "na", "no", "nas", "nos", "se", "e"
])


def limpar_texto(texto):

    if not isinstance(texto, str):
        return ""

    # Normaliza acentos
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("utf-8")

    # Remove caracteres que não sejam letras ou espaço
    texto = re.sub(r"[^a-zA-Z\s]", " ", texto)

    # Converte para minúsculo
    texto = texto.lower()

    # Remove espaços múltiplos
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto


def remover_stopwords(palavras):
    return [p for p in palavras if p not in STOPWORDS and len(p) > 2]


def preprocessar_corpus(lista_textos):
    textos_limpos = []
    tokens_limpos = []

    for texto in lista_textos:
        t = limpar_texto(texto)

        palavras = t.split()
        palavras = remover_stopwords(palavras)

        textos_limpos.append(" ".join(palavras))
        tokens_limpos.append(palavras)

    return {
        "textos_limpos": textos_limpos,
        "tokens": tokens_limpos
    }
