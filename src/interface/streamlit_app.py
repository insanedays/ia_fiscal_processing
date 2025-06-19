import streamlit as st
from src.agents.run_graph import run_graph
from utilis.load_db_catalog import load_catalog

# Carrega conteúdo do catálogo de dados
catalog_content = load_catalog()

def run():
    st.set_page_config(page_title="Chat Fiscal Inteligente")
    st.title("Consulta de Dados Fiscais com LLM")

    question = st.text_input("Digite sua pergunta sobre notas fiscais:")

    if st.button("Consultar") and question:
        with st.spinner("Processando sua pergunta..."):
            resposta = run_graph(question=question, catalog=catalog_content)
        st.subheader("Resposta:")
        st.write(resposta)
