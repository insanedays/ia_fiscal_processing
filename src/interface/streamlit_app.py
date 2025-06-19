import streamlit as st
from src.agents.run_graph import run_graph
from src.utilis.load_db_catalog import load_catalog
import pandas as pd


# Carrega conteúdo do catálogo de dados
catalog_content = load_catalog()

import streamlit as st
import pandas as pd
from src.agents.run_graph import run_graph
from src.utilis.load_db_catalog import load_catalog

# Carrega conteúdo do catálogo de dados
catalog_content = load_catalog()

def run():
    st.set_page_config(page_title="Chat Fiscal Inteligente", layout="wide")
    st.title("Consulta de Dados Fiscais com LLM")

    # Pergunta do usuário
    question = st.text_input("Digite sua pergunta sobre notas fiscais:")

    if st.button("Consultar") and question:
        with st.spinner("Processando sua pergunta..."):
            resposta = run_graph(question=question, catalog=catalog_content)

        st.subheader("Resposta:")

        if isinstance(resposta, pd.DataFrame):
            # Altura adaptável: 35px por linha, até 800px
            altura = min(800, 40 + len(resposta) * 35)

            # Exibe DataFrame responsivo
            st.dataframe(resposta, use_container_width=True, height=altura)

            # CSS opcional para garantir scroll horizontal (seguro extra)
            st.markdown("""
                <style>
                .element-container:has(.dataframe) {
                    overflow-x: auto;
                }
                </style>
            """, unsafe_allow_html=True)

        else:
            st.write(resposta)
