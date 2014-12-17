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
        

        
    

class Lines:
    
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
        
        
    def ajoutcell(cell):
        self.tabcell.append(cell)                  
        
    def ajoutlines(line):                          
        self.tablines.append(line)
        


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
    
    return init_terrain(init_string) # Objet de type graphe
    
    
    
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
    Map = init_pooo(init_string) # Instanciation de la Map (objet Graphe)
    print(Map.listInfoTerrain)
    
if __name__ == '__main__':
    main()