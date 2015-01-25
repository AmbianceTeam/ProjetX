# -*- coding: utf-8 -*-
import re
#from poooc import order, state, state_on_update, etime
import poooc


#####A mettre en commentaire lors des tests sur Cloud9#####
"""import tkinter 
from interface_graphique import dessiner_terrain
import threading



class GUIThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        #ici ça ne marchera pas self.window=GUIInterface()
 
 
    def run(self):
        #là ça marche
        self.window=GUIInterface()
        self.window.mainloop()
 
    def stop(self):
        self.window.destroy()
 
 
class GUIInterface(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title("Interface Graphique AmbianceTeam")
 
        self.canvas = tkinter.Canvas(self , width=800, height =800) # Création d'un Canvas à partir de la fenetre "window"
        self.canvas.pack()
 
    def exit(self):
        self.destroy()



global newGUIThread; newGUIThread = GUIThread()
newGUIThread.start()"""
###########################################################

# Définition de la classe Cellule
class Cellule:
    
    
    # Fonction d'initialisation
    def __init__(self,idcell,offsize,defsize,radius,x,y,prod=0,nboff=0,nbdef=0,couleur=-1,voisinsAlly = [], voisinsEnem = [], voisinsNeut = [], redirection = 0): #-1 pour le neutre
        
        self.idcell = idcell                      # Initialisation de l'id de la cellule Type : entier
        self.offsize = offsize                    # Initialisation de la capacité offensive de la cellule Type : entier
        self.defsize = defsize                    # Initialisation de la capacité défensive de la cellule Type : entier
        self.radius = radius                      # Initialisation du rayon de la cellule Type : entier
        self.x = x                                # Initialisation de l'abcisse de la cellule Type : entier
        self.y = y                                # Initialisation de l'ordonnée de la cellule Type : entier
        self.prod = prod                          # Initialisation de la production d'unités de la cellule. Type : entier
        self.nboff = nboff                        # Initialisation du nombre d'unités offensives présentes dans la cellule. Type : entier 
        self.nbdef = nbdef                        # Initialisation du nombre d'unités défensives présentes dans la cellule. Type : entier
        self.couleur = couleur                    # Initialisation de la couleur de la cellule càd à qui elle appartient, -1 -> Neutre, sinon elle appartient à quelqu'un. Type : entier
        self.voisins = []                         # Initialisation du tableau contenant les voisins de la cellule. Type : tuple (objet Ligne,objet Cellule correspondant)
        self.voisinsAlly = voisinsAlly
        self.voisinsEnem = voisinsEnem
        self.voisinsNeut = voisinsNeut
        self.redirection = redirection            # Initialisation de la Cellule vers laquelle doivent être redirigées les unités produites. Egale à 0 si aucune redirection doit être effectuée

        
    
# Définition de la classe Ligne
class Ligne:
    
   
    # Fonction d'initialisation 
    def __init__(self,idline,Cell1,Cell2, dist, nbunitfrom1=[(0,0,0)], nbunitfrom2=[(0,0,0)]):   
        self.idline = idline                      # Numéro de ligne
        self.Cell1 = Cell1                        # objet de type Cellule 
        self.Cell2 = Cell2                        # objet de type Cellule
        self.dist = dist                          # Distance entre les deux cellules
        self.nbunitfrom1 = nbunitfrom1            # Initialisation des infos sur les unités venant de la cellule Cell1 présentes sur la ligne : triplet de la forme (nbunits, owner, timestamp)
        self.nbunitfrom2 = nbunitfrom2            # Initialisation des infos sur les unités venant de la cellule Cell2 présentes sur la ligne : triplet de la forme (nbunits, owner, timestamp)
    


