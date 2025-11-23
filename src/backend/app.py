import os
from flask import Flask, render_template, jsonify
from tranformers_topic_model import gerar_topicos_transformers
from coleta import coletar_noticias
from preprocessing_pipeline import preprocessar_corpus
from text_representation import criar_bow
from topic_model import treinar_lda, obter_topicos_palavras

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    try:
        # 1. Coleta de Dados
        df = coletar_noticias(limit=30)
        noticias = df.to_dict(orient="records")
        textos = [n["texto"] for n in noticias]

        # 2. Pré-processamento
        textos_limpos, tokens = preprocessar_corpus(textos)

        # 3. Representação Vetorial (BoW)
        bow_matrix, feature_names, vectorizer = criar_bow(textos_limpos)

        # 4. Modelagem de Tópicos (LDA)
        lda_model = treinar_lda(bow_matrix, n_topicos=5)

        # 5. Extração de Tópicos e Palavras
        topicos = obter_topicos_palavras(lda_model, feature_names, n_palavras=10)

        print("Tópicos extraídos:", topicos)

        # 6. Preparação dos Dados para o Frontend
        topic_distribution = lda_model.transform(bow_matrix)
        topic_proportions = topic_distribution.mean(axis=0)

        chart_data = {
            "pie_chart": {
                "labels": [f"Tópico {i+1}" for i in range(len(topicos))],
                "data": topic_proportions.tolist()
            },
            "bar_charts": [
                {
                    "topic": f"Tópico {i+1}",
                    "words": [palavra for palavra, _ in topicos[i]],
                    "scores": [score for _, score in topicos[i]]
                }
                for i in range(len(topicos))
            ]
        }

        return jsonify({
            "status": "ok",
            "topicos": topicos,
            "chart_data": chart_data
        })

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

@app.route("/processtransformers", methods=["POST"])
def process_transformers():
    try:
        # Coleta notícias
        df = coletar_noticias(limit=150)
        textos = [n["texto"] for n in df.to_dict(orient="records")]

        # Pré-processa textos
        textos_limpos, tokens = preprocessar_corpus(textos)

        # Gera tópicos com Transformers
        topicos, chart_data = gerar_topicos_transformers(textos_limpos)

        print("Tópicos extraídos:", topicos)

        return jsonify({
            "status": "ok",
            "topicos": topicos,
            "chart_data": chart_data
        })

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
