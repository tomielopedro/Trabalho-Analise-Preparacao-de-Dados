import streamlit as st
from dataclasses import asdict

partido = st.session_state['selected_partido']

tabs = ['Informações do Partido', 'Deputados', 'Gastos', 'Propostas', 'Eventos']
st.title(partido.nome)
info_partido, deputados_partido, gastos_partido, prospostas_partido, eventos_partido = st.tabs(tabs)

with info_partido:
    st.title(partido.nome)
    st.write(asdict(partido))

with deputados_partido:
    st.write(partido.membros)

with gastos_partido:
    st.write('Em construção')

with prospostas_partido:
    st.write('Em construção')

with eventos_partido:
    st.write('Em construção')


