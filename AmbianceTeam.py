# -*- coding: utf-8 -*-
import re
#from poooc import order, state, state_on_update, etime
import poooc




# Définition de la classe Cellule
class Cellule:
    
    
    # Fonction d'initialisation
    def __init__(self,idcell,offsize,defsize,radius,x,y,prod=0,nboff=0,nbdef=0,couleur=-1,voisinsAlly = [], voisinsEnem = [], voisinsNeut = []): #-1 pour le neutre
        
        self.idcell = idcell                      # Initialisation de l'id de la cellule Type : entier
        self.offsize = offsize                    # Initialisation de la capacité offensive de la cellule Type : entier
        self.defsize = defsize                    # Initialisation de la capacité défensive de la cellule Type : entier
        self.radius = radius                      # Initialisation du rayon de la cellule Type : entier
        self.x = x                                # Initialisation de l'abcisse de la cellule Type : entier
        self.y = y                                # Initialisation de l'ordonnée de la cellule Type : entier
        self.prod = prod                          # Initialisation de la production d'unités de la cellule. Type : entier
        self.nboff = nboff                        # Initialisation du nombre d'unités offensives présentes dans la cellule. Type : entier 
        self.nbdef = nbdef                        # Initialisation du nombre d'unités défensives présentes dans la cellule. Type : entier
        self.couleur = couleur                    # Initialisation de la couleur de la cellule càd à qui elle appartient, 0 -> Neutre, sinon elle appartient à quelqu'un. Type : entier
        self.voisins = []                         # Initialisation du tableau contenant les voisins de la cellule. Type : tuple (objet Ligne,objet Cellule correspondant)
        self.voisinsAlly = voisinsAlly
        self.voisinsEnem = voisinsEnem
        self.voisinsNeut = voisinsNeut

        
    
# Définition de la classe Ligne
class Ligne:
    
   
    # Fonction d'initialisation 
    def __init__(self,idline,Cell1,Cell2, dist, nbunitfrom1=[], nbunitfrom2=[]):   
        self.idline = idline                      # Numéro de ligne
        self.Cell1 = Cell1                        # objet de type Cellule 
        self.Cell2 = Cell2                        # objet de type Cellule
        self.dist = dist                          # Distance entre les deux cellules
        self.nbunitfrom1 = nbunitfrom1            # Initialisation des infos sur les unités venant de la cellule Cell1 présentes sur la ligne : triplet de la forme (nbunits, owner, timestamp)
        self.nbunitfrom2 = nbunitfrom2            # Initialisation des infos sur les unités venant de la cellule Cell2 présentes sur la ligne : triplet de la forme (nbunits, owner, timestamp)
    


class Graphe:
    
    def __init__(self,listCellules,listLignes,listInfoTerrain, cellAlly = [], cellEnem = [], cellNeut = []):
        self.listCellules = listCellules
        self.listLignes = listLignes
        self.listInfoTerrain = listInfoTerrain                          # liste contenant : match_id, nb_players, no_color, speed, nb_cells, nb_lines
        self.cellAlly = cellAlly                                        # liste contenant les objets Cellule alliés
        self.cellEnem = cellEnem                                        # liste contenant les objets Cellule Ennemis
        self.cellNeut = cellNeut                                        # liste contenant les objets Cellule neutres


"""Robot-joueur de Pooo
    
    Le module fournit les fonctions suivantes :
        register_pooo(uid)
        init_pooo(init_string)
        play_pooo()
        
"""

__version__='0.1'
 

## chargement de l'interface de communication avec le serveur
#from poooc import order, state, state_on_update, etime

# mieux que des print partout
import logging
# pour faire de l'introspection
import inspect


def register_pooo(uid):
    """Inscrit un joueur et initialise le robot pour la compétition

        :param uid: identifiant utilisateur
        :type uid:  chaîne de caractères str(UUID) 
        
        :Example:
        
        "0947e717-02a1-4d83-9470-a941b6e8ed07"

    """
    global userid
    userid = uid


