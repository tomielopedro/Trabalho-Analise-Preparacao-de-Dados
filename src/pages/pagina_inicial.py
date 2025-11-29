import streamlit as st
import math
from utils.utils import Deputados, Partidos

DEPUTADOS, PARTIDOS = Deputados(), Partidos()

st.markdown("""
    <style>
    /* Card Geral com Sombra e Hover */
    .st-emotion-cache-1r6slb0, .st-emotion-cache-12w0qpk { /* Classes containers do Streamlit */
        transition: transform 0.2s, box-shadow 0.2s;
    }

    /* Estilo Customizado para nossos Cards */
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        background-color: white;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.2s ease-in-out;
    }
    div[data-testid="stVerticalBlock"] > div[style*="border"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        border-color: #007bff;
    }

    /* Títulos e Textos */
    h3, h4, h5 { color: #2c3e50; margin-bottom: 5px; }
    p { color: #666; font-size: 0.9rem; }

    /* Badges (Etiquetas) */
    .badge-partido {
        background-color: #007bff; color: white; 
        padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;
    }
    .badge-uf {
        background-color: #e9ecef; color: #495057; 
        padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; border: 1px solid #dee2e6;
    }
    .badge-membros {
        background-color: #d4edda; color: #155724;
        padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: bold;
    }

    /* Imagens */
    img { border-radius: 8px; }

    /* Paginação */
    div[data-testid="stNumberInput"] label { display: none; }
    </style>
""", unsafe_allow_html=True)

st.title("🗂️ Visão Geral Parlamentar")
st.markdown("Explore as bancadas partidárias e a lista completa de deputados em exercício.")
st.markdown("---")

partidos_tab, deputados_tab = st.tabs(['🏢 Partidos Políticos', '👔 Deputados Federais'])


def ir_para_partido(partido):
    st.session_state['selected_partido'] = PARTIDOS.enrich_with_membros(partido)
    st.switch_page('pages/pagina_partido.py')


def ir_para_deputado(deputado):
    st.session_state['selected_deputado'] = DEPUTADOS.get_by_id(deputado.id)
    st.switch_page('pages/pagina_deputado.py')


# ==========================================
# 3. TAB: PARTIDOS
# ==========================================
with partidos_tab:
    col_search, col_stats = st.columns([3, 1])
    with col_search:
        busca_partido = st.text_input("🔍 Filtrar Partidos", placeholder="Digite a sigla ou nome (ex: PL, PT)...")

    partidos = st.session_state.get('partidos', [])

    if busca_partido:
        partidos_filtrados = [
            p for p in partidos
            if busca_partido.lower() in p.nome.lower() or busca_partido.lower() in p.sigla.lower()
        ]
    else:
        partidos_filtrados = partidos


    with col_stats:
        st.metric("Total de Partidos", len(partidos_filtrados))

    if not partidos_filtrados:
        st.warning("Nenhum partido encontrado com este critério.")
    else:
        st.markdown("<br>", unsafe_allow_html=True)

        cols_per_row = 3
        rows = [partidos_filtrados[i:i + cols_per_row] for i in range(0, len(partidos_filtrados), cols_per_row)]

        for row in rows:
            cols = st.columns(cols_per_row)
            for idx, partido in enumerate(row):
                with cols[idx]:
                    with st.container(border=True):
                        c_img, c_info = st.columns([1, 2])

                        with c_img:
                            logo = partido.url_logo if partido.url_logo else 'https://via.placeholder.com/100?text=Sigla'
                            st.image(logo, use_container_width=True)

                        with c_info:
                            st.markdown(f"### {partido.sigla}")
                            membros = partido.status.total_membros if partido.status else 0
                            st.markdown(f"<span class='badge-membros'>👥 {membros} Membros</span>",
                                        unsafe_allow_html=True)

                        st.markdown(f"**{partido.nome}**")

                        lider = partido.status.lider.nome if (partido.status and partido.status.lider) else "—"
                        st.caption(f"Líder: {lider}")

                        if st.button('Ver Detalhes', key=f'btn_part_{partido.id}', use_container_width=True):
                            ir_para_partido(partido)

with deputados_tab:
    deputados = st.session_state.get('deputados', [])

    with st.container(border=True):
        st.markdown("#### 🔎 Filtros de Pesquisa")
        c1, c2, c3 = st.columns([3, 1.5, 1.5])

        with c1:
            busca_nome = st.text_input("Nome do Parlamentar", placeholder="Digite para buscar...")
        with c2:
            lista_partidos = sorted(list(set([d.sigla_partido for d in deputados if d.sigla_partido])))
            filtro_partido = st.selectbox("Filtrar por Partido", ["Todos"] + lista_partidos)
        with c3:
            lista_ufs = sorted(list(set([d.sigla_uf for d in deputados if d.sigla_uf])))
            filtro_uf = st.selectbox("Filtrar por UF", ["Todos"] + lista_ufs)

    deputados_filtrados = deputados
    if busca_nome:
        deputados_filtrados = [d for d in deputados_filtrados if busca_nome.lower() in d.nome.lower()]
    if filtro_partido != "Todos":
        deputados_filtrados = [d for d in deputados_filtrados if d.sigla_partido == filtro_partido]
    if filtro_uf != "Todos":
        deputados_filtrados = [d for d in deputados_filtrados if d.sigla_uf == filtro_uf]

    st.divider()
    items_por_pagina = 24
    total_items = len(deputados_filtrados)
    total_paginas = math.ceil(total_items / items_por_pagina)

    col_resumo, col_pag = st.columns([3, 1])
    with col_resumo:
        st.caption(f"Exibindo **{total_items}** parlamentares encontrados.")

    pagina_atual = 1
    if total_paginas > 1:
        with col_pag:
            pagina_atual = st.number_input(
                f"Página (1 de {total_paginas})",
                min_value=1,
                max_value=total_paginas,
                value=1,
                label_visibility="collapsed"
            )

    inicio = (pagina_atual - 1) * items_por_pagina
    fim = inicio + items_por_pagina
    lote_atual = deputados_filtrados[inicio:fim]


    if not lote_atual:
        st.info("🚫 Nenhum deputado encontrado com os filtros selecionados.")
    else:

        cols_per_row = 4
        rows = [lote_atual[i:i + cols_per_row] for i in range(0, len(lote_atual), cols_per_row)]

        for row in rows:
            cols = st.columns(cols_per_row)
            for idx, deputado in enumerate(row):
                with cols[idx]:

                    with st.container(border=True):
                        c_foto, c_status = st.columns([1, 2])

                        if deputado.url_foto:
                            st.image(deputado.url_foto, use_container_width=True)
                        else:
                            st.image("https://via.placeholder.com/150?text=Foto", use_container_width=True)

                        st.markdown(f"**{deputado.nome}**")

                        html_badges = f"""
                        <div style='margin-bottom:10px;'>
                            <span class='badge-partido'>{deputado.sigla_partido}</span>
                            <span class='badge-uf'>{deputado.sigla_uf}</span>
                        </div>
                        """
                        st.markdown(html_badges, unsafe_allow_html=True)

                        if st.button("Ver Perfil", key=f"btn_d_{deputado.id}", use_container_width=True):
                            ir_para_deputado(deputado)