class Graphe:
    
    def __init__(self,listCellules,listLignes,listInfoTerrain, cellAlly = [], cellEnem = [], cellNeut = [], cellFront = []):
        self.listCellules = listCellules
        self.listLignes = listLignes
        self.listInfoTerrain = listInfoTerrain                          # liste contenant : match_id, nb_players, no_color, speed, nb_cells, nb_lines
        self.cellAlly = cellAlly                                        # liste contenant les objets Cellule alliés
        self.cellEnem = cellEnem                                        # liste contenant les objets Cellule Ennemis
        self.cellNeut = cellNeut                                        # liste contenant les objets Cellule neutres
        self.cellFront = cellFront                                      # liste contenant les objets Cellule qui ont au moins un ennemi dans leurs voisins (Cellules du front). ( [Cellule,idcell], ...)


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
            
            
def dijkstra(CellS,CellD): # Algorithme de Dijsktra qui recherche le chemin le plus court parmis les cellules alliées 

    listAExplorer = []
    listDist = []
    listPred = []
    
    chemin = []
    
    # INITIALISATION de la liste des Distances
    for i in range(len(Map.cellAlly)):
        listAExplorer.append([i,Map.cellAlly[i]]) #Liste des cellules à explorer i = idlocal
        listPred.append(0) #liste des prédessesseur  [0,0,0,0,0,0,0....]
        if Map.cellAlly[i]==CellD: #récupération de l'indice local de CellDestination
            indiceDest = i
			#logging.info('#########___________INDICE DEST INITIALISE___________##################')
        
        if Map.cellAlly[i]==CellS: #récupération de l'indice local de CellSource 
            indiceSource = i
            
        if Map.cellAlly[i]==CellS:
            listDist.append([Map.cellAlly[i],0]) # listDist : [ [Cell,dist] , [Cell,dist] , ... ]
        else :
            listDist.append([Map.cellAlly[i],2147483647])  #2 147 483 647 considéré comme l'infini
    #print('S :'+ str(indiceSource) + ' D: '+ str(indiceDest))

    
    while len(listAExplorer) != 0: 
        # CHOIX du PIVOT 
        distMin = 2147483647
        for i in range(len(listAExplorer)):
            if(listDist[listAExplorer[i][0]][1] < distMin):
                distMin = listDist[listAExplorer[i][0]][1]
                pivot = listAExplorer[i][0] # pivot : indice du pivot   
        #print('pivot__: '+str(pivot)) #indice pivot
        
        for j in range(len(listDist[pivot][0].voisinsAlly)):
            for m in range(len(listDist)):                                      # trouver l'indice des voisins du pivot dans la listDist
                if(listDist[pivot][0].voisinsAlly[j]==listDist[m][0]):
                    indiceVoisin = m
                
            if( listDist[pivot][1] + ligne(Map,listDist[pivot][0].idcell,listDist[pivot][0].voisinsAlly[j].idcell).dist < listDist[indiceVoisin][1] ):
                listDist[indiceVoisin][1] = listDist[pivot][1] + ligne(Map,listDist[pivot][0].idcell,listDist[pivot][0].voisinsAlly[j].idcell).dist
                listPred[indiceVoisin] = pivot
        
        listAExplorer.remove([pivot,listDist[pivot][0]]) # on enleve le pivot de la listAExplorer
        #print('listAExplorer __: ')
        #print(listAExplorer)
        
    indice=indiceDest #indice de la cellule de destination dans la liste des cellules Alliées
    for l in range(len(listPred)):
        indice = listPred[indice]
        if(indice == indiceSource):                                             # Si on trouve l'indice source , on arrete la boucle 
            break
        chemin.insert(0,listDist[indice][0])                                    # On insère la cellule qui constitue une étape du chemin

        
    chemin.insert(0,listDist[indiceSource][0]) # on ajoute la tête et la queue du chemin 
    chemin.append(listDist[indiceDest][0])
    return chemin
    
def lenChemin(chemin):                                                          # Calcule la longueur d'un chemin 
    lenC = 0
    for i in range(len(chemin)-1):
        lenC = lenC + ligne(Map,chemin[i].idcell,chemin[i+1].idcell).dist
    return lenC
    
def fillRedirection(chemin):                                                    # Met à jour les redirections des cellules
    for i in range(len(chemin)-1):
        if(chemin[i].redirection == 0):
            chemin[i].redirection = chemin[i+1]
            
            
    