def init_pooo(init_str):
    """Initialise le robot pour un match
        
        :param init_string: instruction du protocole de communication de Pooo (voire ci-dessous)
        :type init_string: chaîne de caractères (utf-8 string)
       
       
       INIT<matchid>TO<#players>[<me>];<speed>;\
       <#cells>CELLS:<cellid>(<x>,<y>)'<radius>'<offsize>'<defsize>'<prod>,...;\
       <#lines>LINES:<cellid>@<dist>OF<cellid>,...

       <me> et <owner> désignent des numéros de 'couleur' attribués aux joueurs. La couleur 0 est le neutre.
       le neutre n'est pas compté dans l'effectif de joueurs (<#players>).
       '...' signifie que l'on répète la séquence précédente autant de fois qu'il y a de cellules (ou d'arêtes).
       0CELLS ou 0LINES sont des cas particuliers sans suffixe.
       <dist> est la distance qui sépare 2 cellules, exprimée en... millisecondes !
       /!\ attention: un match à vitesse x2 réduit de moitié le temps effectif de trajet d'une cellule à l'autre par rapport à l'indication <dist>.
       De manière générale temps_de_trajet=<dist>/vitesse (division entière).
        
        :Example:
        
        "INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3"
        
    """
    
    listCellules=[]
    listLignes=[]
    listInfoTerrain=[]
    
    
    regex1 = re.compile('INIT[A-Za-z0-9-]+TO') # Recuperation de l'id du match
    resultat = regex1.findall(init_str)
    match_id=resultat[0][4:-2]
    
    regex2 = re.compile('TO[0-9]+') # Recuperation de nb joueurs
    resultat  = regex2.findall(init_str)
    nb_players = int(resultat[0][2::])
    
    
    regex3 = re.compile('\[[0-9]+\]') # Recuperation de numero de couleur
    resultat  = regex3.findall(init_str)
    no_color = int(resultat[0][1:-1])
    
    regex4 = re.compile(';[0-9]+;') # Recuperation de la vitesse de jeu
    resultat  = regex4.findall(init_str)
    speed = int(resultat[0][1:-1])
    
    regex5 = re.compile(';[0-9]+CELLS') # Recuperation du nombre de cellules
    resultat  = regex5.findall(init_str)
    nb_cells = int(resultat[0][1:-5])
    
    regex5_2 = re.compile(';[0-9]+LINES') # Recuperation du nombre de lignes
    resultat  = regex5_2.findall(init_str)
    nb_lines = int(resultat[0][1:-5])
    
    listInfoTerrain = [match_id,nb_players,no_color,speed,nb_cells,nb_lines]
    
    
    
    regex6 = re.compile('[0-9]+\([0-9]+,[0-9]+\)\'[0-9]+\'[0-9]+\'[0-9]+\'I+') 
    cellules_init  = regex6.findall(init_str)
    # cellules_init est une liste contenant toutes les infos sur les cellules. exemple: [ "1(23,9)'2'30'8'I" , "2(41,55)'1'30'8'II" , "3(23,103)'1'20'5'I" ]
    
    # Boucle qui va successivement traiter les elements de la liste "cellules_init"
    for i in range (nb_cells): #Recuperation et instanciation des cellules 

        regex7 = re.compile('[0-9]+\(') # Recuperation de l'ID de la cellule
        id_cellule  = regex7.findall(cellules_init[i])
        id_cellule  = int(id_cellule[0][:-1])
        
        regex8 = re.compile('\([0-9]+,') # Recuperation de l'abscisse de la cellue
        x  = regex8.findall(cellules_init[i])
        x  = int(x[0][1:-1])
        
        regex9 = re.compile(',[0-9]+\)') # Recuperation de l'ordonnee de la cellule
        y  = regex9.findall(cellules_init[i])
        y  = int(y[0][1:-1])
        
        regex10 = re.compile('\)\'[0-9]+\'') # Recuperation du rayon de la cellule
        radius  = regex10.findall(cellules_init[i])
        radius  = int(radius[0][2:-1])
        
        regex11 = re.compile('[0-9]+\'[0-9]+\'[0-9]+') # Recuperation du nombre maximum d'unité offensive 
        offsize  = re.compile('\'[0-9]+\'').findall(regex11.findall(cellules_init[i])[0])
        offsize  = int(offsize[0][1:-1])
        
        regex12 = re.compile('\'[0-9]+\'') # Recuperation du nombre maximum d'unité defensive
        defsize = regex12.findall(cellules_init[i])
        defsize = int(defsize[1][1:-1])
        
        regex13 = re.compile('\'I+') # Recuperation de la vitesse de production d'unité 
        prod = regex13.findall(cellules_init[i])
        prod = len(prod[0][1:]) # La vitesse de production est represente par des "I" , on compte donc le nombre de "I" avec un len()
        
        
        listCellules.append(Cellule(id_cellule,offsize,defsize,radius,x,y,prod)) #instanciation des Cellules

    
    
    regex14 = re.compile('[0-9]+@[0-9]+OF[0-9]+')
    lignes_init  = regex14.findall(init_str)

    
    for j in range (nb_lines): #Recuperation et instanciation des lignes
        
        regex15 = re.compile('[0-9]+@') # Recuperation de l'ID de la 1ere cellule qui forme la ligne 
        idcell1 = regex15.findall(lignes_init[j])
        idcell1 = int(idcell1[0][:-1])
        
        regex16 = re.compile('@[0-9]+OF') # Recuperation de la distance entre les deux cellules (en ms)
        dist = regex16.findall(lignes_init[j])
        dist = int(dist[0][1:-2])
        
        regex17 = re.compile('OF[0-9]+') # Recuperation de l'ID de la 2eme cellule qui forme la ligne 
        idcell2 = regex17.findall(lignes_init[j])
        idcell2 = int(idcell2[0][2:])
        
        idline = j+1                    #Association d'un numéro ID à chaque ligne
        
        listLignes.append(Ligne(idline,listCellules[idcell1],listCellules[idcell2],dist)) #instanciation des Lignes

        listCellules[idcell1].voisins.append((listLignes[len(listLignes)-1],listCellules[idcell2])) # on ajoute dans les voisins de la cellule1 (cellid1) l'objet ligne dernièrement ajouté et l'objet cellule2 (cellid2)
        listCellules[idcell2].voisins.append((listLignes[len(listLignes)-1],listCellules[idcell1])) # on ajoute dans les voisins de la cellule2 (cellid2) l'objet ligne dernièrement ajouté et l'objet cellule1 (cellid1)

        #print("idcell1 : " + str(idcell1) + " ; idcell2 : " + str(idcell2))
    
        
        
        
    global Map
    Map=Graphe(listCellules,listLignes,listInfoTerrain)



