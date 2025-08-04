import requests

class Partido:
    def __init__(self):
        self.endpoint = 'https://dadosabertos.camara.leg.br/api/v2'

    def get_partidos(self):
        response = requests.get(f'{self.endpoint}/partidos')
        if response.status_code == 200:
            return response.json()['dados']
        else:
            print(f"Erro na requisição: {response.status_code}")
            return []


    def get_partidos_membros(self,partidos_id ):
        response = requests.get(f'{self.endpoint}/partidos/{partidos_id}/membros')
        if response.status_code == 200:
            return response.json()['dados']
        else:
            print(f"Erro na requisição: {response.status_code}")
            return []



if __name__ == '__main__':
    proposicoes = Partido()
    result = proposicoes.get_partidos()
    for prep in result:

        print(prep)