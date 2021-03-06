# -*- coding: utf-8 -*-
from tkinter import *

def dessiner_terrain(c,Graphe):                                                 # c est un objet de type Canvas
    c.delete("all")
    listCellules = Graphe.listCellules
    listLignes = Graphe.listLignes
    listInfoTerrain = Graphe.listInfoTerrain
    listCouleurs=["#4628DC","#C82525","#D0D0D0"]

    
    
    offsetX = 100 # valeur de décalage en X
    offsetY = 100 # valeur de décalage en Y
    scaleX = (1/25) # agrandissement du plateau en X
    scaleY = (1/25) # agrandissement du plateau en Y
    
    c.create_rectangle(0 , 0 , 1000 , 800 , fill="#13084E") # Fond de la fenetre
    c.create_text(35,20,text="couleur bot: "+str(listInfoTerrain[2]),fill=listCouleurs[listInfoTerrain[2]],anchor="n")   # titre de la fentre (couleur du bot)

    #w.create_circle_arc(100, 120, 48, fill="green", outline="", start=275, end=305)
    #w.create_circle_arc(100, 120, 60, style="arc", outline="white", width=6, start=270-25, end=270+25)

    for j in range (listInfoTerrain[5]): # dessin des lignes
        #Couleur de la ligne
        if(listLignes[j].Cell1.couleur == listLignes[j].Cell2.couleur): # si les deux cellules formant la ligne sont de même couleur, alors la ligne est de la même couleur.
            couleurLigne=listCouleurs[listLignes[j].Cell1.couleur]
        else:
            couleurLigne=listCouleurs[-1] #sinon on met la couleur neutre (gris)
                
        c.create_line(listLignes[j].Cell1.x*scaleX+offsetX , listLignes[j].Cell1.y*scaleY+offsetY , listLignes[j].Cell2.x*scaleX+offsetX , listLignes[j].Cell2.y*scaleY+offsetY , fill=couleurLigne,width=3)

    for i in range (listInfoTerrain[4]): # dessin des cellules
        c.create_circle(listCellules[i].x*scaleX+offsetX, listCellules[i].y*scaleY+offsetY, (listCellules[i].radius)/4, fill=listCouleurs[listCellules[i].couleur], outline="#FCFCFC", width=2)
        c.create_text(listCellules[i].x*scaleX+offsetX,listCellules[i].y*scaleY+offsetY,text=str(listCellules[i].nboff),fill="white",anchor="s")
        c.create_text(listCellules[i].x*scaleX+offsetX,listCellules[i].y*scaleY+offsetY,text="I"*listCellules[i].prod,fill="white",anchor="n")
        c.create_text(listCellules[i].x*scaleX+offsetX,listCellules[i].y*scaleY+offsetY,text=str(round(listCellules[i].priorite[1]*100)/100),fill="black",anchor="e")

    
        
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle_arc = _create_circle_arc

"""
def main() :
    #window creation
    window = Tk() # Création de l'objet window (fenetre)
    #canvas creation
    w = Canvas(window , width=1000, height =500) # Création d'un Canvas à partir de la fenetre "window"
    w. pack ()

    init_str = "INIT013fe2e8-86df-4fa3-960d-a0a537849a68TO2[1];2;7CELLS:0(0,0)'100'30'8'I,1(0,5)'100'30'8'I,2(5,0)'100'30'8'I,3(5,5)'200'30'8'II,4(5,10)'100'30'8'I,5(10,5)'100'30'8'I,6(10,10)'100'30'8'I;6LINES:0@4800OF1,0@4800OF2,2@4700OF3,3@4700OF4,4@4800OF6,5@4800OF6"
    #init_str = "INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3"
    Map = init_pooo(init_str)

    print(Map.listLignes[1].Cell1.x)



    #main loop to allow interaction
    dessiner_terrain(w,Map)

    mainloop()  

                    
                     
if __name__ == '__main__':
    main()
"""
    



    
