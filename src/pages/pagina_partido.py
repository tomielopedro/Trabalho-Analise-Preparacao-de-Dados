import streamlit as st
import pandas as pd
import plotly.express as px
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from datetime import datetime, date

from pages.pagina_deputado import filtro_data
from utils.utils import Deputados, Partidos

# ==========================================
# 0. CONFIGURAÇÃO E ESTILO
# ==========================================


st.set_page_config(layout="wide", page_title="Portal Parlamentar - Partidos", page_icon="🏛️")

st.markdown("""
    <style>
    /* Cartão Geral */
    .card-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border: 1px solid #f0f0f0;
    }

    /* Títulos e Textos */
    h1, h2, h3 { color: #2c3e50; }
    .highlight-text { color: #007bff; font-weight: bold; }

    .status-badge {
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }

    /* Métricas (KPIs) Customizadas */
    div[data-testid="stMetric"] {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #007bff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Ajustes Gerais */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    </style>
""", unsafe_allow_html=True)

DEPUTADOS, PARTIDOS = Deputados(), Partidos()


# ==========================================
# 1. FUNÇÕES LÓGICAS
# ==========================================

def informacoes_deputado_button(deputado):
    if st.button('Ver Perfil', key=f'btn_dep_{deputado.id}', use_container_width=True):
        st.session_state['selected_deputado'] = DEPUTADOS.get_by_id(deputado.id)
        st.switch_page('pages/pagina_deputado.py')


def _buscar_gastos(deputado):
    df_temp = pd.DataFrame(DEPUTADOS.get_despesas(deputado_id=deputado.id))
    if not df_temp.empty:
        df_temp.insert(0, 'id_deputado', deputado.id)
    return df_temp


@st.cache_data(ttl=3600, show_spinner=False)
def _consolidar_gastos_partido_cached(partido_id, membros_ids):

    partido_obj = PARTIDOS.get_by_id(partido_id)

    return None


def _consolidar_gastos_partido(partido):
    deputados = partido.membros
    df_gastos_list = []

    progress_text = "Consolidando despesas da bancada... Isso pode levar alguns segundos."
    my_bar = st.progress(0, text=progress_text)

    with ThreadPoolExecutor(max_workers=10) as executor:
        resultados = list(executor.map(_buscar_gastos, deputados))

    my_bar.progress(50, text="Processando dados...")

    for df_temp in resultados:
        if not df_temp.empty:
            df_gastos_list.append(df_temp)

    if df_gastos_list:
        df_gastos = pd.concat(df_gastos_list, ignore_index=True)
    else:
        df_gastos = pd.DataFrame()

    my_bar.empty()
    return df_gastos


# ==========================================
# 2. CONTEÚDO PRINCIPAL
# ==========================================

partido = st.session_state.get('selected_partido')

