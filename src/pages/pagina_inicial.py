import streamlit as st
import math
from utils.utils import Deputados, Partidos  # Certifique-se que suas funções de carga (partido_with_membros, etc) estão aqui

DEPUTADOS, PARTIDOS = Deputados(), Partidos()
# === ESTILO CSS ===
st.markdown("""
    <style>
    div[data-testid="stContainer"] {
        transition: transform 0.2s;
    }
    div[data-testid="stContainer"]:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton button {
        width: 100%;
        border-radius: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🗂️ Visão Geral")
partidos_tab, deputados_tab = st.tabs(['🏢 Partidos Políticos', '👔 Deputados Federais'])


# === FUNÇÕES DE NAVEGAÇÃO ===

def informacoes_partido_button(partido):
    if st.button('Ver Detalhes', key=f'btn_part_{partido.id}', use_container_width=True):
        st.session_state['selected_partido'] = PARTIDOS.enrich_with_membros(partido)
        st.switch_page('pages/pagina_partido.py')


def informacoes_deputado_button(deputado):
    if st.button('Ver Perfil', key=f'btn_dep_{deputado.id}', use_container_width=True):
        st.session_state['selected_deputado'] = DEPUTADOS.get_by_id(deputado.id)
        st.switch_page('pages/pagina_deputado.py')


# === TAB: PARTIDOS ===
with partidos_tab:
    st.subheader("Bancadas Partidárias")

    # Filtro de Busca
    busca_partido = st.text_input("🔍 Buscar Partido (Nome ou Sigla)", placeholder="Ex: PT, PL, Avante...")

    partidos = st.session_state.get('partidos', [])

    # Lógica de Filtro
    if busca_partido:
        partidos_filtrados = [
            p for p in partidos
            if busca_partido.lower() in p.nome.lower() or busca_partido.lower() in p.sigla.lower()
        ]
    else:
        partidos_filtrados = partidos

    if not partidos_filtrados:
        st.warning("Nenhum partido encontrado.")
    else:
        # Layout em Grade (3 colunas)
        cols = st.columns(3)
        for index, partido in enumerate(partidos_filtrados):
            col = cols[index % 3]  # Distribui entre as 3 colunas

            with col:
                # Definindo altura fixa de 200px para alinhar cards
                with st.container(border=True, height=200):
                    # Cabeçalho do Card
                    col_img, col_txt = st.columns([1, 2])

                    logo = partido.url_logo if partido.url_logo else 'https://via.placeholder.com/100'
                    with col_img:
                        st.image(logo, width=60)

                    with col_txt:
                        st.write(f"**{partido.sigla}**")
                        st.caption(f"Membros: {partido.status.total_membros}")

                    st.markdown(f"**{partido.nome}**")

                    # Tratamento seguro para Líder (pode ser None no dataclass)
                    nome_lider = partido.status.lider.nome if partido.status and partido.status.lider else "Não informado"
                    st.caption(f"Líder: {nome_lider}")

                    st.divider()
                    informacoes_partido_button(partido)

# === TAB: DEPUTADOS ===
with deputados_tab:
    st.subheader("Lista de Parlamentares")

    deputados = st.session_state.get('deputados', [])

    # --- BARRA DE FILTROS ---
    with st.expander("🔎 Filtros de Pesquisa", expanded=True):
        c1, c2, c3 = st.columns([2, 1, 1])

        with c1:
            busca_nome = st.text_input("Nome do Deputado", placeholder="Digite o nome...")

        with c2:
            # Extrair lista única de partidos para o selectbox
            lista_partidos = sorted(list(set([d.sigla_partido for d in deputados if d.sigla_partido])))
            filtro_partido = st.selectbox("Partido", ["Todos"] + lista_partidos)

        with c3:
            # Extrair lista única de UFs
            lista_ufs = sorted(list(set([d.sigla_uf for d in deputados if d.sigla_uf])))
            filtro_uf = st.selectbox("UF", ["Todos"] + lista_ufs)

    # Lógica de Filtragem
    deputados_filtrados = deputados

    if busca_nome:
        deputados_filtrados = [d for d in deputados_filtrados if busca_nome.lower() in d.nome.lower()]

    if filtro_partido != "Todos":
        deputados_filtrados = [d for d in deputados_filtrados if d.sigla_partido == filtro_partido]

    if filtro_uf != "Todos":
        deputados_filtrados = [d for d in deputados_filtrados if d.sigla_uf == filtro_uf]

    # --- PAGINAÇÃO (Crucial para performance) ---
    items_por_pagina = 20
    total_items = len(deputados_filtrados)
    total_paginas = math.ceil(total_items / items_por_pagina)

    if total_paginas > 1:
        col_pag_1, col_pag_2 = st.columns([4, 1])
        with col_pag_2:
            pagina_atual = st.number_input("Página", min_value=1, max_value=total_paginas, value=1)
    else:
        pagina_atual = 1

    inicio = (pagina_atual - 1) * items_por_pagina
    fim = inicio + items_por_pagina
    lote_atual = deputados_filtrados[inicio:fim]

    st.caption(f"Mostrando {len(lote_atual)} de {total_items} resultados.")

    # --- GRID DE DEPUTADOS ---
    if not lote_atual:
        st.info("Nenhum deputado encontrado com os filtros atuais.")
    else:
        # Grade de 4 colunas
        cols_dep = st.columns(4)
        for index, deputado in enumerate(lote_atual):
            c_dep = cols_dep[index % 4]

            with c_dep:
                # Definindo altura fixa de 370px para alinhar cards (comporta foto + infos)
                with st.container(border=True, height=370):
                    # Foto centralizada
                    if deputado.url_foto:
                        st.image(deputado.url_foto, use_container_width=True)

                    st.markdown(f"##### {deputado.nome}")

                    # Tags visuais
                    st.markdown(f"""
                        <div style="display: flex; gap: 5px; margin-bottom: 10px;">
                            <span style="background-color: #e0e0e0; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">{deputado.sigla_partido}</span>
                            <span style="background-color: #d1e7dd; padding: 2px 8px; border-radius: 4px; font-size: 12px;">{deputado.sigla_uf}</span>
                        </div>
                    """, unsafe_allow_html=True)

                    informacoes_deputado_button(deputado)