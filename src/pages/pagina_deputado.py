import streamlit as st
from dataclasses import asdict
from utils.utils import deputado_despesas, deputado_hitorico
import pandas as pd

deputado = st.session_state['selected_deputado']

col1, col2 = st.columns([0.5, 2])
col1.image(deputado.ultimo_status.url_foto, width=100)
col2.write(f'### {deputado.nome}')

tabs = ['Informações', 'Histórioco', 'Eventos', 'Propostas', 'Despesas']
info_deputado, historico_deputado, eventos_deputado, propostas_deputado, despesas_deputado = st.tabs(tabs)


with info_deputado:
    st.write(asdict(deputado))

with historico_deputado:
    st.write(deputado_hitorico(deputado.id))

with eventos_deputado:
    st.write('Em construção')

with propostas_deputado:
    st.write('Em construção')

with despesas_deputado:
    df = pd.DataFrame(deputado_despesas(deputado.id))
    st.data_editor(df)
