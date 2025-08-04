import requests

class Deputados:

    def __init__(self):
        self.endpoint = 'https://dadosabertos.camara.leg.br/api/v2/'

    def get_deputados(self):
        """ Retorna uma lista de dados básicos sobre deputados que
         em exercício parlamentar em algum intervalo de tempo. """

        get_deputados = f'{self.endpoint}deputados'
        response = requests.get(get_deputados)
        if response.status_code == 200:
            return response.json()['dados']
        else:
            print(f"Erro na requisição: {response.status_code}")
            return []

    def get_deputados_id(self, deputado_id):

        """Retorna os dados cadastrais de um parlamentar identificado por {id} que,
         em algum momento da história e por qualquer período, entrou em exercício na Câmara."""
        get_deputados = f'{self.endpoint}deputados/{deputado_id}'
        response = requests.get(get_deputados)
        if response.status_code == 200:
            return response.json()['dados']
        else:
            print(f"Erro na requisição: {response.status_code}")
            return []

    def get_deputados_despesas(self, deputado_id):


        get_deputados = f'{self.endpoint}deputados/{deputado_id}/despesas'
        response = requests.get(get_deputados)
        if response.status_code == 200:
            return response.json()['dados']
        else:
            print(f"Erro na requisição: {response.status_code}")
            return []


if __name__ == '__main__':
    deputados = Deputados()
    result = deputados.get_deputados_despesas('91228')
    print(result)
    for dep in result:

        print(dep)
