from flask import Flask, jsonify
import json

app = Flask(__name__)

def carregar_clima():
    with open("clima.json", "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/")
def home():
    return jsonify({"mensagem": "API de Clima - Curitiba 🌦"})

@app.route("/clima/atual")
def clima_atual():
    dados = carregar_clima()
    atual = dados["current"]
    return jsonify({
        "temperatura": atual["temp"],
        "sensacao_termica": atual["feels_like"],
        "descricao": atual["weather"][0]["description"]
    })

@app.route("/clima/previsao")
def previsao():
    dados = carregar_clima()
    previsoes = []
    for dia in dados["daily"]:
        previsoes.append({
            "minima": dia["temp"]["min"],
            "maxima": dia["temp"]["max"],
            "descricao": dia["weather"][0]["description"]
        })
    return jsonify(previsoes)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4000)