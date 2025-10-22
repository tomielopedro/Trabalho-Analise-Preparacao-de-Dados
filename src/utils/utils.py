from service.partidos_service import get_partidos, get_partidos_membros, get_partidos_by_id
from service.deputados_service import get_deputados, get_deputados_id
from models.deputados_models import Deputado, DeputadoDetalhado
from models.partidos_models import Membro, Partido


def all_deputados() -> list[Deputado]:
    deputados = get_deputados()
    return [Deputado.from_dict(d) for d in deputados]


def deputado_by_id(deputado_id: int) -> DeputadoDetalhado:
    deputado = get_deputados_id(deputado_id)
    return DeputadoDetalhado.from_dict(deputado)


def all_partidos() -> list[Partido]:
    partidos = get_partidos()
    return [Partido.from_dict(p) for p in partidos]


def partido_by_id(partido_id: int) -> Partido:
    partido = get_partidos_by_id(partido_id)
    return Partido.from_dict(partido)


def all_partidos_detailed() -> list[Partido]:
    partidos = all_partidos()
    partidos_detailed = []
    for partido in partidos:
        partidos_detailed.append(partido_by_id(partido.id))
    return partidos_detailed


def partidos_membros(partido_id: int) -> list[Membro]:
    membros = get_partidos_membros(partido_id)
    return [Membro.from_dict(m) for m in membros]


def partido_with_membros(partido: Partido) -> Partido:
    membros = partidos_membros(partido.id)
    print(membros)
    partido.membros = membros
    return partido