def ligne(graph,cell1,cell2):                                                   #Fonction qui prend en paramètre l'objet Graphe, l'ID de la cellule 1 et l'ID de la cellule 2 et qui renvoie un objet Ligne correspondant
   
    for i in range(len(graph.listCellules[cell1].voisins)):                     #On recherche dans les voisins de la cellule 1, la cellule qui a l'ID de la cellule2
        
        if graph.listCellules[cell1].voisins[i][1].idcell == cell2 :
            line = graph.listCellules[cell1].voisins[i][0]
            return line
    



def decrypt_state(graph,state_str):                                                       #Fonction de traitement de state
    
    graph.cellAlly = []                                                         # Réinit des listes de cellules (alliées, ennemies et neutres)
    graph.cellEnem = []
    graph.cellNeut = []

    
    """regex1 = re.compile('STATE[A-Za-z0-9-]+IS')                                 #Recupération de l'id du match
    res = regex1.findall(state_str)                                             
    match_id = res[0][5:-2]"""
    
    """regex2 = re.compile('IS[0-9]+')                                             #Récupération du nombre de joueurs
    res = regex2.findall(state_str)
    nb_players = int(res[0][2::])"""
    
    regex3 = re.compile(';[0-9]+CELLS')                                         #Récupération du nombre de cellules
    res = regex3.findall(state_str)
    nb_cells = int(res[0][1:-5])
    
    
    regex4 = re.compile('[0-9]+\[\-?[0-9]+\][0-9]+\'[0-9]')                        #Récupération de des informations sur les cellulles sous forme de liste
    info_cells = regex4.findall(state_str)
    
    regex5 = re.compile('[0-9]+MOVES')                                          #Récupération du nombre de mouvements en cours
    res = regex5.findall(state_str)
    nb_moves = int(res[0][0:-5])
    
    regex6 = re.compile('([0-9]+([<>][0-9]+\[[0-9]+\]@[0-9]+\')+[0-9]+)')    
    info_moves = regex6.findall(state_str)                                      #Liste avec (infos de déplacement entre 2 cellules + truc qui sert à rien mais je vois pas comment faire autrement)
    
    
    
   
    for i in range(nb_cells):                                                   #Recupération des infos sur les cellules (boucle qui parcourt chaque objet cellule pour actualiser les infos)
        
        graph.listCellules[i].voisinsAlly = []
        graph.listCellules[i].voisinsEnem = []
        graph.listCellules[i].voisinsNeut = []
        
        regex8 = re.compile('\[\-?[0-9]+\]')                                       #MàJ de la couleur de la cellule
        res = regex8.findall(info_cells[i])
        color = int(res[0][1:-1])
        graph.listCellules[i].couleur = int(res[0][1:-1])
        
        if color == graph.listInfoTerrain[2] :                                  # Ajout des cellules alliées, ennemies ou neutres dans leur liste repective
            graph.cellAlly.append(graph.listCellules[i])
        elif color == -1 :
            graph.cellNeut.append(graph.listCellules[i])
        else :
            graph.cellEnem.append(graph.listCellules[i])
            
        regex9 = re.compile('[0-9]+\'')                                         #MàJ du nombre d'unités offensives actuel de la cellule
        res = regex9.findall(info_cells[i])
        graph.listCellules[i].nboff = int(res[0][0:-1])
        
        regex10 = re.compile('\'[0-9]+')                                        #MàJ du nombre d'unités défensives actuel de la cellule
        res = regex10.findall(info_cells[i])
        graph.listCellules[i].nbdef = int(res[0][1::])
        
    for i in range(nb_cells):
        
        for j in range(len(graph.listCellules[i].voisins)):                     # Ajout des voisins de la cellule dans des listes en fonction de leur statut (Neutre, allié ou ennemi)
            
            if graph.listCellules[i].voisins[j][1].couleur == int(-1) :
                
                graph.listCellules[i].voisinsNeut.append(graph.listCellules[i].voisins[j][1])
                
            if graph.listCellules[i].voisins[j][1].couleur == graph.listInfoTerrain[2] :
                graph.listCellules[i].voisinsAlly.append(graph.listCellules[i].voisins[j][1])
                
            elif graph.listCellules[i].voisins[j][1].couleur != int(-1) and graph.listCellules[i].voisins[j][1].couleur != graph.listInfoTerrain[2] :
                graph.listCellules[i].voisinsEnem.append(graph.listCellules[i].voisins[j][1])       
        
    for i in range(len(info_moves)):                                            # Récupération des infos sur les mouvements des unités
        
        graph.listLignes[i].nbunitfrom2 = []                                    #Réinitialisation des listes comportant les infos sur les unités en mvt sur chaque ligne
        graph.listLignes[i].nbunitfrom1 = []
        
        regex12 = re.compile('[0-9]+[<>]')                                      #Récupération de la premiere cell composant la ligne
        res = regex12.findall(info_moves[i][0])
        cell1 = int(res[0][0:-1])
        
        regex13 = re.compile('\'[0-9]+')                                        #Récupération de la 2eme cellule composant la ligne
        res = regex13.findall(info_moves[i][0])
        cell2 = int(res[0][1::])
        
        for j in range(len(graph.listCellules[cell1].voisins)):               #Récupération de l'ID de la ligne correspondant aux 2 cellules récupérées
            
            if graph.listCellules[cell1].voisins[j][1].idcell == cell2 :
                line = graph.listCellules[cell1].voisins[j][0].idline
                
                
        
        regex11 = re.compile('[<>]')
        sens = regex11.findall(info_moves[i][0])                                #Recupération du sens des unités
        
        regex14 = re.compile('[<>][0-9]+')                                      #Récupération d'un tableau contenant le nb unités en mvt pour la ligne courante
        tab_nbunit = regex14.findall(info_moves[i][0])
        
        regex15 = re.compile('\[[0-9]+\]')                                      #Récupération d'un tableau contenant l'owner de chaque paquet d'unités sur la ligne courante
        tab_owner = regex15.findall(info_moves[i][0])
        
        regex16 = re.compile('@[0-9]+')                                         #Récupération d'un tableau contenant le timestamp de chaque paquet d'unités sur la ligne courante
        tab_time = regex16.findall(info_moves[i][0])
        
        for k in range(len(tab_nbunit)):                                                                                                        #Ajout des 3 dernieres données récupérées dans l'objet ligne correspondant à la ligne courante
            if sens[k] == '<':
                graph.listLignes[line-1].nbunitfrom2.append((int(tab_nbunit[k][1::]),tab_owner[k][1:-1],int(tab_time[k][1::])))
            else :
                graph.listLignes[line-1].nbunitfrom1.append((int(tab_nbunit[k][1::]),tab_owner[k][1:-1],int(tab_time[k][1::])))
    
    
