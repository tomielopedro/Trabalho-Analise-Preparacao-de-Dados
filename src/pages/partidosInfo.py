import pandas as pd
import streamlit as st
import plotly.express as px
from PartidoClass import Partido
from DeputadosClass import Deputados

# === Dados do Partido e Membros ===
partido = Partido()
deputados_class = Deputados()

partido_atual = st.session_state.partido
membros = partido.get_partidos_membros(partido_atual['id'])

# === Carregando Despesas de Todos os Membros ===
deputados_despesas = []
for membro in membros:
    despesas = deputados_class.get_deputados_despesas(membro['id'])
    for d in despesas:
        d['id_deputado'] = membro['id']
        deputados_despesas.append(d)

# === Convertendo para DataFrame ===
df_despesas = pd.DataFrame(deputados_despesas)

# === Título Principal ===
st.title(partido_atual['nome'])
st.subheader(partido_atual['sigla'])

# === Criação das Abas ===
estatisticas_tab, membros_tab = st.tabs(['Estatísticas do Partido', 'Membros do Partido'])

# -----------------------------------------------------------
# Aba de Estatísticas
# -----------------------------------------------------------
with estatisticas_tab:
    # Métricas principais
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Total de Membros', value=len(membros), border=True)
    with col2:
        total_gastos = df_despesas['valorLiquido'].sum()
        st.metric('Total de Gastos', value=f'R$ {total_gastos:,.2f}', border=True)

    # Gráfico de barras por tipo de despesa
    despesas_por_tipo = (
        df_despesas.groupby('tipoDespesa')['valorLiquido']
        .sum()
        .reset_index()
        .sort_values(by='valorLiquido', ascending=False)
    )

    fig = px.bar(
        despesas_por_tipo,
        x='tipoDespesa',
        y='valorLiquido',
        title='Despesas por Tipo',
        labels={'valorLiquido': 'Total Gasto (R$)', 'tipoDespesa': 'Tipo de Despesa'},
        text_auto='.2s'
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    # Editor de dados (opcional para visualização rápida)
    st.data_editor(df_despesas)

# -----------------------------------------------------------
# Aba de Membros
# -----------------------------------------------------------
with membros_tab:
    for i in range(0, len(membros), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(membros):
                membro = membros[i + j]
                with cols[j]:
                    with st.container(border=True):
                        st.image(membro['urlFoto'], width=100)
                        st.write(f"**{membro['nome']}**")
                        st.json(membro, expanded=False)

                        # Filtra despesas do membro atual
                        despesas_membro = df_despesas[df_despesas['id_deputado'] == membro['id']]
                        total_despesas_membro = despesas_membro['valorLiquido'].sum()

                        st.write(f"Total de despesas: R$ {total_despesas_membro:,.2f}")
