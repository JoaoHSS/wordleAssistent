import pygame as pg

ALTURA, LARGURA = 800, 800

#   CORES
BLACK, WHITE, DARKGREY = (50,50,50), (255,255,255), (75,75,75)
RED, BLUE, GREEN, YELLOW = (255,0,0,255), (0,0,100,255), (0,255,0,255), (255,255,0,255)

#   ELEMENTOS PARA O PYGAME
pg.init()
janela = pg.display.set_mode([LARGURA, ALTURA])

#   LISTA COM PALAVRAS DE 5 LETRAS
listaPalavras = "cincoLetras.txt"   #6026 palavras nesta lista

#   INICIALIZA LISTAS DE LETRAS (  TEM A POSIÇÃO CONFIRMADA, TEM NA PALAVRAS MAS NÃO SABE A POSIÇÃO, NÃO TEM NA PALAVRA)
pos_certa, pos_incerta, nao_tem_l = [], [], []
alfabeto = list("abcdefghijklmnopqrstuvwxyzç")

#   INICIALIZA A O ÍNDICE QUE VAI SER PEGO DO "pos_certa" (O NÚMERO NA PARTE DE BAIXO DA TELA, AO SER EXIBIDO TEM +1)
pos_escolha = 0

#   BOTÕES
bot_limpar = (575, 50, 200, 100)
bot_escolha = (485, 65, 75, 75)
bot_posicao = (400, 625 , 50, 50)

def main():

    conteudo = obterConteudo()
    bot_escol_cor = YELLOW
    correndo = True
    while correndo:
        
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                correndo = False

            #   tratamento dos cliques do mouse
            if evento.type == pg.MOUSEBUTTONUP:
                if estaNoBotao(bot_limpar):
                    #   reinicia as listas, "limpa"
                    global nao_tem_l, pos_incerta, pos_certa, alfabeto
                    nao_tem_l, pos_incerta, pos_certa, alfabeto =     [],     [],     [],     list("abcdefghijklmnopqrstuvwxyzç")
                    conteudo = obterConteudo()

                if estaNoBotao(bot_escolha):
                    #   muda as opçoes de ação que vai ser feita
                    if bot_escol_cor == YELLOW:     bot_escol_cor = GREEN
                    elif bot_escol_cor == GREEN:    bot_escol_cor = RED
                    else:                           bot_escol_cor = YELLOW
                            
                if estaNoBotao(bot_posicao):
                    # faz um loop pelos índices e recomeça ao chegar no final
                    global pos_escolha
                    pos_escolha += 1
                    if pos_escolha == 5:    pos_escolha = 0

            #   tratamento das letras
            if evento.type == pg.KEYDOWN:
                #   obtem uma string da tecla pressionada
                letra = pg.key.name(evento.key)
                if letra in alfabeto:
                    alfabeto.remove(letra)
                    if bot_escol_cor == RED:      
                        nao_tem_l.append(letra) 
                        conteudo = naotemletra(letra, conteudo)
                    if bot_escol_cor == YELLOW:  
                        pos_incerta.append(letra)   
                        conteudo = temletra(letra, conteudo)
                    if bot_escol_cor == GREEN:
                        pos_certa.append(letra)  
                        conteudo = posConfirmada(letra, pos_escolha, conteudo)
                if letra in pos_incerta:
                    if bot_escol_cor == GREEN:
                        pos_incerta.remove(letra)
                        pos_certa.append(letra)  
                        conteudo = posConfirmada(letra, pos_escolha, conteudo)

        #   desenha o fundo
        janela.fill(BLACK)
        janela.fill(BLUE, (LARGURA/1.7, 0, LARGURA, ALTURA))
        
        #   desenha as letras
        desenharTexto("Letras possíveis:", 50, 30)
        desenharListaLetras(alfabeto, 100)
        desenharTexto("Posição não confirmada:", 50, 280)
        desenharListaLetras(pos_incerta, 350)
        desenharTexto("Não tem na palavra:", 50, 430)
        desenharListaLetras(nao_tem_l, 500)
        desenharTexto("Posição confirmada:", 50, 580)
        desenharListaLetras(pos_certa, 650)

        #   botão limpar
        pg.draw.rect(janela, WHITE, bot_limpar)
        desenharTexto("LIMPAR", bot_limpar[0], bot_limpar[1]+25, size=50, cor_l=BLACK, cor_f=WHITE)

        #   botao escolha de ação
        pg.draw.rect(janela, bot_escol_cor, bot_escolha)

        #   botao posição
        pg.draw.rect(janela, WHITE, bot_posicao)
        desenharTexto(str(pos_escolha+1), bot_posicao[0], bot_posicao[1], size=50, cor_l=BLACK, cor_f=WHITE)
        
        #   parte de sugestões
        desenharTexto("SUGESTÕES:", 500, 175, size=40, cor_l=WHITE, cor_f=BLUE)

        pos_y = 0
        for palavra in conteudo[:14]:
            desenharTexto(palavra, 500, pos_y+250, cor_l=WHITE, cor_f=BLUE)
            pos_y += 40
        pos_y = 0
        for palavra in conteudo[14:28]:
            desenharTexto(palavra, 650, pos_y+250, cor_l=WHITE, cor_f=BLUE)
            pos_y += 40
        
        #   atualiza tela
        pg.display.update()

