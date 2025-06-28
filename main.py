from scanner import AnalisadorLexico
from sources.tabela_simbolos import imprimir_tabela_simbolos
from parser import AnalisadorSintatico
#from sources.importar_tabela_shift_reduce import carregar_tabelas_shift_reduce


parser = AnalisadorSintatico("sources/arquivo.txt")
parser.parser()
