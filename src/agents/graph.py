# src/core/graph.py

from typing import TypedDict, Literal, Optional
from langgraph.graph import StateGraph, END
from src.agents.llm_clients import LLMClients
from src.agents.prompt_loader import load_prompt
from src.agents.query_runner import run_query

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
    prompt = load_prompt("analyze_intent")
    filled = prompt.format(input_do_usuario=state["question"])
    response = llms.get_response(filled)
    output = eval(response)
    return {
        **state,
        "intent": output.get("intencao"),
        "orientation": output.get("orientacao")
    }

def generate_payload(state: AgentState) -> AgentState:
    prompt = load_prompt("generate_payload")
    filled = prompt.format(
        input_do_usuario=state["question"],
        catalogo_de_dados_injetado_pelo_rag=state["catalog"]
    )
    response = llms.get_response(filled)
    return {**state, "payload": eval(response)}

def validate_payload(state: AgentState) -> AgentState:
    prompt = load_prompt("validate_payload")
    filled = prompt.format(
        payload_gerado=state["payload"],
        catalogo_de_dados_injetado_pelo_rag=state["catalog"]
    )
    response = llms.get_response(filled)
    payload_validado = eval(response)
    status = "valid" if payload_validado else "invalid"
    return {**state, "payload": payload_validado, "validation_status": status}

def run_sql(state: AgentState) -> AgentState:
    result = run_query(state["payload"])
    return {**state, "query_result": result}

def rewrite_response(state: AgentState) -> AgentState:
    prompt = load_prompt("rewrite_response")
    filled = prompt.format(
        input_do_usuario=state["question"],
        resultado_sql=state["query_result"]
    )
    response = llms.get_response(filled)
    return {**state, "final_answer": response}

# -----------------------------
# Construção do grafo
# -----------------------------
graph = StateGraph(AgentState)

# Nós
graph.add_node("analyze_intent", analyze_intent)
graph.add_node("generate_payload", generate_payload)
graph.add_node("validate_payload", validate_payload)
graph.add_node("run_query", run_sql)
graph.add_node("rewrite_response", rewrite_response)

# Ciclos e fluxo

graph.set_entry_point("analyze_intent")
graph.add_edge("analyze_intent", "generate_payload")
graph.add_edge("generate_payload", "validate_payload")

graph.add_conditional_edges(
    "validate_payload",
    condition=lambda state: "valid" if state["validation_status"] == "valid" else "invalid",
    edges={
        "valid": "run_query",
        "invalid": "analyze_intent"
    }
)

graph.add_edge("run_query", "rewrite_response")
graph.add_edge("rewrite_response", END)

# Executor
graph_executor = graph.compile()