#   -----------         FUNÇÕES PARA A LÓGICA         -----------

#   RETORNA A PRÓPRIA LISTA PASSADA, MAS APENAS COM AS PALAVRAS QUE TEM A LETRA NO INDICE ESPECIFICADO
def posConfirmada(letra, posicao, conteudo):
    sugestoes = []
    for palavra in conteudo:
        if letra == palavra[posicao]:
            sugestoes.append(palavra)
    return sugestoes

#   RETORNA A PRÓPRIA LISTA PASSADA, MAS APENAS COM AS PALAVRAS QUE TEM A LETRA
def temletra(letra, conteudo):
    sugestoes = []
    for palavra in conteudo:
        if letra in palavra:
            sugestoes.append(palavra)
    return sugestoes

#   RETORNA A PRÓPRIA LISTA PASSADA, MAS SEM AS PALAVRAS QUE TEM A LETRA
def naotemletra(letra, conteudo):
    sugestoes = []
    for palavra in conteudo:
        if letra not in palavra:
            sugestoes.append(palavra)
    return sugestoes

#   OBTÉM AS PALAVRAS PARA AS SUGESTÕES
def obterConteudo():
    with open(listaPalavras, 'r', encoding="utf8") as arquivo:
        conteudo = [x.rstrip('\n') for x in arquivo.readlines()]
        return conteudo

#   -----------         FUNÇÕES SIMPLES E EXIBIÇÃO         -----------

#   DESENHA UMA LISTA DE LETRAS NA PARTE ESQUERDA DA E TELA NA ALTURA ESPECIFICADA
def desenharListaLetras(lista, altura):
    for letra in lista:
        if lista.index(letra) < 10:  
            desenharTexto(letra, lista.index(letra)*40+50, altura)
        elif lista.index(letra) < 20:  
            desenharTexto(letra, lista.index(letra)*40-350, altura + 50)
        else:  
            desenharTexto(letra, lista.index(letra)*40-750, altura + 100)

#   VERIFICA SE O MOUSE ESTÁ DENTRO DE UM RETÂNGULO
def estaNoBotao(retangulo):
    mouse = pg.mouse.get_pos()
    if mouse[0] in range(retangulo[0], retangulo[0]+retangulo[2]) and mouse[1] in range(retangulo[1], retangulo[1]+retangulo[3]):
        return True

#   DESENHA UM TEXTO    (PARÂMETROS AUTOEXPLICATIVOS)
def desenharTexto(string, X , Y, size=30, cor_l=WHITE, cor_f=BLACK):
    font = pg.font.Font('freesansbold.ttf', size)
    text = font.render(string, True, cor_l, cor_f)
    textRect = text.get_rect()
    textRect.topleft = (X, Y)
    janela.blit(text, textRect)

if __name__ == "__main__":
    main()
