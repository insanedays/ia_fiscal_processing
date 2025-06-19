from typing import TypedDict, Literal, Optional
from langgraph.graph import StateGraph, END
from src.agents.llm_clients import LLMClients
from src.agents.prompt_loader import load_prompt
from src.agents.query_runner import run_query
import json
import pandas as pd

# -----------------------------
# Definição do estado do grafo
# -----------------------------
class AgentState(TypedDict):
    question: str
    intent: Optional[str]
    orientation: Optional[str]
    payload: Optional[dict]
    validation_status: Optional[Literal["valid", "invalid"]]
    query_result: Optional[str]
    final_answer: Optional[str]
    catalog: str

llms = LLMClients()

# -----------------------------
# Funções dos agentes
# -----------------------------
def analyze_intent(state: AgentState) -> AgentState:
    prompt = load_prompt("analyze_intent")["prompt"]
    filled = prompt.format(input_do_usuario=state["question"])
    response = llms.get_response(filled)
    try:
        output = json.loads(response)
    except json.JSONDecodeError:
        raise ValueError(f"Resposta malformada do modelo: {response}")
    return {
        **state,
        "intent": output.get("intencao"),
        "orientation": output.get("orientacao")
    }

def generate_payload(state: AgentState) -> AgentState:
    prompt = load_prompt("generate_payload")["prompt"]
    filled = prompt.format(
        input_do_usuario=state["question"],
        catalogo_de_dados_injetado_pelo_rag=state["catalog"]
    )
    response = llms.get_response(filled)
    try:
        payload = json.loads(response)
    except json.JSONDecodeError:
        raise ValueError(f"Payload malformado do modelo: {response}")
    return {**state, "payload": payload}

def validate_payload(state: AgentState) -> AgentState:
    prompt = load_prompt("validate_payload")["prompt"]
    filled = prompt.format(
        payload_gerado=json.dumps(state["payload"]),
        catalogo_de_dados_injetado_pelo_rag=state["catalog"]
    )
    response = llms.get_response(filled)

    try:
        result = json.loads(response)
        status = result.get("status", "invalid").lower()
        if status not in ("valid", "invalid"):
            raise ValueError(f"Status fora do esperado: {status}")
    except json.JSONDecodeError:
        raise ValueError(f"Resposta não é JSON válido:\n {state["payload"]}")

    return {**state, "validation_status": status}


def run_sql(state: AgentState) -> AgentState:
    raw_result = run_query(state["payload"])

    try:
        result = json.loads(raw_result)

        if isinstance(result, dict) and "error" in result:
            return {**state, "query_result": result["error"]}

        if not result:
            return {**state, "query_result": "Nenhum resultado encontrado."}

        df = pd.DataFrame(result)
        return {**state, "query_result": df}

    except Exception as e:
        return {**state, "query_result": f"Erro ao processar resultado: {e}\nConteúdo bruto:\n{raw_result}"}


# -----------------------------
# Construção do grafo
# -----------------------------
graph = StateGraph(AgentState)

# Nós
graph.add_node("analyze_intent", analyze_intent)
graph.add_node("generate_payload", generate_payload)
graph.add_node("validate_payload", validate_payload)
graph.add_node("run_query", run_sql)
# graph.add_node("rewrite_response", rewrite_response)

# Ciclos e fluxo

graph.set_entry_point("analyze_intent")
graph.add_edge("analyze_intent", "generate_payload")
graph.add_edge("generate_payload", "validate_payload")

graph.add_conditional_edges(
    "validate_payload",
    lambda state: "valid" if state["validation_status"] == "valid" else "invalid",
    {
        "valid": "run_query",
        "invalid": "analyze_intent"
    }
)

graph.add_edge("run_query", END)
# graph.add_edge("run_query", "rewrite_response")
# graph.add_edge("rewrite_response", END)

# Executor
graph_executor = graph.compile()
