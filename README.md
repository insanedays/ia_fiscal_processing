# Projeto: Chatbot Fiscal Inteligente com LLM + LangGraph

Este projeto implementa um sistema de atendimento automatizado que responde a perguntas em linguagem natural sobre dados fiscais (ex: notas fiscais eletrônicas), utilizando modelos de linguagem (LLMs), orquestração via LangGraph, execução de queries SQL dinâmicas em PostgreSQL e interface via Streamlit ou FastAPI (para WhatsApp).

---

## Objetivo

Permitir que usuários consultem uma base de dados fiscal usando linguagem natural, sem conhecer SQL ou estrutura da base. O sistema interpreta a pergunta, gera uma consulta estruturada, executa no banco e retorna a resposta formatada.

---

## Tecnologias Utilizadas

| Tecnologia            | Função no Sistema                            | Justificativa                                |
| --------------------- | -------------------------------------------- | -------------------------------------------- |
| Python 3.10+          | Linguagem principal                          | Amplo suporte para IA, SQL, APIs             |
| Groq API              | LLM (ex: Mixtral, LLaMA 3)                   | Alta velocidade e custo reduzido             |
| LangChain + LangGraph | Orquestração dos agentes e controle de fluxo | Controle condicional, ciclos, escalabilidade |
| PostgreSQL            | Banco de dados fiscal                        | Robusto, compatível com SQL dinâmico         |
| Streamlit             | Interface local para testes                  | Rápido, simples, sem backend                 |
| FastAPI               | Backend REST para integração com WhatsApp    | Desempenho, suporte a webhooks               |
| YAML                  | Armazenamento dos prompts e catálogo         | Leitura humana, fácil edição                 |

---

## Arquitetura Geral

```plaintext
Usuário pergunta
↓
[Agente 1: analyze_intent]
↓
[Agente 2: generate_payload]
↓
[Agente 3: validate_payload]
   ↓
   ❌ Se inválido: retorna para analyze_intent
   ✔ Se válido:
     ↓
[Executa SQL via query_runner.py]
↓
[Agente 4: rewrite_response]
↓
Resposta final para o usuário
```

### Agentes LLM

* **`analyze_intent`**: Classifica a intenção da pergunta e determina se é processável
* **`generate_payload`**: Gera um JSON com filtros e campos conforme o catálogo
* **`validate_payload`**: Verifica se o payload é consistente com o catálogo
* **`rewrite_response`**: Formata a resposta do banco em linguagem amigável

### Catálogo de Dados

O sistema usa um catálogo YAML com todas as tabelas e campos disponíveis para consulta. Esse catálogo é injetado nos prompts para orientar a geração e validação dos payloads. A leitura do catálogo é feita dinamicamente por meio do utilitário `utils.load_db_catalog` que busca o caminho via variável de ambiente `CATALOG_PATH`.

### LangGraph com Ciclos

A orquestração do fluxo de agentes é feita com `StateGraph` e `TypedState`. O fluxo permite retornar ao `analyze_intent` se o payload for inválido, evitando respostas incorretas e aumentando a confiabilidade.

---

## Estrutura de Diretórios

```plaintext
├── .env
├── .gitignore
├── README.md
├── data
│   ├── raw
│   │   ├── 202401_NFs_Cabecalho.csv
│   │   └── 202401_NFs_Itens.csv
│   └── silver
│       ├── nf_header.parquet
│       └── nf_itens.parquet
├── docs
│   └── melhorias_database.md
├── env_example
├── main.py
├── notebook
│   └── normalize.ipynb
├── repo.py
├── requirements.txt
├── src
│   ├── agents
│   │   ├── graph.py
│   │   ├── llm_clients.py
│   │   ├── payload.yaml
│   │   ├── prompt_loader.py
│   │   ├── query_runner.py
│   │   └── run_graph.py
│   ├── database
│   │   ├── catalog.yaml
│   │   ├── config
│   │   │   ├── create_tables.yaml
│   │   │   ├── init_db.py
│   │   │   ├── models_db.py
│   │   │   ├── populate_db.py
│   │   │   ├── reset_db.py
│   │   │   └── session_db.py
│   │   ├── crud
│   │   │   ├── nf_header.py
│   │   │   └── nf_itens.py
│   │   └── queries
│   │       └── dinamic_query.py
│   ├── interface
│   │   ├── fastapi_app.py
│   │   └── streamlit_app.py
│   └── utilis
│       ├── load_db_catalog.py
│       └── normalize_db.py
```

---

## Interfaces

* **Streamlit (`streamlit_app.py`)**: Interface local para testes com campo de entrada e resposta direta.
* **FastAPI (`fastapi_app.py`)**: API REST para produção, com rota `/ask` recebendo pergunta e retornando resposta. Integrável com WhatsApp via WAHA ou Twilio.
* **start.py**: Roteador principal controlado via `INTERFACE_MODE` no `.env`

---

## Requisitos de Execução

* Python >= 3.10
* Variáveis de ambiente no arquivo `.env`:

```dotenv
# PostgreSQL
HOST=
DATABASE=
USER=
PASSWORD=
PORT=5432

# APIs
GROQ_API_KEY=your-groq-key
OPENAI_API_KEY=your-openai-key
COHERE_API_KEY=your-cohere-key
ANTHROPIC_API_KEY=your-anthropic-key

# Execução
INTERFACE_MODE=streamlit  # ou 'api'
CATALOG_PATH=src/database/catalog.yaml
```

Instalação:

```bash
# Crie ambiente virtual (opcional, mas recomendado)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate    # Windows

# Instale as dependências
pip install -r requirements.txt
```

Execução:

```bash
# Interface local com Streamlit
python src/start.py

# API REST com FastAPI
INTERFACE_MODE=api python src/start.py
```

Inicialização do banco:

```bash
# Criação das tabelas
python src/database/config/init_db.py

# População com dados de exemplo
python src/database/config/populate_db.py
```

---

## Testes da API REST

Endpoint: `POST /ask`

```bash
curl -X POST http://localhost:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"pergunta": "Quais notas fiscais foram emitidas em janeiro de 2023?"}'
```

Resposta esperada:
```json
{
  "resposta": "Foram encontradas X notas fiscais emitidas em janeiro de 2023."
}
```

---

## Roadmap

* [x] CRUD e base de dados prontos
* [x] Prompts YAML definidos por agente
* [x] Modularização dos agentes com client Groq
* [x] Implementação do `graph.py` com ciclo entre `validate` e `intent`
* [x] Função `run_graph()` unificada
* [x] Integração com query dinâmica via ORM (advanced_query)
* [x] Interface Streamlit funcional
* [x] FastAPI com webhook funcional
* [ ] Integração com WhatsApp (WAHA)
* [ ] Testes unitários e de fluxo

---

## Licença

Este projeto é de uso privado enquanto estiver em fase de desenvolvimento.

---

## Dados de exemplo

Os arquivos em `data/raw/` são dados sintéticos para testes e demonstrações:

- `202401_NFs_Cabecalho.csv`
- `202401_NFs_Itens.csv`

Esses dados não contêm informações reais ou sensíveis.

---

## Dados JSON

Os arquivos `.json` não são versionados porque são gerados automaticamente a partir dos arquivos `.yaml`. O repositório considera os `.yaml` como fonte de verdade.
