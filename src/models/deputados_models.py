from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class Gabinete:
    nome: Optional[str]
    predio: Optional[str]
    sala: Optional[str]
    andar: Optional[str]
    telefone: Optional[str]
    email: Optional[str]

    @staticmethod
    def from_dict(data: Optional[Dict[str, Any]]) -> Optional["Gabinete"]:
        if not data:
            return None
        return Gabinete(
            nome=data.get("nome"),
            predio=data.get("predio"),
            sala=data.get("sala"),
            andar=data.get("andar"),
            telefone=data.get("telefone"),
            email=data.get("email")
        )


@dataclass
class UltimoStatus:
    id: int
    uri: str
    nome: str
    sigla_partido: Optional[str]
    uri_partido: Optional[str]
    sigla_uf: Optional[str]
    id_legislatura: Optional[int]
    url_foto: Optional[str]
    email: Optional[str]
    data: Optional[str]
    nome_eleitoral: Optional[str]
    gabinete: Optional[Gabinete]
    situacao: Optional[str]
    condicao_eleitoral: Optional[str]
    descricao_status: Optional[str]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "UltimoStatus":
        gabinete = Gabinete.from_dict(data.get("gabinete"))
        return UltimoStatus(
            id=data.get("id"),
            uri=data.get("uri"),
            nome=data.get("nome"),
            sigla_partido=data.get("siglaPartido"),
            uri_partido=data.get("uriPartido"),
            sigla_uf=data.get("siglaUf"),
            id_legislatura=data.get("idLegislatura"),
            url_foto=data.get("urlFoto"),
            email=data.get("email"),
            data=data.get("data"),
            nome_eleitoral=data.get("nomeEleitoral"),
            gabinete=gabinete,
            situacao=data.get("situacao"),
            condicao_eleitoral=data.get("condicaoEleitoral"),
            descricao_status=data.get("descricaoStatus")
        )


# ===== Deputado Básico =====
@dataclass
class Deputado:
    id: int
    uri: str
    nome: Optional[str] = None
    sigla_partido: Optional[str] = None
    uri_partido: Optional[str] = None
    sigla_uf: Optional[str] = None
    id_legislatura: Optional[int] = None
    url_foto: Optional[str] = None
    email: Optional[str] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Deputado":
        # Aceita JSON dentro de "dados"
        if "dados" in data:
            dados = data["dados"]
            if isinstance(dados, list):
                data = dados[0]
            else:
                data = dados

        return Deputado(
            id=data.get("id"),
            uri=data.get("uri"),
            nome=data.get("nome") or data.get("nomeCivil"),
            sigla_partido=data.get("siglaPartido"),
            uri_partido=data.get("uriPartido"),
            sigla_uf=data.get("siglaUf"),
            id_legislatura=data.get("idLegislatura"),
            url_foto=data.get("urlFoto"),
            email=data.get("email")
        )


# ===== Deputado Detalhado =====
@dataclass
class DeputadoDetalhado:
    id: int
    uri: str
    nome: Optional[str] = None
    ultimo_status: Optional[UltimoStatus] = None
    cpf: Optional[str] = None
    sexo: Optional[str] = None
    url_website: Optional[str] = None
    rede_social: Optional[List[str]] = None
    data_nascimento: Optional[str] = None
    data_falecimento: Optional[str] = None
    uf_nascimento: Optional[str] = None
    municipio_nascimento: Optional[str] = None
    escolaridade: Optional[str] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "DeputadoDetalhado":
        # Aceita JSON dentro de "dados"
        if "dados" in data:
            dados = data["dados"]
            if isinstance(dados, list):
                data = dados[0]
            else:
                data = dados

        ultimo_status_data = data.get("ultimoStatus")
        ultimo_status = UltimoStatus.from_dict(ultimo_status_data) if ultimo_status_data else None

        return DeputadoDetalhado(
            id=data.get("id"),
            uri=data.get("uri"),
            nome=data.get("nome") or data.get("nomeCivil"),
            ultimo_status=ultimo_status,
            cpf=data.get("cpf"),
            sexo=data.get("sexo"),
            url_website=data.get("urlWebsite"),
            rede_social=data.get("redeSocial"),
            data_nascimento=data.get("dataNascimento"),
            data_falecimento=data.get("dataFalecimento"),
            uf_nascimento=data.get("ufNascimento"),
            municipio_nascimento=data.get("municipioNascimento"),
            escolaridade=data.get("escolaridade")
        )
