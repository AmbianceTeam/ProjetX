from AmbianceTeam import *
from recup_terrain import *
from tkinter import *

init_str = "INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3"

listInfoTerrain=[]
listCellules=[]
listLignes=[]

listInfoTerrain = init_terrain(init_str,listCellules,listLignes,listInfoTerrain)

print(listLignes[1].Cell1.x)

#function definition
def draw_point( canvas , x , y , color="black"):
    canvas.create_rectangle (x , y , x , y , fill=color , width=0)

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

#window creation
window = Tk()
#canvas creation
w = Canvas(window , width=400, height =400)
w. pack ()

#drawing functions
w.create_circle(100, 120, 50, fill="blue", outline="#DDD", width=4)
w.create_line(0 , 100 , 200 , 0 , fill="red")
w.create_rectangle(50 , 25 , 150 , 75 , fill="blue")

#main loop to allow interaction
mainloop ()





#usage
draw_point (w,10 ,10)
    
