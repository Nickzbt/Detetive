import json
import os
import random
import time

prop = {
    "A1-1":"saiu mais cedo as 7:15 PM.",
    "A1-2":"Foi ao medico as 7:30 PM.",
    "G1-1":"Fechou o banco as 8 PM.",
    "G1-2":"Conferiu o quadro de luz apos a queda da luz.",
    "G1-3":"Ligou o gerador de emergencia.",
    "G2-1":"Verificou os ambientes internos.",
    "G2-2":"Fez uma ronda no banco apos a queda da luz.",
    "Z-1":"Chegou 8 PM para a limpeza.",
    "Z-2":"Viu todos os funcionarios no banco.",
    "A2-1":"Saiu junto de A3 as 8:20 PM.",
    "A3-1":"Saiu junto de A2 as 8:20 PM.",
    "GB-1":"Documentou valores até 9 PM.",
    "GB-2":"Trancou o cofre 9 PM.",
    "Q-1":"O cofre estava trancado.",
    "Q-2":"Nao houve roubo.",
    "L-1":"A luz caiu entre 12 PM e 2 AM.",
    "C-1":"Não há cameras ligadas.",
    "C-2":"Cameras voltaram 30 min após ligar o gerador."
}
solution = [
    ("""
        (A1-2 -> A1-1)
        (Z-2 -> Z-1)
        (~A1-1 v ~Z-1)
        ---------------
        (~A1-2 v ~Z-2)
    """),
    ("""
        (~A1-2 v ~Z-2)
        (Z-2)
        ---------------
        A1-2
    """),
    ("""
        (Q-1 -> Q-2)
        (GB-1 -> GB-2)
        (~Q-2 v ~GB-2)
        ---------------
        (~Q-1 v ~GB-1)
    """),
    ("""
        (~Q-1 v ~GB-1)
        (GB-1)
        ---------------
        (~Q-1)
    """),
    ("""
        (L-1 -> C-1)
        (L-1)
        ---------------
        (C-1)
    """),
    ("""
        (G1-3 -> C-2)
        (G1-3)
        ---------------
        (C-2)
    """)
]


suspects = [
    "Guarda 1 (G1)",
    "Guarda 2 (G2)",
    "Zelador (Z)",
    "Gerente do banco (GB)",
    "Atendente 1 (A1)",
    "Atendente 2 (A2)",
    "Atendente 3 (A3)",
    ]

clues = [
    "(P1)  Se A1 foi ao médico 7:30 PM, então A1 saiu mais cedo as 7:15PM (A1-2 -> A1-1)",
    "(P2)  Se Z viu todos os funcionário, então Z chegou as 8PM (Z-2 -> Z-1)",
    "(P3)  Ou A1 saiu mais cedo ou Z chegou as 8PM (~A1-1 v ~Z-1)",
    "(P4)  Z chegou as 8 PM (Z-1)",
    "(P5)  Z viu todos os funcionários(Z-2)",
    "(P6)  Se G1 fechou o banco, entao G2 verificou os ambientes internos (G1-1 -> G2-1)",
    "(P7)  Se A2 saiu as 8:20 PM, entao A3 saiu com ele (A2-1 -> A3-1)",
    "(P8)  A2 saiu 8:20 PM (A2-1)",
    "(P9)  Se o cofre estava trancado, entao nao houve roubo (Q-1 -> Q-2)",
    "(P10) Se GB documentou os valores ate 9 PM, entao GB trancou o cofre 9PM (GB-1 ->  GB-2)",
    "(P11) Ou houve roubo ou GB nao documentou os valores (~Q-2 v ~GB--1)",
    "(P12) GB documentou os valores (GB-1)",
    "(P13) Se a luz caiu, entao as cameras desligaram (L-1 -> C1)",
    "(P14) A luz caiu entre 12 PM e 2 AM (L-1)",
    "(P15) Se a luz caiu, entao G1 verificou o quadro de luz (L-1 -> G1-2)",
    "(P16) Se G1 verificou o quadro de luz, entao G1 ligou o gerador de emergencia (G1-2 -> G1-3)",
    "(P17) Se G1 ligou o gerador de emergencia, entao as cameras voltaram 1 PM (G1-3 -> C-2)",
]

