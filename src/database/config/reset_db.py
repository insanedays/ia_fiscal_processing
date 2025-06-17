import sys
from pathlib import Path

# ===  Adds the project ROOT to sys.path to allow absolute imports ===
CURRENT_FILE = Path(__file__).resolve()
ROOT = CURRENT_FILE.parents[3] 
sys.path.insert(0, str(ROOT))

from src.database.config.models_db import Base
from src.database.config.init_db import get_db

def reset_schemas():
    """
    Dropa todas as tabelas e recria a estrutura conforme os modelos atuais.
    CUIDADO: isso apaga todos os dados do banco.
    """
    with get_db() as db:
        bind = db.get_bind()
        print("[INFO] Dropando todas as tabelas...")
        Base.metadata.drop_all(bind=bind)

        print("[INFO] Recriando todas as tabelas com o schema atualizado...")
        Base.metadata.create_all(bind=bind)

        print("[INFO] Estrutura recriada com sucesso.")

if __name__ == "__main__":
    print(f"[INFO] Executando reset_schemas com ROOT: {ROOT}")
    reset_schemas()
