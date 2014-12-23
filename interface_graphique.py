# -*- coding: utf-8 -*-
from AmbianceTeam import *
from recup_terrain import *
from tkinter import *

def dessiner_terrain(w,Graphe):
    listCellules = Graphe.listCellules
    listLignes = Graphe.listLignes
    listInfoTerrain = Graphe.listInfoTerrain
    listCouleurs=["#D0D0D0","#4628DC","#C82525"]
    
    offsetX = 50 # valeur de décalage en X
    offsetY = 50 # valeur de décalage en Y
    scaleX = 2 # agrandissement du plateau en X
    scaleY = 2 # agrandissement du plateau en Y
    
    w.create_rectangle(0 , 0 , 1000 , 500 , fill="#13084E") # Fond de la fenetre

    #w.create_circle_arc(100, 120, 48, fill="green", outline="", start=275, end=305)
    #w.create_circle_arc(100, 120, 60, style="arc", outline="white", width=6, start=270-25, end=270+25)

    for j in range (listInfoTerrain[5]): # dessin des lignes
        #Couleur de la ligne
        if(listLignes[j].Cell1.etat == listLignes[j].Cell2.etat): # si les deux cellules formant la ligne sont de même couleur, alors la ligne est de la même couleur.
            couleurLigne=listCouleurs[listLignes[j].Cell1.etat]
        else:
            couleurLigne=listCouleurs[0] #sinon on met la couleur neutre (gris)
                
        w.create_line(listLignes[j].Cell1.x*scaleX+offsetX , listLignes[j].Cell1.y*scaleY+offsetY , listLignes[j].Cell2.x*scaleX+offsetX , listLignes[j].Cell2.y*scaleY+offsetY , fill=couleurLigne,width=3)

    for i in range (listInfoTerrain[4]): # dessin des cellules
        
        w.create_circle(listCellules[i].x*scaleX+offsetX, listCellules[i].y*scaleY+offsetY, (listCellules[i].radius)*15, fill=listCouleurs[listCellules[i].etat], outline="#FCFCFC", width=2)
        w.create_text(listCellules[i].x*scaleX+offsetX,listCellules[i].y*scaleY+offsetY,text=str(listCellules[i].nboff),fill="white",anchor="s")
        w.create_text(listCellules[i].x*scaleX+offsetX,listCellules[i].y*scaleY+offsetY,text="I"*listCellules[i].prod,fill="white",anchor="n")
    
    
        
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle_arc = _create_circle_arc

#window creation
window = Tk() # Création de l'objet window (fenetre)
#canvas creation
w = Canvas(window , width=1000, height =500) # Création d'un Canvas à partir de la fenetre "window"
w. pack ()

init_str = "INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3"

Map = init_pooo(init_str)

print(Map.listLignes[1].Cell1.x)



#main loop to allow interaction
dessiner_terrain(w,Map)

mainloop()


    
