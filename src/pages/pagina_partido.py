from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from pages.pagina_inicial import informacoes_deputado_button
from utils.utils import (get_deputado_despesa, get_deputado_historico,
                         get_deputados_id)


def _buscar_gastos(deputado):
        df_temp = pd.DataFrame(get_deputado_despesa(deputado_id=deputado.id))
        df_temp.insert(0, 'id_deputado', deputado.id)
        return df_temp


def _consolidar_gastos_partido(partido):
    deputados = partido.membros
    df_gastos_list = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        resultados = executor.map(_buscar_gastos, deputados)

    for df_temp in resultados:
        df_gastos_list.append(df_temp)

    df_gastos = pd.concat(df_gastos_list, ignore_index=True)
    return df_gastos


partido = st.session_state['selected_partido']
if partido:
    infos = asdict(partido)

    if ('gastos_partido' not in st.session_state or st.session_state.get('gastos_partido_partido_id') != partido.id):
        st.session_state['gastos_partido'] = _consolidar_gastos_partido(partido)
        st.session_state['gastos_partido_partido_id'] = partido.id

    st.title(partido.nome)

    tabs = ['Informações do Partido', 'Deputados', 'Gastos', 'Propostas', 'Eventos']
    info_partido, deputados_partido, gastos_partido, prospostas_partido, eventos_partido = st.tabs(tabs)

    with info_partido:
        status = infos["status"]
        lider = status["lider"]

        st.subheader("📋 Dados gerais")
        st.write(f"**Sigla:** {infos['sigla']}")
        st.write(f"**Situação:** `{status['situacao']}`")
        st.write(f"**Total de membros:** {status['total_membros']}")
        data_formatada = datetime.fromisoformat(status['data']).strftime("%d/%m/%Y %H:%M")
        st.write(f"**Data do status:** {data_formatada}")
        st.write(f"**Legislatura:** {status['id_legislatura']}")
        st.divider()

        st.subheader("👤 Liderança")
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(lider["url_foto"], width=120)
        with col2:
            st.write(f"### {lider['nome']}")
            st.write(f"**UF:** {lider['uf']}")
            # informacoes_deputado_button(lider)
        st.divider()

    with deputados_partido:
        search_name = st.text_input(
            "Buscar deputado por nome:",
            placeholder="Digite o nome para filtrar...",
            key=f'search_{partido.sigla}'
        )

        if search_name:
            membros_filtrados = [
                deputado for deputado in partido.membros
                if deputado.nome.lower().startswith(search_name.lower())
            ]
        else:
            membros_filtrados = partido.membros

        if membros_filtrados:
            for deputado in membros_filtrados:
                with st.container(border=True, key=f'container_{deputado.nome}'):
                    col1, col2 = st.columns([0.5, 2])
                    col1.image(deputado.url_foto, width=100)
                    col2.write(f'### {deputado.nome}')
                    col2.write(f'**UF**: {deputado.sigla_uf}')
                    informacoes_deputado_button(deputado)
        elif search_name:
            st.error("Nenhum deputado encontrado com esse nome.")
        else:
            st.info("Este partido não possui membros na lista.")

    with gastos_partido:
        valor_total = st.session_state['gastos_partido']["valorLiquido"].sum()
        valor_total_str = f'{valor_total:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        st.write(f'## Valor Total: R${valor_total_str}')
        st.divider()

        # GASTOS POR TIPO - GRÁFICO DE PIZZA
        gastos_por_tipo = (
            st.session_state['gastos_partido'].groupby("tipoDespesa")["valorLiquido"]
            .sum()
            .reset_index()
            .sort_values(by="valorLiquido", ascending=False)
        )
        fig1 = px.pie(
            gastos_por_tipo,
            values="valorLiquido",
            names="tipoDespesa",
            title="Distribuição percentual dos gastos por tipo de despesa",
            hole=0,
        )
        fig1.update_traces(textinfo="percent")
        st.plotly_chart(fig1, use_container_width=True)
        st.divider()

        # GASTOS MENSAIS - GRÁFICO DE LINHA
        gastos_mensais = (
            st.session_state['gastos_partido'].groupby(["ano", "mes"])["valorLiquido"]
            .sum()
            .reset_index()
        )
        gastos_mensais["data"] = (
            pd.to_datetime
            (gastos_mensais["ano"].astype(int).astype(str) + "-" + gastos_mensais["mes"].astype(int).astype(str) + "-01")
        )
        fig2 = px.line(
            gastos_mensais,
            x="data",
            y="valorLiquido",
            title="Evolução mensal dos gastos do partido",
            labels={"valorLiquido": "Valor total (R$)", "data": "Mês"},
            markers=True
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.divider()

        # GASTOS POR DEPUTADO - GRÁFICO DE BARRA
        gasto_por_deputado = (
            st.session_state['gastos_partido'].groupby("id_deputado")["valorLiquido"]
            .sum()
            .reset_index()
        ).sort_values("valorLiquido", ascending=True)
        gasto_por_deputado["nome"] = gasto_por_deputado["id_deputado"].map({d.id: d.nome for d in partido.membros})
        fig3 = px.bar(
            gasto_por_deputado,
            x="valorLiquido",
            y="nome",
            orientation="h",
            title="Total gasto por deputado",
            labels={"valorLiquido": "Valor total (R$)", "nome": "Deputado"},
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.divider()

        # GASTOS POR FORNECEDOR - GRÁFICO DE BARRA
        fornecedores = (
            st.session_state['gastos_partido'].groupby("nomeFornecedor")["valorLiquido"]
            .sum()
            .reset_index()
            .sort_values("valorLiquido", ascending=False)
            .head(10)
        ).sort_values('valorLiquido')
        fig4 = px.bar(
            fornecedores,
            x="valorLiquido",
            y="nomeFornecedor",
            orientation="h",
            title="Top 10 Fornecedores mais Pagos",
            labels={"valorLiquido": "Valor total (R$)", "nomeFornecedor": "Fornecedor"},
        )
        st.plotly_chart(fig4, use_container_width=True)
        st.divider()

    with prospostas_partido:
        st.write('Em construção')

    with eventos_partido:
        st.write('Em construção')
else:
    st.warning('Nenhum partido selecionado')

