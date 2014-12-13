import re
from AmbianceTeam import *


def decrypt_state():
    
    state_str = "STATE20ac18ab-6d18-450e-94af-bee53fdc8fcaIS2;3CELLS:1[2]12'4,2[2]15'2,3[1]33'6;4MOVES:1<5[2]@232'>6[2]@488'>3[1]@4330'2,1<10[1]@2241'3"
    
    test = "06abcabcabc07"
    
    regex1 = re.compile('STATE[A-Za-z0-9-]+IS')
    res = regex1.findall(state_str)
    match_id = res[0][5:-2]
    
    regex2 = re.compile('IS[0-9]+')
    res = regex2.findall(state_str)
    nb_players = res[0][2::]
    
    regex3 = re.compile(';[0-9]+CELLS')
    res = regex3.findall(state_str)
    nb_cells = res[0][1:-5]
    
    regex4 = re.compile('[0-9]+\[[0-9]+\][0-9]+\'[0-9]')
    info_cells = regex4.findall(state_str)
    
    regex5 = re.compile('[0-9]+MOVES')
    res = regex5.findall(state_str)
    nb_moves = res[0][0:-5]
    
    regex6 = re.compile('([0-9]+([<>][0-9]+\[[0-9]+\]@[0-9]+\')+[0-9]+)')    
    info_moves = regex6.findall(state_str)                                      #Liste avec (infos de déplacement entre 2 cellules, truc qui sert à rien mais je vois pas comment faire autrement)

    
    
    regex7 = re.compile('[0-9]+(abc)+[0-9]+')
    tt = regex7.findall(test)
    
    
    print(info_moves)
    

    
    
    
decrypt_state()