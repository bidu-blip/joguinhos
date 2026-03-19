"""
   Vamos fazer uma versão simplificada do joguinho da velha(tic-tac-toe).
 Ele será feito usando o terminal, com o console compartilhado. O tabuleiro
 haverá coordenadas que você pode dizer onde jogar.
"""
from enum import (StrEnum, auto)
from time import (time)
from random import (choice)
from os import (system as System)


class Peca(StrEnum):
    BOLA = 'O'
    XIS = 'X'

    def __repr__(self) -> str:
        match self:
            case Peca.BOLA:
                return "O "
            case Peca.XIS:
                return "X "
                    
    def __str__(self):
        match self:
            case Peca.BOLA:
                return 'Bola(O)'
            case Peca.XIS:
                return "Xis(X)"
    
        
class Jogador:
    # Contagem de instância(jogadores) criados.
    INSTANCIAS = 0

    def __init__(self, peca: Peca) -> None:
        assert isinstance(peca, Peca)

        self.inicio = time()
        self.tempo_medio_de_jogada = 0.0
        self.jogadas = []
        self.peca = peca
        Jogador.INSTANCIAS += 1
    
    def __str__(self):
        "Representação de debug da instância."
        decorrido = abs(time() - self.inicio)
        jogadas = len(self.jogadas)

        return f"Jogador com {self.peca}; iniciou à {decorrido:0.2}seg; realizou {jogadas} jogadas."

    def __repr__(self):
        decorrido = abs(time() - self.inicio)
        jogadas = len(self.jogadas)

        return f"Jogador {self.peca} [{decorrido:0.0f}seg | {jogadas}]"
    
    def __eq__(self, outro) -> bool:
        "Verifica não só a peça de cada jogado, porém sua instância também."
        PECAS_DIFERENTES = (self.peca != outro.peca)
        NAO_E_A_MESMA_INSTANCIA = not (self is outro)
        
        if __debug__:
            print(f"Instância: {self}")
            print(f"Outro: {outro}")
        
        return PECAS_DIFERENTES and NAO_E_A_MESMA_INSTANCIA

class Tabuleiro:
    def __init__(self):
        self.formatacao = """
                    1      2      3
               
                        *     *
             A      %s  *  %s *   %s
                        *     *
                 **********************
                        *     *
             B      %s  *  %s *   %s
                        *     *                                                
                 **********************
                        *     *
             C      %s  *  %s *   %s
                        *     *                                                

            """
        self.grade = (
            [None, None, None],
            [None, None, None],
            [None, None, None]
        )

    def __str__(self):
        # Conversão da matriz numa sequência.
        sequencia = tuple(self.grade[0]) + tuple(self.grade[1]) + tuple(self.grade[2])
        # Conversão de peças em suas respectívas representações:
        CLOSURE = lambda X: "  " if X is None else repr(X)
        tupla = tuple(map(CLOSURE, sequencia))

        return self.formatacao % tupla

    @staticmethod
    def decodifica(codigo) -> tuple[int, int]:
        assert len(codigo) == 2
        assert codigo[0].upper() in "ABC"
        assert codigo[1] in "123"

        match codigo[0].upper():
            case "A": linha = 0
            case "B": linha = 1
            case "C": linha = 2
            case _:
                raise AttributeError("Não aceito!")
            
        match codigo[1]:
            case "1": coluna = 0
            case "2": coluna = 1
            case "3": coluna = 2
            case _:
                raise AttributeError("Não aceito!")
        return (linha, coluna)
        
    def coloca_peca(self, peca: Peca, linha: int, coluna: int) -> bool:
        (L, C) = (linha, coluna)

        if self.grade[L][C] is None:
            self.grade[L][C] = peca
            return True
        else:
            return False
    
    def verifica_vencedor(self) -> tuple[Peca, bool]:
        matriz = self.grade
        
        # Tabuleiro nomeada, cada lugar nomeada de 'a' à 'i', isso, começando de cima prá baixo e
        # da esquerda à direita.
        #        a  |  b  |  c
        #      -----------------
        #        d  |  e  |  f
        #      -----------------
        #        g  |  h  |  i
        (a, b, c) = matriz[0][:]
        (d, e, f) = matriz[1][:]
        (g, h, i) = matriz[2][:]
        
        # Primeira parte todas as linhas.
        if (a is not None) and (a == b == c):
            vencedor = a
            alguem_venceu = True
        elif (d is not None) and (d == e == f):
            vencedor = d
            alguem_venceu = True
        elif (g is not None) and (g == h == i):
            vencedor = g
            alguem_venceu = True
        # Segunda verificação é das colunas.
        elif (a is not None) and (a == d == g):
            vencedor = a
            alguem_venceu = True
        elif (b is not None) and (b == e == h):
            vencedor = b
            alguem_venceu = True
        elif (c is not None) and (c == f == i):
            vencedor = c
            alguem_venceu = True
        # Terceiro, verificação das diagonais:
        elif (a is not None) and (a == e == i):
            vencedor = a
            alguem_venceu = True
        elif (c is not None) and (c == e == g):
            vencedor = c
            alguem_venceu = True
        else:
            vencedor = None
            alguem_venceu = False

        return (vencedor, alguem_venceu)
    
   
