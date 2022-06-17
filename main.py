import os
import time

msg_init = ("""|----------------------------------------JOGO DE DETETIVE----------------------------------------|
    Assalto ao banco ocorrido durante a noite entre 12 PM e 2 AM, onde o alarme não foi 
    tocado e câmeras de segurança foram desligadas, descubra através das pistas quem 
    é o culpado pelo crime, baseando-se nos álibis dados pelos suspeitos do crime.
""")

msg_rules = ("""|-----------------------------------------REGRAS DO JOGO-----------------------------------------|
    -> O jogo possuí até 4 etapas, cada qual será dada ao jogador um conjunto de hipoteses/pistas.
    -> As tres etapas iniciais fornecem 4 pistas cada, a ultima etapa fornecera as pistas restantes..
    -> Em cada etapa há a chance de se apontar o culpado ou passar para a próxima.
    -> Acertando o culpado o jogo acaba (valendo mais ou menos pontos de acordo com a etapa).
    -> Há 7 suspeitos no total, inicialmente todos são igualmente suspeitos.
    -> Partindo dos 7 suspeitos cada um apresentou álibis sobre o dia do incidente.
    -> Há um total de 17 pistas baseadas nos álibis obtidos.
    -> Ao escolher apontar um suspeito, todas suas pistas serao exibidas para auxilia-lo, porem se
        errar 2 pontos possiveis.
    -> Ao pular para a próxima etapa, diminuirá 1 ponto possível.
    -> Apenas um dos suspeitos é o culpado.
""")

suspects = [
    "Guarda 1 (G1)",
    "Guarda 2 (G2)",
    "Zelador (Z)",
    "Gerente do banco (GB)",
    "Atendente 1 (A1)",
    "Atendente 2 (A2)",
    "Atendente 3 (A3)",
]

prop = {
    "A1-1":"saiu mais cedo as 7:15 PM.",
    "A1-2":"Foi ao medico as 7:30 PM.",
    "A1-3":"Ligou para GB as 8:50 PM.",
    "G1-1":"Fechou o banco as 8 PM.",
    "G1-2":"Conferiu o quadro de luz apos a queda da luz.",
    "G1-3":"Ligou o gerador de emergencia.", 
    "G2-1":"Verificou os ambientes internos.",
    "G2-2":"Fez uma ronda no banco apos a queda da luz.",
    "Z-1" :"Chegou 8 PM para a limpeza.",
    "Z-2" :"Viu todos os funcionarios no banco.",
    "A2-1":"Saiu junto de A3 as 8:20 PM.",
    "A3-1":"Saiu junto de A2 as 8:20 PM.",
    "GB-1":"Documentou valores até 9 PM.",
    "GB-2":"Trancou o cofre 9 PM.",
    "GB-3":"Documentou os valores e foi embora 8:55 PM.",
    "Q-1" :"O cofre estava trancado.",
    "Q-2" :"Nao houve roubo.",
    "L-1" :"A luz caiu entre 12 PM e 2 AM.",
    "C-1" :"Não há cameras ligadas.",
    "C-2" :"Cameras voltaram 30 min após ligar o gerador."
}

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
    "(P10) Se GB documentou os valores ate 9 PM, entao GB trancou o cofre 9PM (GB-1 -> GB-2)",
    "(P11) Ou houve roubo ou GB nao documentou os valores (~Q-2 v ~GB--1)",
    "(P12) GB documentou os valores (GB-1)",
    
    "(P13) Se a luz caiu, entao as cameras desligaram (L-1 -> C1)",
    "(P14) A luz caiu entre 12 PM e 2 AM (L-1)",
    "(P15) Se a luz caiu, entao G1 verificou o quadro de luz (L-1 -> G1-2)",
    "(P16) Se G1 verificou o quadro de luz, entao G1 ligou o gerador de emergencia (G1-2 -> G1-3)",

    "(P17) Se G1 ligou o gerador de emergencia, entao as cameras voltaram 1 PM (G1-3 -> C-2)",
    "(P18) Se A1 ligou para GB, então GB saiu mais cedo.",
    
    "(P19) Se ... entao A1 roubou",
    "(P20) Se ... entao Z roubou",
    "(P20) Se ... entao GB roubou",
    "(P20) Se ... entao G1 roubou",
]

