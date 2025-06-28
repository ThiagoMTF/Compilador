import csv

def carregar_tabelas_shift_reduce(caminho_csv):
    tabela_action = []
    tabela_goto = []

    with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
        leitor = csv.reader(csvfile, delimiter=';')

        for linha in leitor:
            sub_tabelaAction = linha[1:26]
            tabela_action.append(sub_tabelaAction)

            sub_tabelaGoto = linha[26:44]
            tabela_goto.append(sub_tabelaGoto)

    return tabela_action, tabela_goto
