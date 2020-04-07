import Fonctions_de_base


def MiniMax_Decision(etat, player): #Pour l'ORDI
    #Retourne une action à effectuer : Donc une valeurs de la liste possibilities

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