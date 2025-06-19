from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from src.agents.run_graph import run_graph
from src.utilis.load_db_catalog import load_catalog

load_dotenv()

app = FastAPI(title="Chatbot Fiscal API")

catalog_content = load_catalog()

class PerguntaInput(BaseModel):
    pergunta: str

@app.post("/ask")
def consultar_dado_fiscal(body: PerguntaInput):
    if not body.pergunta.strip():
        raise HTTPException(status_code=400, detail="Pergunta vazia.")

    resposta = run_graph(question=body.pergunta, catalog=catalog_content)
    return {"resposta": resposta}
