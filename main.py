import os
import time

msg_init = ("""|----------------------------------------JOGO DE DETETIVE----------------------------------------|
    Assalto ao banco ocorrido durante a noite entre 12 PM e 2 AM, onde o alarme não foi 
    tocado e câmeras de segurança foram desligadas, descubra através das pistas quem 
    é o culpado pelo crime, baseando-se nos álibis dados pelos suspeitos do crime.
""")

msg_rules = ("""|-----------------------------------------REGRAS DO JOGO-----------------------------------------|
    -> O jogo possui até 4 etapas, cada qual será dada ao jogador um conjunto de hipoteses/pistas.
    -> As três etapas iniciais fornecem 4 pistas cada, a ultima etapa fornecerá as pistas restantes.
    -> Em cada etapa há a chance de se apontar o culpado ou passar para a próxima.
    -> Acertando o culpado o jogo acaba (valendo mais ou menos pontos de acordo com a etapa).
    -> Há 7 suspeitos no total, inicialmente todos são igualmente suspeitos.
    -> Partindo dos 7 suspeitos cada um apresentou álibis sobre o dia do incidente.
    -> Há um total de 24 pistas baseadas nos álibis obtidos.
    -> Ao escolher apontar um suspeito, todas suas pistas serao exibidas para auxilia-lo, porem se
        errar perderá 2 pontos possiveis.
    -> Ao pular para a próxima etapa, diminuirá 1 ponto possível.
    -> Apenas um dos suspeitos é o culpado.
""")

suspects = [
    "Nicola (Ni)",
    "Adam (Ad)",
    "Anastácia (An)",
    "Carolina (Ca)",
    "Lena (Le)",
    "Francesca (Fr)",
    "Lourenço (Lo)",
]

prop = {
    "Le-1":"Saiu mais cedo as 7:15 PM.",
    "Le-2":"Foi ao médico as 7:30 PM.",
    "Le-3":"Ligou para Carolina as 8:50 PM.",
    "Ni-1":"Fechou o banco as 8 PM.",
    "Ni-2":"Conferiu o quadro de luz apos a queda da luz.",
    "Ni-3":"Ligou o gerador de emergência.", 
    "Ad-1":"Verificou os ambientes internos.",
    "Ad-2":"Fez uma ronda no banco após a queda da luz.",
    "An-1":"Chegou 8 PM para a limpeza.",
    "An-2":"Viu todos os funcionários no banco.",
    "Fr-1":"Saiu junto de Lourenço as 8:20 PM.",
    "Lo-1":"Saiu junto de Francesca as 8:20 PM.",
    "Ca-1":"Documentou valores até 9 PM.",
    "Ca-2":"Trancou o cofre as 9 PM.",
    "Ca-3":"Documentou os valores e foi embora as 8:55 PM.",
    "CT"  :"O cofre estava trancado.",
    "NR"  :"Não houve roubo.",
    "Lu-1" :"A luz caiu entre 12 PM e 2 AM.",
    "Cv" :"Câmeras voltaram 30 min após ligar o gerador."
}

clues = [
    "(P1)  Se Lena Foi ao médico, então Lena saiu mais cedo as 7:15PM (Le-2 -> Le-1)",
    "(P2)  Se Anastácia chegou as 8 PM no banco, então Anastácia viu todos os funcionários (An-2 -> An-1)",
    "(P3)  Lena saiu mais cedo as 7:15 PM ou Anastácia chegou as 8 PM para limpeza (Le-1 v An-1)",
    "(P4)  Anastácia viu todos os funcionários (An-2)",
    
    "(P5)  Adam não verificou os ambientes internos.",
    "(P6)  Se Nicola fechou o banco, então Adam verificou os ambientes internos (Ni-1 -> Ad-1)",
    "(P7)  Se Francesca saiu, então Lourenço saiu com ele (Fr-1 -> Lo-1)",
    "(P8)  Francesca saiu as 8:20 PM (Fr-1)",
    
    "(P9)  Se o cofre estava trancado, então nao houve roubo (CT -> NR)",
    "(P10) Se Carolina documentou os valores ate 9 PM, então Carolina trancou o cofre 9PM (Ca-1 -> Ca-2)",
    "(P11) Nao houve roubo ou Carolina documentou os valores (Q-2 v Ca-1)",
    "(P12) Carolina documentou os valores (Ca-1)",
    
    "(P13) Se a luz caiu, então as câmeras desligaram (Lu-1 -> C1)",
    "(P14) A luz caiu entre 12 PM e 2 AM (Lu-1)",
    "(P15) Se a luz caiu, então Nicola verificou o quadro de luz (Lu-1 -> Ni-2)",
    "(P16) Se Nicola verificou o quadro de luz, então Nicola ligou o gerador de emergência (Ni-2 -> Ni-3)",

    "(P17) Se Nicola ligou o gerador de emergência, então as câmeras voltaram as 1 PM (Ni-3 -> Cv)",
    "(P19) Se Francesca estava com Lourenço, então ambos são inocentes (Fr-1 -> Lo-2)",
    "(P20) Se Nicola ligou o gerador de emergência, então Nicola é inocente. (Ni-3 -> Ni-4)",
    "(P21) Se Nicola é inocente, então Adam tambem é",
    
    "(P22) Se a luz caiu, então Anastácia foi para casa",
    "(P23) Se Anastácia foi para casa, então Anastácia é inocente",
    "(P24) Se Carolina documentou os valores, então Carolina é inocente",
]

