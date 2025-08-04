import pandas as pd
import streamlit as st
from PartidoClass import Partido

partido = Partido()
partidos = partido.get_partidos()
if 'partido' not in st.session_state:
    st.session_state['partido'] = None

st.title(f'Total de Partidos {len(partidos)}')
st.divider()
for i in range(0, len(partidos), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j < len(partidos):
            part = partidos[i + j]
            with cols[j]:
                with st.container(border=True):
                    st.write('Partido: ' + part['nome'])
                    col1, col2, col3 = st.columns(3)
                    col1.write(f"Id: {part['id']}")
                    with col3:
                        if st.button('Entrar', key=f"entrar_{part['id']}"):
                            st.session_state['partido'] = part
                            st.switch_page('pages/partidosInfo.py')
