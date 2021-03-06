import random
import json
import os.path
insperdex=[]

def load():                                 #Carrega o dicionário de Inspermons
    
    with open('inspermons.json') as pd:    
        lista_p = json.load(pd)
    return lista_p

def encontra_r(lista_p):                    #Encontra o rival
    rival=dict(random.choice(lista_p))
    return rival

def CalculaBatalha (pokj,lista_p):          #Função principal da batalha
    rival=encontra_r(lista_p)
    rivalb=dict(rival)
    fugir=[1]*6+[0]*4                      #Lista para adicionar falha na fuga
    sorte=[0,7]+[0,8]*2+[0,9]*3+[1]*4+[1,1]*3+[1,2]*2+[1,3]
    
    print("Você encontrou um {0}".format(rival['nome']))
    if rival not in insperdex:              #Verifica se Inspèrmon está no Insperder
        insperdex.append(rival)             #Adiciona o novo Inspermon à Insperder
    
    
    while pokj["vida"] > 0 and rival["vida"] > 0:#Inicio do loop principal da 
        print("""Vida do seu {0}:{2}
Vida do rival {1}:{3}              
""".format(pokj["nome"],rival["nome"],pokj["vida"],rival["vida"]))
        bat=int(input("""(1) Atacar
(2) Fugir"""))
        
        if bat==2:
            if random.choice(fugir):        #Acessa lista aleatóriamente,                                            
                print("Fuga com sucesso")   #dando 40% de chance de falha na fuga
                return (1,pokj)
            else:
                print("Falha na fuga, batalha continua!")
                
        rival["vida"] = rival["vida"] - ( pokj["poder"] - rival["defesa"] )*random.choice(sorte) #Ataque do jogador com fator sorte
        if rival["vida"] <= 0:
            print("Seu Inspèrmon ganhou")
            pokj["exp"]=pokj["exp"]+rivalb["vida"]*0.25
            print("""Experiência ganha:+{0}
Experiência Total:{1}/{2}""".format(rivalb["vida"]*0.25,pokj["exp"],int(pokj["vida"]*2)))
            if pokj["exp"]>pokj["vida"]*1.1:   #Evolução do Inspermon do jogador
                print("""O SEU POKEMON EVOLUIU!
Atributos ganhos:
Vida: +{0} -> {3}
Poder: +{1} -> {4}
Defesa: +{2} -> {5}
""".format(int(pokj["vida"]*0.1),int(pokj["poder"]*0.1),int(pokj["defesa"]*0.1),int(pokj["vida"]*1.1),int(pokj["poder"]*1.1),int(pokj["defesa"]*1.1)))
                pokj["vida"]=int(pokj["vida"]*1.1)
                pokj["poder"]=int(pokj["poder"]*1.1)
                pokj["defesa"]=int(pokj["defesa"]*1.1)
                pokj["nivel"]+=1
            return (1,pokj)
            
        pokj["vida"] = pokj["vida"] - ( rival["poder"] - pokj["defesa"] )*random.choice(sorte)  #Ataque do rival com fator sorte
        if pokj["vida"] <= 0:
            print("Seu Inspèrmon perdeu! Game over :( ")
            os.remove("data.txt")
            return (0,pokj)
        
############################
#Inicio do código principal#
lista_p=load()
  
op=int(input ("""(1)Novo Jogo
(2)Carregar Jogo Salvo
Ação:"""))
verifica=1
while verifica:
    if op==1:  
        print("Escolha um Inspèrmon:")
        for i in range(len(lista_p)):
            print("({0}) {1}".format(i+1, lista_p[i]["nome"]))
        pokn=int(input())-1
        pokj=dict(lista_p[pokn])                       #-1 pois no menu foi adicionado +1 na escolha
        pokj["nivel"]=1
        pokj["exp"]=0
        pokj["pokn"]=pokn
        verifica=0
    else:    
        if os.path.exists('data.txt'):
            with open('data.txt', 'r') as arquivo:
                pokj=json.load(arquivo)
                
            print("""Jogo Carregado...
            Nome:{0}
            Vida:{1}
            Poder:{2}
            Defesa:{3}
            Experiência:{5}
            Nível:{4}""".format(pokj["nome"],pokj["vida"],pokj["poder"],pokj["defesa"],pokj["nivel"],pokj["exp"]))
            verifica=0
        else:
            print("Erro, save não encontrado")
            op=1
        
        
pokn=pokj["pokn"]     
loop=1    
while loop:
    
    with open('data.txt', 'w') as arquivo:
        json.dump({'nome':pokj["nome"], 'vida':pokj["vida"], 'poder':pokj["poder"], 'defesa':pokj["defesa"], 'nivel':pokj["nivel"], 'exp':pokj["exp"], 'pokn':pokn}, arquivo, indent=4)
    
    
    acao=int(input("""MENU:
 (1) Acessar o Insperdex
 (2) Passear
 (3) Status
 (4) Acessar Centro Inspèrmon
 (5) Dormir
"""))
        
    if acao==1:
        print("Inspèrmons encontrados:")
        for i in range(len(insperdex)):     #Imprime o Insperdex
            print(insperdex[i]['nome'])
                
    elif acao==2:
        y=CalculaBatalha(pokj,lista_p)
        loop=y[0]
        pokj=y[1]        

    elif acao==5:
        print("Boa Noite !")                 
        loop=0                              #Encerra o jogo
        
    elif acao==3:
        print("""Status do seu Inspèrmon:
Nome:{0}
Vida:{1}
Poder:{2}
Defesa:{3}
Experiência:{5}
Nível:{4}""".format(pokj["nome"],pokj["vida"],pokj["poder"],pokj["defesa"],pokj["nivel"],pokj["exp"]))
            
    elif acao==4:
        pokj["vida"]=lista_p[pokn]["vida"]
        for i in range(pokj["nivel"]-1):
            pokj["vida"]=pokj["vida"]+pokj["vida"]*0.1                        
        print("A vida do seu Inspèrmon foi recuperada")
        
    else:
        print("Opção inválida")
        

