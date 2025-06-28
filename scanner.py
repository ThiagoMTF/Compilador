from sources.tabela_simbolos import consultar_inserir_identificador
from sources.afd import alfabeto, transicoes, final_states 

class AnalisadorLexico:
    def __init__(self, arquivo):
        self.arquivo = open(arquivo, "r")
        self.linha = 1
        self.coluna = 1
        self.posicao = 0
        self.linha_somada = False

    def categoria(self, c, est):
        if est == "Q9":
            if c == "\"":
                return c
            elif c in alfabeto or c == " " or c == "\t":
                return "QQC"
            elif c in ("\n", ""):
                return -9
            else:
                return -1
        elif est == "Q12":
            if c == "}":
                return c
            elif c in alfabeto or c == " " or c == "\t":
                return "QQC"
            elif c in ("\n", ""):
                return -12
            else:
                return -1
        else:
            if c.isalpha():
                if est == "Q4" and c in ("E", "e"):
                    return c
                else:
                    return "L"
            elif c.isdigit():
                return "D"
            elif c == "\n":
                return "SDL"
            elif c == "\t":
                return "TAB"  
            elif c == " ":
                return "ESP"      
            elif c == "":
                return "EOF"
            elif c in ("(", ")", ";", ",", "+", "-", "*", "/", "{", "}", ">", "<", "=", "E", "e", ".", "'", "\"", "_", "]", "[", "!", "?"):
                return c
            else:
                return -1
            
    @staticmethod
    def verifica_tabela_simbolos(classe, lexema, estado_atual):
        match classe:
            case "ID":
                return consultar_inserir_identificador(lexema)
            case "NUM":
                match estado_atual:
                    case "Q1" | "Q2":
                        return (classe, lexema, consultar_inserir_identificador("inteiro")[2])
                    case "Q4" | "Q8":
                        return (classe, lexema, consultar_inserir_identificador("real")[2])
            case "LIT":
                return (classe, lexema, consultar_inserir_identificador("literal")[2])
            case "EOF":
                return ("EOF", "EOF", "EOF")
            case _:
                return (classe, lexema, "NULL")
    
    @staticmethod
    def ERROR(estado, cod, linha, coluna): 
        msgError = '' 
        if estado in ("Q3", "Q5", "Q6", "Q7"):
            msgError = "Numero real incompleto"
        elif estado == "Q0":
            msgError = "Caractere inesperado"
        else:
            match cod:
                case -1:
                    msgError = "Caractere inválido na linguagem"
                case -12:
                    msgError = "Comentário não finalizado"
                case -9:
                    msgError = "Literal não finalizado;"
        return f"ERRO - {msgError} - Linha: {linha}, Coluna: {coluna}"

    def SCANNER(self):
        self.lexema = ''        
        self.estado_atual = "Q0"

        while True:
            pos_anterior = self.arquivo.tell()
            caractere = self.arquivo.read(1)
            pos_linha = self.linha
            pos_coluna = self.coluna

            simbolo = self.categoria(caractere, self.estado_atual)

            if self.estado_atual in transicoes and simbolo in transicoes[self.estado_atual]:
                proximo_estado = transicoes[self.estado_atual][simbolo]
                self.estado_atual = proximo_estado
                self.lexema += caractere

                if caractere == '\n':
                    self.coluna = 1
                    if self.linha_somada == False:
                        self.linha += 1
                        self.linha_somada = True
                else:
                    self.linha_somada = False
                    self.coluna += 1

            else:
                if caractere == '\n':                    
                    self.coluna = 1
                    if self.linha_somada == False:
                        self.linha += 1
                        self.linha_somada = True
                else:
                    self.linha_somada = False
                    self.coluna += 1

                if self.estado_atual in final_states:
                    self.arquivo.seek(pos_anterior)
                    if self.estado_atual in ('Q13', 'Q26'):
                        self.SCANNER()
                    else:
                        token = AnalisadorLexico.verifica_tabela_simbolos(final_states[self.estado_atual], self.lexema, self.estado_atual)
                        return (token, self.linha, self.coluna)
                   
                else:
                    print(AnalisadorLexico.ERROR(self.estado_atual, simbolo, pos_linha, pos_coluna))
                    self.SCANNER()
            
