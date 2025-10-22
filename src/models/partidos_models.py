from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class Membro:
    id: str
    uri: str
    nome: str
    sigla_partido: Optional[str] = None
    uri_partido: Optional[str] = None
    sigla_uf: Optional[str] = None
    id_legislatura: Optional[int] = None
    url_foto: Optional[str] = None
    email: Optional[str] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Membro":
        return Membro(
            id=str(data.get("id", "")),
            uri=data.get("uri", ""),
            nome=data.get("nome", ""),
            sigla_partido=data.get("siglaPartido") or data.get("sigla_partido"),
            uri_partido=data.get("uriPartido") or data.get("uri_partido"),
            sigla_uf=data.get("siglaUf") or data.get("uf"),
            id_legislatura=data.get("idLegislatura"),
            url_foto=data.get("urlFoto") or data.get("url_foto"),
            email=data.get("email")
        )


@dataclass
class Lider:
    uri: str
    nome: str
    sigla_partido: Optional[str] = None
    uri_partido: Optional[str] = None
    uf: Optional[str] = None
    id_legislatura: Optional[int] = None
    url_foto: Optional[str] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Lider":
        return Lider(
            uri=data.get("uri", ""),
            nome=data.get("nome", ""),
            sigla_partido=data.get("siglaPartido"),
            uri_partido=data.get("uriPartido"),
            uf=data.get("uf"),
            id_legislatura=data.get("idLegislatura"),
            url_foto=data.get("urlFoto")
        )


@dataclass
class Status:
    data: Optional[str] = None
    id_legislatura: Optional[int] = None
    situacao: Optional[str] = None
    total_posse: Optional[int] = None
    total_membros: Optional[int] = None
    uri_membros: Optional[str] = None
    lider: Optional[Lider] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Status":
        lider_data = data.get("lider")
        lider = Lider.from_dict(lider_data) if lider_data else None

        return Status(
            data=data.get("data"),
            id_legislatura=data.get("idLegislatura"),
            situacao=data.get("situacao"),
            total_posse=int(data["totalPosse"]) if data.get("totalPosse") else None,
            total_membros=int(data["totalMembros"]) if data.get("totalMembros") else None,
            uri_membros=data.get("uriMembros"),
            lider=lider
        )


@dataclass
class Partido:
    id: str
    sigla: str
    nome: str
    uri: str
    status: Optional[Status] = None
    membros: Optional[List[Membro]] = None
    url_logo: Optional[str] = None
    url_website: Optional[str] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Partido":
        # Se JSON tem "dados", usa ele
        if "dados" in data:
            data = data["dados"]

        status_data = data.get("status")
        status = Status.from_dict(status_data) if status_data else None

        return Partido(
            id=str(data.get("id", "")),
            sigla=data.get("sigla", ""),
            nome=data.get("nome", ""),
            uri=data.get("uri", ""),
            status=status,
            membros=None,  # membros serão adicionados manualmente ou via endpoint separado
            url_logo=data.get("urlLogo"),
            url_website=data.get("urlWebSite")
        )
