import pandas as pd
import streamlit as st
from PartidoClass import Partido
from DeputadosClass import Deputados

partido = Partido()
partido_atual = st.session_state.partido
membros = partido.get_partidos_membros(partido_atual['id'])

deputados_class = Deputados()
deputados_despesas = []

for memb in membros:
    despesas = deputados_class.get_deputados_despesas(memb['id'])
    for d in despesas:
        d['id_deputado'] = memb['id']  # adiciona o id em cada despesa
        deputados_despesas.append(d)

deputados_despesas = pd.DataFrame(deputados_despesas)


st.title(partido_atual['nome'])
st.subheader(partido_atual['sigla'])
estatisticas_tab, membros_tab = st.tabs(['Estatatísticas do Partido', 'Membros do partido'])


with estatisticas_tab:
    col1,col2 = st.columns(2)
    with col1:
        st.metric('Total de Membros', value=len(membros), border=True)
    with col2:
        st.metric('Total de Gastos', value=f'R$ {deputados_despesas['valorLiquido'].sum():,.2f}', border=True)
    st.data_editor(deputados_despesas)

with membros_tab:
    for i in range(0, len(membros), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(membros):
                membro = membros[i + j]
                with cols[j]:
                    with st.container(border=True):
                        despesas = deputados_class.get_deputados_despesas(membro['id'])
                        st.image(membro['urlFoto'], width=100)
                        st.write(membro['nome'])
                        st.json(membro, expanded=False)
                        despesas = deputados_despesas[deputados_despesas['id_deputado']==membro['id']]
                        st.write(f'Total de despesas: R$ {despesas['valorLiquido'].sum():,.2f}')