import streamlit as st
from dataclasses import asdict
partido = st.session_state['selected_partido']

st.title(partido.nome)
st.write(asdict(partido))
