import json
from decimal import Decimal
from datetime import datetime, date, time
from typing import Dict, Any
from src.database.queries.dinamic_query import advanced_query  # ajuste se necessário

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, (datetime, date, time)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

def run_query(payload: Dict) -> str:
    """
    Executa uma consulta dinâmica no banco a partir de um payload e retorna
    os resultados como JSON serializado.

    Se ocorrer erro durante a execução, retorna um JSON com a chave "error".

    Retorno:
        str: JSON com lista de dicionários representando os registros consultados
             ou JSON com {"error": "..."} em caso de falha.
    """
    try:
        result = advanced_query(payload)

        return json.dumps(result, ensure_ascii=False, cls=CustomJSONEncoder)

    except Exception as e:
        return json.dumps({"error": f"Erro ao executar a consulta: {str(e)}"})

