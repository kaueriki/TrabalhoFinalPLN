
from sklearn.decomposition import LatentDirichletAllocation

# Treina um modelo LDA a partir de uma matriz Bag of Words
def treinar_lda(bow_matrix, n_topicos):

    # Inicializa o modelo LDA com o número de tópicos desejado e um estado aleatório para reprodutibilidade
    lda = LatentDirichletAllocation(n_components=n_topicos, random_state=42)
    
    # Treina o modelo com a matriz Bag of Words
    lda.fit(bow_matrix)

    return lda

# Extrai os tópicos e as palavras mais importantes de cada tópico
def obter_topicos_palavras(lda_model, feature_names, n_palavras):

    topicos = []
    # Itera sobre cada tópico no modelo (os componentes do LDA)
    for topic_idx, topic_distribution in enumerate(lda_model.components_):
        # Obtém os índices das N palavras com maior pontuação para o tópico atual
        top_words_indices = topic_distribution.argsort()[:-n_palavras - 1:-1]
        
        # Cria uma lista de tuplas (palavra, pontuação) para o tópico
        topic_words = [(feature_names[i], topic_distribution[i]) for i in top_words_indices]
        
        # Adiciona a lista de palavras do tópico a lista principal
        topicos.append(topic_words)
        
    return topicos
