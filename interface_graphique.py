from AmbianceTeam import *
from recup_terrain import *

init_str = "INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3"

listInfoTerrain=[]
listCellules=[]
listLignes=[]

listInfoTerrain = init_terrain(init_str,listCellules,listLignes,listInfoTerrain)

print(listLignes[1].Cell1.x)