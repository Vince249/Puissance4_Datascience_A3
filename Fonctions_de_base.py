import Initialisation
import numpy as np
import copy


'''
Cette méthode va renvoyer la liste des colonnes dans lesquelles on peut encore jouer.
On a donc besoin de juste parcourir la première ligne de la matrice : 
   * si la case de la colonne est vide, alors on peut jouer dans cette colonne
   * sinon, on ne peut pas jouer dedans car la colonne est remplie.
'''
def Action (state):
    liste_actions = []
    ligne=0
    for j in range (state.size_Colonne):
        #On ne regarde que la case au sommet du plateau de jeu car si elle n'est pas remplie alors il est possible d'y joueur au-moins une fois
        if(state[ligne,j] != 'X' and state[ligne,j] != 'O'):
            liste_actions.append(j)
            
    return liste_actions

'''
Applique l'action à l'état state, on procède avec la fonction .copy() pour ne pas modifier le state d'origine
@ state     Une liste de liste au format d'un tabelau multi-dimensionnel avec les symboles correspondants
@ action    Colonne dans laquelle placer le symbole
@ return    Le nouveau state avec les symboles correspondants
'''
def Result(state,action,joueur):
    '''
    Liens : https://www.science-emergence.com/Articles/Copier-une-matrice-avec-numpy-de-python/
    #! Importer copy : import copy
    #! On utilise une deepcopy
    *Si on modifie la matrice y alors x n'est pas modifiée
    '''
    result = copy.deepcopy(state) #Copie de state en deepcopy donc changement de result ne change pas state
    #Result est un tableau multi-dimensionnel donc utiliser la librairie numpy
    #! Méthode de gravité qui renvoie x : valeur de la ligne
    
    column = action 
    row = Gravity(result, column)
    if(row ==-1) : return "ERREUR Votre play n'est pas valide"
    result[row, column] = joueur#On affecte la valeur de joueur à la case correspondante
    return result



'''
Fonction gravité pour une colonne, elle return la ligne à laquelle on peut placer un symbole
@state      tableau multi-dimensionnel
@column     valeur de la colonne à analyser
@return     retourne la valeur x de la ligne libre ou -1 s'il n'y en a pas
'''
def Gravity(state, column):

    for i in range(state.size_Ligne-1,-1,-1): #De 5 à 0
        if(state[i,column]=='.') : return i
    return -1


