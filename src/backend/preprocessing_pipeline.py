import re
import unicodedata
import spacy
from spacy.util import is_package

MODEL_NAME = "pt_core_news_sm"

# Verifica se o modelo já está instalado
if not is_package(MODEL_NAME):
    spacy.cli.download(MODEL_NAME)

# Carrega o modelo de língua portuguesa do spaCy para lematização e stopwords
nlp = spacy.load("pt_core_news_sm")

# Obtém a lista de stopwords padrão do spaCy para o português
STOPWORDS = nlp.Defaults.stop_words

def limpar_texto(texto):
    # Garante que o texto seja uma string
    if not isinstance(texto, str):
        return ""
    
    # Remove acentos e caracteres especiais
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("utf-8")
    # Remove tudo que não for letra ou espaço
    texto = re.sub(r"[^a-zA-Z\s]", " ", texto)
    # Converte o texto para minúsculas
    texto = texto.lower()
    # Remove espaços extras
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto

# Aplica a pipeline completa de pré-processamento a uma lista de textos
def preprocessar_corpus(lista_textos):
    textos_processados = []
    tokens_processados = []

    # Itera sobre cada texto da lista
    for texto in lista_textos:
        # Aplica a limpeza inicial
        texto_limpo = limpar_texto(texto)
        
        # Processa o texto com o spaCy para obter os tokens, lemas, etc.
        doc = nlp(texto_limpo)
        
        # Realiza a lematização e remove stopwords e pontuações
        tokens = [
            token.lemma_  # Pega o lema (forma base da palavra)
            for token in doc 
            if token.text not in STOPWORDS  # Remove stopwords
            and not token.is_punct  # Remove pontuações
            and len(token.text) > 2  # Remove palavras muito curtas
        ]
        
        # Junta os tokens para formar o texto processado
        textos_processados.append(" ".join(tokens))
        # Mantém a lista de tokens para possíveis usos futuros
        tokens_processados.append(tokens)

    return textos_processados, tokens_processados
