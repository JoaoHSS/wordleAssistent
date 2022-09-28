from unidecode import unidecode

#   abre o arquivo e cria uma lista com todas as palavras

with open('palavras.txt', 'r', encoding="utf8") as arquivo:
    conteudo = arquivo.readlines()
    conteudo = [x.rstrip('\n') for x in conteudo]

#   vai conter as palavras com 5 letras

cincoLetras = ""

#   lê todas as palavras e adiciona apenas as que tem 5 letras

for palavra in conteudo:
    if len(palavra) == 5:
        cincoLetras += palavra +'\n'

#   remove os acentos

cincoLetras = unidecode(cincoLetras)

#   escreve um arquivo com a nova lista

with open('cincoLetras.txt', 'w', encoding="utf8") as arquivo:
    arquivo.write(cincoLetras.lower())