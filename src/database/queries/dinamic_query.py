from typing import Dict, List
from src.database.config.session_db import get_db
from src.database.config.models_db import NFHeader, NFItens

def advanced_query(payload: Dict) -> List[Dict]:
    """
    Executa uma consulta dinâmica com JOIN entre NFHeader e NFItens,
    aplicando filtros e projetando apenas os campos especificados.

    Espera um payload com a seguinte estrutura:

    payload = {
        "filters": {
            "NFHeader": {
                "uf_emitente": "SP"
            },
            "NFItens": {
                "quantidade": 10
            }
        },
        "fields": [
            "NFHeader.chave_de_acesso",
            "NFHeader.serie",
            "NFItens.descricao"
        ]
    }

    Retorna:
        Uma lista de dicionários, onde cada dicionário representa uma linha da consulta,
        com os campos nomeados exatamente como especificado no campo "fields" do payload.

    Exemplo de retorno:

    [
        {
            "NFHeader.chave_de_acesso": "35240134028316923228550010003691801935917886",
            "NFHeader.serie": 1,
            "NFItens.descricao": "Produto XYZ"
        },
        ...
    ]
    """
    with get_db() as db:
        query = db.query(NFHeader).join(NFItens)

        # Aplica filtros dinamicamente
        for table_model, table_filters in payload.get("filters", {}).items():
            model = {"NFHeader": NFHeader, "NFItens": NFItens}.get(table_model)
            if not model:
                raise ValueError(f"Tabela inválida no filtro: {table_model}")
            for attr, value in table_filters.items():
                if hasattr(model, attr):
                    query = query.filter(getattr(model, attr) == value)
                else:
                    raise ValueError(f"Campo inválido em {table_model}: {attr}")

        # Projeta os campos solicitados
        field_objs = []
        col_names = []

        for full_field in payload.get("fields", []):
            table_name, column_name = full_field.split(".")
            model = {"NFHeader": NFHeader, "NFItens": NFItens}.get(table_name)
            if not model or not hasattr(model, column_name):
                raise ValueError(f"Campo inválido: {full_field}")
            field_objs.append(getattr(model, column_name))
            col_names.append(full_field)  # usa como chave no dict final

        query = query.with_entities(*field_objs)
        result = query.all()

        # Constrói lista de dicionários (coluna: valor)
        return [dict(zip(col_names, row)) for row in result]

