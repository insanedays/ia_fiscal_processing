import os

def load_catalog() -> str:
    catalog_path = os.getenv("CATALOG_PATH")
    if not catalog_path:
        raise ValueError("A variável de ambiente CATALOG_PATH não foi definida.")
    with open(catalog_path, "r", encoding="utf-8") as f:
        return f.read()