solution = [
    ("""
    ----Dilema destrutivo----
        (A1-2 -> A1-1)
        (Z-2 -> Z-1)
        (~A1-1 v ~Z-1)
        ---------------
        (~A1-2 v ~Z-2)
    """),
    ("""
    ----Silogismo disjuntivo
        (~A1-2 v ~Z-2)
        (Z-2)
        ---------------
        ~A1-2
    """),
    ("""
    ----Dilema destrutivo
        (Q-1 -> Q-2)
        (GB-1 -> GB-2)
        (~Q-2 v ~GB-2)
        ---------------
        (~Q-1 v ~GB-1)
    """),
    ("""
    ----Silogismo disjuntivo
        (~Q-1 v ~GB-1)
        (GB-1)
        ---------------
        (~Q-1)
    """),
    ("""
    ----Modus ponens----
        (L-1 -> C-1)
        (L-1)
        ---------------
        (C-1)
    """),
    ("""
    ----Modus ponens----
        (G1-3 -> C-2)
        (G1-3)
        ---------------
        (C-2)
    """)
]

my_clues = []
score = 10

def get_choice_game():
    choice = int(input("Digite [1] para continuar ou [0] para encerrar o program: "))
    os.system("cls")
    if choice == 0:
        exit()
    elif choice < 0 or choice >= 2:
        print("Ops! Não é uma das opções!")
        get_choice_game()

def game_step_msg(step: int):
    if 1 <= step <=3:
        print(f"|----------------------------------------ETAPA {step}----------------------------------------|")
        print(f"As 4 pistas desta etapa estao em ordem cronológica, certifiquue-se de presetar atencao aos detalhes\n")
    else:
        print(f"|----------------------------------------ETAPA {step}----------------------------------------|")
        print("ATENÇAO!! Ultima etapa para adivinhar o suspeito, encontre o culpado ou o mesmo saira impune")
        print("Estas sao as ultimas pistas para que voce resolva o caso, preste atencao aos detalhes\n")

def get_suspects():
    print("Os suspeitos atuais sao:")
    for i in suspects:
        print("-> ",i)

def list_suspects():
    print('Os culpados listados por numeros sao:')
    for i in suspects:
        print(f"({suspects.index(i)}) {i}")

def show_clues(max: int = 4):
    print("\nAs pistas desta etapa sao:")
    for _ in range(max):
        item = clues[0]
        clues.remove(item)
        my_clues.append(item)
        print(f"{item}")

def indica_culpado(step: int):
    global score
    print("Suas pistas ate o momento sao:")
    for i in my_clues:
        print(i)
    list_suspects()
    culpado = int(input("Insira o numero do culpado:"))
    if suspects[culpado] == "Atendente 1 (A1)":
        os.system("cls")
        print("PARABENS VOCE ADIVINHOU QUEM E O RESPONSAVEL PELO CRIME!!!")
        print(f"GANHOU O JOGO NA ETAPA {step}, CONTABILIZANDO {score} PONTOS.")
        quit()
    elif step == 4:
        print("""Voce nao conseguiu adivinhar quem foi responsavel pelo crime.
        Tente novamente ou finalize o jogo para ver a solução.""")
        choice = int(input("[1] para ver a solucao ou [0] para finalizar:"))
        if choice == 1:
            for i in solution:
                print(i)
        else:
            quit()
    else:
        suspects.pop(culpado)
        print("-> Voce errou o culpado, o indicado será removido da lista de suspeitos.")
        print("-> Duas pistas aleatorias foram removidas do banco de pistas.")
        print("-> Passando para a proxima etapa, boa sorte...")
        score = score - 2
        time.sleep(3)
        os.system("cls")

def get_choice_sus(step: int):
    global score
    choice = int(input("Digite [1] para continuar ou [0] para indicar um suspeito:"))
    os.system("cls")
    if choice == 0:
        indica_culpado(step)

    elif choice < 0 or choice >= 2:
        print("Ops! Não é uma das opções!")
        get_choice_sus()
    
    else:
        score = score - 1 

os.system("cls")

print(msg_init)
get_choice_game()
print(msg_rules)
get_choice_game()

for i in range(4):
    i = i + 1
    game_step_msg(i)
    get_suspects()
    show_clues()
    get_choice_sus(i)
