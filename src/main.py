from models.deputados_models import Deputado
from service.deputados_service import get_deputados_id
import streamlit as st

if 'selected_partido' not in st.session_state:
    st.session_state['selected_partido'] = None

if 'selected_deputado' not in st.session_state:
    st.session_state['selected_deputado'] = None

pages = {
    "Paginas": [
        st.Page("pages/pagina_inicial.py", title="Pagina Inicial"),
    ]
}

pg = st.navigation(pages)
pg.run()
