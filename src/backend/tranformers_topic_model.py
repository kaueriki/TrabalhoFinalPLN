from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

def gerar_topicos_transformers(textos_limpos):

    # Cria embeddings semânticos usando modelo pré-treinado MiniLM (Sentence-BERT)
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embedding_model.encode(textos_limpos, show_progress_bar=True)

    # Cria modelo BERTopic para descoberta de tópicos
    topic_model = BERTopic(language="portuguese")

    # Treina o modelo e atribui um tópico para cada documento
    topics, probs = topic_model.fit_transform(textos_limpos, embeddings)

    # Obtém informações gerais sobre os tópicos (ID, quantidade de documentos, etc.)
    topic_info = topic_model.get_topic_info()
    print(topic_info) 

    # Extrai as palavras mais importantes de cada tópico
    topic_words = {}
    for topic_id in topic_info["Topic"].unique():
        if topic_id != -1:   # Ignora tópicos de outliers
            topic_words[f"Tópico {topic_id}"] = topic_model.get_topic(topic_id)

    # Dados para o gráfico de pizza
    topic_sizes = topic_info[topic_info["Topic"] >= 0]["Count"]
    topic_labels = [f"Tópico {i}" for i in topic_info[topic_info["Topic"] >= 0]["Topic"]]

    # Estrutura que será retornada ao front-end para visualização
    chart_data = {
        "pie_chart": {
            "labels": topic_labels,
            "data": topic_sizes.tolist()
        },
        "bar_charts": [
            {
                "topic": key,
                "words": [w[0] for w in topic_words[key]],
                "scores": [w[1] for w in topic_words[key]]
            }
            for key in topic_words
        ]
    }

    return topic_words, chart_data
