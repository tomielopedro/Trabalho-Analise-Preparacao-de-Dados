from service.partidos_service import *
from service.deputados_service import *
from models.deputados_models import *
from models.partidos_models import *
from datetime import datetime


# === FUNÇÕES UTILITÁRIAS (Helpers) ===

def interval_years_months(data_inicio: str, data_fim: str):
    """
    Gera:
      anos  -> lista de anos entre as datas
      meses -> lista de meses SEM repetir
    """
    inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
    fim = datetime.strptime(data_fim, "%Y-%m-%d")

    # ----- ANOS -----
    anos = list(range(inicio.year, fim.year + 1))

    # ----- MESES (sem repetição) -----
    meses = []
    seen = set()

    ano = inicio.year
    mes = inicio.month

    while (ano < fim.year) or (ano == fim.year and mes <= fim.month):
        if mes not in seen:
            meses.append(mes)
            seen.add(mes)

        # avança para o próximo mês
        mes += 1
        if mes > 12:
            mes = 1
            ano += 1

    return anos, meses


# === CLASSES DE DOMÍNIO ===

class Deputados:

    @staticmethod
    def get_all() -> list[Deputado]:
        deputados = get_deputados()
        return [Deputado.from_dict(d) for d in deputados]

    @staticmethod
    def get_by_id(deputado_id: int) -> DeputadoDetalhado:
        deputado = get_deputados_id(deputado_id)
        return DeputadoDetalhado.from_dict(deputado)

    @staticmethod
    def get_despesas(deputado_id: int, **kwargs) -> Despesa:
        despesas = get_deputado_despesa(deputado_id, **kwargs)
        return [Despesa.from_dict(d) for d in despesas]

    @staticmethod
    def get_historico(deputado_id: int):

        return get_deputado_historico(deputado_id)

    @staticmethod
    def get_eventos(deputado_id: int, **kwargs):
        eventos = get_deputados_eventos(deputado_id, **kwargs)
        return [Evento.from_dict(evento) for evento in eventos]

    @staticmethod
    def tratar_data_historico(deputado_id: int):
        """
        Retorna uma lista com os anos únicos encontrados no histórico do deputado.
        """
        historico = get_deputado_historico(deputado_id)

        if not historico or not isinstance(historico, list):
            return []

        anos = [
            item["dataHora"][:7].replace("-", "/")
            for item in historico
            if "dataHora" in item and item["dataHora"]
        ]
        return sorted(anos, reverse=True)


class Partidos:

    @staticmethod
    def get_all() -> list[Partido]:
        partidos = get_partidos()
        return [Partido.from_dict(p) for p in partidos]

    @staticmethod
    def get_by_id(partido_id: int) -> Partido:
        partido = get_partidos_by_id(partido_id)
        return Partido.from_dict(partido)

    @classmethod
    def get_all_detailed(cls) -> list[Partido]:
        """
        Busca todos os partidos e depois busca os detalhes de cada um individualmente.
        """
        partidos = cls.get_all()
        partidos_detailed = []
        for partido in partidos:
            partidos_detailed.append(cls.get_by_id(partido.id))
        return partidos_detailed

    @staticmethod
    def get_membros(partido_id: int) -> list[Membro]:
        membros = get_partidos_membros(partido_id)
        return [Membro.from_dict(m) for m in membros]

    @classmethod
    def enrich_with_membros(cls, partido: Partido) -> Partido:
        """
        Recebe um objeto Partido, busca seus membros e retorna o objeto atualizado.
        """
        membros = cls.get_membros(partido.id)
        partido.membros = membros
        return partido