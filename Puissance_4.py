import AlphaBetaMiniMax
import Fonctions_de_base
import Initialisation
import time
from shutil import get_terminal_size #pour fonction clear

'''
fonction clear -> #? pratique car ça nous laisse la possibilité de voir l'historique des coups joués
'''
def clear():
    print("\n" * get_terminal_size().lines, end='')


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
            list_Actions = Fonctions_de_base.Action(plateau) #On recupere toutes les actions possibles
            print("Action(s) possible(s) : ", list_Actions)
            action = ""
            action_Autorise = False #Verification que ce coup est autorise
            while(action_Autorise == False): 
                action = Selection_colonne('\nHumain, indique la colonne dans laquelle tu veux placer ton pion (0-11) \n')
                if(action in list_Actions):
                    action_Autorise = True

            plateau = Fonctions_de_base.Result(plateau,action,humain)        
            #!Si la partie est finie, l'IA ne joue pas
            check_partie_fini = Fonctions_de_base.Terminal_Test(plateau)
            if(check_partie_fini) : break

        #! L'IA détermine son play ici
        print(plateau)
        list_Actions = Fonctions_de_base.Action(plateau) #On recupere toutes les actions possibles
        print("Action(s) possible(s) pour l'IA : ", list_Actions)


        action=AlphaBetaMiniMax.Alpha_Beta(plateau,ia)
        
        #action contient la value et l'action associée
        clear()
        print("L'IA joue : "+ str(action[1]))
        print()
        plateau = Fonctions_de_base.Result(plateau,action[1],ia)
        #!Si la partie est finie, l'humain ne joue pas
        check_partie_fini = Fonctions_de_base.Terminal_Test(plateau)
        if(check_partie_fini) : break

        if(first == ia): #Si l'IA joue en premier maintenant c'est le tour de l'Humain
            print(plateau)
            action = Selection_colonne('Humain, indique la colonne dans laquelle tu veux placer ton pion (0-11) \n')
            clear()
            plateau = Fonctions_de_base.Result(plateau,action,humain)
            #!Si la partie est finie, l'IA ne joue pas
            check_partie_fini = Fonctions_de_base.Terminal_Test(plateau)
            if(check_partie_fini) : break

    print(plateau)
    print('La partie est terminée, bien joué à vous deux !')



