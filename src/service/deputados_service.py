import requests

ENDPOINT = 'https://dadosabertos.camara.leg.br/api/v2/'


def get_deputados():

    deputados = f'{ENDPOINT}deputados'
    response = requests.get(deputados)
    if response.status_code == 200:
        return response.json()['dados']
    else:
        print(f"Erro na requisição: {response.status_code}")
        return []


def get_deputados_id(deputado_id: int):

    deputados = f'{ENDPOINT}deputados/{deputado_id}'
    response = requests.get(deputados)
    if response.status_code == 200:
        return response.json()['dados']
    else:
        print(f"Erro na requisição: {response.status_code}")
        return []



def get_deputado_despesa(deputado_id: int, **kwargs):

    deputados = f'{ENDPOINT}deputados/{deputado_id}/despesas'

    response = requests.get(deputados, kwargs)
    if response.status_code == 200:
        return response.json()['dados']
    else:
        print(f"Erro na requisição: {response.status_code}")
        return []


def get_deputado_historico(deputado_id: int):
    deputados = f'{ENDPOINT}deputados/{deputado_id}/historico'
    response = requests.get(deputados)
    if response.status_code == 200:
        return response.json()['dados']
    else:
        print(f"Erro na requisição: {response.status_code}")
        return []


def get_deputados_eventos(deputado_id: int, **kwargs):
    deputados = f'{ENDPOINT}deputados/{deputado_id}/eventos'
    response = requests.get(deputados, params=kwargs)

    if response.status_code == 200:
        return response.json()['dados']
    else:
        print(f"Erro na requisição: {response.status_code}")
        return []

