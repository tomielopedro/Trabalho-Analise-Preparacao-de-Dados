import streamlit as st
import pandas as pd
from datetime import datetime, date
from utils.utils import deputado_despesas, deputado_hitorico, tratar_data_historico, deputados_eventos, \
    interval_years_months

# === CSS CUSTOMIZADO PARA ESTILO ===
st.markdown("""
    <style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
    }
    .profile-card {
        padding: 20px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# === CONFIG ===
deputado = st.session_state.get('selected_deputado')

if deputado:
    # ==========================================
    # 1. CABEÇALHO (PERFIL)
    # ==========================================
    with st.container():
        col_foto, col_info, col_extra = st.columns([1, 3, 2])

        with col_foto:
            st.image(deputado.ultimo_status.url_foto, width=150)

        with col_info:
            st.title(deputado.nome)
            st.markdown(f"### {deputado.ultimo_status.sigla_partido} - {deputado.ultimo_status.sigla_uf}")

            # Status badge
            situacao_cor = "green" if "Exercício" in str(deputado.ultimo_status.situacao) else "orange"
            st.markdown(
                f":{situacao_cor}[●] **{deputado.ultimo_status.situacao}** | {deputado.ultimo_status.condicao_eleitoral}")

        with col_extra:
            st.markdown("##### Contato & Redes")

            cols_redes = st.columns(4)
            icon_map = {'twitter': '🐦', 'facebook': '📘', 'instagram': '📷', 'youtube': '▶️'}

            for i, rede in enumerate(deputado.rede_social[:4]):
                nome_rede = next((k for k in icon_map if k in rede), '🔗')
                icone = icon_map.get(nome_rede, '🔗')
                with cols_redes[i]:
                    st.link_button(icone, rede)

            st.caption(f"📧 {deputado.ultimo_status.gabinete.email}")

    st.divider()

    # ==========================================
    # 2. TABS DE CONTEÚDO
    # ==========================================
    tabs = ['🏛️ Informações', '📊 Dashboard & Despesas', '📜 Histórico', '📅 Eventos']
    tab_info, tab_despesas,  tab_historico, tab_eventos = st.tabs(tabs)


    # --- FUNÇÃO HELPER PARA FILTRO DE DATA ---
    def filtro_data(key_suffix):
        hoje = date.today()
        inicio_ano = date(hoje.year, 1, 1)

        c1, c2 = st.columns(2)
        with c1:
            d_ini = st.date_input('📅 Data Inicial', value=inicio_ano, format='DD/MM/YYYY', key=f'ini_{key_suffix}')
        with c2:
            d_fim = st.date_input('📅 Data Final', value=hoje, format='DD/MM/YYYY', key=f'fim_{key_suffix}')
        return d_ini, d_fim


    # ==========================================
    # TAB: DESPESAS
    # ==========================================
    with tab_despesas:
        st.subheader("Transparência e Gastos")
        d_ini, d_fim = filtro_data('despesas')

        if d_ini > d_fim:
            st.error('A data inicial deve ser menor que a final')
        else:
            anos, mes = interval_years_months(str(d_ini), str(d_fim))
            # Pega os dados
            lista_despesas = deputado_despesas(deputado.id, ano=anos, mes=mes)

            if lista_despesas:
                # Converter para DataFrame do Pandas para facilitar análise
                data_dicts = [
                    {
                        "Data": f"{d.ano}-{d.mes:02d}-01",
                        "Ano": d.ano,
                        "Mês": d.mes,
                        "Tipo": d.tipo_despesa,
                        "Fornecedor": d.nome_fornecedor,
                        "Valor": d.valor_liquido,
                        "Documento": d.url_documento
                    }
                    for d in lista_despesas
                ]
                df = pd.DataFrame(data_dicts)
                df['Data'] = pd.to_datetime(df['Data'])

                # --- KPIs ---
                kpi1, kpi2, kpi3 = st.columns(3)
                kpi1.metric("Total Gasto no Período", f"R$ {df['Valor'].sum():,.2f}")
                kpi2.metric("Média por Gasto", f"R$ {df['Valor'].mean():,.2f}")
                kpi3.metric("Maior Gasto Único", f"R$ {df['Valor'].max():,.2f}")

                st.divider()

                # --- GRÁFICOS ---
                g1, g2 = st.columns(2)

                with g1:
                    st.markdown("##### Gastos por Categoria")
                    # Agrupar por tipo
                    df_tipo = df.groupby("Tipo")["Valor"].sum().sort_values(ascending=True)
                    st.bar_chart(df_tipo, color="#ff4b4b", horizontal=True)

                with g2:
                    st.markdown("##### Evolução Temporal")
                    df_tempo = df.groupby("Data")["Valor"].sum()
                    st.line_chart(df_tempo)

                st.markdown("##### Detalhamento das Despesas")

                st.dataframe(
                    df[['Ano', 'Mês', 'Tipo', 'Fornecedor', 'Valor', 'Documento']],
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Valor": st.column_config.NumberColumn(
                            "Valor (R$)", format="R$ %.2f"
                        ),
                        "Documento": st.column_config.LinkColumn(
                            "Nota Fiscal", display_text="Abrir NF"
                        )
                    }
                )
            else:
                st.info("Nenhuma despesa encontrada para o período selecionado.")

    # ==========================================
    # TAB: INFORMAÇÕES
    # ==========================================
    with tab_info:
        c1, c2 = st.columns(2)

        with c1:
            with st.container(border=True):
                st.markdown("#### 🏛️ Dados Políticos")
                st.write(f"**ID Legislatura:** {deputado.ultimo_status.id_legislatura}")
                st.write(
                    f"**Gabinete:** {deputado.ultimo_status.gabinete.nome} - Prédio {deputado.ultimo_status.gabinete.predio}")
                st.write(f"**Telefone:** {deputado.ultimo_status.gabinete.telefone}")

        with c2:
            with st.container(border=True):
                st.markdown("#### 👤 Dados Pessoais")
                dt_nasc = datetime.strptime(deputado.data_nascimento, '%Y-%m-%d').strftime('%d/%m/%Y')
                st.write(f"**Nascimento:** {dt_nasc} ({deputado.uf_nascimento})")
                st.write(f"**Escolaridade:** {deputado.escolaridade}")
                st.write(f"**CPF:** {deputado.cpf[:3]}.***.***-**")

    # ==========================================
    # TAB: HISTÓRICO
    # ==========================================
    with tab_historico:
        historico = deputado_hitorico(deputado.id)
        # Inverter para mostrar o mais recente primeiro
        for item in reversed(historico):
            with st.container(border=True):
                col_ano, col_desc = st.columns([1, 4])
                with col_ano:
                    st.markdown(f"### {item.get('ano', '????')}")
                with col_desc:
                    st.markdown(f"**{item.get('siglaPartido')}** - {item.get('situacao')}")
                    st.caption(item.get('descricaoStatus'))

    # ==========================================
    # TAB: EVENTOS
    # ==========================================
    with tab_eventos:
        d_ini, d_fim = filtro_data('eventos')

        if d_ini <= d_fim:
            eventos = deputados_eventos(deputado.id, dataInicio=d_ini, dataFim=d_fim)

            if not eventos:
                st.info("Nenhum evento neste período.")

            for e in eventos:

                data_formatada = f"{e.dataHoraInicio[8:10]}/{e.dataHoraInicio[5:7]} - {e.dataHoraInicio[11:16]}"

                with st.expander(f"🗓️ {data_formatada} | {e.descricaoTipo}"):
                    st.write(f"**Descrição:** {e.descricao}")
                    st.write(f"**Situação:** {e.situacao}")

                    if e.orgaos:
                        st.markdown("**Órgãos envolvidos:**")
                        for org in e.orgaos:
                            st.code(f"{org.sigla} - {org.nome}")

                    if e.urlRegistro:
                        st.link_button("▶️ Assistir Vídeo / Ver Registro", e.urlRegistro)
else:
    st.warning('⚠️ Selecione um deputado na página anterior para visualizar os dados.')