import requests

ENDPOINT = 'https://dadosabertos.camara.leg.br/api/v2/'


def get_deputados():
    """ Retorna uma lista de dados básicos sobre deputados que
     em exercício parlamentar em algum intervalo de tempo. """

    deputados = f'{ENDPOINT}deputados'
    response = requests.get(deputados)
    if response.status_code == 200:
        return response.json()['dados']
    else:
        print(f"Erro na requisição: {response.status_code}")
        return []


def get_deputados_id(deputado_id: int):
    """Retorna os dados cadastrais de um parlamentar identificado por {id} que,
     em algum momento da história e por qualquer período, entrou em exercício na Câmara."""

    deputados = f'{ENDPOINT}deputados/{deputado_id}'
    response = requests.get(deputados)
    if response.status_code == 200:
        return response.json()['dados']
    else:
        print(f"Erro na requisição: {response.status_code}")
        return []



