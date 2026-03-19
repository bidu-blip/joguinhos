"""
O jogo consiste numa string, e a pessoa tem que escrever todas as combinações dela com seus caractéres alternados em minúsculas e maiúsculas.
"""

from dataclasses import dataclass
from time import (time)
from sys import (argv  as Argumentos)
from random import (choice)

# Todas as regras de desclassificação da Partida.

class RegraDePerdaDos50PorcentosDoTotal:
    """
    A regra consiste em que, baseado na quantidade de jogadas -- isso se já tiver pelo menos
    passado mais de LIMITE, já que a teoria dos pequenos números(volatilidade), faria tal 
    regra extremamente restrita -- se, seus erros, passarem tal, você perde.
    """
    def perdeu(self) -> bool:
        TOTALIDADE = (self.acertos + self.erros)
        LIMITE = 8

        if TOTALIDADE >= LIMITE:
            return self.erros > (0.50 * TOTALIDADE)
        else:
            return False

class RegraDePerdaExarcebaTodasCombinacoes:
    """
    Regra mais flexível. Há uma quantia total de combinações que o jogador deve acertar para
    vencer o jogo. Se os erros passarem este limite, então ele também perde o jogo.
    """
    def perdeu(self) -> bool:
        return self.erros > 2 ** len(self.texto)
    

class Tabuleiro(RegraDePerdaExarcebaTodasCombinacoes):
    def __init__(self, texto: str) -> None:
        assert(2 <= len(texto) <= 4)

        self.texto = texto.lower()
        self.combinacoes = [self.texto]
        self.acertos = 0
        self.erros = 0

        self.relogio = time()

    def listagem_dos_acertos(self):
        COLUNAS = 3
        if self.combinacoes == []:
            print("Você ainda não acertou nenhuma!")
            return None
        
        for (p, item) in enumerate(self.combinacoes):
            print("\t\u00b7 {}".format(item), end='')
            if (p + 1) % COLUNAS == 0:
                print("")
            
        print("")
    
    def realiza_jogada(self, entrada: str) -> bool:
        conteudo = entrada

        if conteudo.lower() == self.texto and (conteudo not in self.combinacoes):
            self.acertos += 1
            self.combinacoes.append(conteudo)
            return True
        else:
            self.erros += 1
            return False
            print("Erro, ela já existe, talvez você tenha digitado!")

    def prompt(self) -> str:
        nome = self.texto
        quantia = len(self.combinacoes)
        a = self.acertos; e = self.erros
        conteudo = input(
            "[{} \u2713 | {} \u2717] Digite uma combinação de '{}': "
            .format(a, e, nome)
        )

        return conteudo
    
    def venceu(self) -> bool:
        "Vence o jogo se o jogador colocar todas versões alternadas da string possíveis."
        TOTAL = 2 ** len(self.texto)
        return len(self.combinacoes) == TOTAL

    def introducao():
        "Introdução inicial do jogo."
        print(
            "\n\nO objetivo do jogo é pegar escrever todas combinações da palavra dada, com seus " + "caractéres, mesmos que iguais, alternado de minúsculas e maiúsculas. Se você" + "escrever todas possíveis, o jogo acaba.", end="\n\n"
        )


PADROES = ["oi", "ovo", "dez", "dedo", "muro", "hey"]
Tabuleiro.introducao()

try:
    jogo = Tabuleiro(Argumentos[1])
except:
    jogo = Tabuleiro(choice(PADROES))

# Enquanto você não passar o limite de derrota, ou vencer o jogo. Este último seria acertar
# todas as combinações, de acordo com a condição do jogo, ele fica pedindo mais entradas.
while (not jogo.venceu() and (not jogo.perdeu())):
    entrada = jogo.prompt()

    if entrada.lower() == "listar":
        jogo.listagem_dos_acertos()
    elif entrada.lower() == "desistir":
        print("\nVocê desistiu, logo perdeu,... quÁ-QuÁ-quA-quÁÁÁ!")
        break
    else:
        if (not jogo.realiza_jogada(entrada)):
            print("Você já digitou!")
else:
    if jogo.venceu():
        print("\nVocê venceu o jogo.")
    else:
        print("\nVocê perdeu,... quÁ-QuÁ-quA-quÁÁÁ!")
        
print("Aqui estão todas suas jogadas:")
jogo.listagem_dos_acertos()
    