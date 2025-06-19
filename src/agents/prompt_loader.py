import yaml
import os

PROMPT_PATH = os.path.join("src", "agents", "payload.yaml")

def load_prompt(agent_name: str, path: dict = PROMPT_PATH) -> dict:
    """Carrega o prompt do agente a partir do YAML"""
    with open(path, "r", encoding="utf-8") as f:
        content = yaml.safe_load(f)
        print(f"Carregando prompt para o agente: {agent_name}")
    return content[agent_name]