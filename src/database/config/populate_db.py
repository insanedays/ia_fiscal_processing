import pandas as pd
from sqlalchemy.orm import DeclarativeMeta

def insert_parquet_to_table(parquet_path: str, model_class: DeclarativeMeta, db):
    """
    Lê um arquivo .parquet e insere os dados na tabela correspondente ao modelo SQLAlchemy informado,
    apenas se a tabela estiver vazia.

    Parâmetros:
    - parquet_path: caminho para o arquivo .parquet
    - model_class: classe do modelo SQLAlchemy (ex: NFItens)
    - db: sessão ativa do SQLAlchemy
    """
    try:
        has_data = db.query(model_class).first() is not None
        if has_data:
            print(f"[INFO] Tabela {model_class.__tablename__} já possui dados. Insert ignorado.")
            return

        df = pd.read_parquet(parquet_path)

        expected_columns = {col.name for col in model_class.__table__.columns}
        df_filtered = df[[col for col in df.columns if col in expected_columns]]

        records = [model_class(**row.to_dict()) for _, row in df_filtered.iterrows()]

        db.add_all(records)
        print(f"[INFO] Inseridos {len(records)} registros em {model_class.__tablename__}")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Erro ao inserir em {model_class.__tablename__}: {e}")
        raise

