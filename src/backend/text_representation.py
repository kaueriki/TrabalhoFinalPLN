from sklearn.feature_extraction.text import CountVectorizer

 # Cria a representação Bag of Words (BoW) de uma lista de textos
def criar_bow(textos_limpos):

    # Inicializa o vetorizador com hiperparâmetros:
    # - max_features=1000: Limita o vocabulário às 1000 palavras mais frequentes
    # - max_df=0.95: Ignora palavras que aparecem em mais de 95% dos documentos (muito comuns)
    # - min_df=2: Ignora palavras que aparecem em menos de 2 documentos (muito raras)
    vectorizer = CountVectorizer(max_features=1000, max_df=0.95, min_df=2)

    # Ajusta o vetorizador ao corpus e transforma os textos na matriz BoW
    bow_matrix = vectorizer.fit_transform(textos_limpos)

    # Obtém a lista de palavras que formam o vocabulário
    feature_names = vectorizer.get_feature_names_out()
    return bow_matrix, feature_names, vectorizer
