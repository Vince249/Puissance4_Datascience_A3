import AlphaBetaMiniMax
import Fonctions_de_base
import Initialisation
import MiniMax
import time
import os








os.system('clear')
print('Début de la nouvelle partie !')
humain = input('Choisissez votre symbole (X/O) \n')
if(humain == 'X') : ia = 'O'
if(humain == 'O') : ia = 'X'
plateau = Initialisation.Plateau()
first = input('Choisir qui commence (X/O) \n')
os.system('clear')
print(plateau)
check_partie_fini = False
while(not check_partie_fini):
    
    if(first == humain): #si l'humain joue en premier
        action = int(input('Humain, indique la colonne dans laquelle tu veux placer ton pion (0-18) \n'))
        os.system('clear')
        plateau = Fonctions_de_base.Result(plateau,action,humain)
        print(plateau)
        check_partie_fini = Fonctions_de_base.Terminal_Test(plateau)
        if(check_partie_fini) : break
        print("Au tour de l'IA !") 
        os.system('clear')
        print(plateau)


    #L'IA détermine son play ici
    #Pour l'instant c'est un autre humain qui joue

    action = int(input('IA, indique la colonne dans laquelle tu veux placer ton pion (0-18) \n'))
    os.system('clear')
    plateau = Fonctions_de_base.Result(plateau,action,ia)
    print(plateau)
    print("Au tour de l'humain !")
    os.system('clear')
    print(plateau)

    if(first == ia): #si l'ia joue en premier
        action = int(input('Humain, indique la colonne dans laquelle tu veux placer ton pion (0-18) \n X'))
        os.system('clear')
        plateau = Fonctions_de_base.Result(plateau,action,humain)
        os.system('clear')
        print(plateau)
        print("Au tour de l'IA !")
        os.system('clear')

print('La partie est terminée, bien joué à vous deux !')



