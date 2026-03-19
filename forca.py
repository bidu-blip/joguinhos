'''
   Joguinha da forca básico apenas com o que foi ensinado até o momento para o professor.
 Como ainda não entramos em função, ficará tudo no 'main', o corpo nú do arquivo.
'''
import random, os

# Constantes de configuração do programa:
TOTEM_CORPO     = '@'
TOTEM_PLACAR    = '#'
TOTEM_PL_ERROR  = '%'           # Totem do placar de erro.
INDICES_CORPO   = []
PARTES_CORPO    = ('O', '/', '|', '\\', '/', '\\')
MAXIMO_DE_ERROS = len(PARTES_CORPO)
INDICES_PLACAR  = []
INDICES_PLERROS = []            # Índices do placar de erros.
BANCO_DE_DADOS  = [
    ("cavalo", "Uma animal de quatro patas que costuma ser montado"),
    ("gato", "Um felino domésticado"),
    ("computador", "Você usa ele para multiplas tarefas, como escutar música, fazer trabalhos,"+
        " pesquisar assuntos para trabalho ou não, e etc..."),
    ("balao", "Um veículo áereo não motorizado."),
    ("brasilia", "Uma das maiores e mais importantes cidade do Brasil."),
    ("arvore", "Cosume carbono, expele oxigênio. Se alimenta de energia do Sol."),
    ("bueiro", "Aonde toda a água da chuva, eventualmente, irá."),
    ("tomate", "Vegetal bem vermelho. O favorito de cadeias de fast-food."),
    ("bicicleta", "Tipo de veículo com duas rodas não motorizado."),
    ("papagaio", "Ave conhecida por falar.")
]
selecao = random.choice(BANCO_DE_DADOS)
(PALAVRA_CHAVE, DICA) = selecao
(erros, acertos) = (0, 0)
ja_colocadas = set([])
passes_corretos = set([])
tabuleiro = bytearray(
    b"""                                                   

        _________                                             
        |       |                                                           
        |       @                                                  
        |      @@@
        |      @ @            # # # # # # # # # # # # # # # # # # # # #           
        |
        |
      =====
                                                    Erros: % % % % % %
    """
)
PALAVRA_CHAVE = PALAVRA_CHAVE.upper()
teclou_mesma_letra = False 


# Faz uma iteração, onde pega os índices referentes ao corpo e ao placar na string.
for (indice, caractere) in enumerate(tabuleiro):
    if chr(caractere) == TOTEM_CORPO:
        INDICES_CORPO.append(indice)
        
    if chr(caractere) == TOTEM_PLACAR:
        INDICES_PLACAR.append(indice)
    
    if chr(caractere) == TOTEM_PL_ERROR:
        INDICES_PLERROS.append(indice)
        
if __debug__:
    print("Descobrindo índices referentes ao corpo na forca.")
    for (p, caractere) in enumerate(tabuleiro):

        if chr(caractere) == TOTEM_CORPO or chr(caractere) == TOTEM_PLACAR:
            print(f"{p} - {chr(caractere)}")
    
    print(f"Índices do corpo:  {INDICES_CORPO}")
    print(f"Índices do placar: {INDICES_PLACAR}")

# Ajustando o placar com apenas as letras necesária da 'palavra chave'.
cursor = 0
for posicao in INDICES_PLACAR:
    if cursor < len(PALAVRA_CHAVE):
        tabuleiro[posicao] = ord('_')
    else:
        tabuleiro[posicao] = ord(' ')
    cursor += 1
# Formatando o placar com as letras erradas que foram chutadas.
for posicao in INDICES_PLERROS:
    tabuleiro[posicao] = ord('_')
# Ajustando o corpo -- apenas deixando o que não foi marcado como vázio. Ao invés
# do token inicialmente.
for posicao in INDICES_CORPO:
    tabuleiro[posicao] = ord(' ')
    
if __debug__:
    print("Após a primeira alteração:")
    print(tabuleiro.decode(encoding="utf8"))

while (erros < MAXIMO_DE_ERROS) and (passes_corretos != frozenset(PALAVRA_CHAVE)):
    # Aqui mostra o tabuleiro do jogo, ou seja, a forca e o placar com as as 
    # letras.
    os.system("clear")
    print(f"Dica: \"{DICA}\"")
    # Verifica a letra, seja ela certa ou errada, já foi escolhida.
    if teclou_mesma_letra:
        print("Você já escolheu está letra!")
        teclou_mesma_letra = False
    # Imprime o tabuleiro:
    print(tabuleiro.decode(encoding="utf8"))
    
    if __debug__:
        print(f"Acertos: {acertos} Erros: {erros}", end="\n\n")
    
    # Aqui você coloca as letras, e ajusta alguma entrada inválida, porém
    # quase certa.
    letra = input("Uma letra: ")
    letra = letra.upper()
    letra = letra[0]
    
    if letra in ja_colocadas:
        teclou_mesma_letra = True
        continue
    
    if letra in PALAVRA_CHAVE:
        # Preenche o 'placar' com letras, nas suas respectivas posições.
        for (p, char) in enumerate(PALAVRA_CHAVE):
            if char == letra:
                posicao = INDICES_PLACAR[p]
                tabuleiro[posicao] = ord(char)
        acertos += 1
        passes_corretos.add(letra)
        
    else:
        if erros == MAXIMO_DE_ERROS:
            break
        # Se a letra está errada, então ele preenche mais um campo na forca.
        parte = ord(PARTES_CORPO[erros])
        indice = INDICES_CORPO[erros]
        tabuleiro[indice] = parte
       
        erros += 1
    ja_colocadas.add(letra)

    # Agora preenchendo o placar de erros. Onde não houver letra, apenas 
    # coloca vázio(_).
    for (erro, elemento) in enumerate(ja_colocadas - passes_corretos):
        indice = INDICES_PLERROS[erro]
        tabuleiro[indice] = ord(elemento)
    
# Mostra o tabuleiro uma última vez antes de avaliar o resultado da 
# partida.
os.system("clear")
print(f"Dica: \"{DICA}\"")
print(tabuleiro.decode(encoding="utf8"))
if __debug__:
    print(f"Acertos: {acertos} Erros: {erros}", end="\n\n")

if len(PARTES_CORPO) == erros:
    print(f"Você perdeu! A palavra correta é '{PALAVRA_CHAVE}'.")
else:
    print("Você venceu.")