def play_pooo():
    """Active le robot-joueur
    
    """
    logging.info('Entering play_pooo fonction from {} module...'.format(inspect.currentframe().f_back.f_code.co_filename))
    ### Début stratégie joueur ### 
    # séquence type :
    
    # (1) récupère l'état initial 
    # init_state = state()
    #userid = 'Ambianceteam'
    #init_string = "INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3" # donné par le serveur , mais par quelle fonction ? 
    
    # (2) TODO: traitement de init_state                                              # On initialise Map qui est un objet de type Graphe 
    init_state = poooc.state()
    decrypt_state(Map,init_state)                                               # Initialisation des informations de state

    maCouleur = Map.listInfoTerrain[2]                                          # On récupère notre couleur 
    
    
    while True:
        state = poooc.state_on_update()
        # Mise à jour de la Map :
        decrypt_state(Map,state)
        
        '''for i in range(len(Map.cellAlly)):
            poooc.order(setmove(userid,100,Map.cellAlly[i],Map.cellAlly[i].voisinsNeut[0]))'''
        '''if Map.listCellules[0].nboff > Map.listCellules[1].nboff :
            poooc.order(setmove(userid,100,Map.listCellules[0],Map.listCellules[1]))'''
        ####### IA ########
        for i in range(len(Map.cellAlly)):                                      # On parcourt la liste des cellules alliées
            prodmax = 0
            danger = 0
            ratioCourant = 0
            
            if Map.cellAlly[i].voisinsEnem == [] and Map.cellAlly[i].voisinsNeut != []  :       #S'il n'y a pas d'ennemis autour de la cellule et qu'il y a des voisins neutres
                cible = Map.cellAlly[i].voisinsNeut[0]
                bestRatio = (Map.cellAlly[i].voisinsNeut[0].nbdef + Map.cellAlly[i].voisinsNeut[0].nboff + ligne(Map,Map.cellAlly[i].idcell, Map.cellAlly[i].voisinsNeut[0].idcell).dist)/Map.cellAlly[i].voisinsNeut[0].prod
                for j in range(len(Map.cellAlly[i].voisinsNeut)) :                              #On parcourt les voisins neutres
                    ratioCourant = (Map.cellAlly[i].voisinsNeut[j].nbdef + Map.cellAlly[i].voisinsNeut[j].nboff + ligne(Map,Map.cellAlly[i].idcell, Map.cellAlly[i].voisinsNeut[j].idcell).dist)/Map.cellAlly[i].voisinsNeut[j].prod
                    if ratioCourant < bestRatio :                                               #Et on choisit celle qui a le plus petit ratio (cellule la plus rentable) et elle devient la cible
                        bestRatio = ratioCourant                           
                        cible = Map.cellAlly[i].voisinsNeut[j]
            

                if (cible.nboff + cible.nbdef) < Map.cellAlly[i].nboff :                            #Du coup dès que notre cellule a assez d'unités on envoie pour conquérir la cellule cible
                    mv = setmove(userid,100,Map.cellAlly[i],cible)
                    poooc.order(mv)
                    
                    
                    
            if Map.cellAlly[i].voisinsEnem == [] and Map.cellAlly[i].voisinsNeut == [] and Map.cellAlly[i].voisinsAlly != [] :    #Si la cellule courante est entourés d'alliés
                for j in range(len(Map.cellAlly[i].voisinsAlly)):                                                               #On parcourt la liste des voisins de cette cellules
                    
                    if Map.cellAlly[i].voisinsAlly[j].voisinsEnem != [] :                                                       #Si une des cellules voisines est proche d'un ennemi, on lui enverra les unités en priorité (d'où le danger = 1)
                        danger = 1
                        cible2 = Map.cellAlly[i].voisinsAlly[j] 
                    elif Map.cellAlly[i].voisinsAlly[j].voisinsNeut != [] and danger == 0 :                                     #Si il n'y a pas de danger et qu'une cellule voisine a une cellule neutre à portée, on lui envoie les units
                        cible2 = Map.cellAlly[i].voisinsAlly[j]     
                    else :                                                                                                      #Sinon on envoie à la premiere cellule voisine rencontrée (possibilité d'améliorer bien sur ;))
                        cible2 = Map.cellAlly[i].voisinsAlly[0]
                        
                if Map.cellAlly[i].nboff >= 5 :                                                                     #Pour éviter de surcharger le serv, on fait transiter les unités par paquets de 5 (sinon ça plante)
                    poooc.order(setmove(userid,100,Map.cellAlly[i],cible2))
        
            if Map.cellAlly[i].voisinsEnem != [] :
                 cible = Map.cellAlly[i].voisinsEnem[0]
                 bestRatio = (Map.cellAlly[i].voisinsEnem[0].nbdef + Map.cellAlly[i].voisinsEnem[0].nboff + ligne(Map,Map.cellAlly[i].idcell, Map.cellAlly[i].voisinsEnem[0].idcell).dist)/Map.cellAlly[i].voisinsEnem[0].prod
                 for j in range(len(Map.cellAlly[i].voisinsEnem)) :
                     ratioCourant = (Map.cellAlly[i].voisinsEnem[j].nbdef + Map.cellAlly[i].voisinsEnem[j].nboff + ligne(Map,Map.cellAlly[i].idcell, Map.cellAlly[i].voisinsEnem[j].idcell).dist)/Map.cellAlly[i].voisinsEnem[j].prod
                     if (ratioCourant < bestRatio) and (Map.cellAlly[i].voisinsEnem[j].nbdef + Map.cellAlly[i].voisinsEnem[j].nboff < Map.cellAlly[i].nboff) :           #Ne prend pas en compte les unités ennemies présentent sur la ligne (à corriger donc) + les unités que l'ennemi aura produit le temps du déplacement des unités alliées 
                        bestRatio = ratioCourant                           
                        cible = Map.cellAlly[i].voisinsEnem[j]    
        ####### FIN IA ########
        
    
    
    
    
        