'''
Vérifie si l'état state est terminal
@ state     Un tableau 2D similaire à une liste de liste mais avec numpy avec les symboles correspondants
@ nb        Le nombre de cases qui doivent être alignées pour finir
@ return    True si l'état est terminal/False sinon
'''
def Terminal_Test(plateau,nb=4):
    state = plateau.myMat
    nb_Ligne, nb_Colonne = np.shape(state) #Récupère les dimensions de la matrice avec numpy
    end_Game = False 
    empty_box = "." #Symbole de la case vide
    
    #CAS 1 : Visctoire d'un des joueurs
    #Test Sur les LIGNES && COLONNES && DIAGONALES
    for i in range(nb_Ligne):
        for j in range(nb_Colonne):
            if(state[i,j] != empty_box):
                #Test sur la ligne
                if(j+ nb <= nb_Colonne and (np.all(state[i, j:j+nb] == 'X') or np.all(state[i, j:j+nb] == 'O'))):
                    #Vérification de ne pas sortir de la matrice
                    #Si toute les valeurs de la liste =='X' or 'O' alors ...
                    #Slicing : sur la ligne i on prend les éléments de j à j+4 (j+4 exclu) donc 4 éléments
                    return True #end_Game = True et on le renvoie directement pr sortir de la méthode
               
                #Test sur la colonne 
                if(i+nb <= nb_Ligne and (np.all(state[i:i+nb ,j] == 'X') or np.all(state[i:i+nb ,j] == 'O'))):
                    return True #end_Game = True
                
                #Diagonale descendante vers la droite
                if(i+nb <= nb_Ligne and j+nb <= nb_Colonne): #On crée un carré de dimension i+nb x j+nb (ici 4x4)                 
                    #On ne regarde qu'à droite de la case car les diagonales sur la gauches seront testées à un autre moment avec leur somment donc en analysant vers la droite
                    cpt = 1 #Compteur du nombre de cases identiques : La PREMIERE case est déjà comptabilisée
                    add = 1 #Variation de la ligne t de la colonne
                    end_Game=True
                    while(cpt < nb and end_Game==True):
                        if(state[i+add, j+add] != state[i,j]): #Une case sur la diago est != de la case d'origine => On arrete
                            end_Game = False
                            break
                        else:
                            cpt+=1
                            add+=1
                    if(cpt==nb):
                        return True #Un joueur a gagné
                #Diagonale montante vers la droite
                if(i-nb >= 0 and j+nb <= nb_Colonne):
                    cpt= 1 #La PREMIERE case est déjà comptabilisée
                    add = 1
                    end_Game = True 
                    #Diagonale montante vers la droite
                    while(cpt < nb and end_Game==True):
                        if(state[i-add, j+add] != state[i,j]): #Une case sur la diago est != de la case d'origine => On arrete
                            end_Game = False
                            break
                        else:
                            cpt+=1
                            add+=1
                    if(cpt==nb):
                        return True #Un joueur a gagné                        

    #CAS 2 : Jeu plein
    end_Game = True
    if(np.any(state[0, : ] == empty_box)): #Si au moins une case de la ligne du sommet == "."
        end_Game = False #Au moins une case est vide donc la matrice n'est pas pleine
    return end_Game


'''
Détermine l'intérêt d'un état
@ state     Une liste de liste au format [[-,-,-],[-,-,-],[-,-,-]] avec les symboles correspondants
@ joueur    Le symbole correspondant au joueur (X/O)
@ return    +1 pour une victoire, 0 pour une défaite, -1 pour une défaite

UNIT TEST FAIT
'''
def Utility_OLD (state, joueur):
    #ligne
    result = 0
    for element in state :
        if(element[0]==element[1] and element[2]==element[1]):
            if(element[0] == joueur):
                result = 1
            else:
                result = -1
    #colonne
    for i in range (len(state)):
        listetemp = []
        for j in range (len(state)):
            listetemp.append(state[j][i])
        if(listetemp[0]==listetemp[1] and listetemp[2]==listetemp[1]):
            if(listetemp[0] == joueur):
                result = 1
            else:
                result = -1
    #diagonale

    if((state[0][0] == state[1][1] and state[2][2] == state[1][1] ) or (state[1][1] == state[2][0] and state[2][0] == state[0][2])):
        if(state[1][1] == joueur):
            result = 1
        else:
            result = -1

    return result

'''
Détermine l'intérêt d'un état
@ state     Tableau multi-dimensionnel
@ joueur    Le symbole correspondant au joueur voulant gagner (X/O)
@ opposant  Le symbole correspondant au joueur voulant perdre (X/O)
@ return    Valeur de l'état pour positive_Player
*Inspiration site_Web (fin de la page): https://www.christian-schmidt.fr/puissance4
'''
def Utility (state, joueur, opposant):
    mat_Reference = np.array([[3,4,5,7,7,7,7,7,7,5,4,3],
                              [4,6,8,10,10,10,10,10,10,8,6,4],
                              [5,8,11,13,13,13,13,13,13,11,8,5],
                              [5,8,11,13,13,13,13,13,13,11,8,5],
                              [4,6,8,10,10,10,10,10,10,8,6,4],
                              [3,4,5,7,7,7,7,7,7,5,4,3]])

    result = 0
    for i in range(state.size_Ligne):
        for j in range(state.size_Colonne):
            if(state[i,j] == joueur):
                result += mat_Reference[i,j]
            elif(state[i,j] == opposant ):
                result -= mat_Reference[i,j]
    return result
