from flask import Flask, jsonify, request
import requests
import time
from threading import Lock
import logging

app = Flask(__name__)

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configurações
BASE_URL = "http://localhost:4000"
CACHE_TTL = 60  # segundos
REQUEST_TIMEOUT = 5  # segundos

# Cache simples com Lock para concorrência
cache = {
    "previsoes": None,
    "timestamp": 0
}
cache_lock = Lock()

def is_valid_previsoes(data):
    """Valida se os dados da API são válidos."""
    return isinstance(data, list) and all(
        isinstance(dia, dict) and "minima" in dia and "maxima" in dia and "descricao" in dia
        for dia in data
    )

def get_previsoes():
    """Obtém previsões do cache ou faz nova requisição se expirado."""
    now = time.time()
    with cache_lock:
        # Verifica se o cache é válido
        if cache["previsoes"] is not None and (now - cache["timestamp"]) <= CACHE_TTL:
            logger.info("Retornando dados do cache")
            return cache["previsoes"]

    # Fora do lock para evitar bloqueio prolongado
    try:
        logger.info("Buscando novos dados da API")
        resposta = requests.get(f"{BASE_URL}/clima/previsao", timeout=REQUEST_TIMEOUT)
        resposta.raise_for_status()
        dados = resposta.json()

        # Valida os dados antes de armazenar
        if not is_valid_previsoes(dados):
            raise ValueError("Dados da API inválidos")

        with cache_lock:
            cache["previsoes"] = dados
            cache["timestamp"] = now
            logger.info("Cache atualizado com sucesso")
        return cache["previsoes"]

    except requests.RequestException as e:
        logger.error(f"Erro ao buscar dados da API: {str(e)}")
        with cache_lock:
            # Retorna cache antigo se disponível, mesmo que expirado
            if cache["previsoes"] is not None:
                logger.warning("Retornando cache expirado devido a erro")
                return cache["previsoes"]
        raise Exception(f"Erro ao buscar dados da API: {str(e)}")

@app.route("/")
def home():
    return jsonify({"mensagem": "API Consumidora de Clima"})

@app.route("/filtrar/temperatura")
def filtrar_temperatura():
    try:
        min_temp = float(request.args.get("min", -100))
        max_temp = float(request.args.get("max", 100))

        previsoes = get_previsoes()
        filtrados = [
            dia for dia in previsoes
            if min_temp <= dia["minima"] and dia["maxima"] <= max_temp
        ]

        return jsonify(filtrados)

    except Exception as e:
        logger.error(f"Erro ao filtrar temperatura: {str(e)}")
        return jsonify({"erro": str(e)}), 500

@app.route("/filtrar/descricao")
def filtrar_descricao():
    try:
        termo = request.args.get("termo", "").lower()

        previsoes = get_previsoes()
        filtrados = [
            dia for dia in previsoes
            if termo in dia["descricao"].lower()
        ]

        return jsonify(filtrados)

    except Exception as e:
        logger.error(f"Erro ao filtrar descrição: {str(e)}")
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # Alterado para evitar conflito de porta