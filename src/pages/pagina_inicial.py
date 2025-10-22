import streamlit as st
from utils.utils import *

partidos_tab, deputados_tab = st.tabs(['Lista de Partidos', 'Lista de Deputados'])

@st.fragment
def informacoes_partido_button(partido):
    if st.button('Informações', key=f'button_{partido.nome}'):
        st.session_state['selected_partido'] = partido
        st.switch_page('pagina_partido')

with partidos_tab:
    partidos = all_partidos_detailed()
    for partido in partidos:
        with st.container(border=True, key=f'container_{partido.nome}'):
            col1, col2 = st.columns([0.5, 2])

            logo = 'assets/images/sem_foto.png'
            if partido.url_logo:
                logo = partido.url_logo
            col1.image(logo, width=100)

            with col2:
                st.write(f'### {partido.nome}')
                col3, col4, col5 = st.columns(3)

                col3.write(f'##### Situação: {partido.status.situacao}')
                col4.write(f'##### Membros: {partido.status.total_membros}')
                col5.write(f'##### Líder: {partido.status.lider.nome}')

            informacoes_partido_button(partido)

with deputados_tab:
    deputados = all_deputados()

    for deputado in deputados:
        with st.container(border=True, key=f'container_{deputado.nome}'):
            col1, col2 = st.columns([0.5, 2])
            col1.image(deputado.url_foto, width=100)
            col2.write(f'### Deputado: {deputado.nome}')
            col2.write(f'Partido: {deputado.sigla_partido.title()} | UF: {deputado.sigla_uf}')







