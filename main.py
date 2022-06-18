import os
import time

msg_init = ("""|----------------------------------------JOGO DE DETETIVE----------------------------------------|
    Assalto ao banco ocorrido durante a noite entre 12 PM e 2 AM, onde o alarme não foi 
    tocado e câmeras de segurança foram desligadas, descubra através das pistas quem 
    é o culpado pelo crime, baseando-se nos álibis dados pelos suspeitos do crime.
""")

msg_rules = ("""|-----------------------------------------REGRAS DO JOGO-----------------------------------------|
    -> O jogo possui até 4 etapas, cada qual será dada ao jogador um conjunto de hipoteses/pistas.
    -> As etapas iniciais fornecem 4 pistas cada, a ultima etapa fornecerá as pistas restantes.
    -> Em cada etapa há a chance de se apontar o culpado ou passar para a próxima.
    -> Acertando o culpado o jogo acaba (valendo mais ou menos pontos de acordo com a etapa).
    -> Há 7 suspeitos no total, inicialmente todos são igualmente suspeitos.
    -> Partindo dos 7 suspeitos cada um apresentou álibis sobre o dia do incidente.
    -> Há um total de 24 pistas baseadas nos álibis obtidos.
    -> Ao escolher apontar um suspeito, todas suas pistas serão exibidas para auxiliá-lo, porém se
        errar perderá 2 pontos.
    -> Ao pular para a próxima etapa, diminuirá 1 ponto possível.
    -> Apenas um dos suspeitos é o culpado.
""")

suspects = [
    "Nicola",
    "Adam",
    "Anastácia",
    "Carolina",
    "Lena",
    "Francesca",
    "Lourenço",
]

clues = [
    "(P1)  Se Lena foi ao médico, então Lena saiu mais cedo as 7:15PM",
    "(P2)  Se Anastácia chegou as 8 PM no banco, então Anastácia viu todos os funcionários",
    "(P3)  Lena não saiu mais cedo as 7:15 PM ou Anastácia não chegou as 8 PM para limpeza",
    "(P4)  Anastácia viu todos os funcionários",
    
    "(P5)  Adam não verificou os ambientes internos",
    "(P6)  Se Nicola fechou o banco, então Adam verificou os ambientes internos",
    "(P7)  Se Francesca saiu, então Lourenço saiu com ele",
    "(P8)  Francesca saiu as 8:20 PM",
    
    "(P9)  Se o cofre estava trancado, então nao houve roubo",
    "(P10) Se Carolina documentou os valores ate 9 PM, então Carolina trancou o cofre 9PM",
    "(P11) Nao houve roubo ou Carolina documentou os valores",
    "(P12) Carolina documentou os valores",
    
    "(P13) Se a luz caiu, então as câmeras desligaram",
    "(P14) A luz caiu entre 12 PM e 2 AM",
    "(P15) Se a luz caiu, então Nicola verificou o quadro de luz",
    "(P16) Se Nicola verificou o quadro de luz, então Nicola ligou o gerador de emergência",

    "(P17) Se Nicola ligou o gerador de emergência, então as câmeras voltaram as 1 PM",
    "(P18) Se Francesca estava com Lourenço, então ambos são inocentes",
    "(P19) Se Nicola ligou o gerador de emergência, então Nicola é inocente",
    "(P20) Se Nicola é inocente, então Adam tambem é",
    
    "(P21) Se a luz caiu, então Anastácia foi para casa as 2 AM",
    "(P22) Se Anastácia foi para casa, então Anastácia é inocente",
    "(P23) Se Carolina documentou os valores, então Carolina é inocente",
    "(P24) Se Lena é inocente, então Lena foi ao médico",
]

solution = [
    "(P25) An-1          | MP[P2-P4]",
    "(P26) ~An-1 v ~Le-1 | COMT[P3]",
    "(P27) An-1 -> ~Le-1 | CONT-I[P26]",
    "(P28) ~Le-1         | MP[P27-P25]",
    "(P29) ~Le-2         | MT[P1-P28]",
    "* (P30) ~ILe         | MT[P24-P29] *",
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
        print("ATENÇÃO!! Última etapa para adivinhar o suspeito, encontre o culpado ou o mesmo sairá impune")
        print("Essas sao as últimas pistas para que você resolva o caso, preste atenção aos detalhes!\n")

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
    print("Suas pistas até o momento são:")
    for i in my_clues:
        print(i)
    list_suspects()
    culpado = int(input("Insira o número do culpado: "))
    if suspects[culpado] == "Lena":
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
