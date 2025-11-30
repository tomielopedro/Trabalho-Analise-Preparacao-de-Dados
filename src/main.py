from utils.utils import Deputados, Partidos
import streamlit as st
deputados, partidos = Deputados(), Partidos()
st.set_page_config(layout="wide", page_title="Portal Parlamentar", page_icon="🏛️", initial_sidebar_state="collapsed")
if 'selected_partido' not in st.session_state:
    st.session_state['selected_partido'] = None

if 'selected_deputado' not in st.session_state:
    st.session_state['selected_deputado'] = None

st.session_state['pagina_partido'] = st.Page("pages/pagina_partido.py", title="Pagina Inicial"),


if 'deputados' not in st.session_state:
    st.session_state['deputados'] = deputados.get_all()

if 'partidos' not in st.session_state:
    st.session_state['partidos'] = partidos.get_all_detailed()


pages = {
    "Paginas": [
        st.Page("pages/pagina_inicial.py", title="Pagina Inicial"),
        st.Page("pages/pagina_partido.py", title="Informações do Partido"),
        st.Page("pages/pagina_deputado.py", title="Informações do deputado")
    ]
}


pg = st.navigation(pages)
pg.run()
