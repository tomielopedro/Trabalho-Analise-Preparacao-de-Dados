import streamlit as st
from dataclasses import asdict
deputado = st.session_state['selected_deputado']
tabs = ['Informações', 'Histórioco', 'Eventos', 'Propostas', 'Despesas']
col1, col2 = st.columns([0.5, 2])
col1.image(deputado.ultimo_status.url_foto, width=100)
col2.write(f'### {deputado.nome}')
info_deputado, historico_deputado, eventos_deputado, propostas_deputado, despesas_deputado = st.tabs(tabs)


with info_deputado:
    st.write(asdict(deputado))

with historico_deputado:
    st.write('Em construção')

with eventos_deputado:
    st.write('Em construção')

with propostas_deputado:
    st.write('Em construção')

with despesas_deputado:
    st.write('Em construção')
