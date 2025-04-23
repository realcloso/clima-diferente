import redis
import json

# Conectando ao Redis (localhost:6379 por padrão)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def get_cache(chave):
    dados = redis_client.get(chave)
    if dados:
        return json.loads(dados)
    return None

def set_cache(chave, valor, expira_em=30):
    redis_client.set(chave, json.dumps(valor), ex=expira_em)

def limpar_cache(chave):
    redis_client.delete(chave)