#Fonction permettant de créer le paramètre move pour la fonction order(move)
def setmove(userid,pourcent,Cellfrom,Cellto):
    res = '[' + userid + ']' + 'MOV' + str(pourcent) + 'FROM' + str(Cellfrom.idcell) + 'TO' + str(Cellto.idcell)
    return res


def main() :
    
    init_string = "INIT013fe2e8-86df-4fa3-960d-a0a537849a68TO2[1];2;7CELLS:0(0,0)'100'30'8'I,1(0,5)'100'30'8'I,2(5,0)'100'30'8'I,3(5,5)'200'30'8'II,4(5,10)'100'30'8'I,5(10,5)'100'30'8'I,6(10,10)'100'30'8'I;6LINES:0@4800OF1,0@4800OF2,2@4700OF3,3@4700OF4,4@4800OF6,5@4800OF6"
    init_pooo(init_string) # Instanciation de la Map (objet Graphe)

    state_str = "STATE92352897-2119-4c57-b26d-44ec48982006IS2;7CELLS:0[0]5'0,1[-1]6'0,2[-1]6'0,3[-1]12'0,4[-1]6'0,5[-1]6'0,6[1]5'0;0MOVES"
    state_str2= "STATE9c3a9d60-adaa-46a7-af25-40c933ea3a1eIS2;7CELLS:0[0]1'2,1[-1]6'0,2[-1]6'0,3[-1]12'0,4[-1]6'0,5[-1]6'0,6[1]1'2;2MOVES:0>6[0]@3665229582'1,4<6[1]@3665229576'6"
    decrypt_state(Map,state_str2)
    
    uid = "blablacar"
    register_pooo(uid)
    
    
    
    '''for i in range(len(Map.cellAlly)):                                      # On parcourt la liste des cellules alliées
        prodmax = 0
        if Map.cellAlly[i].voisinsEnem == [] and Map.cellAlly[i].voisinsNeut != []  :       #S'il n'y a pas d'ennemis autour de la cellule et qu'il y a des voisins neutres
            for j in range(len(Map.cellAlly[i].voisinsNeut)) :                              #On parcourt les voisins neutres
                if Map.cellAlly[i].voisinsNeut[j].prod > prodmax :                          #Et on choisit celle qui a la production maximale (elle devient la cellule cible)
                    
                    prodmax = Map.cellAlly[i].voisinsNeut[j].prod                           
                    cible = Map.cellAlly[i].voisinsNeut[j]
                    
                if (cible.nboff+cible.nbdef) > Map.cellAlly[i].nboff :                            #Du coup dès que notre cellule a assez d'unités on envoie pour conquérir la cellule cible
                    mv = setmove(userid,100,Map.cellAlly[i],cible)
                    print(mv)
                    poooc.order(str(mv))'''
                    
                   
    

    
if __name__ == '__main__':
    main()