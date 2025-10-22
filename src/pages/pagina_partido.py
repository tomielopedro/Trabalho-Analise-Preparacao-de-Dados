import streamlit as st

partido = st.session_state['selected_partido']

st.write(partido.nome)