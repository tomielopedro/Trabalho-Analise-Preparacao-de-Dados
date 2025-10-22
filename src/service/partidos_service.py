import requests

ENDPOINT = 'https://dadosabertos.camara.leg.br/api/v2/'


def get_partidos():
    response = requests.get(f'{ENDPOINT}partidos')
    if response.status_code == 200:
        return response.json()['dados']
    else:
        print(f"Erro na requisição: {response.status_code}")
        return []


def get_partidos_by_id(partido_id: int):
    response = requests.get(f'{ENDPOINT}partidos/{partido_id}')
    if response.status_code == 200:
        return response.json()['dados']
    else:
        print(f"Erro na requisição: {response.status_code}")
        return []


def get_partidos_membros(partido_id: int):
    response = requests.get(f'{ENDPOINT}partidos/{partido_id}/membros')
    if response.status_code == 200:
        return response.json()['dados']
    else:
        print(f"Erro na requisição: {response.status_code}")
        return []