def decrypt_state(graph,state_str):                                                       #Fonction de traitement de state
    
    graph.cellAlly = []                                                         # Réinit des listes de cellules (alliées, ennemies et neutres)
    graph.cellEnem = []
    graph.cellNeut = []
    graph.cellFront = []

    
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
    
    for i in range(nb_cells):                                                   # Remplissage des cellules du Front 
        if len(graph.listCellules[i].voisinsEnem) != 0 and graph.listCellules[i].couleur==graph.listInfoTerrain[2]: # Si la cellule a des voisins ennemis et que c'est une cellule alliée alors elle fait partie du front
            graph.cellFront.append((graph.listCellules[i],graph.listCellules[i].idcell))
    
    for i in range(len(graph.listLignes)):
        graph.listLignes[i].nbunitfrom2 = []                                    #Réinitialisation des listes comportant les infos sur les unités en mvt sur chaque ligne
        graph.listLignes[i].nbunitfrom1 = []
    
    for i in range(len(info_moves)):                                            # Récupération des infos sur les mouvements des unités
        """ Ici tu réinitialises les len(info_moves) premières lignes, mais ce n'est pas forcément les len(info_moves) premières lignes qui ont des mouvements,
        de toutes façon l'initialisation est inutile ici puisque tu écris par les nouvelles valeurs par dessus les anciennes"""
        #graph.listLignes[i].nbunitfrom2 = [(0,0,0)]                                    #Réinitialisation des listes comportant les infos sur les unités en mvt sur chaque ligne
        #graph.listLignes[i].nbunitfrom1 = [(0,0,0)]
        
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


    
    

    state = poooc.state_on_update()
    # Mise à jour de la Map :
    decrypt_state(Map,state)
    lastcellFront = []
    
    '''for i in range(len(Map.cellAlly)):
        poooc.order(setmove(userid,100,Map.cellAlly[i],Map.cellAlly[i].voisinsNeut[0]))'''
    '''if Map.listCellules[0].nboff > Map.listCellules[1].nboff :
        poooc.order(setmove(userid,100,Map.listCellules[0],Map.listCellules[1]))'''
    ####### IA ########*
    while True :
        #####A mettre en commentaire lors des tests sur Cloud9#####
        """
        dessiner_terrain(newGUIThread.window.canvas,Map)"""
        ###########################################################
        state = poooc.state_on_update()
        decrypt_state(Map,state)
        
        if(Map.cellFront != lastcellFront):                                     # Réinitialisation des redirections de toutes les cellules
            logging.info('----Réinitialisation des REDIRECTIONS------')
            for k in range(len(Map.listCellules)):
                Map.listCellules[k].redirection = 0
                
        
        for i in range(len(Map.cellAlly)):                                      # On parcourt la liste des cellules alliées

            prodmax = 0
            danger = 0
            ratioCourant = 0
            #logging.info('ratioCourant______________________________: {}'.format(ratioCourant))
            
            
            #   /!\  PHASE 1 : PRISE DES CELLULES NEUTRES /!\
            
            
            
            if Map.cellAlly[i].voisinsEnem == [] and Map.cellAlly[i].voisinsNeut != []  :       #S'il n'y a pas d'ennemis autour de la cellule et qu'il y a des voisins neutres
                
                
                # Initialisation des variables cible et bestRatio, bestRatio correspondant à la cellule que l'on juge la plus intéressante ((nb unités nécessaire + dist)/prod), plus ce ratio est petit, mieux c'est 
                cible = Map.cellAlly[i].voisinsNeut[0]
                bestRatio = (Map.cellAlly[i].voisinsNeut[0].nbdef + Map.cellAlly[i].voisinsNeut[0].nboff + ligne(Map,Map.cellAlly[i].idcell, Map.cellAlly[i].voisinsNeut[0].idcell).dist)/Map.cellAlly[i].voisinsNeut[0].prod
                
                for j in range(len(Map.cellAlly[i].voisinsNeut)) :                              #On parcourt les voisins neutres
                    
                    ratioCourant = (Map.cellAlly[i].voisinsNeut[j].nbdef + Map.cellAlly[i].voisinsNeut[j].nboff + ligne(Map,Map.cellAlly[i].idcell, Map.cellAlly[i].voisinsNeut[j].idcell).dist)/Map.cellAlly[i].voisinsNeut[j].prod
                    
                    if ratioCourant < bestRatio :                                               #Et on choisit celle qui a le plus petit ratio (cellule la plus rentable) et elle devient la cible
                        bestRatio = ratioCourant  
                        cible = Map.cellAlly[i].voisinsNeut[j]
            
                
                
                # Si jamais la cellule neutre qui nous intéresse à un ennemi dans ses voisins
                
                if cible.voisinsEnem != []:
                   
                    nbEnem = 0
                   
                    for j in range(len(cible.voisinsEnem)):
                   
                        ligneEnem = ligne(Map, cible.idcell, cible.voisinsEnem[j].idcell)       # On récupère la ligne qui relie la cible à la cellule ennemie 
                   
                        if (ligneEnem.Cell1.idcell==cible.idcell):                   #Alors les unités ennemies viennent de unitfrom2
                            logging.info('condition______________________ 1')
                   
                            for k in range(len(ligneEnem.nbunitfrom2)):         #On parcourt les différents paquets d'unités circulant de 2 vers 1 
                   
                                if(ligneEnem.nbunitfrom2[k][1] != Map.listInfoTerrain[2]): # On vérifie qu'il s'agit d'un paquet ennemi
                                    logging.info('nbunitfrom2[k]: _______________ {}'.format(ligneEnem.nbunitfrom2[k]))
                                    nbEnem = nbEnem + ligneEnem.nbunitfrom2[k][0]
                        
                        elif(ligneEnem.Cell1.idcell==cible.voisinsEnem[j].idcell):   #Alors les unités ennemies viennent de unitfrom1
                            logging.info('condition______________________ 2')
                   
                            for k in range(len(ligneEnem.nbunitfrom1)):         #On parcourt les différents paquets d'unités circulant de 1 vers 2
                   
                                if(ligneEnem.nbunitfrom1[k][1] != Map.listInfoTerrain[2]): # On vérifie qu'il s'agit d'un paquet ennemi
                                    logging.info('nbunitfrom1[k]: _______________ {}'.format(ligneEnem.nbunitfrom1[k]))
                                    nbEnem = nbEnem + ligneEnem.nbunitfrom1[k][0]
                    
                        logging.info('ligneEnem trouvé ? {} | ID Cell Cible {} | ID Cell ennemie {} | nbEnem : {} | '.format(ligneEnem,cible.idcell,cible.voisinsEnem[j].idcell,nbEnem))
                        
                    nbRest = abs((cible.nboff + cible.nbdef) - nbEnem)                                 # On calcule le nombre d'unités qu'il y aura sur la cellule quand les unités ennemies arriveront    
                    logging.info('nbrest  =  {}'.format(nbRest))
                    
                    # Si le nombre d'unités alliés est supérieure au nombre d'unités restants sur la cellule cible
                    
                    if (nbRest+2) < Map.cellAlly[i].nboff:                     
                        mv = setmove(userid,100,Map.cellAlly[i],cible)          # On envoie nos unités sur la cellule, pour la conquérir
                        poooc.order(mv)
                        
    
    
                elif (cible.nboff + cible.nbdef) < Map.cellAlly[i].nboff:       #Sinon, si il n'y a pas d'ennemis à proximité, on part la conquérir si on a assez d'unités
                    mv = setmove(userid,100,Map.cellAlly[i],cible)            
                    poooc.order(mv)
                    
                    
                    
            
            if Map.cellAlly[i].voisinsEnem != [] and Map.cellAlly[i].voisinsNeut != []  :       #S'il y a des ennemis autour de la cellule et qu'il y a des voisins neutres
                
                cible = Map.cellAlly[i].voisinsNeut[0]                                          #Initialisation de cible et bestRatio
                bestRatio = 100000
                
                
                for j in range(len(Map.cellAlly[i].voisinsNeut)) :                              #On parcourt les voisins NEUTRES de la cellule
                    
                    ratioCourant = (Map.cellAlly[i].voisinsNeut[j].nbdef + Map.cellAlly[i].voisinsNeut[j].nboff + ligne(Map,Map.cellAlly[i].idcell, Map.cellAlly[i].voisinsNeut[j].idcell).dist)/Map.cellAlly[i].voisinsNeut[j].prod                            #Calcul du ratio servant à déterminer la cellule la plus rentable
                    
                    #Si un voisin neutre n'a pas de voisin Ennemi et qu'il a un meilleur ratio, on va le prvilégier
                    
                    if Map.cellAlly[i].voisinsNeut[j].voisinsEnem == [] and ratioCourant < bestRatio :                      
                        cible = Map.cellAlly[i].voisinsNeut[j]
                        bestRatio = ratioCourant
                    
                    
                    
                # Après avoir choisi la cellule à attaquer, on envoie l'ordre en s'assurant qu'on a bien assez d'unités et que la cellule n'a pas de voisins ennemis (au cas où la cellule choisie soit restée celle de l'init)
                
                if (cible.nboff + cible.nbdef) < Map.cellAlly[i].nboff and cible.voisinsEnem == [] :
                    mv = setmove(userid,100,Map.cellAlly[i],cible)            
                    poooc.order(mv)
                    
                    
                
                #   /!\  PHASE 2 : RAVITAILLEMENT  /!\
                
                
                
                    
            if Map.cellAlly[i].voisinsEnem == [] and Map.cellAlly[i].voisinsNeut == [] and Map.cellAlly[i].voisinsAlly != [] :    #Si la cellule courante est entourés d'alliés
                danger = 0
                cible2 = ''
                cible3 = ''
                attentestrat = 0
                distMinFront = 2147483647
                cheminPlusCourt = 0
                
                
                
            
                for j in range(len(Map.cellAlly[i].voisinsAlly)):                                                               #On parcourt la liste des voisins de cette cellules
                    #logging.info('c1 :{}  c2 :{} c3 :{}'.format(Map.cellAlly[i].voisinsAlly[j].voisinsNeut == [],Map.cellFront != [],Map.cellFront != lastcellFront))
					#if len(Map.cellAlly[i].voisinsAlly) == 1:                                                                   #S'il n'y a qu'une seule cellule alliée en voisinage alors on lui envoie automatiquement les unités
                    #    cible2 = Map.cellAlly[i].voisinsAlly[0]
                
                    if Map.cellAlly[i].voisinsAlly[j].voisinsEnem != [] :                                                       #Si une des cellules voisines est proche d'un ennemi, on lui enverra les unités en priorité (d'où le danger = 1)
                        #logging.info('condition 1')
                        danger = 1
                        cible2 = Map.cellAlly[i].voisinsAlly[j]
                        #logging.info('cible2 : _____ {} et Cellule depart : _____ {}'.format(cible2.idcell,Map.cellAlly[i].idcell))
                    
                    elif Map.cellAlly[i].voisinsAlly[j].voisinsNeut != [] and danger == 0 :                                     #Si il n'y a pas de danger et qu'une cellule voisine a une cellule neutre à portée, on lui envoie les units
                        #logging.info('condition 2')
                        attentestrat = 1
                        cible2 = Map.cellAlly[i].voisinsAlly[j] 
                    
					
                    elif Map.cellFront != ([] and lastcellFront):                                                      # Sinon, on doit faire une redirection d'unités vers les celulles qui ont des ennemis dans leur voisins
                        #logging.info('condition____________________ REDIRECTION')
                            
                        for k in range(len(Map.cellFront)):                     # recherche de la cellule du front le plus proche (à changer peut petre. idée : regarder la cellule du front qui a besoin du plus d'aide)
                            cheminCourant = dijkstra(Map.cellAlly[i],Map.cellFront[k][0])
                            distCourante = lenChemin(cheminCourant) # distance du chemin 
                            if( distCourante < distMinFront):
                                distMinFront = distCourante
                                cheminPlusCourt = cheminCourant
                                cible3 = Map.cellFront[k][0]
                        #logging.info('FILL_____REDIRECTIONS ___________________________######################')
                        fillRedirection(cheminPlusCourt)
                
                      
                    
                        
                if Map.cellAlly[i].nboff >= 2 and cible2 != '' and attentestrat == 0 :                                                                     #Pour éviter de surcharger le serv, on fait transiter les unités par paquets de 2 (sinon ça plante)
                    poooc.order(setmove(userid,100,Map.cellAlly[i],cible2))
                
                elif Map.cellAlly[i].nboff >= 5 and cible2 != '' and attentestrat == 1 :                                                                #Quand il y a des cells neutres à coté de la cible on préférera retarder un peu l'envoi pour éviter que l'ennemi ne nous reprenne la cellule derriere
                    poooc.order(setmove(userid,100,Map.cellAlly[i],cible2))
                

            
            
                # /!\  PHASE 3 : CONQUETE CELLULES ENNEMIES  /!\
            
            
            
            
            if Map.cellAlly[i].voisinsEnem != [] :
                #logging.info('Une cellule Ally a un ennemi')
                cible = Map.cellAlly[i].voisinsEnem[0]
                bestRatio = (Map.cellAlly[i].voisinsEnem[0].nbdef + Map.cellAlly[i].voisinsEnem[0].nboff + ligne(Map,Map.cellAlly[i].idcell, Map.cellAlly[i].voisinsEnem[0].idcell).dist)/Map.cellAlly[i].voisinsEnem[0].prod
               
               
               
                for j in range(len(Map.cellAlly[i].voisinsEnem)) :
                    
                    ratioCourant = (Map.cellAlly[i].voisinsEnem[j].nbdef + Map.cellAlly[i].voisinsEnem[j].nboff + ligne(Map,Map.cellAlly[i].idcell, Map.cellAlly[i].voisinsEnem[j].idcell).dist)/Map.cellAlly[i].voisinsEnem[j].prod
                    
                    if (ratioCourant < bestRatio) :           #Ne prend pas en compte les unités ennemies présentent sur la ligne (à corriger donc) + les unités que l'ennemi aura produit le temps du déplacement des unités alliées 
                        bestRatio = ratioCourant                           
                        logging.info('bestRatio: {}'.format(bestRatio))
                        cible = Map.cellAlly[i].voisinsEnem[j]
                        
                if (cible.nboff + cible.nbdef + 3) < Map.cellAlly[i].nboff :                            #Du coup dès que notre cellule a assez d'unités on envoie pour conquérir la cellule cible
                    logging.info('condition____________________ ennemi 1')
                    mv = setmove(userid,100,Map.cellAlly[i],cible)
                    poooc.order(mv)
                    
                
                if Map.cellAlly[i].nboff == Map.cellAlly[i].offsize :
                    logging.info('condition____________________ ennemi 2')
                    mv = setmove(userid,100,Map.cellAlly[i],cible)
                    poooc.order(mv)
        
        
        ##### REDIRECTION DES UNITES #####        
        for l in range(len(Map.listCellules)):                                  # Redirection des unités                                                            
            if(Map.listCellules[l].redirection != 0 and Map.listCellules[l].nboff >= 2):
                logging.info('redirection____________________ vers ID {}'.format(Map.listCellules[l].redirection.idcell))
                poooc.order(setmove(userid,100,Map.listCellules[l],Map.listCellules[l].redirection))
        
        
        lastcellFront = Map.cellFront   # Maj de lastcellFront (une fois qu'on a rempli les redirections des cellules avec fillRedirection()        
                
        ####### FIN IA ########
        
    
    
    
    
        
