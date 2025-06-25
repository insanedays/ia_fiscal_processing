# from typing import Dict, List
# from src.database.config.session_db import get_db
# from src.database.config.models_db import NFHeader, NFItens

# def advanced_query(payload: Dict) -> List[Dict]:
#     """
#     Executa uma consulta dinâmica com JOIN entre NFHeader e NFItens,
#     aplicando filtros e projetando apenas os campos especificados.

#     Espera um payload com a seguinte estrutura:

#     payload = {
#         "filters": {
#             "NFHeader": {
#                 "uf_emitente": "SP"
#             },
#             "NFItens": {
#                 "quantidade": 10
#             }
#         },
#         "fields": [
#             "NFHeader.chave_de_acesso",
#             "NFHeader.serie",
#             "NFItens.descricao"
#         ]
#     }

#     Retorna:
#         Uma lista de dicionários, onde cada dicionário representa uma linha da consulta,
#         com os campos nomeados exatamente como especificado no campo "fields" do payload.

#     Exemplo de retorno:

#     [
#         {
#             "NFHeader.chave_de_acesso": "35240134028316923228550010003691801935917886",
#             "NFHeader.serie": 1,
#             "NFItens.descricao": "Produto XYZ"
#         },
#         ...
#     ]
#     """
#     with get_db() as db:
#         query = db.query(NFHeader).join(NFItens)

#         # Aplica filtros dinamicamente
#         for table_model, table_filters in payload.get("filters", {}).items():
#             model = {"NFHeader": NFHeader, "NFItens": NFItens}.get(table_model)
#             if not model:
#                 raise ValueError(f"Tabela inválida no filtro: {table_model}")
#             for attr, value in table_filters.items():
#                 if hasattr(model, attr):
#                     query = query.filter(getattr(model, attr) == value)
#                 else:
#                     raise ValueError(f"Campo inválido em {table_model}: {attr}")

#         # Projeta os campos solicitados
#         field_objs = []
#         col_names = []

#         for full_field in payload.get("fields", []):
#             table_name, column_name = full_field.split(".")
#             model = {"NFHeader": NFHeader, "NFItens": NFItens}.get(table_name)
#             if not model or not hasattr(model, column_name):
#                 raise ValueError(f"Campo inválido: {full_field}")
#             field_objs.append(getattr(model, column_name))
#             col_names.append(full_field)  # usa como chave no dict final

#         query = query.with_entities(*field_objs)
#         result = query.all()

#         # Constrói lista de dicionários (coluna: valor)
#         return [dict(zip(col_names, row)) for row in result]

from typing import Dict, List
from sqlalchemy import func
from src.database.config.session_db import get_db
from src.database.config.models_db import NFHeader, NFItens

def advanced_query(payload: Dict) -> List[Dict]:
    """
    Executa uma consulta dinâmica sobre as tabelas NFHeader e NFItens com suporte a filtros, seleção de campos
    e operações de agregação (como sum, avg, count, etc), com ou sem agrupamento.

    Espera um payload com a seguinte estrutura:

    {
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
            "NFItens.descricao"
        ],
        "aggregation": {
            "operation": "sum",                    # Opcional: "sum", "avg", "count", "min", "max"
            "target_field": "NFItens.valor_total", # Campo sobre o qual aplicar a operação
            "group_by": "NFHeader.cnpj_emitente"   # Opcional: campo para agrupar os resultados
        }
    }

    A seção "aggregation" é opcional. Se estiver presente, "fields" será ignorado.

    Returns:
        List[Dict]: Lista de registros da consulta, cada um como dicionário com os campos requisitados.

    Raises:
        ValueError: Se o payload contiver nomes de tabelas ou campos inválidos,
                    ou se a operação de agregação for desconhecida.
    """
    with get_db() as db:
        query = db.query(NFHeader).join(NFItens)

        models = {"NFHeader": NFHeader, "NFItens": NFItens}

        # Aplica filtros
        for table_model, table_filters in payload.get("filters", {}).items():
            model = models.get(table_model)
            if not model:
                raise ValueError(f"Tabela inválida no filtro: {table_model}")
            for attr, value in table_filters.items():
                if hasattr(model, attr):
                    query = query.filter(getattr(model, attr) == value)
                else:
                    raise ValueError(f"Campo inválido em {table_model}: {attr}")

        aggregation = payload.get("aggregation")
        field_objs = []
        col_names = []

        if aggregation:
            # Processa agregação
            op = aggregation.get("operation", "").lower()
            target_field = aggregation.get("target_field")
            group_by_field = aggregation.get("group_by")

            if not target_field:
                raise ValueError("Campo alvo da agregação ('target_field') ausente.")

            target_model_name, target_column = target_field.split(".")
            target_model = models.get(target_model_name)
            if not target_model or not hasattr(target_model, target_column):
                raise ValueError(f"Campo inválido para agregação: {target_field}")

            agg_func_map = {
                "sum": func.sum,
                "avg": func.avg,
                "count": func.count,
                "max": func.max,
                "min": func.min
            }

            if op not in agg_func_map:
                raise ValueError(f"Operação de agregação não suportada: {op}")

            agg_expr = agg_func_map[op](getattr(target_model, target_column)).label("resultado")
            field_objs.append(agg_expr)
            col_names.append("resultado")

            if group_by_field:
                group_model_name, group_column = group_by_field.split(".")
                group_model = models.get(group_model_name)
                if not group_model or not hasattr(group_model, group_column):
                    raise ValueError(f"Campo inválido para group_by: {group_by_field}")

                group_expr = getattr(group_model, group_column)
                field_objs.insert(0, group_expr)
                col_names.insert(0, group_by_field)
                query = query.group_by(group_expr)

        else:
            # Consulta padrão (sem agregação)
            for full_field in payload.get("fields", []):
                table_name, column_name = full_field.split(".")
                model = models.get(table_name)
                if not model or not hasattr(model, column_name):
                    raise ValueError(f"Campo inválido: {full_field}")
                field_objs.append(getattr(model, column_name))
                col_names.append(full_field)

        query = query.with_entities(*field_objs)
        result = query.all()

        return [dict(zip(col_names, row)) for row in result]
