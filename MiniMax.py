import Fonctions_de_base

'''
Renvoie le meilleur play à faire suivant le state donné en considérant que l'adversaire va faire les plays optimum
Attention la fonction Utility est faite telle qu'on considère pouvoir étudier l'arbre en entier en sachant jusqu'où va nous mener chaque play

@ state     Une liste de liste au format [[-,-,-],[-,-,-],[-,-,-]] avec les symboles correspondants
@ joueur    Le symbole correspondant au joueur (X/O)
@ return    Une action optimale à faire par le joueur
'''
'''
def MiniMax(state, joueur):
    if(joueur == 'X') : opposant = 'O'
    if(joueur == 'O') : opposant = 'X'
    resultat = Max_Value(state,joueur,opposant,True)
    return resultat

'''
'''
Reflexion pour le tour de l'opposant, qui va prendre l'action qui a le gain minimum pour le joueur

@ state     Une liste de liste au format [[-,-,-],[-,-,-],[-,-,-]] avec les symboles correspondants
@ joueur    Le symbole correspondant au joueur (X/O)
@ opposant  Le symbole correspondant à l'adversaire (X/O)
@ return    La valeur de l'utility d'un état
'''
'''
def Min_Value(state, joueur,opposant):
    if(Fonctions_de_base.Terminal_Test(state)) : return Fonctions_de_base.Utility(state,joueur)
    #valeur infiniment haute
    v = 2
    #Ici ce sont les actions de l'opposant qu'on prend car c'est son tour
    for a in Fonctions_de_base.Action(state,opposant):
        v = min(v,Max_Value(Fonctions_de_base.Result(state,a),joueur,opposant))
    return v
'''

'''
Reflexion pour le tour du joueur, qui va prendre l'action qui a le gain maximum pour lui

@ state     Une liste de liste au format [[-,-,-],[-,-,-],[-,-,-]] avec les symboles correspondants
@ joueur    Le symbole correspondant au joueur (X/O)
@ opposant  Le symbole correspondant à l'adversaire (X/O)
@ return    La valeur de l'utility d'un état
'''

'''
def Max_Value(state, joueur, opposant, renvoyer_action = False):
    if(Fonctions_de_base.Terminal_Test(state)) : return Fonctions_de_base.Utility(state,joueur)
    #valeur infiniment basse
    v = -2
    if(renvoyer_action):
        sauvegarde_action = []
        #Ici ce sont les actions du joueur qu'on prend car c'est son tour
        for a in Fonctions_de_base.Action(state,joueur):
            ancien_v = v
            v = max(v,Min_Value(Fonctions_de_base.Result(state,a),joueur,opposant))
            if(ancien_v != v): sauvegarde_action=a
        return [v,sauvegarde_action]
    #Ici ce sont les actions du joueur qu'on prend car c'est son tour
    for a in Fonctions_de_base.Action(state,joueur):
        v = max(v,Min_Value(Fonctions_de_base.Result(state,a),joueur,opposant))
    return v
'''

def MiniMax_Decision(etat, player): #Pour l'ORDI
    #Retourne une action a effectué : Donc une valeurs de la liste possibilities

    if(player == 'X') : adv = 'O'
    if(player == 'O') : adv = 'X'
    list_act_Poss = Fonctions_de_base.Action(etat) #Liste des actions possibles à cet état
    depth = 0 #Profondeur actuelle
    depth_Max = 2 #Profondeur maximal, on n'étudie pas plus loin
    uti_Action_base = 0
    bonne_Action = []
    for a in list_act_Poss:
        uti_Action = Min_Value(Fonctions_de_base.Result(etat, a, player),player,adv, depth, depth_Max)
        if(uti_Action > uti_Action_base):#Car on veut utility maximale
            bonne_Action = a #Sauvegarde la meilleure actions
            uti_Action_base = uti_Action #MaJ de la meilleur uti
    
    return bonne_Action #Renvoie la meilleure action a effectuer
    
def Min_Value(etat, player, adv, depth, max_Depth):
    #C'est une fonction récursive
    #Player : Joueur qui veut gagner
    #adv = adversaire : joueur qui doit perdre
    #Condition d'arret
    if(Fonctions_de_base.Terminal_Test(etat) == True or depth == max_Depth):
        return Fonctions_de_base.Utility(etat, player, adv)
    else:
        list_act_Poss = Fonctions_de_base.Action(etat) #Liste des actions possibles à cet état
        valReturn = 100
        depth += 1
        for a in list_act_Poss:
            valReturn = min(valReturn, Max_Value(Fonctions_de_base.Result(etat, a, adv),player,adv, depth, max_Depth))
        
        return valReturn
    
                    
def Max_Value(etat, player, adv, depth, max_Depth):
    #C'est une fonction récursive
    #Condition d'arret
    if(Fonctions_de_base.Terminal_Test(etat) == True or depth == max_Depth):
        return Fonctions_de_base.Utility(etat, player, adv)
    else:
        list_act_Poss = Fonctions_de_base.Action(etat) #Liste des actions possibles à cet état
        valReturn = -100
        depth += 1
        for a in list_act_Poss:
            valReturn = max(valReturn, Min_Value(Fonctions_de_base.Result(etat, a, player),player, adv, depth, max_Depth)) 
        
        return valReturn