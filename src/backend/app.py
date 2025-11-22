import os
from flask import Flask, render_template, jsonify, request
from coleta import coletar_noticias
from preprocessing_pipeline import preprocessar_corpus
from language_model_pipeline import calcular_bow_tfidf
from topic_model import gerar_topicos

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

noticias_data = None
preprocess_output = None
bow_global = None
tfidf_global = None
topicos_global = None

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/coletar", methods=["POST"])
def coletar():
    global noticias_data

    try:
        df = coletar_noticias(limit=20)
        noticias_data = df.to_dict(orient="records")

        return jsonify({
            "status": "ok",
            "total": len(noticias_data),
            "noticias": noticias_data
        })

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


@app.route("/processar", methods=["POST"])
def processar():
    global noticias_data, preprocess_output

    if noticias_data is None:
        return jsonify({"status": "erro", "mensagem": "Nenhum dado coletado!"}), 400

    try:
        textos = [n["texto"] for n in noticias_data]
        preprocess_output = preprocessar_corpus(textos)

        return jsonify({
            "status": "ok",
            "qtd_textos": len(preprocess_output["textos_limpos"])
        })

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


@app.route("/bow", methods=["POST"])
def bow():
    global preprocess_output, bow_global, tfidf_global

    if preprocess_output is None:
        return jsonify({"status": "erro", "mensagem": "Execute o pré-processamento antes!"}), 400

    try:
        bow_global, tfidf_global = calcular_bow_tfidf(preprocess_output)

        top_freq = sorted(bow_global.items(), key=lambda x: x[1], reverse=True)[:20]
        top_tfidf = sorted(tfidf_global.items(), key=lambda x: x[1], reverse=True)[:20]

        return jsonify({
            "status": "ok",
            "top_freq": top_freq,
            "top_tfidf": top_tfidf
        })

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


@app.route("/topicos", methods=["POST"])
def topicos():
    global bow_global, tfidf_global, topicos_global

    if bow_global is None or tfidf_global is None:
        return jsonify({"status": "erro", "mensagem": "Execute BOW/TF-IDF antes!"}), 400

    try:
        topicos_global = gerar_topicos(bow_global, tfidf_global)

        return jsonify({
            "status": "ok",
            "topicos": topicos_global
        })

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
