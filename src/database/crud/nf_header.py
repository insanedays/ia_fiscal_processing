from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from typing import Optional, List, Mapping, Any
from sqlalchemy.exc import SQLAlchemyError
from src.database.config.session_db import get_db
from src.database.config.models_db import NFHeader
#import datetime

# Classe gerada automaticamente com base no modelo ORM
class NFHeaderSchema(sqlalchemy_to_pydantic(NFHeader, exclude=["itens"])):
    pass

# CREATE
def create_nf_header(data: NFHeaderSchema) -> NFHeader:
    """
    Insere um novo registro NFHeader no banco de dados.
    
    Requer 21 campos obrigatórios:
    - chave_de_acesso: str (máx. 60)
    - modelo: str (máx. 5)
    - serie: int (BigInteger)
    - numero: int (BigInteger)
    - natureza_da_operacao: str (máx. 255)
    - data_emissao: datetime
    - evento_mais_recente: str (máx. 255)
    - data_hora_evento_mais_recente: datetime
    - cpf_cnpj_emitente: str (14 dígitos)
    - razao_social_emitente: str (máx. 255)
    - inscricao_estadual_emitente: str (máx. 20)
    - uf_emitente: str (2 letras)
    - municipio_emitente: str (máx. 100)
    - cnpj_destinatario: str (14 dígitos)
    - nome_destinatario: str (máx. 255)
    - uf_destinatario: str (2 letras)
    - indicador_ie_destinatario: str (máx. 5)
    - destino_da_operacao: str (máx. 5)
    - consumidor_final: str (máx. 5)
    - presenca_do_comprador: str (máx. 5)
    - valor_nota_fiscal: float (até 15 dígitos, 2 decimais)
    """
    with get_db() as db:
        try:
            new_item = NFHeader(**data.dict())
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
            return new_item
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error creating NFHeader: {e}")

# READ (chave_de_acesso)
def get_nf_header(chave_de_acesso: str) -> Optional[NFHeader]:
    """
    Retorna uma nota fiscal específica a partir da chave_de_acesso infomada (PK).
    """
    with get_db() as db:
        return db.query(NFHeader).get(chave_de_acesso)

# READ ALL
def get_all_nf_headers() -> List[NFHeader]:
    """
    Retorna todos os dados da NFHeader existentes no banco.
    """
    with get_db() as db:
        return db.query(NFHeader).all()

# DELETE
def delete_nf_header(chave_de_acesso: str) -> bool:
    """
    Remove uma nota fiscal com a chave_de_acesso fornecida.
    Retorna True se removido com sucesso, False se não encontrado.
    """
    with get_db() as db:
        try:
            instance = db.query(NFHeader).get(chave_de_acesso)
            if instance:
                db.delete(instance)
                db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error deleting NFHeader: {e}")

# FILTRO DINÂMICO
def filter_nf_header(filters: Mapping[str, Any]) -> List[NFHeader]:
    """
    Permite buscar registros NFHeader com múltiplos filtros dinâmicos.

    Exemplo:
    '''
    filter_nf_header({
        "modelo": "55",
        "uf_emitente": "SP",
        "cnpj_destinatario": "43210987654321",
        "data_emissao": datetime.datetime(2024, 6, 7, 10, 0),
        "numero": 12345
    })
    '''
    """
    with get_db() as db:
        query = db.query(NFHeader)
        for attr, value in filters.items():
            if hasattr(NFHeader, attr):
                query = query.filter(getattr(NFHeader, attr) == value)
        return query.all()