if partido:
    infos = asdict(partido)
    status = infos["status"]
    lider = status["lider"]

    if ('gastos_partido' not in st.session_state or st.session_state.get('gastos_partido_partido_id') != partido.id):
        with st.spinner(f'Baixando dados financeiros do {partido.sigla}...'):
            st.session_state['gastos_partido'] = _consolidar_gastos_partido(partido)
            st.session_state['gastos_partido_partido_id'] = partido.id

    df_gastos = st.session_state['gastos_partido']

    with st.container():
        st.markdown('<div class="card-container">', unsafe_allow_html=True)

        c_foto, c_info, c_lider = st.columns([1, 3, 2])

        with c_foto:
            if partido.url_logo:
                st.image(partido.url_logo, width=120)
            else:
                st.markdown(f"<h1 style='text-align:center; font-size: 80px;'>{infos['sigla']}</h1>",
                            unsafe_allow_html=True)

        with c_info:
            st.markdown(f"## {partido.nome}")
            st.markdown(f"#### <span class='highlight-text'>Bancada: {status['total_membros']} Membros</span>",
                        unsafe_allow_html=True)

            situacao = status['situacao']
            cor_bg = "#d4edda" if "Ativo" in situacao or "Regular" in situacao else "#fff3cd"
            cor_txt = "#155724" if "Ativo" in situacao or "Regular" in situacao else "#856404"

            data_status = datetime.fromisoformat(status['data']).strftime("%d/%m/%Y")

            st.markdown(f"""
                <span class="status-badge" style="background-color:{cor_bg}; color:{cor_txt};">
                    ● {situacao}
                </span>
                <span style="margin-left:10px; font-size:0.9rem; color:#666;">
                    Atualizado em: {data_status} | Legislatura: {status['id_legislatura']}
                </span>
            """, unsafe_allow_html=True)

        with c_lider:
            st.markdown("##### 👤 Liderança Atual")
            cl1, cl2 = st.columns([1, 3])
            with cl1:
                st.image(lider["url_foto"], width=60, output_format='PNG')
            with cl2:
                st.markdown(f"**{lider['nome']}**")
                st.caption(f"UF: {lider['uf']}")

        st.markdown('</div>', unsafe_allow_html=True)

    # --- TABS ---
    tabs = st.tabs(['📊 Dashboard Financeiro', '👥 Bancada (Deputados)', '🗓️ Agenda & Eventos'])

    # ---------------------------------------------------------------------
    # TAB 1: GASTOS (DASHBOARD)
    # ---------------------------------------------------------------------
    with tabs[0]:
        if not df_gastos.empty:
            st.subheader("Transparência e Uso da Cota Parlamentar")

            valor_total = df_gastos["valor_liquido"].sum()
            media_por_deputado = valor_total / max(status['total_membros'], 1)
            maior_fornecedor = df_gastos.groupby("nome_fornecedor")["valor_liquido"].sum().idxmax()
            valor_maior_fornecedor = df_gastos.groupby("nome_fornecedor")["valor_liquido"].sum().max()

            k1, k2, k3 = st.columns(3)
            k1.metric("Gasto Total da Bancada",
                      f"R$ {valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            k2.metric("Média por Deputado",
                      f"R$ {media_por_deputado:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            k3.metric(f"Maior Fornecedor ({maior_fornecedor[:15]}...)",
                      f"R$ {valor_maior_fornecedor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

            st.divider()

            g1, g2 = st.columns(2)

            with g1:
                gastos_por_tipo = (
                    df_gastos.groupby("tipo_despesa")["valor_liquido"]
                    .sum()
                    .reset_index()
                    .sort_values(by="valor_liquido", ascending=False)
                )
                fig1 = px.pie(
                    gastos_por_tipo,
                    values="valor_liquido",
                    names="tipo_despesa",
                    title="Distribuição dos Gastos (Tipo)",
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig1.update_traces(textposition='inside', textinfo='percent+label')
                fig1.update_layout(showlegend=False)
                st.plotly_chart(fig1, use_container_width=True)

            with g2:
                gastos_mensais = (
                    df_gastos.groupby(["ano", "mes"])["valor_liquido"]
                    .sum()
                    .reset_index()
                )
                gastos_mensais["data"] = pd.to_datetime(
                    gastos_mensais["ano"].astype(str) + "-" + gastos_mensais["mes"].astype(str) + "-01"
                )
                gastos_mensais = gastos_mensais.sort_values("data")

                fig2 = px.area(
                    gastos_mensais,
                    x="data",
                    y="valor_liquido",
                    title="Evolução Temporal dos Gastos",
                    labels={"valor_liquido": "R$", "data": "Mês"},
                    markers=True
                )
                st.plotly_chart(fig2, use_container_width=True)

            st.divider()

            g3, g4 = st.columns(2)

            with g3:
                gasto_por_deputado = (
                    df_gastos.groupby("id_deputado")["valor_liquido"]
                    .sum()
                    .reset_index()
                ).sort_values("valor_liquido", ascending=True).tail(10)  # Top 10 Gastadores

                mapa_nomes = {d.id: d.nome for d in partido.membros}
                gasto_por_deputado["nome"] = gasto_por_deputado["id_deputado"].map(mapa_nomes)

                fig3 = px.bar(
                    gasto_por_deputado,
                    x="valor_liquido",
                    y="nome",
                    orientation="h",
                    title="Top 10 Deputados (Maior Utilização da Cota)",
                    text_auto='.2s'
                )
                st.plotly_chart(fig3, use_container_width=True)

            with g4:
                # TOP FORNECEDORES
                fornecedores = (
                    df_gastos.groupby("nome_fornecedor")["valor_liquido"]
                    .sum()
                    .reset_index()
                    .sort_values("valor_liquido",
                                 ascending=True)
                    .tail(10)
                )
                fig4 = px.bar(
                    fornecedores,
                    x="valor_liquido",
                    y="nome_fornecedor",
                    orientation="h",
                    title="Top 10 Fornecedores",
                    text_auto='.2s',
                    color_discrete_sequence=['#ff7f0e']
                )
                st.plotly_chart(fig4, use_container_width=True)

        else:
            st.info("Não há dados de despesas consolidados para este partido ou período.")

    # ---------------------------------------------------------------------
    # TAB 2: DEPUTADOS (MEMBROS)
    # ---------------------------------------------------------------------
    with tabs[1]:
        c_busca, c_vazio = st.columns([2, 1])
        with c_busca:
            search_name = st.text_input(
                "🔎 Buscar na bancada:",
                placeholder="Digite o nome do deputado...",
                key=f'search_{partido.sigla}'
            )

        if search_name:
            membros_filtrados = [
                d for d in partido.membros
                if d.nome.lower().startswith(search_name.lower())
            ]
        else:
            membros_filtrados = partido.membros

        st.markdown(f"**Total listado:** {len(membros_filtrados)} parlamentares")
        st.divider()

        if membros_filtrados:
            for deputado in membros_filtrados:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([0.5, 3, 1])
                    with col1:
                        st.image(deputado.url_foto, width=70, output_format='PNG')
                    with col2:
                        st.markdown(f"### {deputado.nome}")
                        st.markdown(f"**UF:** {deputado.sigla_uf}")
                    with col3:
                        st.markdown("<br>", unsafe_allow_html=True)
                        informacoes_deputado_button(deputado)
        elif search_name:
            st.warning("⚠️ Nenhum deputado encontrado com esse nome.")
        else:
            st.info("Este partido não possui membros cadastrados na API.")

    # ---------------------------------------------------------------------
    # TAB 3: EVENTOS
    # ---------------------------------------------------------------------
    with tabs[2]:
        st.subheader("Agenda Legislativa da Bancada")

        c1, c2 = st.columns([1, 1])
        with c1:
            d_ini, d_fim = filtro_data('eventos_partido')
        with c2:
            nome_deputado_filtro = st.selectbox(
                label='Filtrar por Deputado Específico',
                options=partido.membros,
                format_func=lambda x: x.nome,
                index=None,
                placeholder='Todos os membros'
            )

        st.divider()

        if d_ini <= d_fim:
            list_eventos = dict()

            with st.spinner("Buscando agenda..."):
                if nome_deputado_filtro is None:

                    def _fetch_eventos(dep):
                        return (dep, DEPUTADOS.get_eventos(dep.id, dataInicio=d_ini, dataFim=d_fim))


                    with ThreadPoolExecutor(max_workers=5) as executor:

                        membros_para_busca = partido.membros
                        resultados_eventos = executor.map(_fetch_eventos, membros_para_busca)

                    for dep, evts in resultados_eventos:
                        if evts: list_eventos[dep.nome] = evts
                else:
                    eventos = DEPUTADOS.get_eventos(nome_deputado_filtro.id, dataInicio=d_ini, dataFim=d_fim)
                    if eventos: list_eventos[nome_deputado_filtro.nome] = eventos

            if list_eventos:
                for nome_dep, eventos in list_eventos.items():
                    st.markdown(f"#### 👤 Agenda: {nome_dep}")
                    for e in eventos:
                        data_fmt = f"{e.dataHoraInicio[8:10]}/{e.dataHoraInicio[5:7]} às {e.dataHoraInicio[11:16]}"
                        with st.expander(f"🗓️ {data_fmt} | {e.descricaoTipo}"):
                            st.write(f"**Descrição:** {e.descricao}")
                            if e.localExterno:
                                st.caption(f"📍 Local: {e.localExterno}")
                            if e.urlRegistro:
                                st.link_button("Ver Registro / Vídeo", e.urlRegistro)
                    st.divider()
            else:
                st.info('📅 Nenhum evento encontrado para o período/filtro selecionado.')
        else:
            st.error("Data final deve ser maior que a inicial.")

else:
    st.warning('⚠️ Nenhum partido selecionado. Volte à página inicial e escolha um partido.')