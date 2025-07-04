import os
from dotenv import load_dotenv

load_dotenv()

modo = os.getenv("INTERFACE_MODE")
print(f"Modo de execução: {modo}")

if not modo:
    raise ValueError("A variável de ambiente INTERFACE_MODE não foi definida.")

elif modo == "streamlit":
    from src.interface.streamlit_app import run
    run()

elif modo == "fastapi_app":
    from src.interface.fastapi_app import run
    run()

# elif modo == "init":
#     from src.database.config.init_db import init_db
#     print(init_db())

else:
    raise ValueError(f"Modo de execução desconhecido: {modo}")
