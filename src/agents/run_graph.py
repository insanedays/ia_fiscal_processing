from src.agents.graph import graph_executor
from src.agents.graph import AgentState


def run_graph(question: str, catalog: str) -> str:
    """
    Executa o grafo de agentes a partir de uma pergunta e de um catálogo de dados.
    Retorna a resposta final formatada para o usuário.
    """
    state_input = AgentState(
        question=question,
        catalog=catalog,
        intent=None,
        orientation=None,
        payload=None,
        validation_status=None,
        query_result=None,
        final_answer=None
    )

    final_state = graph_executor.invoke(state_input)
    return final_state.get("query_result", "Erro: nenhuma resposta gerada.")


