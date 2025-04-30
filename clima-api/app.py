from flask import Flask, request, jsonify
from config import clima_collection
from cache import get_cache, set_cache, limpar_cache

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"msg": "API de Clima com Cache Ativa!"})


@app.route('/clima', methods=['POST'])
def adicionar_clima():
    dados = request.json
    if not dados.get("cidade") or not dados.get("temperatura"):
        return jsonify({"erro": "Campos 'cidade' e 'temperatura' são obrigatórios."}), 400

    clima_collection.insert_one(dados)

    # Limpa cache da cidade específica e da lista completa
    limpar_cache(f"clima:{dados['cidade']}")
    limpar_cache("clima:todos")

    return jsonify({"msg": "Clima adicionado e cache atualizado!"}), 201


@app.route('/clima', methods=['GET'])
def listar_clima():
    cache_key = "clima:todos"
    dados = get_cache(cache_key)
    if dados:
        return jsonify({"fonte": "cache", "dados": dados})
    print("ping")
    dados = list(clima_collection.find({}, {"_id": 0}))
    set_cache(cache_key, dados)
    return jsonify({"fonte": "banco", "dados": dados})


@app.route('/clima/<cidade>', methods=['GET'])
def buscar_clima_por_cidade(cidade):
    cache_key = f"clima:{cidade}"
    dados = get_cache(cache_key)
    if dados:
        return jsonify({"fonte": "cache", "dados": dados})

    dados = list(clima_collection.find({"cidade": cidade}, {"_id": 0}))
    if not dados:
        return jsonify({"msg": "Nenhum dado encontrado para essa cidade."}), 404

    set_cache(cache_key, dados)
    return jsonify({"fonte": "banco", "dados": dados})


if __name__ == '__main__':
    app.run(debug=True,port=4000)
