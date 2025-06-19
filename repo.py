import os

IGNORAR = {
    "__pycache__",
    ".venv",
    "venv",
    ".git",
    ".mypy_cache",
    ".idea",
    ".pytest_cache",
    ".vscode",
    "dist",
    "build",
    "*.egg-info",
}

def ignorar(nome):
    for padrão in IGNORAR:
        if "*" in padrão:
            if nome.endswith(padrão.replace("*", "")):
                return True
        elif nome == padrão:
            return True
    return False

def print_tree(caminho='.', prefixo=''):
    itens = sorted(os.listdir(caminho))
    for i, nome in enumerate(itens):
        if ignorar(nome):
            continue
        caminho_completo = os.path.join(caminho, nome)
        é_ultimo = i == len(itens) - 1
        conector = "└── " if é_ultimo else "├── "
        print(prefixo + conector + nome)
        if os.path.isdir(caminho_completo):
            novo_prefixo = prefixo + ("    " if é_ultimo else "│   ")
            print_tree(caminho_completo, novo_prefixo)

print_tree()
