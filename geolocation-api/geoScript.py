from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Base da API original
BASE_URL = "http://clima-api:5001"

@app.route("/")
def home():
    return jsonify({"mensagem": "API Consumidora de Clima"})


@app.route("/filtrar/temperatura")
def filtrar_temperatura():
    try:
        min_temp = float(request.args.get("min", -100))
        max_temp = float(request.args.get("max", 100))

        resposta = requests.get(f"{BASE_URL}/clima/previsao")
        previsoes = resposta.json()

        filtrados = [
            dia for dia in previsoes
            if min_temp <= dia["minima"] and dia["maxima"] <= max_temp
        ]

        return jsonify(filtrados)

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/filtrar/descricao")
def filtrar_descricao():
    try:
        termo = request.args.get("termo", "").lower()

        resposta = requests.get(f"{BASE_URL}/clima/previsao")
        previsoes = resposta.json()

        filtrados = [
            dia for dia in previsoes
            if termo in dia["descricao"].lower()
        ]

        return jsonify(filtrados)

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)