from scanner import AnalisadorLexico
from sources.tabela_simbolos import imprimir_tabela_simbolos
from sources.regras_gramatica import tabela_regras_gramatica, converte_token
from sources.tabela_sintatica import tabela_action, tabela_goTo

class AnalisadorSintatico:
    def __init__(self, arquivo):
        self.scanner = AnalisadorLexico(arquivo)
        self.pilha = [0]
        self.topPilha = 0
        self.token = ''
        self.lastToken = ''
        self.ocorreuErro = False

    @staticmethod
    def indiceItem(lista, item):
        try:
            cabecalho = lista[-1]
            return cabecalho.index(item)
        except ValueError:
            return -1
        
    @staticmethod
    def separaAcao(cell: str):
        if not cell:
            return None, None
        return cell[0], cell[1:]
    
    @staticmethod
    def error_panic(self, valores):
        self.token = valores[0]

    @staticmethod
    def operacaoVazia():
        return ''

    def parser(self):
        try:
            self.token = self.scanner.SCANNER()
            while True:
                if self.ocorreuErro == True:
                    token_normalizado = self.token
                elif self.ocorreuErro == False:
                    token_normalizado = converte_token[self.token[0][0]]

                self.topPilha = self.pilha[-1]
                coluna = self.indiceItem(tabela_action, token_normalizado)
                op = tabela_action[self.topPilha][coluna]

                if op == '':
                        if token_normalizado[0][0] in ('$', 'EOF'):
                            break
                        elif not token_normalizado[0][0] in ('$', 'EOF'):
                            linhaEsperada = tabela_action[self.topPilha]
                            valoresEsperadosIndex = []
                            valoresEsperados = []
                            for valor in linhaEsperada:
                                if valor != '':
                                    valoresEsperadosIndex.append(linhaEsperada.index(valor))
                            for valor in valoresEsperadosIndex:
                                valoresEsperados.append(tabela_action[-1][valor])
                            print(f'Erro Sintático em - Linha: {self.token[1]}, Coluna: {self.token[2]}! Aguardando ler {valoresEsperados} mas foi lido {token_normalizado[0]}')
                            self.error_panic(self, valoresEsperados)
                            self.ocorreuErro = True
                        
                acao, estado = self.separaAcao(op)
                if acao == 'S':
                    self.pilha.append(int(estado))
                    self.token = self.scanner.SCANNER()

                elif acao == 'R':
                    regra_da_gramatica = tabela_regras_gramatica[int(estado)]
                    beta = regra_da_gramatica[2]
                    producao = regra_da_gramatica[1]
                    alpha = regra_da_gramatica[0]
                    for _ in range(beta):
                        self.pilha.pop()
                    t = self.pilha[-1]
                    coluna = self.indiceItem(tabela_goTo, alpha)
                    goTo = tabela_goTo[t][coluna]
                    self.pilha.append(int(goTo))
                    print(f"{alpha} -> {producao}")

                elif acao == 'A':
                    print("Aceito!")
                    break
                self.lastToken = self.token
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            print(self.token)
            print(self.pilha)
            print(self.topPilha)
