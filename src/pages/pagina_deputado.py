import streamlit as st
from dataclasses import asdict
deputado = st.session_state['selected_deputado']

st.title(deputado.nome)
st.write(asdict(deputado))
