# -*- coding: utf-8 -*-
from recup_terrain import *




# Définition de la classe Cellule
class Cellule:
    
    
    # Fonction d'initialisation
    def __init__(self,idcell,offsize,defsize,radius,x,y,prod=0,nboff=0,nbdef=0,etat=0,voisins=[]):
        
        self.idcell = idcell                      # Initialisation de l'id de la cellule
        self.offsize = offsize                    # Initialisation de la capacité offensive de la cellule
        self.defsize = defsize                    # Initialisation de la capacité défensive de la cellule
        self.radius = radius                      # Initialisation du rayon de la cellule
        self.x = x                                # Initialisation de l'abcisse de la cellule
        self.y = y                                # Initialisation de l'ordonnée de la cellule
        self.prod = prod                          # Initialisation de la production d'unités de la cellule
        self.nboff = nboff                        # Initialisation du nombre d'unités offensives présentes dans la cellule
        self.nbdef = nbdef                        # Initialisation du nombre d'unités défensives présentes dans la cellule
        self.etat = etat                          # Initialisation de l'état de la cellule càd à qui elle appartient
        self.voisins = voisins                    # Initialisation du tableau contenant les voisins de la cellule
    
    
    # Méthode permettant la mise à jour d'informations non permanentes
    def update(self,nboff,nbdef,etat):
        self.nboff = nboff                        # Mise à jour du nombre d'unités offensives présentes dans la cellule
        self.nbdef = nbdef                        # Mise à jour du nombre d'unités défensives présentes dans la cellule 
        self.etat = etat                          # Mise à jour de l'état de la cellule, càd son propriétaire
        

        
    
# Définition de la classe Ligne
class Ligne:
    
   
    # Fonction d'initialisation 
    def __init__(self,Cell1,Cell2, dist, nbunitfrom1=0, nbunitfrom2=0):                          
        self.Cell1 = Cell1                        # objet de type Cellule 
        self.Cell2 = Cell2                        # objet de type Cellule
        self.dist = dist                          # Distance entre les deux cellules
        self.nbunitfrom1 = nbunitfrom1            # Nombre d'unités venant de la cellule Cell1 présentes sur la ligne 
        self.nbunitfrom2 = nbunitfrom2            # Nombre d'unités venant de la cellule Cell2 présentes sur la ligne
    
    
    # Méthode permettant la mise à jour d'informations non permanentes
    def update(self,nbunitfrom1,nbunitfrom2):
        self.nbunitfrom1 = nbunitfrom1            # Mise à jour du nombre d'unités venant de la cellule Cell1 présentes sur la ligne
        self.nbunitfrom2 = nbunitfrom2            # Mise à jour du nombre d'unités venant de la cellule Cell2 présentes sur la ligne
        

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
    Map = init_pooo(init_string) # Instanciation de Map (objet Graphe)
    print(Map.listInfoTerrain)
    
if __name__ == '__main__':
    main()