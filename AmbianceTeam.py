# -*- coding: utf-8 -*-
from recup_terrain import *

class Cellule:
    
    def __init__(self,idcell,offsize,defsize,radius,x,y,prod=0,nboff=0,nbdef=0,etat=0,voisins=[]):
        self.idcell = idcell
        self.offsize = offsize
        self.defsize = defsize
        self.radius = radius
        self.x = x
        self.y = y
        self.prod = prod
        self.nboff = nboff
        self.nbdef = nbdef
        self.etat = etat
        self.voisins = voisins
    
    def update(self,nboff,nbdef,etat):
        self.nboff = nboff
        self.nbdef = nbdef
        self.etat = etat
        

        
    

class Ligne:
    
    def __init__(self,Cell1,Cell2, dist, nbunitfrom1=0, nbunitfrom2=0):                          
        self.Cell1 = Cell1 # objet de type Cellule 
        self.Cell2 = Cell2 # objet de type Cellule
        self.dist = dist
        self.nbunitfrom1 = nbunitfrom1
        self.nbunitfrom2 = nbunitfrom2
        
    def update(self,nbunitfrom1,nbunitfrom2):
        self.nbunitfrom1 = nbunitfrom1
        self.nbunitfrom2 = nbunitfrom2
        

class Graphe:
    
    def __init__(self,listCellules,listLignes,listInfoTerrain):
        self.listCellules = listCellules
        self.listLignes = listLignes
        self.listInfoTerrain = listInfoTerrain
        


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
    pass


def init_pooo(init_string):
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
        dist = dist[0][1:-2]
        
        regex17 = re.compile('OF[0-9]+') # Recuperation de l'ID de la 2eme cellule qui forme la ligne 
        idcell2 = regex17.findall(lignes_init[j])
        idcell2 = int(idcell2[0][2:])
        
        listLignes.append(Ligne(listCellules[idcell1-1],listCellules[idcell2-1],dist)) #instanciation des Lignes
        
    
    return Graphe(listCellules,listLignes,listInfoTerrain)
    
    
    
def play_pooo():
    """Active le robot-joueur
    
    """
    logging.info('Entering play_pooo fonction from {} module...'.format(inspect.currentframe().f_back.f_code.co_filename))
    ### Début stratégie joueur ### 
    # séquence type :
    # (1) récupère l'état initial 
    # init_state = state()
    # (2) TODO: traitement de init_state
    # (3) while True :
    # (4)     state = state_on_update()    
    # (5)     TODO: traitement de state et transmission d'ordres order(msg)
    pass
    
    
    
#Fonction permettant de créer le paramètre move pour la fonction order(move)
def setmove(userid,pourcent,Cellfrom,Cellto):
    res =  userid + 'MOV' + str((pourcent*Cellfrom.nboff)/100) + 'FROM' + str(Cellfrom.idcell) + 'TO' + str(Cellto.idcell)
    return res


def main() :
    
    init_string = "INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3"
    Map = init_pooo(init_string) # Instanciation de Map (objet Graphe)
    print(Map.listInfoTerrain)
    
if __name__ == '__main__':
    main()