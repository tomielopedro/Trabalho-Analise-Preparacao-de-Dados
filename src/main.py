from utils.utils import all_deputados, all_partidos_detailed
import streamlit as st
from datetime import datetime, date

if 'selected_partido' not in st.session_state:
    st.session_state['selected_partido'] = None

if 'selected_deputado' not in st.session_state:
    st.session_state['selected_deputado'] = None

st.session_state['pagina_partido'] = st.Page("pages/pagina_partido.py", title="Pagina Inicial"),


if 'deputados' not in st.session_state:
    st.session_state['deputados'] = all_deputados()

if 'partidos' not in st.session_state:
    st.session_state['partidos'] = all_partidos_detailed()


pages = {
    "Paginas": [
        st.Page("pages/pagina_inicial.py", title="Pagina Inicial"),
        st.Page("pages/pagina_partido.py", title="Informações do Partido"),
        st.Page("pages/pagina_deputado.py", title="Informações do deputado")
    ]
}


pg = st.navigation(pages)
pg.run()
