# === BIBLIOTECAS ===
import streamlit as st
from dataclasses import asdict
from utils.utils import deputado_despesas, deputado_hitorico, tratar_data_historico
import pandas as pd
from collections import defaultdict

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
        st.write(f"### Estado: *EM CONSTRUÇÃO*")

    # Tabs para Seleção
    tabs = ['Informações', 'Histórioco', 'Eventos', 'Propostas', 'Despesas']
    info_deputado, historico_deputado, eventos_deputado, propostas_deputado, despesas_deputado = st.tabs(tabs)



    # === INFORMAÇÃOES BASICAS ===
    with info_deputado:

        tabs_info = ['Geral', 'Dados Pessoais']
        info_Geral, info_Pessoal = st.tabs(tabs_info)

        with info_Geral:

            st.write(f"Id do Deputado: {deputado.ultimo_status.id}")
            st.write(f"Id da Legislatura: {deputado.ultimo_status.id_legislatura}")

            st.write(f"Gabinete do Deputado: {deputado.ultimo_status.gabinete.nome}")
            st.write(f"Email para contato: {deputado.ultimo_status.gabinete.email}")
            st.write(f"Telefone para contato: {deputado.ultimo_status.gabinete.telefone}")


            st.write(f"Escolaridade: {deputado.escolaridade}")


        # Redes Sociais !!!!!!
            with st.container(border=True, key=f'container_redes'):
                for redes in deputado.rede_social:
                    if 'twitter' in redes:
                        st.markdown(f"[Twitter]({redes})")
                    elif 'facebook' in redes:
                        st.markdown(f"[Facebook]({redes})")
                    elif 'instagram' in redes:
                        st.markdown(f"[Instagram]({redes})")
                    elif 'youtube' in redes:
                        st.markdown(f"[Youtube]({redes})")

        with info_Pessoal:
            st.write(f"Data de Nascimento: {deputado.data_nascimento}")
            st.write(f"Estado de Nascimento: {deputado.uf_nascimento}")

            st.write(asdict(deputado))

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
    st.warning('Nenhum deputado selecionado')