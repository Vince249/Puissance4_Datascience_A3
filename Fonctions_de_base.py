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
    result = Initialisation.Plateau()
    result.myMat = copy.deepcopy(state.myMat) #Copie de state en deepcopy donc changement de result ne change pas state
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
    
    #CAS 1 : Victoire d'un des joueurs
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
@ state     Tableau multi-dimensionnel
@ joueur    Le symbole correspondant au joueur voulant gagner (X/O)
@ opposant  Le symbole correspondant au joueur voulant perdre (X/O)
@ return    Valeur de l'état pour positive_Player
*Inspiration site_Web (fin de la page): https://www.christian-schmidt.fr/puissance4

#! Cette heuristique s'appuie sur le nombre de coup gagnant dans lequel chaque position peut être impliquée
#! Elle fonctionne pour un plateau normal de puissance 4 mais pas pour le nôtre car les dimensions sont trop grandes
#! Il n'y a pas assez de différence entre les values des différents plays
'''
def Utility_Armand (state, joueur, opposant):

    '''
    mat_Reference = np.array([[3,4,5,7,7,7,7,7,7,5,4,3],
                              [4,6,8,10,10,10,10,10,10,8,6,4],
                              [5,8,11,13,13,13,13,13,13,11,8,5],
                              [5,8,11,13,13,13,13,13,13,11,8,5],
                              [4,6,8,10,10,10,10,10,10,8,6,4],
                              [3,4,5,7,7,7,7,7,7,5,4,3]])
    '''
    
    mat_Reference = np.array([[3,4,5,7,8,10,10,8,7,5,4,3],
                            [4,6,8,10,11,12,12,11,10,8,6,4],
                            [5,8,11,13,14,16,16,14,13,11,8,5],
                            [5,8,11,13,14,16,16,14,13,11,8,5],
                            [4,6,8,10,11,12,12,11,10,8,6,4],
                            [3,4,5,7,8,10,10,8,7,5,4,3]])

    result = 0
    for i in range(state.size_Ligne):
        for j in range(state.size_Colonne):
            if(state[i,j] == joueur):
                result += mat_Reference[i,j]
            elif(state[i,j] == opposant ):
                result -= mat_Reference[i,j]


    ''' Ajout de BONUS :
    * Defaite : -50
    * Victoire : +50
    '''
    nb_Ligne, nb_Colonne = np.shape(state.myMat) #Récupère les dimensions de la matrice avec numpy
    end_Game = False 
    empty_box = "." #Symbole de la case vide
    nb= 4 #Nombre de case necessaire a une victoire
    bonus_Win = 50
    bonus_Lose = -50
    
    #CAS : Victoire d'un des joueurs
    #Test Sur les LIGNES && COLONNES && DIAGONALES
    for i in range(nb_Ligne):
        for j in range(nb_Colonne):
            if(state[i,j] != empty_box):
                #Test sur la ligne
                if(j+ nb <= nb_Colonne and (np.all(state[i, j:j+nb] == 'X') or np.all(state[i, j:j+nb] == 'O'))):
                    #On est dans un cas de victoire
                    if(state[i,j] == joueur):
                        result += bonus_Win
                    if(state[i,j] == opposant):
                        result += bonus_Lose    
                    end_Game = True                
                    break
               
                #Test sur la colonne 
                if(i+nb <= nb_Ligne and (np.all(state[i:i+nb ,j] == 'X') or np.all(state[i:i+nb ,j] == 'O'))):
                    #On est dans un cas de victoire
                    if(state[i,j] == joueur):
                        result += bonus_Win
                    if(state[i,j] == opposant):
                        result += bonus_Lose
                    end_Game = True
                    break
                
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
                        #On est dans un cas de victoire
                        if(state[i,j] == joueur):
                            result += bonus_Win
                        if(state[i,j] == opposant):
                            result += bonus_Lose
                        end_Game = True
                        break
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
                        #On est dans un cas de victoire
                        if(state[i,j] == joueur):
                            result += bonus_Win
                        if(state[i,j] == opposant):
                            result += bonus_Lose
                        end_Game = True
                        break                        

    
    return result


def Combinaisons_potentielle_win(state,joueur,opposant,i,j):
    
    result = 0
    dico = {
        0 : [], #pos_column_up
        1 : [], #'val_column_up'

        2 : [], #'pos_diag_up_right'
        3 : [], #'val_diag_up_right'

        4 : [], #'pos_side_right'
        5 : [], #'val_side_right'

        6 : [], #'pos_diag_bot_right'
        7 : [], #'val_diag_bot_right'

        8 : [], #'pos_diag_bot_left'
        9 : [],#'val_diag_bot_left'

        10 : [], #'pos_side_left'
        11 : [], #'val_side_left'

        12 : [], #'pos_diag_up_left'
        13 : [], #'val_diag_up_left'
        
        
        # 'val_column_bot' : [], inutile car on ne peut pas gagner en mettant des pions en bas
        # 'pos_column_bot' : [], inutile car on ne peut pas gagner en mettant des pions en bas
        
    }
    


    for w in range(0,4): #On regarde les lignes au dessus

        if(i>=3): # Place en haut
            #* colonne up
            dico[1].append(state[i-w,j])
            dico[0].append([i-w,j])

            
            #* Check diagonale gauche haut
            if(j>=3): # Place à gauche
                dico[13].append(state[i-w,j-w])
                dico[12].append([i-w,j-w])


            #* Check diagonale droit haut
            if(j<=8): # Place à droite
                dico[3].append(state[i-w,j+w])
                dico[2].append([i-w,j+w])
        
        

        if(j>=3): # Place à gauche
            #* side left
            dico[11].append(state[i,j-w])
            dico[10].append([i,j-w])

            
            #* Check diagonale gauche bas
            if(i<=2): # Place en bas
                dico[9].append(state[i+w,j-w])
                dico[8].append([i+w,j-w])

        if(j<=8): # Place à droite
            #* side right
            dico[5].append(state[i,j+w])
            dico[4].append([i,j+w])

            
            #* Check diagonale droite bas
            if(i<=2): # Place en bas
                dico[7].append(state[i+w,j+w])
                dico[6].append([i+w,j+w])

    for y in range(0,13,2):
        if(opposant not in dico[y+1] and len(dico[y+1]) != 0 ): #Si l'adversaire n'est pas présent
            compteur = dico[y+1].count(joueur)
            distance = 0
            for i in range(4) :
                if(dico[y+1][i]=='.' and y != 0): #on regarde pas la distance pour la colonne
                    distance += Gravity(state,dico[y][i][1])- dico[y][i][0]

            result += (compteur**2)/(distance+1) 
            if(compteur ==4): result += 10000
    
    return result


def Utility_Vincent_Remi(state,joueur,opposant):

    result = 0
    for i in range(state.size_Ligne):
        for j in range(state.size_Colonne):
            if(state[i,j] == joueur):
                result += Combinaisons_potentielle_win (state,joueur,opposant,i,j)
            elif(state[i,j] == opposant ):
                result -= Combinaisons_potentielle_win (state,opposant,joueur,i,j)

    return result


            
            

