import streamlit as st
import pandas as pd
from datetime import datetime, date
import base64
import os
from utils.utils import Deputados, interval_years_months

# ==========================================
# 0. CONFIGURAÇÃO E ESTILO
# ==========================================

st.set_page_config(layout="wide", page_title="Portal Parlamentar - Deputados", page_icon="🏛️")


DEPUTADOS = Deputados()


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

    /* Ajuste de imagens */
    .profile-img {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 1. FUNÇÕES AUXILIARES
# ==========================================

def get_img_as_base64(file_path):
    """Lê imagem local e converte para base64 para uso em HTML"""
    if not os.path.exists(file_path):
        return None
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def render_social_icon(url, icon_path, alt_text):
    """Renderiza ícone social ou fallback textual"""
    img_b64 = get_img_as_base64(icon_path)
    if img_b64:
        return f"""
            <a href="{url}" target="_blank" style="text-decoration:none; margin-right:10px;">
                <img src="data:image/png;base64,{img_b64}" width="24" height="24" title="{alt_text}">
            </a>
        """
    else:
        # Fallback profissional usando Emoji se a imagem não existir
        emojis = {'twitter': '🐦', 'facebook': '📘', 'instagram': '📸', 'youtube': '▶️'}
        emoji = next((v for k, v in emojis.items() if k in alt_text.lower()), '🔗')
        return f'<a href="{url}" target="_blank" style="text-decoration:none; font-size:20px; margin-right:10px;">{emoji}</a>'


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
# 2. CONTEÚDO PRINCIPAL
# ==========================================

deputado = st.session_state.get('selected_deputado')

if deputado:
    # --- HEADER / PERFIL
    with st.container():
        st.markdown('<div class="card-container">', unsafe_allow_html=True)

        # COLUNAS: [Foto (Pequena)] [Dados Principais (Largo)] [Contatos (Médio)]
        c_foto, c_info, c_contato = st.columns([1, 3, 2])

        with c_foto:
            st.image(deputado.ultimo_status.url_foto, width=150)

        with c_info:
            st.markdown(f"## {deputado.nome}")
            st.markdown(
                f"#### <span class='highlight-text'>{deputado.ultimo_status.sigla_partido}</span> - {deputado.ultimo_status.sigla_uf}",
                unsafe_allow_html=True)


            situacao = deputado.ultimo_status.situacao
            cor_bg = "#d4edda" if "Exercício" in situacao else "#fff3cd"
            cor_txt = "#155724" if "Exercício" in situacao else "#856404"

            st.markdown(f"""
                <span class="status-badge" style="background-color:{cor_bg}; color:{cor_txt};">
                    ● {situacao}
                </span>
                <span style="margin-left:10px; font-size:0.9rem; color:#666;">
                    Condição: {deputado.ultimo_status.condicao_eleitoral}
                </span>
            """, unsafe_allow_html=True)

        with c_contato:
            st.markdown("##### Contato Direto")
            st.markdown(f"**📧** `{deputado.ultimo_status.gabinete.email}`")
            st.markdown(f"**📞** `{deputado.ultimo_status.gabinete.telefone}`")

            st.markdown("##### 🌐 Redes Sociais")

            icon_map = {
                'twitter': 'assets/images/x.png',
                'facebook': 'assets/images/facebook.png',
                'instagram': 'assets/images/instagram.png',
                'youtube': 'assets/images/youtube.png'
            }

            html_icons = ""
            # Pega apenas as 5 primeiras redes para não quebrar layout
            for rede in deputado.rede_social[:5]:
                nome_rede = next((k for k in icon_map if k in rede), "Link")
                html_icons += render_social_icon(rede, icon_map.get(nome_rede, ""), nome_rede)

            st.markdown(html_icons, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


    tabs = st.tabs(['Dashboard & Despesas', 'Informações Gerais', 'Histórico', 'Agenda'])

    # ==========================================
    # TAB 1: DASHBOARD FINANCEIRO
    # ==========================================
    with tabs[0]:
        st.subheader("Transparência e Gastos")

        with st.expander("🔍 Filtros de Período", expanded=True):
            d_ini, d_fim = filtro_data('despesas')

        if d_ini > d_fim:
            st.error('⚠️ A data inicial deve ser menor que a final.')
        else:
            anos, mes = interval_years_months(str(d_ini), str(d_fim))

            with st.spinner('Carregando dados financeiros...'):
                lista_despesas = DEPUTADOS.get_despesas(deputado.id, ano=anos, mes=mes)

            if lista_despesas:
                data_dicts = [{
                    "Data": datetime(d.ano, d.mes, 1),
                    "Tipo": d.tipo_despesa,
                    "Fornecedor": d.nome_fornecedor,
                    "Valor": d.valor_liquido,
                    "Doc": d.url_documento
                } for d in lista_despesas]

                df = pd.DataFrame(data_dicts)


                k1, k2, k3, k4 = st.columns(4)
                k1.metric("Total Gasto", f"R$ {df['Valor'].sum():,.2f}")
                k2.metric("Média Mensal", f"R$ {df.groupby('Data')['Valor'].sum().mean():,.2f}")
                k3.metric("Maior Despesa", f"R$ {df['Valor'].max():,.2f}")
                k4.metric("Qtd. Notas", len(df))

                st.divider()

                g1, g2 = st.columns(2)
                with g1:
                    st.markdown("#### Gastos por Categoria")
                    chart_data = df.groupby("Tipo")["Valor"].sum().sort_values(ascending=True)
                    st.bar_chart(chart_data, color="#007bff", horizontal=True)

                with g2:
                    st.markdown("#### Evolução Temporal")
                    time_data = df.groupby("Data")["Valor"].sum()
                    st.line_chart(time_data, color="#28a745")

                st.markdown("#### Detalhamento das Notas")
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Data": st.column_config.DateColumn("Mês/Ano", format="MM/YYYY"),
                        "Valor": st.column_config.NumberColumn("Valor (R$)", format="R$ %.2f"),
                        "Doc": st.column_config.LinkColumn("Nota Fiscal", display_text="Abrir PDF")
                    }
                )
            else:
                st.info("ℹ️ Nenhuma despesa encontrada para o período selecionado.")

    # ==========================================
    # TAB 2: INFORMAÇÕES
    # ==========================================
    with tabs[1]:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 🏛️ Dados Parlamentares")
            with st.container(border=True):
                st.markdown(f"**Legislatura ID:** {deputado.ultimo_status.id_legislatura}")
                st.markdown(f"**Gabinete:** {deputado.ultimo_status.gabinete.nome}")
                st.markdown(
                    f"**Localização:** Prédio {deputado.ultimo_status.gabinete.predio}, Sala {deputado.ultimo_status.gabinete.sala} - Andar {deputado.ultimo_status.gabinete.andar}")

        with c2:
            st.markdown("### 👤 Dados Pessoais")
            with st.container(border=True):
                try:
                    nasc = datetime.strptime(deputado.data_nascimento, '%Y-%m-%d').strftime('%d/%m/%Y')
                except:
                    nasc = deputado.data_nascimento

                st.markdown(f"**Nascimento:** {nasc}")
                st.markdown(f"**Naturalidade:** {deputado.municipio_nascimento} - {deputado.uf_nascimento}")
                st.markdown(f"**Escolaridade:** {deputado.escolaridade}")

    # ==========================================
    # TAB 3: HISTÓRICO
    # ==========================================
    with tabs[2]:
        historico = DEPUTADOS.get_historico(deputado.id)
        if historico:
            st.markdown("### Linha do Tempo")
            for h in reversed(historico):
                ano_evento = h.get('dataHora', '')[:4]
                with st.container(border=True):
                    col_ico, col_txt = st.columns([0.5, 4])
                    with col_ico:
                        st.markdown(f"## {ano_evento}")
                    with col_txt:
                        st.markdown(f"**{h.get('siglaPartido')}** - {h.get('situacao')}")
                        st.caption(f"Status: {h.get('descricaoStatus')}")
        else:
            st.warning("Histórico indisponível.")

    # ==========================================
    # TAB 4: EVENTOS
    # ==========================================
    with tabs[3]:
        d_ini, d_fim = filtro_data('eventos')
        if d_ini <= d_fim:
            eventos = DEPUTADOS.get_eventos(deputado.id, dataInicio=d_ini, dataFim=d_fim)
            if eventos:
                eventos = sorted(eventos, key=lambda x: x.dataHoraInicio)
                for e in eventos:
                    data_fmt = f"{e.dataHoraInicio[8:10]}/{e.dataHoraInicio[5:7]} às {e.dataHoraInicio[11:16]}"
                    with st.expander(f"🗓️ {data_fmt} | {e.descricaoTipo}"):
                        st.write(e.descricao)
                        if e.localExterno:
                            st.caption(f"📍 Local: {e.localExterno}")
                        if e.urlRegistro:
                            st.link_button("Ver Registro / Vídeo", e.urlRegistro)
            else:
                st.info("Nenhum evento agendado neste período.")

else:
    st.markdown("""
        <div style='text-align: center; padding: 50px;'>
            <h2>👈 Selecione um Deputado no menu para começar</h2>
            <p style='color: gray;'>Visualize gastos, histórico e agenda parlamentar de forma simplificada.</p>
        </div>
    """, unsafe_allow_html=True)