class Jogo:
    def __init__(self, board: Tabuleiro, a: Jogador, b: Jogador):
        assert (a != b)
        assert (a.peca != b.peca)
        
        self.tabuleiro = board
        self.jogadores = [a, b]
        self.atual = choice(self.jogadores)
        # O encerramento foi requisitado por algum jogador.
        self.requisitado = False
        
    def total_de_jogadas(self) -> int:
        (ja, jb) = self.jogadores
        return len(ja.jogadas) + len(jb.jogadas) 
    
    def encerrado(self) -> bool:
        ALGUEM_VENCEU = self.tabuleiro.verifica_vencedor()[1]
        JOGADAS_ESGOTADAS = self.total_de_jogadas() == 9
        
        return ALGUEM_VENCEU or JOGADAS_ESGOTADAS or self.requisitado
    
    def alterna_jogador(self):
        # Sorteia um novo jogador até que ele seja diferente do usual. Sim, um 
        # método bem computacionalmente inefficiente.
        novo = choice(self.jogadores)
        
        while novo != self.atual:
            novo = choice(self.jogadores)
        self.atual = novo
    
    def visualizar_tabuleiro(self):
        System("clear")
        print(self.tabuleiro)
    
    def realiza_jogada(self):
        coordenada = input(f"{repr(self.atual)}, coordenada: ")
        
        # Se for escrito para sair do programa, então ele muda o status para encerrado.
        if coordenada.lower() in ("sair", "quit", "exit"):
            self.requisitado = True
            return None
        else:
            (lin, col) = Tabuleiro.decodifica(coordenada)
        
        if (not self.tabuleiro.coloca_peca(self.atual.peca, lin, col)):
            print("Local indisponível! Tente em outro.")
            self.realiza_jogada()
        self.atual.jogadas.append((lin, col))
    
    def resultado_final(self):
        (vencedor, resultado) = self.tabuleiro.verifica_vencedor()
        
        if vencedor is None:
            print("Houve um empate técnico na partida.")
        else:
            print(f"O jogador de '{vencedor}' teve vitória.")

"""
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
                             Execução do Programa
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 
"""
if __name__ == "__main__":
    partida = Jogo(
        Tabuleiro(),
        Jogador(Peca.BOLA),
        Jogador(Peca.XIS)
    )
    
    # Até não se detecar um vencedor, ou não mais jogadas, ou também um pedido para 
    # encerrar a partida, fica num loop. Este, que consiste na: impressão do tabuleiro;
    # a entrada de um novo jogador(uma coordenada correta, do usuário da vez), verificando
    # se sua coordenada de jogo foi correta(não preenchida ou válida); e a alternância dele.
    while (not partida.encerrado()):
        partida.visualizar_tabuleiro()
        partida.realiza_jogada()
        partida.alterna_jogador()
    else:
        # Impressão final do tabuleiro. Garantir que ele fique preenchido de forma que,
        # compatibilize com a mensagem final. Algumas vezes, no motor afirma o vencedor
        # mais o tabuleiro não mostra isso, pois falta a gravação da última partida.
        partida.visualizar_tabuleiro()
    # O anúcio do vencedor, se houve alguma é claro.
    partida.resultado_final()
    
