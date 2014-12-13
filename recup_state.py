#Fonction pas encore terminée 


import re
from AmbianceTeam import *


def decrypt_state():
    
    state_str = "STATE20ac18ab-6d18-450e-94af-bee53fdc8fcaIS2;3CELLS:1[2]12'4,2[2]15'2,3[1]33'6;4MOVES:1<5[2]@232'>6[2]@488'>3[1]@4330'2,1<10[1]@2241'3"

    
    regex1 = re.compile('STATE[A-Za-z0-9-]+IS')                                 #Recupération de l'id du match
    res = regex1.findall(state_str)                                             
    match_id = res[0][5:-2]
    
    regex2 = re.compile('IS[0-9]+')                                             #Récupération du nombre de joueurs
    res = regex2.findall(state_str)
    nb_players = int(res[0][2::])
    
    regex3 = re.compile(';[0-9]+CELLS')                                         #Récupération du nombre de cellules
    res = regex3.findall(state_str)
    nb_cells = int(res[0][1:-5])
    
    regex4 = re.compile('[0-9]+\[[0-9]+\][0-9]+\'[0-9]')                        #Récupération de des informations sur les cellulles sous forme de liste
    info_cells = regex4.findall(state_str)
    
    regex5 = re.compile('[0-9]+MOVES')                                          #Récupération du nombre de mouvements en cours
    res = regex5.findall(state_str)
    nb_moves = int(res[0][0:-5])
    
    regex6 = re.compile('([0-9]+([<>][0-9]+\[[0-9]+\]@[0-9]+\')+[0-9]+)')    
    info_moves = regex6.findall(state_str)                                      #Liste avec (infos de déplacement entre 2 cellules, truc qui sert à rien mais je vois pas comment faire autrement)

    
    print(info_cells)    
    
    for i in range(nb_cells):
        
        regex7 = re.compile('[0-9]+\[')
        res = regex7.findall(info_cells[i])
        cell_id = res[0][0:-1]
        
        regex8 = re.compile('\[[0-9]+\]')
        res = regex8.findall(info_cells[i])
        etat = res[0][1:-1]
        
        print(etat)
        
    

    

    

    
    
    
decrypt_state()