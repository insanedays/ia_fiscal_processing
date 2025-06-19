from pathlib import Path
import sys

# ===  Adds the project ROOT to sys.path to allow absolute imports ===
CURRENT_FILE = Path(__file__).resolve()
ROOT = CURRENT_FILE.parents[3] 
sys.path.insert(0, str(ROOT))

from src.database.config.session_db import get_db  
from src.database.config.models_db import *
from src.database.config.populate_db import insert_parquet_to_table
from src.database.config.models_db import NFItens, NFHeader

# Database initialization
with get_db() as db:
    Base.metadata.create_all(db.bind)

    insert_parquet_to_table("data/silver/nf_itens.parquet", NFItens, db)
    insert_parquet_to_table("data/silver/nf_header.parquet", NFHeader, db) 

    db.commit()
    print( "[INFO] Banco de dados inicializado e populado com sucesso.")
