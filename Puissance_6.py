import AlphaBetaMiniMax
import Fonctions_de_base
import Initialisation
import MiniMax
import time
from os import system, name #pour fonction clear_bis
from shutil import get_terminal_size #pour fonction clear

'''
fonction clear -> #? Sur MAC la fonction clear2 me fait de la merde, celle-ci semble mieux, elle fait juste plein de sauts à la ligne
                  #? (ça nous laisse la possibilité de voir l'historique des commandes aussi)
'''
def clear():
    print("\n" * get_terminal_size().lines, end='')

'''
fonction clear --> #? Cette fonction me fait un affichage degueu, à vous de me dire ce que ça donne sur Windows mais perso j'aime pas
'''
def clear_bis(): 
    if name == 'nt': _ = system('cls') #for windows 
    else: _ = system('clear') #for mac and linux

'''
fonction pour définir la valeur d'action --> évite les erreurs de types ou valeur impossible
#* uniquement destiné à rendre le main plus lisible et épuré
'''
def Selection_colonne(phrase):
    action=-1
    dim_Colonne = 12
    while True:
        try:
            action = int(input(phrase))
            if (action >= 0 and action <= dim_Colonne) : break
        except ValueError:
            print("Erreur : type de l'input")
    return action


if __name__ == '__main__': 
    #! Début du code
    clear()
    print('Début de la nouvelle partie !')

    #Choix symbole
    while True: #*on répète jusqu'à ce qu'un des deux symbole soit choisi
        humain = input('Choisissez votre symbole (X/O) \n')
        if(humain == 'X') : 
            ia = 'O'
            break
        if(humain == 'O') : 
            ia = 'X'
            break
        clear()

    #Choix commencement
    while True: #*on répète jusqu'à ce qu'un des deux symbole soit choisi
        first = input('Choisir qui commence (X/O) \n')
        if(first == 'X') : break
        if(first == 'O') : break
        clear()

    plateau = Initialisation.Plateau()
    check_partie_fini = False
    while(not check_partie_fini):
        
        if(first == humain): #Si l'humain joue en premier
            print(plateau)
            action = Selection_colonne('Humain, indique la colonne dans laquelle tu veux placer ton pion (0-11) \n')
            plateau = Fonctions_de_base.Result(plateau,action,humain)        
            #!Si la partie est finie, l'IA ne joue pas
            check_partie_fini = Fonctions_de_base.Terminal_Test(plateau)
            if(check_partie_fini) : break

        #L'IA détermine son play ici (pour l'instant c'est un autre humain qui joue)
        print(plateau)
        action = Selection_colonne('IA, indique la colonne dans laquelle tu veux placer ton pion (0-11) \n')
        clear()
        plateau = Fonctions_de_base.Result(plateau,action,ia)
        #!Si la partie est finie, l'humain ne joue pas
        check_partie_fini = Fonctions_de_base.Terminal_Test(plateau)
        if(check_partie_fini) : break

        if(first == ia): #Si l'IA joue en premier
            print(plateau)
            action = Selection_colonne('Humain, indique la colonne dans laquelle tu veux placer ton pion (0-11) \n')
            clear()
            plateau = Fonctions_de_base.Result(plateau,action,humain)
            #!Si la partie est finie, l'IA ne joue pas
            check_partie_fini = Fonctions_de_base.Terminal_Test(plateau)
            if(check_partie_fini) : break

    print(plateau)
    print('La partie est terminée, bien joué à vous deux !')



