# -*- coding: utf-8 -*-


class Cellule:
    
    def __init__(self,idcell,offsize,defsize,radius,x,y,proddef=0,prodoff=0,nboff=0,nbdef=0,etat=0):
        self.idcell = idcell
        self.offsize = offsize
        self.defsize = defsize
        self.radius = radius
        self.x = x
        self.y = y
        self.proddef = proddef
        self.prodoff = prodoff
        self.nboff = nboff
        self.nbdef = nbdef
        self.etat = etat
    
    def update(self,nboff,nbdef,etat):
        self.nboff = nboff
        self.nbdef = nbdef
        self.etat = etat
        
    

class Lines:
    
    def __init__(self,idcell1,idcell2, dist, nbunit=0):
        self.idcell1 = idcell1
        self.idcell2 = idcell2
        self.dist = dist
        self.nbunit = nbunit
        
    def update(self,nbunit):
        self.nbunit = nbunit
        

class Graphe:
    
    def __init__(self,tabcell,tablines,listeadj):
        self.tabcell = tabcell
        self.tablines = tablines
        self.listeadj = listeadj
        
        
    def ajoutcell(cell):
        self.tabcell.append(cell)                   # MODIFIER POUR LISTEADJ, PUISQUE SI ON AJOUTE UNE CELLULE, LISTEADJ DOIT ETRE MODIFIE
        
    def ajoutlines(line):                           # MEME CHOSE
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
    pass
    
    
    
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
def setmove(userid,pourcent,cellfrom,cellto):
    res = ''
    res = res  + userid + 'MOV' + str((pourcent*cellfrom.nboff)/100) + 'FROM' + str(cellfrom.idcell) + 'TO' + str(cellto.idcell)
    return res