"""
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
                                    Testes Unitários
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 
"""
from unittest import(TestCase)

class PecaRepresentacao(TestCase):
    def runTest(self):
        a = Peca.XIS
        b = Peca.BOLA
        c = Peca.BOLA

        print(a, b, c)

class OperacoesSobrePeca(TestCase):
    def runTest(self):
        a = Peca.XIS
        b = Peca.BOLA
        c = Peca.BOLA

        self.assertEqual(c, b)
        self.assertFalse(a == b or a == c)

class RepresentacaoDoJogador(TestCase):
    def runTest(self):
        obj = Jogador(Peca.BOLA)
        outro = Jogador(Peca.BOLA)

        print(obj, outro, sep='\n')

class RepresentacaoDoTabuleiro(TestCase):
    def runTest(self):
        obj = Tabuleiro()

        print(obj)
        obj.coloca_peca(Peca.BOLA, 0, 1)
        obj.coloca_peca(Peca.BOLA, 0, 2)
        obj.coloca_peca(Peca.XIS, 2, 1)
        obj.coloca_peca(Peca.XIS, 1, 1)
        obj.coloca_peca(Peca.XIS, 2, 2)
        print(obj)

class FuncaoDeDecodificacao(TestCase):
    def runTest(self):
        entradas = ["a1", "b2", "c3", "b3"]

        for item in entradas:
            print(item, "===>", Tabuleiro.decodifica(item))

class ConfiguracoesVencedoras(TestCase):
    @staticmethod
    def seleciona_uma_posicao() -> str:
        return choice("abc") + choice("123")
    
    def arranja_uma_configuracao_aleatoria(self):
        board = self.board
        contagem = 0
        PECAS = (Peca.BOLA, Peca.XIS)

        while contagem < 9:
            coordenadas = ConfiguracoesVencedoras.seleciona_uma_posicao() 
            (lin, col) = Tabuleiro.decodifica(coordenadas)
            peca = choice(PECAS)

            if board.coloca_peca(peca, lin, col):
                contagem += 1
        
    
    def setUp(self):
        self.board = Tabuleiro()

        print("Preenchendo ele, ...", end=" ")
        self.arranja_uma_configuracao_aleatoria()
        print("feito.")

    def runTest(self):
        print(self.board)
        print(f"Venceu?{self.board.verifica_vencedor()}")
        
class PrototipoDoJogo(TestCase):
    def runTest(self):
        tabuleiro = Tabuleiro()
        jogador_bola = Jogador(Peca.BOLA)
        jogador_xis = Jogador(Peca.XIS)
        partida = Jogo(tabuleiro, jogador_bola, jogador_xis)
        
        while (not partida.encerrado()):
            partida.visualizar_tabuleiro()
            partida.realiza_jogada()
            partida.alterna_jogador()
        else:
            partida.visualizar_tabuleiro()
        partida.resultado_final()

class ComparacaoDeJogadores(TestCase):
    def runTest(self):
        a = Jogador(Peca.XIS)
        b = Jogador(Peca.BOLA)
        
        self.assertNotEqual(a, b)

class VisualizacaoDaPeca(TestCase):
    def runTest(self):
        a = Peca.BOLA
        b = Peca.XIS
        
        print("Peças via 'debug':")
        print("", a, b, sep='\t\t')
        print("Peças via 'display':")
        print("", repr(a), repr(b), sep='\t\t')

class ComparacaoDaPeca(TestCase):
    def runTest(self):
        a = Peca.BOLA
        b = Peca.XIS
        c = Peca.BOLA
        d = Peca.XIS
        
        self.assertNotEqual(a, b)
        self.assertEqual(d, b)
        self.assertEqual(b, d)
        self.assertEqual(a, c)
        
        print("Todas afirmações foram bem sucedidas.")
        