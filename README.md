# Projeto: Chatbot Fiscal Inteligente com LLM + LangGraph

Este projeto implementa um agente conversacional capaz de realizar consultas de notas fiscais em um banco de dadados, ele interpretar perguntas em linguagem natural e realiza consultas no banco, retornando o resultado. A arquitetura combina:

- Modelos de linguagem (LLMs) para interpretação e geração de instruções SQL
- Orquestração modular com LangGraph, permitindo controle explícito do fluxo de raciocínio
- Execução dinâmica de queries SQL em banco PostgreSQL
- Validação semântica de payloads JSON baseados em um catálogo YAML
- Interface adaptável via Streamlit ou FastAPI, com integração planejada para WhatsApp via WAHA
- Modularização completa e reaproveitável para outros domínios além do fiscal
- Compatibilidade com múltiplos provedores de LLMs, via abstração por client único
- Flexibilidade de execução via interface gráfica (Streamlit) ou API REST (FastAPI)

## Objetivo
Permitir que qualquer usuário, mesmo sem conhecimento técnico, consulte informações fiscais complexas utilizando linguagem natural. O sistema identifica a intenção da pergunta, gera e valida um payload estruturado com base em um catálogo de dados, executa a consulta SQL correspondente e reescreve a resposta em linguagem acessível. Também permite retorno ao início do raciocínio em caso de erro, garantindo robustez e confiança no fluxo.

---

## Tecnologias Utilizadas

| Tecnologia            | Função no Sistema                            | Justificativa                                |
| --------------------- | -------------------------------------------- | -------------------------------------------- |
| Python 3.10+          | Linguagem principal                          | Amplo suporte para IA, SQL, APIs             |
| Groq API              | LLM (ex: Mixtral, LLaMA 3)                   | Alta velocidade e custo reduzido             |
| LangChain + LangGraph | Orquestração dos agentes e controle de fluxo | Controle condicional, ciclos, escalabilidade |
| PostgreSQL + AWS RDS           | Banco de dados fiscal em nuvem                       | Robusto, compatível com SQL dinâmico         |
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

- **`analyze_intent`**: Classifica a intenção da pergunta e determina se é processável
- **`generate_payload`**: Gera um JSON com filtros e campos conforme o catálogo
- **`validate_payload`**: Verifica se o payload é consistente com o catálogo e opcionalmente o corrige
- **`rewrite_response`**: Formata a resposta do banco em linguagem amigável

### Catálogo de Dados

O sistema usa um catálogo YAML com todas as tabelas e campos disponíveis para consulta. Esse catálogo é injetado nos prompts para orientar a geração e validação dos payloads. A leitura do catálogo é feita dinamicamente por meio do utilitário `utils.load_db_catalog` 

### LangGraph com Ciclos

A orquestração do fluxo de agentes é feita com `StateGraph` e `TypedState`. O fluxo permite retornar ao `analyze_intent` se o payload for inválido, evitando respostas incorretas e aumentando a confiabilidade.

---

## Estrutura de pastas

```plaintext
├── .env
├── .gitignore
├── README.md
├── data
│   ├── raw
│   └── silver
├── docs
├── env_example
├── main.py
├── notebook
├── repo.py
├── requirements.txt
├── src
│   ├── agents
│   ├── database
│   │   ├── catalog.yaml
│   │   ├── config
│   │   ├── crud
│   │   └── queries
│   ├── interface
│   └── utilis
```

---

## Interfaces

- **Streamlit (`streamlit_app.py`)**: Interface local para testes com campo de entrada e resposta direta.
- **FastAPI (`fastapi_app.py`)**: API REST para produção, com rota `/ask` recebendo pergunta e retornando resposta. Integrável com WhatsApp via WAHA ou Twilio.
- **start.py**: Roteador principal controlado via `INTERFACE_MODE` no `.env`

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
Streamlit run start.py

# API REST com FastAPI
INTERFACE_MODE=api python start.py
```

Inicialização do banco:

```bash
# Criação das tabelas e popolação dos dados
python main.py

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
* [ ] Fallback com SQLDatabaseToolkit para perguntas fora do catálogo

---

## Licença

Este projeto foi desenvolvido com fins educacionais e de pesquisa. O código é de uso pessoal e está **proibida sua utilização comercial ou revenda sem autorização explícita da autora**.

**Se você utilizar este projeto como base ou inspiração, por favor inclua um link para este repositório.**

---

## Dados de exemplo

Os arquivos em `data/raw/` são dados sintéticos para testes e demonstrações:

- `202401_NFs_Cabecalho.csv`
- `202401_NFs_Itens.csv`.