msg_init = ("""|----------------------------------------JOGO DE DETETIVE----------------------------------------|
    Assalto ao banco ocorrido durante a noite entre 12 PM e 2 AM, onde o alarme não foi 
    tocado e câmeras de segurança foram desligadas, descubra através das pistas quem 
    é o culpado pelo crime, baseando-se nos álibis dados pelos suspeitos do crime.
""")

msg_rules = ("""|-----------------------------------------REGRAS DO JOGO-----------------------------------------|
    -> O jogo possuí até 4 etapas, cada qual será dada ao jogador um conjunto de hipoteses/pistas
    -> As tres etapas iniciais fornecem 4 pistas cada, a ultima etapa fornecera as pistas restantes
    -> Em cada etapa há a chance de se apontar o culpado ou passar para a próxima
    -> Acertando o culpado o jogo acaba (valendo mais ou menos pontos de acordo com a etapa)
    -> Errando o culpado serão retiradas 2 pistas da etapa seguinte
    -> Há 7 suspeitos total, inicialmente todos são igualmente suspeitos
    -> Partindo dos 7 suspeitos cada um apresentou álibis sobre o dia do incidente
    -> Há um total de 17 pistas baseadas nos álibis obtidos
    -> Ao escolher apontar um suspeito, todas suas pistas serao exibidas para auxilia-lo, porem se
        errar perdera 2 pistas da etapa seguinte e diminuira 1 ponto possivel.
    -> Apenas um dos suspeitos é o culpado.
""")

my_clues = []

score = 10

os.system("cls")

print(msg_init)
choice = int(input("Digite [1] para continuar ou [0] para fechar o programa:"))
if choice != (1):
    os.system("cls")
    exit()
os.system("cls")

print(msg_rules)
choice = int(input("Digite [1] para continuar ou [0] para fechar o programa:"))
if choice != (1):
    os.system("cls")
    exit()
os.system("cls")

print("Os suspeitos do crime são:")
for i in suspects:
    print("->" ,i)

choice = int(input("Digite [1] para continuar ou [0] para fechar o programa:"))
if choice != (1):
    os.system("cls")
    exit()

os.system("cls")

print("|----------------------------------------ETAPA 1----------------------------------------|")
print("As 4 pistas desta etapas são aleatorias, certifique-se de prestar atencao aos detalhes\n")
for i in range (4):
    item = random.choice(clues)
    clues.remove(item)
    my_clues.append(item)
    print(f"->{item}")

choice = int(input("Digite [1] para continuar ou [0] para apontar o culpado:"))
if choice != (1):
    os.system("cls")
    print("Suas pistas atuais são:")
    for i in my_clues:
        print(i)
    print("\n")
    print("Informe quem roubou o banco:")
    for i in range(len(suspects)):
        print(f"({i}) {suspects[i]}")
    culpado = int(input("Insira o numero do culpado:"))
    if suspects[culpado] == "Atendente 1 (A1)":
        os.system("cls")
        print("PARABENS VOCE ADIVINHOU QUEM E O RESPONSAVEL PELO CRIME!!!")
        print(f"GANHOU O JOGO NA ETAPA 1, CONTABILIZANDO {score} PONTOS.")
        quit()
    else:
        for i in range (2):
            item = random.choice(clues)
            clues.remove(item)
        suspects.pop(culpado)
        score = score - 2
        print("-> Voce errou o culpado, o indicado será removido da lista de suspeitos.")
        print("-> Duas pistas aleatorias foram removidas do banco de pistas.")
        print("-> Passando para a proxima etapa, boa sorte...")
        time.sleep(5)
else:
    score = score - 1 

os.system("cls")

print("|----------------------------------------ETAPA 2----------------------------------------|")
print("As 4 pistas desta etapas são aleatorias, certifique-se de prestar atencao aos detalhes\n")
for i in range (4):
    item = random.choice(clues)
    clues.remove(item)
    my_clues.append(item)
    print(f"->{item}")

