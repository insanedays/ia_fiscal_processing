from typing import Dict, List
from src.database.config.session_db import get_db
from src.database.config.models_db import NFHeader, NFItens

def advanced_query(payload: Dict) -> List:
    """
    Realiza uma consulta dinâmica multi-tabela com filtros e projeção de campos.
    
    Espera receber no payload:
    - filters: dicionário com filtros separados por tabela.
    - fields: lista de campos (tabela.campo) a serem retornados.

    Exemplo de payload:
    payload = {
        "filters": {
            "NFHeader": {
                "cnpj_destinatario": "12345678901234",
                "uf_emitente": "SP"
            },
            "NFItens": {
                "tipo_produto": "Mercadoria",
                "quantidade": 10
            }
        },
        "fields": [
            "NFHeader.chave_de_acesso",
            "NFHeader.razao_social_emitente",
            "NFItens.descricao",
            "NFItens.valor_unitario",
            "NFItens.valor_total"
        ]
    }
    """

    with get_db() as db:
        # Começa o query fazendo o JOIN entre as tabelas
        query = db.query(NFHeader).join(NFItens)

        # Aplica filtros na tabela NFHeader
        for attr, value in payload.get("filters", {}).get("NFHeader", {}).items():
            if hasattr(NFHeader, attr):
                query = query.filter(getattr(NFHeader, attr) == value)
            else:
                raise ValueError(f"Campo inválido em NFHeader: {attr}")

        # Aplica filtros na tabela NFItens
        for attr, value in payload.get("filters", {}).get("NFItens", {}).items():
            if hasattr(NFItens, attr):
                query = query.filter(getattr(NFItens, attr) == value)
            else:
                raise ValueError(f"Campo inválido em NFItens: {attr}")

        # Define a projeção (campos a serem retornados)
        fields = []
        for field in payload.get("fields", []):
            # Divide o campo no formato Tabela.Campo
            table_name, column_name = field.split(".")
            # Mapeia o nome da tabela para o Model ORM correto
            table = {
                "NFHeader": NFHeader,
                "NFItens": NFItens
            }.get(table_name)

            if not table:
                raise ValueError(f"Tabela inválida: {table_name}")

            # Adiciona o campo correspondente ao query
            if hasattr(table, column_name):
                fields.append(getattr(table, column_name))
            else:
                raise ValueError(f"Campo inválido em {table_name}: {column_name}")

        # Substitui a query pela projeção dos campos solicitados
        query = db.query(*fields)

        # Executa e retorna o resultado (lista de tuplas)
        result = query.all()
        return result
