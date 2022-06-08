"""
    Assalto ao banco ocorrido durante a noite entre 8 PM e 5 AM, onde o alarme não foi 
    tocado e câmeras de segurança foram desligadas, descubra através das pistas quem 
    é o culpado pelo crime, baseando-se nos álibis dados pelos suspeitos do crime.
    
    # --------
    
    Suspeitos:
        - Guarda 1;
        - Guarda 2;
        - Zelador;
        - Gerente do banco;
        - Atendente 1;
        - Atendente 2;
        - Atendente 3;
    Culpado:
        - Atendente 1;
    
    # --------
    Hipótese/Álibis:
        - A1: Saiu mais cedo às 7:15 PM devido a um compromisso.
        * A1: Foi a uma consulta médica as 7:30 PM.
        - G1: Fechou o banco as 8 PM.
        - G2: Enquanto G1 fechava o banco, G2 verificava os ambientes internos.
        - Z : Chegou ao fechamento 8 PM para começar a limpeza, afirma não ter visto nada
                de estranho e nenhum desconhecido no banco.
        - A2: Saiu as 8:20 PM, junto do A3.
        - A3: Saiu as 8:20 PM, junto do A2.
        - GB: Documentou valores do cofre até as 9 PM.
        - GB: Trancou o cofre as 9 PM.
        - G1: Foi conferir o cofre as 10:15 PM.
        - Z : Foi limpar a região do cofre as 10:20 PM.
        - P1: Os dois afirmam não ter encontrado ninguém.
        - P2: A1 não apresentou atestado no outro dia.
        - P3: A2 e A3 chegaram 1h atrasados no dia seguinte.
        - A2: Não se lembra daquela noite após o trabalho.
        - A3: Informou que ele/a e A2 foram em uma festa de um conhecido e beberam.
        - P4: Caiu a luz da região das 12 PM as 2 AM.
        - G1: Foi conferir o quadro de luz depois da queda.
        - G1: Ligou o gerador reserva as 12:30 PM, e as câmeras voltaram 30 min depois.
        - G2: Depois da queda de luz foi fazer uma ronda no banco.
        - Z : Foi para casa após a volta da energia às 2 AM.
        - G2: Desligou o gerador.
"""

import json
import os

msg_init = ("""|----------------------------------------JOGO DE DETETIVE----------------------------------------|
    Assalto ao banco ocorrido durante a noite entre 8 PM e 5 AM, onde o alarme não foi 
    tocado e câmeras de segurança foram desligadas, descubra através das pistas quem 
    é o culpado pelo crime, baseando-se nos álibis dados pelos suspeitos do crime.
""")

msg_rules = ("""|-----------------------------------------REGRAS DO JOGO-----------------------------------------|
    -> O jogo possuí até 4 etapas, cada qual será dada ao jogador um conjunto de hipoteses/pistas
    -> Em cada etapa há a chance de se apontar o culpado ou passar para a próxima
    -> Acertando o culpado o jogo acaba (valendo mais ou menos pontos de acordo com a etapa)
    -> Errando o culpado serão retiradas 2 pistas da etapa seguinte
    -> Há 7 suspeitos total, inicialmente todos são igualmente suspeitos
    -> Partindo dos 7 suspeitos cada um apresentou álibis sobre o dia do incidente
    -> Há um total de 22 proposições baseadas nos álibis obtidos
    -> Apenas um dos suspeitos é o culpado.
""")

suspects = (
    "Guarda 1",
    "Guarda 2",
    "Zelador",
    "Gerente do banco",
    "Atendente 1",
    "Atendente 2",
    "Atendente 3",
)

propos: tuple[dict[str, float]] = (
    {"text": f"{suspects[4]}: Saiu mais cedo às 7:15 PM devido a um compromisso.", "time": 7.15},
    {"text": f"{suspects[4]}: Foi a uma consulta médica as 7:30 PM.", "time": 7.3},
    {"text": f"{suspects[0]}: Fechou o banco as 8 PM.", "time": 8},
    {"text": f"{suspects[1]}: Enquanto {suspects[0]} fechava o banco, {suspects[1]} verificava os ambientes internos.", "time": 8},
    {"text": f"{suspects[2]}: Chegou ao fechamento 8 PM para começar a limpeza, afirma não ter visto nada de estranho e nenhum desconhecido no banco.", "time": 8},
    {"text": f"{suspects[5]}: Saiu as 8:20 PM, junto do A3.", "time": 8.2},
    {"text": f"{suspects[6]}: Saiu as 8:20 PM, junto do {suspects[5]}.", "time": 8.2},
    {"text": f"{suspects[3]}: Documentou valores do cofre até as 9 PM.", "time": 9},
    {"text": f"{suspects[3]}: Trancou o cofre as 9 PM.", "time": 9},
    {"text": f"{suspects[0]}: Foi conferir o cofre as 10:15 PM.", "time": 10.15},
    {"text": f"{suspects[2]}: Foi limpar a região do cofre as 10:20 PM.", "time": 10.20},
    {"text": f"P1: Os dois afirmam não ter encontrado ninguém.", "time": 10.20},
    {"text": f"P2: {suspects[4]} não apresentou atestado no outro dia.", "time": -1},
    {"text": f"P3: {suspects[5]} e {suspects[6]} chegaram 1h atrasados no dia seguinte.", "time": -1},
    {"text": f"{suspects[5]}: Não se lembra daquela noite após o trabalho.", "time": -1},
    {"text": f"{suspects[6]}: Informou que ele/a e {suspects[5]} foram em uma festa de um conhecido e beberam.", "time": -1},
    {"text": f"P4: Caiu a luz da região das 12 PM as 2 AM.", "time": 12},
    {"text": f"{suspects[0]}: Foi conferir o quadro de luz depois da queda.", "time": 12},
    {"text": f"{suspects[1]}: Depois da queda de luz foi fazer uma ronda no banco.", "time": 12},
    {"text": f"{suspects[0]}: Ligou o gerador reserva as 12:30 PM, e as câmeras voltaram 30 min depois.", "time": 12.3},
    {"text": f"{suspects[2]}: Foi para casa após a volta da energia às 2 AM.", "time": 12+2},
    {"text": f"{suspects[1]}: Desligou o gerador depois da volta da energia.", "time": 12+2},
)
print(msg_init)
choice = str(input("Digite [Y] para continuar ou [N] para fechar o programa:"))
if choice.capitalize() != ('Y'):
    os.system("cls")
    exit()

os.system("cls")
print(msg_rules)
choice = str(input("Digite [Y] para continuar ou [N] para fechar o programa:"))
if choice.capitalize() != ('Y'):
    os.system("cls")
    exit()
os.system("cls")
print("Os suspeitos do crime são:")
for i in suspects:
    print("->" ,i)
