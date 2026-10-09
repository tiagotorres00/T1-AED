import requests
import json

URL = "https://api.le-systeme-solaire.net/rest/bodies/"
API_KEY = ""

CAMPOS = [
    "id", "name", "englishName", "isPlanet", "bodyType",
    "gravity", "meanRadius", "avgTemp", "mass", "density",
    "aroundPlanet", "alternativeName", "escape",
    "discoveredBy", "discoveryDate", "meanRadius",
    "semimajorAxis",
]

def buscar_da_api():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    resposta = requests.get(URL, headers=headers)
    return resposta.json()["bodies"]

def filtrar_campos(corpo):
    return {campo: corpo.get(campo) for campo in CAMPOS}

def obter_corpos():
    return [filtrar_campos(c) for c in buscar_da_api()]

def salvar_dados(corpos):

    with open("dados/dados.json", "w", encoding="utf-8") as arquivo:
        json.dump(corpos, arquivo, ensure_ascii=False, indent=4)