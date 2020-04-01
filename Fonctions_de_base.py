import Initialisation
import numpy as np

'''
Liste les actions possibles à partir d'un état donné
@ state     Une liste de liste au format [[-,-,-],[-,-,-],[-,-,-]] avec les symboles correspondants
@ joueur    Le symbole correspondant au joueur (X/O)
@ return    Une liste de listes au format [[X/O , x , y],...] avec x,y les coordonnées du X/O que l'action ajoute

UNIT TEST FAIT
'''
#Cette méthode va retourner toutes les actions possibles à l'état state pour le joueur.
#On va donc retourner une liste de 19 entiers : l'indice de la liste correspond au numéro de colonne et 
#l'entier à cet indice correspond au numéro de ligne.
#On va parcourir la matrice colonne par colonne. On part du haut de chaque colonne et tant qu'on n'est pas
#tombé sur une case non vide, on continue à la ligne suivante. Lorsque l'on tombe sur une case non vide,
#On rentre le numéro de la ligne de la case au dessus.
def Action (state, joueur):
    liste_actions = []
    for i in range(nb_Colonne):
        for j in range (nb_Ligne):
            if(state[j][i] == 'X' or state[j][i] == 'O'):
                liste_actions.append(nb_Ligne-1)
                break
            #Si on a parcouru toutes les cases de la colonne et que toutes étaient vides, 
            #on ajoute le numéro de cette dernière ligne à la liste
            elif(j==nb_Ligne-1):
                liste_action.append(j)
    return liste_actions

'''
Applique l'action à l'état state, on procède avec la fonction .copy() pour ne pas modifier le state d'origine
@ state     Une liste de liste au format [[-,-,-],[-,-,-],[-,-,-]] avec les symboles correspondants
@ action    Liste [joueur,i,j] avec joueur : 'X' ou 'O'
@ return    Le nouveau state au format [[-,-,-],[-,-,-],[-,-,-]] avec les symboles correspondants

UNIT TEST FAIT
'''
def Result(state,action):
    resultat = []
    for liste in state:
        resultat.append(liste.copy())
    resultat[action[1]][action[2]]=action[0]
    return resultat

'''
Vérifie si l'état state est terminal
@ state     Un tableau 2D similaire à une liste de liste mais avec numpy ([[-,-,-,-,-,-],[-,-,-],[-,-,-]]) avec les symboles correspondants
@ nb        Le nombre de cases qui doivent être alignées pour finir
@ return    True/False
'''
def Terminal_Test(state,nb=6):
    nb_Ligne, nb_Colonne = np.shape(state) #Récupère les dimensions de la matrice avec numpy
    end_Game = False 
    empty_box = "." #Symbole de la case vide
    
    #CAS 1 : Visctoire d'un des joueurs
    #Test Sur les LIGNES && COLONNES
    for i in range(nb_Ligne):
        for j in range(nb_Colonne):
            if(state[i,j] != empty_box):
                #Test sur la ligne
                if(j+ nb <= nb_Colonne and (np.all(state[i, j:j+nb] == 'X') or np.all(state[i, j:j+nb] == 'O'))):
                    #Vérification de ne pas sortir de la matrice
                    #Si toute les valeurs de la liste =='X' or 'O' alors ...
                    #Slicing : sur la ligne i on prend les éléments de j à j+6 (j+6 exclu) donc 6 éléments
                    return True #end_Game = True et on le renvoie directement pr sortir de la méthode
               
                #Test sur la colonne
                if(i+nb <= nb_Colonne and (np.all(state[i:i+nb ,j] == 'X') or np.all(state[i:i+nb ,j] == 'O'))):
                    return True #end_Game = True
                
                #Test sur la Diagonale
                if(i+nb <= nb_Ligne and i+nb >= 0 and j+nb <= nb_Colonne): #On crée un carré de dimension i+nb x j+nb (ici 6x6)                 
                    #On ne regarde qu'à droite de la case car les diagonales sur la gauches seront testées à un autre moment avec leur somment donc en analysant vers la droite
                    #Diagnole montante/descendante vers la droite
                    cpt = 0 #Compteur du nombre de cases identiques
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
                    #On teste l'autre diagonale car pas de victoire
                    cpt=0 
                    end_Game = True 
                    #Diagonale descendante vers la droite
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

'''   Ancien code Pour le Morpion :

    reponse = False
    plein = True
    #si toutes les cases sont remplies, fini
    #si 3 croix/ronds sont alignés
    for element in state:
        for case in element:
            if(case != 'X' and case != 'O'): plein = False 
    if(not plein):
        #lignes
        for element in state :
            if (element == ['X','X','X'] or element == ['O','O','O']):
                reponse = True
        if(not reponse):
            #colonnes
            for i in range (len(state)):
                listetemp = []
                for j in range (len(state)):
                    listetemp.append(state[j][i])
                if (listetemp == ['X','X','X'] or listetemp == ['O','O','O']) :
                    reponse = True
            if(not reponse):
                #diagonales
                if((state[0][0] == state[1][1] and state[2][2] == state[1][1] and (state[1][1] == 'X' or state[1][1] == 'O')) or (state[1][1] == state[2][0] and state[2][0] == state[0][2] and (state[2][0] =='X' or state[2][0] =='O'))):
                    reponse = True
    else:
        reponse= True
    return reponse
'''

'''
Détermine l'intérêt d'un état
@ state     Une liste de liste au format [[-,-,-],[-,-,-],[-,-,-]] avec les symboles correspondants
@ joueur    Le symbole correspondant au joueur (X/O)
@ return    +1 pour une victoire, 0 pour une défaite, -1 pour une défaite

UNIT TEST FAIT
'''
def Utility (state, joueur):
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


#! Test unitaire pour vérifier le fonctionnement des méthodes
if __name__ == '__main__':
    mat = Initialisation.Plateau()
    #print(mat)
    
    mat.myMat[0] = ['O','X','O','O','O','O','O','X','X','O','X','X','O','O','X','X','X','X','X']
    print("Etat terminale de mat : ", Terminal_Test(mat.myMat))