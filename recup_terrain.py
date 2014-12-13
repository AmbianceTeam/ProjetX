# -*- coding: utf-8 -*-
import re
from AmbianceTeam import *


def init_terrain(init_str,listCellules,listLignes,listInfoTerrain):
    
    
    regex1 = re.compile('INIT[A-Za-z0-9-]+TO') # Recuperation de l'id du match
    resultat = regex1.findall(init_str)
    match_id=resultat[0][4:-2]
    
    regex2 = re.compile('TO[0-9]+') # Recuperation de nb joueurs
    resultat  = regex2.findall(init_str)
    nb_players = int(resultat[0][2::])
    
    
    regex3 = re.compile('\[[0-9]+\]') # Recuperation de numero de couleur
    resultat  = regex3.findall(init_str)
    no_color = int(resultat[0][1:-1])
    
    regex4 = re.compile(';[0-9]+;') # Recuperation de la vitesse de jeu
    resultat  = regex4.findall(init_str)
    speed = int(resultat[0][1:-1])
    
    regex5 = re.compile(';[0-9]+CELLS') # Recuperation du nombre de cellules
    resultat  = regex5.findall(init_str)
    nb_cells = int(resultat[0][1:-5])
    
    regex5_2 = re.compile(';[0-9]+LINES') # Recuperation du nombre de lignes
    resultat  = regex5_2.findall(init_str)
    nb_lines = int(resultat[0][1:-5])
    
    listInfoTerrain = [match_id,nb_players,no_color,speed,nb_cells,nb_lines]
    
    
    
    regex6 = re.compile('[0-9]+\([0-9]+,[0-9]+\)\'[0-9]+\'[0-9]+\'[0-9]+\'I+') 
    cellules_init  = regex6.findall(init_str)
    # cellules_init est une liste contenant toutes les infos sur les cellules. exemple: [ "1(23,9)'2'30'8'I" , "2(41,55)'1'30'8'II" , "3(23,103)'1'20'5'I" ]
    
    # Boucle qui va successivement traiter les elements de la liste "cellules_init"
    for i in range (nb_cells): #Recuperation et instanciation des cellules 

        regex7 = re.compile('[0-9]+\(') # Recuperation de l'ID de la cellule
        id_cellule  = regex7.findall(cellules_init[i])
        id_cellule  = int(id_cellule[0][:-1])
        
        regex8 = re.compile('\([0-9]+,') # Recuperation de l'abscisse de la cellue
        x  = regex8.findall(cellules_init[i])
        x  = int(x[0][1:-1])
        
        regex9 = re.compile(',[0-9]+\)') # Recuperation de l'ordonnee de la cellule
        y  = regex9.findall(cellules_init[i])
        y  = int(y[0][1:-1])
        
        regex10 = re.compile('\)\'[0-9]+\'') # Recuperation du rayon de la cellule
        radius  = regex10.findall(cellules_init[i])
        radius  = int(radius[0][2:-1])
        
        regex11 = re.compile('[0-9]+\'[0-9]+\'[0-9]+') # Recuperation du nombre maximum d'unité offensive 
        offsize  = re.compile('\'[0-9]+\'').findall(regex11.findall(cellules_init[i])[0])
        offsize  = int(offsize[0][1:-1])
        
        regex12 = re.compile('\'[0-9]+\'') # Recuperation du nombre maximum d'unité defensive
        defsize = regex12.findall(cellules_init[i])
        defsize = int(defsize[1][1:-1])
        
        regex13 = re.compile('\'I+') # Recuperation de la vitesse de production d'unité 
        prod = regex13.findall(cellules_init[i])
        prod = len(prod[0][1:]) # La vitesse de production est represente par des "I" , on compte donc le nombre de "I" avec un len()
        
        listCellules.append(Cellule(id_cellule,offsize,defsize,radius,x,y,prod)) #instanciation des Cellules

    
    
    regex14 = re.compile('[0-9]+@[0-9]+OF[0-9]+')
    lignes_init  = regex14.findall(init_str)

    
    for j in range (nb_lines): #Recuperation et instanciation des lignes
        
        regex15 = re.compile('[0-9]+@') # Recuperation de l'ID de la 1ere cellule qui forme la ligne 
        idcell1 = regex15.findall(lignes_init[j])
        idcell1 = int(idcell1[0][:-1])
        
        regex16 = re.compile('@[0-9]+OF') # Recuperation de la distance entre les deux cellules (en ms)
        dist = regex16.findall(lignes_init[j])
        dist = dist[0][1:-2]
        
        regex17 = re.compile('OF[0-9]+') # Recuperation de l'ID de la 2eme cellule qui forme la ligne 
        idcell2 = regex17.findall(lignes_init[j])
        idcell2 = int(idcell2[0][2:])
        
        listLignes.append(Lines(listCellules[idcell1-1],listCellules[idcell2-1],dist)) #instanciation des Lignes
        
        
    return listInfoTerrain
        
     
