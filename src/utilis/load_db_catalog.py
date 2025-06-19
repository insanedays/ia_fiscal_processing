import os

def load_catalog() -> str:
    catalog_path = 'src/database/catalog.yaml'
    with open(catalog_path, "r", encoding="utf-8") as f:
        return f.read()
    



