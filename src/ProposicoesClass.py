import requests

class Proposicoes:
    def __init__(self):
        self.endpoint = 'https://dadosabertos.camara.leg.br/api/v2/'

    def get_preposicoes(self):
        get_proposicoes = f'{self.endpoint}proposicoes'
        response = requests.get(get_proposicoes)
        if response.status_code == 200:
            return response.json()['dados']
        else:
            print(f"Erro na requisição: {response.status_code}")
            return []

    def get_cod_tema(self):
        get_proposicoes = f'{self.endpoint}/referencias/proposicoes/codTema'
        response = requests.get(get_proposicoes)
        if response.status_code == 200:
            return response.json()['dados']
        else:
            print(f"Erro na requisição: {response.status_code}")
            return []

    def get_situacao_proposicao(self):
        get_proposicoes = f'{self.endpoint}/referencias/situacoesProposicao'
        response = requests.get(get_proposicoes)
        if response.status_code == 200:
            return response.json()['dados']
        else:
            print(f"Erro na requisição: {response.status_code}")
            return []

    def get_tipos_proposicao(self):
        get_proposicoes = f'{self.endpoint}/referencias/tiposProposicao'
        response = requests.get(get_proposicoes)
        if response.status_code == 200:
            return response.json()['dados']
        else:
            print(f"Erro na requisição: {response.status_code}")
            return []

if __name__ == '__main__':
    proposicoes = Proposicoes()
    result = proposicoes.get_tipos_proposicao()
    for prep in result:

        print(prep)