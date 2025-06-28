tabela_simbolos = {
    #chave: (Classe, Lexema, Tipo)
    "inicio": ("inicio", "inicio", "inicio"),
    "varinicio": ("varinicio", "varinicio", "varinicio"),
    "varfim": ("varfim", "varfim", "varfim"),
    "escreva": ("escreva", "escreva", "escreva"),
    "leia": ("leia", "leia", "leia"),
    "se": ("se", "se", "se"),
    "entao": ("entao", "entao", "entao"),
    "fimse": ("fimse", "fimse", "fimse"),
    "faca_ate": ("faca_ate", "faca_ate", "faca_ate"),
    "fimfaca": ("fimfaca", "fimfaca", "fimfaca"),
    "fim": ("fim", "fim", "fim"),
    "inteiro": ("inteiro", "inteiro", "inteiro"),
    "literal": ("literal", "literal", "literal"),
    "real": ("real", "real", "real")
}

def consultar_inserir_identificador(nome, linha=None, coluna=None):
    if nome not in tabela_simbolos:
        tabela_simbolos[nome] = ("ID", nome, "NULL")
    return tabela_simbolos[nome]

def imprimir_tabela_simbolos():
    print("\nTabela de Símbolos:")
    print(f"{'Lexema':<20} {'Classe':<15} {'Tipo':<10}")
    print("-" * 45)
    for lexema, (classe, _, tipo) in tabela_simbolos.items():
        print(f"{lexema:<20} {classe:<15} {tipo:<10}")
