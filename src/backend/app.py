import os
import numpy as np
from flask import Flask, render_template, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
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

# Variáveis globais para armazenar estado entre requisições
_dados = {
    "noticias": [],
    "textos_limpos": [],
    "tokens": [],
    "bow_matrix": None,
    "feature_names": None,
    "vectorizer": None
}

@app.route("/coletar", methods=["POST"])
def coletar():
    try:
        df = coletar_noticias(limit=30)
        _dados["noticias"] = df.to_dict(orient="records")
        return jsonify({
            "status": "ok",
            "total": len(_dados["noticias"])
        })
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

@app.route("/processar", methods=["POST"])
def processar():
    try:
        if not _dados["noticias"]:
            return jsonify({"status": "erro", "mensagem": "Colete as notícias primeiro"}), 400
        
        textos = [n["texto"] for n in _dados["noticias"]]
        textos_limpos, tokens = preprocessar_corpus(textos)
        _dados["textos_limpos"] = textos_limpos
        _dados["tokens"] = tokens
        
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

@app.route("/bow", methods=["POST"])
def bow():
    try:
        if not _dados["textos_limpos"]:
            return jsonify({"status": "erro", "mensagem": "Processe os textos primeiro"}), 400
        
        # Bag of Words
        bow_matrix, feature_names, vectorizer = criar_bow(_dados["textos_limpos"])
        _dados["bow_matrix"] = bow_matrix
        _dados["feature_names"] = feature_names
        _dados["vectorizer"] = vectorizer
        
        # TF-IDF
        tfidf_vectorizer = TfidfVectorizer(max_features=100)
        tfidf_matrix = tfidf_vectorizer.fit_transform(_dados["textos_limpos"])
        tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()
        
        # Top palavras por frequência
        freq_sum = np.array(bow_matrix.sum(axis=0)).flatten()
        top_freq_idx = freq_sum.argsort()[-10:][::-1]
        top_freq = [(feature_names[i], int(freq_sum[i])) for i in top_freq_idx]
        
        # Top palavras por TF-IDF
        tfidf_sum = np.array(tfidf_matrix.sum(axis=0)).flatten()
        top_tfidf_idx = tfidf_sum.argsort()[-10:][::-1]
        top_tfidf = [(tfidf_feature_names[i], float(tfidf_sum[i])) for i in top_tfidf_idx]
        
        return jsonify({
            "status": "ok",
            "top_freq": top_freq,
            "top_tfidf": top_tfidf
        })
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

@app.route("/topicos", methods=["POST"])
def topicos():
    try:
        if _dados["bow_matrix"] is None:
            return jsonify({"status": "erro", "mensagem": "Gere o BOW primeiro"}), 400
        
        lda_model = treinar_lda(_dados["bow_matrix"], n_topicos=5)
        topicos = obter_topicos_palavras(lda_model, _dados["feature_names"], n_palavras=10)
        
        return jsonify({
            "status": "ok",
            "topicos": topicos
        })
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

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
