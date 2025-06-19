from database.queries.dinamic_query import advanced_query


def run_query(payload: dict) -> str:
    try:
        result = advanced_query(payload)
        if not result:
            return "Nenhum resultado encontrado."

        field_names = payload.get("fields", [])
        rows = [dict(zip(field_names, row)) for row in result]
        return str(rows)

    except Exception as e:
        return f"Erro ao executar a consulta: {str(e)}"
