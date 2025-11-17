from flask import Flask, jsonify
from back.coleta import coletar_noticias

app = Flask(__name__)

@app.route("/")
def home():
    return "Trabalho Final de PLN - Coleta de Notícias do G1 Economia"

# Rota de coletar os dados 
@app.route("/coletar")
def coletar():
    df = coletar_noticias()

    dados_json = df.to_dict(orient="records")
    return jsonify(dados_json)


if __name__ == "__main__":
    app.run(debug=True)
