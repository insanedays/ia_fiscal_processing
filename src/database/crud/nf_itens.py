from typing import Optional, List, Mapping, Any
from sqlalchemy.exc import SQLAlchemyError
from src.database.config.session_db import get_db
from src.database.config.models_db import  NFItens
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
import datetime

# Automatically generated class based on the ORM model on models_db
class NFItemSchema(sqlalchemy_to_pydantic(NFItens)):
    """
    Schema derivado automaticamente da tabela NFItens em models_db.

    Campos esperados:
    - chave_de_acesso: str
    - descricao: str
    - codigo_ncm_sh: str
    - tipo_produto: str
    - cfop: str
    - quantidade: float
    - unidade: str
    - valor_unitario: float
    - valor_total: float
    """
    pass

# CREATE NFItens

def create_nf_item(data: NFItemSchema) -> NFItens:
    """
    Insere um novo registro NFItens no banco de dados.

    Requer os seguintes campos:
    - chave_de_acesso: str
    - descricao: str
    - codigo_ncm_sh: str
    - tipo_produto: str
    - cfop: str
    - quantidade: float
    - unidade: str
    - valor_unitario: float
    - valor_total: float
    """
    with get_db() as db:
        try:
            new_item = NFItens(**data.dict())
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
            return new_item
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error creating NFItens: {e}")

# READ NFItens (por ID)
def get_nf_item(id_: int) -> Optional[NFItens]:
    """
    Retorna um item específico da NF pelo id do item (PK).
    """
    with get_db() as db:
        return db.query(NFItens).get(id_)

# READ ALL NFItens
def get_all_nf_items() -> List[NFItens]:
    """
    Retorna todos os registros de NFItens presentes no banco.
    """
    with get_db() as db:
        return db.query(NFItens).all()

# DELETE NFItens
def delete_nf_item(id_: int) -> bool:
    """
    Remove um item da nota fiscal pelo ID.
    Retorna True se removido com sucesso, False se não encontrado.
    """
    with get_db() as db:
        try:
            instance = db.query(NFItens).get(id_)
            if instance:
                db.delete(instance)
                db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error deleting NFItens: {e}")

# FILTRO DINÂMICO NFItens
def filter_nf_items(filters: Mapping[str, Any]) -> List[NFItens]:
    """
    Permite buscar registros NFItens com múltiplos filtros dinâmicos.

    Exemplo:
    '''
    filter_nf_items({
        "chave_de_acesso": "123456789012345678901234567890",
        "tipo_produto": "Mercadoria",
        "valor_total": 1500.50
    })
    '''
    """
    with get_db() as db:
        query = db.query(NFItens)
        for attr, value in filters.items():
            if hasattr(NFItens, attr):
                query = query.filter(getattr(NFItens, attr) == value)
        return query.all()