solution = [
    ("""
    ----Dilema destrutivo----
        (Le-2 -> Le-1)
        (An-2 -> An-1)
        (~Le-1 v ~An-1)
        ---------------
        (~Le-2 v ~An-2)
    """),
    ("""
    ----Silogismo disjuntivo
        (~Le-2 v ~An-2)
        (An-2)
        ---------------
        ~Le-2
    """),
    ("""
    ----Dilema destrutivo
        (Q-1 -> Q-2)
        (Ca-1 -> Ca-2)
        (~Q-2 v ~Ca-2)
        ---------------
        (~Q-1 v ~Ca-1)
    """),
    ("""
    ----Silogismo disjuntivo
        (~Q-1 v ~Ca-1)
        (Ca-1)
        ---------------
        (~Q-1)
    """),
    ("""
    ----Modus ponens----
        (Ni-3 -> Cv)
        (Ni-3)
        ---------------
        (Cv)
    """)
]

my_clues = []
score = 20

def get_choice_game():
    choice = int(input("Digite [1] para continuar ou [0] para encerrar o programa: "))
    os.system("cls")
    if choice == 0:
        exit()
    elif choice < 0 or choice >= 2:
        print("Ops! Não é uma das opções!")
        get_choice_game()

def game_step_msg(step: int):
    print(f"|----------------------------------------ETAPA {step}----------------------------------------|")
    if 1 <= step <=5:
        print(f"As 4 pistas desta etapa estao em ordem cronológica, certifiquue-se de presetar atencao aos detalhes\n")
    else:
        print("ATENÇAO!! Ultima etapa para adivinhar o suspeito, encontre o culpado ou o mesmo saira impune")
        print("Estas sao as ultimas pistas para que voce resolva o caso, preste atencao aos detalhes\n")

def show_suspects():
    print("Os suspeitos atuais são:")
    for i in suspects:
        print("-> ",i)

def list_suspects():
    print('Os culpados listados por números são:')
    for i in suspects:
        print(f"({suspects.index(i)}) {i}")

def show_clues(max: int = 4):
    print("\nAs pistas desta etapa são:")
    # se len clues < 4
    # então
    #   len clues
    # senão
    #   max
    quantity = (len(clues) < 4 and len(clues)) or max
    for _ in range(quantity):
        item = clues[0]
        clues.remove(item)
        my_clues.append(item)
        print(f"{item}")

def indica_culpado(step: int):
    global score
    print("Suas pistas atá o momento são:")
    for i in my_clues:
        print(i)
    list_suspects()
    culpado = int(input("Insira o número do culpado: "))
    if suspects[culpado] == "Lena (Le)":
        os.system("cls")
        print("PARABÉNS VOCÊ ADIVINHOU QUEM É O RESPONSAVEL PELO CRIME!!!")
        print(f"GANHOU O JOGO NA ETAPA {step}, CONTABILIZANDO {score} PONTOS.")
        quit()
    elif step == 6:
        print("""Você não conseguiu adivinhar quem foi responsável pelo crime.
        Tente novamente ou finalize o jogo para ver a solução.""")
        choice = int(input("[1] para ver a solução ou [0] para finalizar: "))
        if choice == 1:
            for i in solution:
                print(i)
        else:
            quit()
    else:
        suspects.pop(culpado)
        print("-> Você errou o culpado, o indicado será removido da lista de suspeitos.")
        print("-> Passando para a proxima etapa, boa sorte...")
        score = score - 2
        time.sleep(3)
        os.system("cls")

def get_choice_sus(step: int):
    global score
    choice = -1

    if step <= 5:
        choice = int(input("Digite [1] para continuar ou [0] para indicar um suspeito: "))
        
        os.system("cls")
        if choice == 0:
            indica_culpado(step)

    elif step == 6:
        choice = int(input("Digite [1] para indicar um suspeito ou [0] para encerrar o programa: "))
        
        os.system("cls")
        if choice == 1:
            indica_culpado(step)

    if choice < 0 or choice >= 2:
        print("Ops! Não é uma das opções!")
        get_choice_sus()
    
    else:
        score = score - 1 

os.system("cls")

print(msg_init)
get_choice_game()
print(msg_rules)
get_choice_game()

for i in range(6):
    i += 1
    game_step_msg(i)
    show_suspects()
    show_clues()
    get_choice_sus(i)