#Fonction permettant de créer le paramètre move pour la fonction order(move)
def setmove(userid,pourcent,Cellfrom,Cellto):
    res = '[' + userid + ']' + 'MOV' + str(pourcent) + 'FROM' + str(Cellfrom.idcell) + 'TO' + str(Cellto.idcell)
    return res


def main() :
    
    init_string = "INIT6c78da94-1d8a-45bf-aa3b-3dce9a275ce1TO2[1];2;11CELLS:0(0,0)'100'20'8'I,1(2500,2500)'100'20'8'I,2(5000,2500)'100'20'8'I,3(7500,2500)'100'20'8'I,4(2500,5000)'100'20'8'I,5(5000,5000)'300'40'8'III,6(7500,5000)'100'20'8'I,7(2500,7500)'100'20'8'I,8(5000,7500)'100'20'8'I,9(7500,7500)'100'20'8'I,10(10000,10000)'100'20'8'I;18LINES:0@5390OF2,0@7705OF7,0@7705OF3,0@3335OF1,0@5390OF4,1@3135OF5,2@2100OF5,3@3135OF5,3@7705OF10,4@2100OF5,5@3135OF7,5@2100OF8,5@3135OF9,5@2100OF6,6@5390OF10,7@7705OF10,8@5390OF10,9@3335OF10"
    init_pooo(init_string) # Instanciation de la Map (objet Graphe)

    state_str = "STATE92352897-2119-4c57-b26d-44ec48982006IS2;7CELLS:0[0]5'0,1[-1]6'0,2[-1]6'0,3[-1]12'0,4[-1]6'0,5[-1]6'0,6[1]5'0;0MOVES"
    state_str2= "STATE6c78da94-1d8a-45bf-aa3b-3dce9a275ce1IS2;11CELLS:0[0]2'8,1[0]2'8,2[0]1'4,3[1]6'0,4[-1]6'0,5[1]4'0,6[1]2'4,7[-1]6'0,8[1]1'0,9[1]2'8,10[1]2'8;2MOVES:0>7[0]@4349032374'4,8<7[1]@4349032375'10"
    decrypt_state(Map,state_str2)
    
    uid = "blablacar"
    register_pooo(uid)
    
    #print(Map.listCellules[10].voisinsNeut)
    #print(dijkstra(Map.listCellules[10],Map.listCellules[5]))
    print(Map.listCellules[7].voisinsEnem)
    print(Map.cellFront)
    
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
