# === BIBLIOTECAS ===
import streamlit as st
from dataclasses import asdict
from utils.utils import deputado_despesas, deputado_hitorico, tratar_data_historico
import pandas as pd
from collections import defaultdict
from datetime import datetime

# === CONFIG ===
deputado = st.session_state['selected_deputado']
if deputado:
    # === DEPUTADO ===
    col1, col2 = st.columns([0.5, 2])

    with col1:
        # Imagem do Deputado
        st.image(deputado.ultimo_status.url_foto, width=100)

    with col2:
        # Info Basica do Deputado
        st.write(f'## {deputado.nome}')
        st.write(f"### Partido ***{deputado.ultimo_status.sigla_partido}***")
        st.write(f"### Estado {deputado.ultimo_status.sigla_uf}")

        # Redes Sociais !!!!!!
        with st.container(border=False, key='container_redes'):
                html = "<div style='text-align:left;'>"
                for redes in deputado.rede_social:
                    if 'twitter' in redes:
                        html += f"🐦 <a href='{redes}' target='_blank'>Twitter</a> &nbsp;&nbsp;"
                    elif 'facebook' in redes:
                        html += f"📘 <a href='{redes}' target='_blank'>Facebook</a> &nbsp;&nbsp;"
                    elif 'instagram' in redes:
                        html += f"📷 <a href='{redes}' target='_blank'>Instagram</a> &nbsp;&nbsp;"
                    elif 'youtube' in redes:
                        html += f"▶️ <a href='{redes}' target='_blank'>YouTube</a> &nbsp;&nbsp;"
                html += "</div>"

                st.markdown(html, unsafe_allow_html=True)

    # Tabs para Seleção
    tabs = ['Informações', 'Histórioco', 'Eventos', 'Propostas', 'Despesas']
    info_deputado, historico_deputado, eventos_deputado, propostas_deputado, despesas_deputado = st.tabs(tabs)



    # === INFORMAÇÃOES BASICAS ===
    with info_deputado:

        # Dados Politicos
        with st.container(border=True, key='container_Dados'):
            st.markdown(f"### Dados Politicos")
            st.markdown(f"Id do Deputado: ***{deputado.ultimo_status.id}***")
            st.markdown(f"Situação Eleitoral ***{deputado.ultimo_status.situacao}***")
            st.markdown(f"Condição ***{deputado.ultimo_status.condicao_eleitoral}***")
            st.markdown(f"Id da Legislatura: ***{deputado.ultimo_status.id_legislatura}***")

         # Gabinete
        with st.container(border=True, key='container_Gabinete'):
            st.markdown(f"### Gabinete")
            st.write(f"Gabinete do Deputado: {deputado.ultimo_status.gabinete.nome}°")
            st.write(f"Predio: {deputado.ultimo_status.gabinete.predio}°")
            # Contato
            st.markdown(f"Telefone para Contato: ***{deputado.ultimo_status.gabinete.telefone}***")
            st.markdown(f"Email para Contato: *{deputado.ultimo_status.gabinete.email}*")

        # Dados Pessoais
        with st.container(border=True, key='container_Dados_Pessoais'):
            st.markdown(f"### Dados Pessoais")
            st.markdown(f"CPF: ***{deputado.cpf}***")
            st.markdown(f"Nivel de Escolaridade: **{deputado.escolaridade}**")
            st.markdown(f"Estado de Nascimento: {deputado.uf_nascimento}")
            st.markdown(f"Municipio de Nascimento: **{deputado.municipio_nascimento}**")
            st.markdown(f"Data de Nascimento: {datetime.strptime(deputado.data_nascimento, '%Y-%m-%d').strftime('%d/%m/%Y')}")



    # === HISTÓRICO ===
    with historico_deputado:
        # Config da Tab
        historico = deputado_hitorico(deputado.id)
        ano = tratar_data_historico(deputado.id)

        for i in range(len(ano)):   # Incrementar
            with st.container(border=True, key=f'container_historico{i}'):
                st.write(f"### Ano {ano[i]}")
                st.write(f'Situação: {historico[i]["situacao"] if historico[i]["situacao"] else "---"}')
                st.write(f'Status: {historico[i]["condicaoEleitoral"] if historico[i]["condicaoEleitoral"] else "---"}')
                st.write(f'Partido: {historico[i]["siglaPartido"] if historico[i]["siglaPartido"] else "---"}')
                st.write(f'Descrição: {historico[i]["descricaoStatus"] if historico[i]["descricaoStatus"] else "---"}')



    # === EVENTOS ===
    with eventos_deputado:
        st.write('Em construção')




    # === PROPOSTAS ===
    with propostas_deputado:
        st.write('Em construção')




    # === DESPESAS ===
    with despesas_deputado:
        # Ordenar a Lista de Objetos do tipo Despesa
        despesa = sorted(deputado_despesas(deputado.id), key=lambda d: (d.ano, d.mes), reverse=True)

        # Criar Tabs para Janelas de Gastos
        tabs_gasto = ['Geral', 'Específico']
        gasto_geral, gasto_especifico = st.tabs(tabs_gasto)

        # Gastos Geral Por tipo e Data
        with gasto_geral:
            # Obter todos os anos disponíveis nas despesas
            anos_disponiveis = sorted({d.ano for d in despesa}, reverse=True)
            ano_selecionado = st.selectbox("Selecione o ano:", ["Todos"] + anos_disponiveis) # Select Box

            if ano_selecionado == "Todos":
                despesas_filtradas = despesa
            else:
                despesas_filtradas = [d for d in despesa if d.ano == ano_selecionado]

            # Agrupa os Gastos Por Tipo
            agrupado = defaultdict(list)
            for d in despesa:
                agrupado[d.tipo_despesa].append(d)


            st.write(f"## Gastos {'(Todos os anos)' if ano_selecionado == 'Todos' else f'de {ano_selecionado}'}")

            if not despesas_filtradas:
                st.warning("Nenhuma despesa encontrada para o filtro selecionado.")
            else:
                for tipo, lista in agrupado.items():
                    with st.container(border=True, key=f'container_Despesa_total_{tipo}_{ano_selecionado}'):
                        total = sum(d.valor_liquido for d in lista)
                        st.write(f"### {tipo}")
                        st.write(f"Total gasto: R$ {total:.2f}")
                        st.write(f"Número de compras: {len(lista)}")
                        st.write(f"Valor médio por gasto: R$ {(total / len(lista)):.2f}")



        # Gastos Especificos Detalhados
        with gasto_especifico:
            # Loop para mostrar todas as despesas
            for i, des in enumerate(despesa):
                # Cria o Container Geral da Página
                with st.container(border=True, key=f'container_despesa{i}'):

                    # Colunas Internas das Despesas
                    col_despesa_1, col_despesa_2 = st.columns([2, 1])

                    with col_despesa_1:
                        # Despesas
                        st.write(f"## Ano {des.ano}/{des.mes}")
                        st.write(f'### {des.tipo_despesa.title()}')
                        st.write(f"Valor da Compra **R${des.valor_documento}**")
                        st.markdown(f"Acesse a NF clicando aqui [*Nota Fiscal*]({des.url_documento})")

                    with col_despesa_2:
                        # Container interno do Vendedor
                        with st.container(border=True, key=f'container_despesa_Vendedor{i}'):
                            # Info Basica do Vendedor
                            st.write(f'***{des.nome_fornecedor}***')
                            st.write(f"CNPJ *{des.cnpj_cpf_fornecedor}*")
                            st.write(f"Cod do Lot. **{des.cod_lote}**")
                            st.write(f"A compra foi feita em  *{des.parcela}* vezes.")
else:
    st.warning('Nenhum deputado encontrado')