choice = int(input("Digite [1] para continuar ou [0] para apontar o culpado:"))
if choice != (1):
    os.system("cls")
    print("Suas pistas atuais são:")
    for i in my_clues:
        print(i)
    print("\n")
    print("Informe quem roubou o banco:")
    for i in range(len(suspects)):
        print(f"({i}) {suspects[i]}")
    culpado = int(input("Insira o numero do culpado:"))
    if suspects[culpado] == "Atendente 1 (A1)":
        os.system("cls")
        print("PARABENS VOCE ADIVINHOU QUEM E O RESPONSAVEL PELO CRIME!!!")
        print(f"GANHOU O JOGO NA ETAPA 2, CONTABILIZANDO {score} PONTOS.")
        quit()
    else:
        for i in range (2):
            item = random.choice(clues)
            clues.remove(item)
        suspects.pop(culpado)
        score = score - 2
        print("-> Voce errou o culpado, o indicado será removido da lista de suspeitos.")
        print("-> Duas pistas aleatorias foram removidas do banco de pistas.")
        print("-> Passando para a proxima etapa, boa sorte...")
        time.sleep(5)

else:
    score = score - 1 

os.system("cls")

print("|----------------------------------------ETAPA 3----------------------------------------|")
print("As 4 pistas desta etapas são aleatorias, certifique-se de prestar atencao aos detalhes\n")
for i in range (4):
    item = random.choice(clues)
    clues.remove(item)
    my_clues.append(item)
    print(f"->{item}")

choice = int(input("Digite [1] para continuar ou [0] para apontar o culpado:"))
if choice != (1):
    os.system("cls")
    print("Suas pistas atuais são:")
    for i in my_clues:
        print(i)
    print("\n")
    print("Informe quem roubou o banco:")
    for i in range(len(suspects)):
        print(f"({i}) {suspects[i]}")
    culpado = int(input("Insira o numero do culpado:"))
    if suspects[culpado] == "Atendente 1 (A1)":
        os.system("cls")
        print("PARABENS VOCE ADIVINHOU QUEM E O RESPONSAVEL PELO CRIME!!!")
        print(f"GANHOU O JOGO NA ETAPA 3, CONTABILIZANDO {score} PONTOS.")
        quit()
    else:
        for i in range (2):
            item = random.choice(clues)
            clues.remove(item)
        suspects.pop(culpado)
        score = score - 2
        print("-> Voce errou o culpado, o indicado será removido da lista de suspeitos.")
        print("-> Duas pistas aleatorias foram removidas do banco de pistas.")
        print("-> Passando para a proxima etapa, boa sorte...")
        time.sleep(5)

else:
    score = score - 1 

os.system("cls")

print("|----------------------------------------ETAPA 4----------------------------------------|")
print("ATENÇAO!! Ultima etapa para adivinhar o suspeito, encontre o culpado ou o mesmo saira impune")
print("Estas sao as ultimas pistas para que voce resolva o caso, preste atencao aos detalhes\n")
for i in range (len(clues)):
    item = random.choice(clues)
    clues.remove(item)
    my_clues.append(item)
print("Suas pistas atuais são:")
for i in my_clues:
    print(i)
print("\n")
print("Informe quem roubou o banco:")
for i in range(len(suspects)):
    print(f"({i}) {suspects[i]}")
culpado = int(input("Insira o numero do culpado:"))
if suspects[culpado] == "Atendente 1 (A1)":
    os.system("cls")
    print("PARABENS VOCE ADIVINHOU QUEM E O RESPONSAVEL PELO CRIME!!!")
    print(f"GANHOU O JOGO NA ETAPA 4, CONTABILIZANDO {score} PONTOS.")
    quit()
else:
    print("""Voce nao conseguiu adivinhar quem foi responsavel pelo crime.
    Tente novamente ou finalize o jogo para ver a solução.""")
    choice = int(input("[1] para ver a solucao ou [0] para finalizar e ver a solução"))
    if choice == 1:
        for i in solution:
            print(i)
    else:
        quit()

