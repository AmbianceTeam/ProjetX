import re


init_str = "INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3"

# Recuperation de l'id du match

regex1 = re.compile('INIT[A-Za-z0-9-]+TO')
resultat = regex1.findall(init_str)
match_id=resultat[0][4:-2]

regex2 = re.compile('TO[0-9]+')
resultat  = regex2.findall(init_str)
nb_players = resultat[0][2::]


regex3 = re.compile('\[[0-9]+\]')
resultat  = regex3.findall(init_str)
no_color = resultat[0][1:-1]

regex4 = re.compile(';[0-9]+;')
resultat  = regex4.findall(init_str)
speed = resultat[0][1:-1]

regex5 = re.compile(';[0-9]+CELLS')
resultat  = regex5.findall(init_str)
nb_cells = resultat[0][1:-5]

regex6 = re.compile('[0-9]+\([0-9]+,[0-9]+\)\'[0-9]+\'[0-9]+\'[0-9]+\'I+')
resultat  = regex6.findall(init_str)

for i in range (nb_cells):
    resultat[i]

nb_cells = resultat[0][1:-5]



print(resultat)
