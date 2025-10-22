from service.partidos_service import get_partidos, get_partidos_membros, get_partidos_by_id
from service.deputados_service import get_deputados, get_deputados_id
from models.deputados_models import Deputado, DeputadoDetalhado
from models.partidos_models import Membro, Partido

def partidos_membros(partido_id: int) -> list[Membro]:
    membros = get_partidos_membros(partido_id)
    return [Membro.from_dict(m) for m in membros]



def partido_with_membros(partido: Partido) -> Partido:
    print(partido)
    membros = partidos_membros(partido.id)
    partido.membros.append(membros)
    return partido


def partido_by_id(partido_id: int) -> Partido:

    partido = get_partidos_by_id(partido_id)
    return Partido.from_dict(partido)
partido = partido_by_id(36898)
print(partido_with_membros(partido))