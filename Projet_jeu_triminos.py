"""

Jeu de Triminos
Par Laura Brisoux et Thomas Desrumeaux
CPG2A Promo 64 
2020

"""
##Bibliothèques
import math
from tkinter import *
import random
import tkinter.font as tkFont

## Variables

Width = 600 #Largeur du plateau de jeu
Height = 600 #Hauteur du plateau de jeu

nombre_ligne = 10 #Nombre de lignes horizontales dans le plateau de jeu

Hauteur_triangle = Height/nombre_ligne #Calcul de la hauteur d'un trimino
cote_triangle = Hauteur_triangle*2/(3**0.5)


Width_canvas_selection = 120 #Largeur de l'affichage du trimino sélectionné
Height_canvas_selection = 120 #Hauteur de l'affichage du trimino sélectionné

trimino_selectionne = [[],0,0] #Définition du trimino sélectionné


Nombre_Joueurs = int(input("Nombre de joueurs :")) 


Pile = [] #Pioche
Plateau = [] #Variable comportant les triminos posés sur le plateau
Tour = 0 #C'est le tour du joueur n. Si Tour = 0 alors le jeu n'est pas lancé 
Triminos_distribues = 5 

color=['yellow','blue','green','red','orange','brown','purple','pink','black'] #Liste des couleurs possible sur un trimino


fenetre = Tk() #Création de la fenêtre
fenetre.resizable(False,False) #Fenêtre non modifiable en taille 
fenetre.title("Triminos Game")

LabelText = StringVar() #Texte d'information

font = tkFont.Font(size=12, weight='bold') #Police du texte affiché



def generer_pile(Nombre_triminos = Nombre_Joueurs*10): #Créée une liste comportant n triminos générés aléatoirement(C'est la pioche)
    Pile.clear()
    for i in range(Nombre_triminos):
        L=[]
        for j in range(3):
            L.append(color[random.randint(0,len(color)-1)])
        Pile.append(L)
    random.shuffle(Pile)


def Position_dans_repere(x,y): #Détermination position dans le repère non orthogonal
    Y = math.floor((Height-y)/Hauteur_triangle)
    X = math.floor((x-math.tan(math.pi/6)*(Height-y))/cote_triangle) 
    return(X,Y)

def placer_trimino(event, x = 0,y = 0): #Placement du trimino séléctionné après un clic de souris
    global trimino_selectionne
    if (x,y) == (0,0): #Si c'est le joueur qui place un trimino
        if Tour == 0: #Si le joueur essaye de placer un trimino alors que la partie n'a paas commencé
            LabelText.set(Erreur.e)
            return
        x,y = event.x, event.y #Aquisition de la position de la souris
        if trimino_selectionne[0] == []: #Si le joueur n'a pas séléctionné de trimino
            LabelText.set(Erreur.c)
            return
        X,Y = Position_dans_repere(x,y) #Détermination de la position du trimino dans le repère
        for i in range (0,len(Plateau)): 
            if (X,Y) == Plateau[i][1] and trimino_selectionne[1]%2 == Plateau[i][0][1]%2: #Vérification si la case choisie est libre
                LabelText.set(Erreur.a)
                return
        if verification_placement_trimino(trimino_selectionne,X,Y,Plateau) != True: #Vérification de la correspondance des couleurs
            LabelText.set(Erreur.d)
            return
        triangle1,triangle2 = position_centre_triangle(X,Y) #Calcul du centre des triangles de la case séléctionée dans le repère
        centre = distance_entre_deux_points(x,y,triangle1,triangle2) #Détermination du triangle souhaité entre les deux présents dans le repère
    else: #Placement du trimino de départ au centre du plateau de jeu
        trimino_selectionne = [Pile.pop(),0,0]
        X,Y = Position_dans_repere(x,y)
        triangle1,triangle2 = position_centre_triangle(X,Y)
        centre = (triangle1,True)
    if (centre[0][1] <= Height and centre[0][0] <= Width) and ((centre[1] == False and trimino_selectionne[1]%2 == 1) or (centre[1] == True and trimino_selectionne[1]%2 == 0)): #Vérification si le trimino ne sort pas du plateau et que le trimino est placé dans le bon sens
        dessiner_triminos(centre[0][0],centre[0][1],trimino_selectionne[0],trimino_selectionne[1],canvas,cote_triangle) #Affichage du trimino sur le plateau
        Plateau.append((trimino_selectionne,(X,Y))) #Ajout du trimino dans le plateau
        trimino_selectionne = [[],0] #Désélection du trimino
        piocher() #Le joueur picohe pour garder 5 triminos en main
        affciher_trimino_selectionne(trimino_selectionne)
    else:
        LabelText.set(Erreur.a)
    
def verification_placement_trimino(trimino,X,Y,Plateau): #Vérification de la correspondance des couleurs et si le trimino est bien placé à côté d'un autre 
    A_cote_trimino = False
    Score = 0
    if trimino[1]%2 == 0: #Si le trimino est placé à l'endroit
        for i in range(0,len(Plateau)):
            if Plateau[i][0][1]%2 == 1: #On vérifie juste les triminos qui sont à l'envers
                if Plateau[i][1] == (X,Y): #Vérifiaction avec le trimino qui a la même coordonée dans le repère
                    A_cote_trimino = True
                    Score += 30
                    if Plateau[i][0][0][(Plateau[i][0][1]-1)%3] != trimino[0][(trimino[1]-1)%3]:
                        return 
                if Plateau[i][1] == (X-1,Y): #Trimino à gauche
                    A_cote_trimino = True
                    Score += 30
                    if Plateau[i][0][0][(Plateau[i][0][1])%3] != trimino[0][(trimino[1])%3]:
                        return
                if Plateau[i][1] == (X,Y-1): #Trimino en dessous
                    A_cote_trimino = True
                    Score += 30
                    if Plateau[i][0][0][(Plateau[i][0][1]+1)%3] != trimino[0][(trimino[1]+1)%3]:
                        return
                        
    else: #Si le trimino est placé à l'envers
        for i in range(0,len(Plateau)):
            if Plateau[i][0][1]%2 == 0:
                if Plateau[i][1] == (X,Y): #Vérifiaction avec le trimino qui a la même coordonée dans le repère
                    A_cote_trimino = True
                    Score += 30
                    if Plateau[i][0][0][(Plateau[i][0][1]-1)%3] != trimino[0][(trimino[1]-1)%3]:
                        return 
                if Plateau[i][1] == (X+1,Y): #Trimino à droite
                    A_cote_trimino = True
                    Score += 30
                    if Plateau[i][0][0][(Plateau[i][0][1])%3] != trimino[0][(trimino[1])%3]:
                        return
                if Plateau[i][1] == (X,Y+1): #Trimino au dessus
                     A_cote_trimino = True
                     Score += 30
                     if Plateau[i][0][0][(Plateau[i][0][1]+1)%3] != trimino[0][(trimino[1]+1)%3]:
                        return
    Joueurs[trimino[2]-1].score += Score #Augmentation du score du joueur
    Joueurs[trimino[2]-1].Label.set(str(Joueurs[trimino[2]-1].name) + "    Score : " + str(Joueurs[trimino[2]-1].score))#Actualisation de l'affichage du score
    return A_cote_trimino
    
    
def distance_entre_deux_points(sourisx,sourisy,point1,point2): #Détermination du triangle souhaité entre les deux présents dans le repère
    dist1=math.sqrt((point1[0]-sourisx)**2+(point1[1]-sourisy)**2)
    dist2=math.sqrt((point2[0]-sourisx)**2+(point2[1]-sourisy)**2)
    if dist1<dist2:
        x=point1[0]
        y=point1[1]
        a_plat = True
    else:
        x=point2[0]
        y=point2[1]
        a_plat = False
    return ((x,y),a_plat)
    

def position_centre_triangle(X,Y):#Calcul du centre des triangles de la case séléctionée dans le repère
    y = math.floor(Height-Y*Hauteur_triangle)
    x = math.floor(Y*cote_triangle/2 + X*cote_triangle)
    return (x + cote_triangle/2,y - cote_triangle*3**(1/2)/6),(x + cote_triangle,y-Hauteur_triangle + cote_triangle*3**(1/2)/6)
    

def dessiner_triminos(x,y,color,rotation,can,size): #On dessine un trimino dans le canvas choisi, à la taille et position demandée
    cote = size
    if color == []:
        return
    if rotation%2==0: #Trimino à l'endroit
        can.create_polygon(x,y,x,y-cote*(3**0.5)/3,x-cote/2,y+(3**0.5)*cote/6, outline='black', fill=color[(0-int(rotation/2))%3], width=1)
        can.create_polygon(x,y,x-cote/2,y+(3**0.5)*cote/6,x+cote/2,y+(3**0.5)*cote/6, outline='black', fill=color[(1-int(rotation/2))%3], width=1)
        can.create_polygon(x,y,x,y-cote*(3**0.5)/3,x+cote/2,y+(3**0.5)*cote/6, outline='black', fill=color[(2-int(rotation/2))%3], width=1)
        
    else: #Trimino à l'envers
        can.create_polygon(x,y,x,y+cote*(3**0.5)/3,x-cote/2,y-(3**0.5)*cote/6, outline='black', fill=color[(0-int(rotation/2))%3], width=1)
        can.create_polygon(x,y,x,y+cote*(3**0.5)/3,x+cote/2,y-(3**0.5)*cote/6, outline='black', fill=color[(1-int(rotation/2))%3], width=1)
        can.create_polygon(x,y,x-cote/2,y-(3**0.5)*cote/6,x+cote/2,y-(3**0.5)*cote/6, outline='black', fill=color[(2-int(rotation/2))%3], width=1)
    canvas.create_rectangle(3,3,Width,Height,width = 3)
    
    if can == "canvas_selection": 
        can.create_rectangle(3,3,Width_canvas_selection,Height_canvas_selection,width = 3)

    
def affciher_trimino_selectionne(trimino_selectionne): #Affichage du trimino séléctionné dans le tableau de sélection
    canvas_selection.create_rectangle(0,0,Width_canvas_selection,Height_canvas_selection, fill = "white",outline='white')
    canvas_selection.create_rectangle(3,3,Width_canvas_selection,Height_canvas_selection,width = 3)
    if trimino_selectionne[0] == []:
        return
    else:
        dessiner_triminos(Width_canvas_selection/2 + 1.5,Height_canvas_selection/2 + 1.5,trimino_selectionne[0],trimino_selectionne[1],canvas_selection,Width_canvas_selection/1.5)
    
    
def rotation_gauche(a): #Rotation du trimino sélectionné dans le sens trigo
    global trimino_selectionne
    trimino_selectionne[1] = (trimino_selectionne[1]+1)%6
    affciher_trimino_selectionne(trimino_selectionne)
    
def rotation_droite(a): #Rotation du trimino sélectionné dans le sens horaire
    global trimino_selectionne
    trimino_selectionne[1] = (trimino_selectionne[1]-1)%6
    affciher_trimino_selectionne(trimino_selectionne)
    
def piocher(): #Le joueur pioche un trimino
    if Tour == 0: 
        LabelText.set(Erreur.e)
        return
    if len(Pile) == 0:
        passer_tour()
        return
    Joueurs[Tour-1].main.append(Pile.pop())
    Joueurs[Tour-1].Actualiser_main()
    passer_tour()
    

def passer_tour(): #Le joueur finit son tour et c'est le tour du prochain joueur
    global Tour
    if trimino_selectionne[0] != []: #On rend le trimino sélectionné au joueur correspondant
        Joueurs[trimino_selectionne[2]-1].main.append(trimino_selectionne[0])
        trimino_selectionne[0] = []
        affciher_trimino_selectionne(trimino_selectionne)
    if len(Joueurs[Tour-1].main) == 0: #Condition de fin: Si l'un des joueur à sa main vide
        Max_score = [Joueurs[0].name,Joueurs[0].score]
        for i in range (1,len(Joueurs)): #Détermination du gagnant en fonction des points
            if Joueurs[i].score == Max_score[1]:
                 Max_score[0] = Max_score[0] + " et " + Joueurs[i].name
            elif Joueurs[i].score > Max_score[1]:
                Max_score = [Joueurs[i].name,Joueurs[i].score]
        LabelText.set("Victoire de : " + Max_score[0])
        Tour = 0
        return
    Tour = (Tour+1)%(Nombre_Joueurs+1)
    if Tour == 0:
        Tour = 1
    LabelText.set("C'est au tour de " + str(Joueurs[Tour-1].name) + " de jouer")
    actualiser_mains()

def commencer_partie(): #On commence une nouvelle partie en vidant la pioche,le plateau, les main, les scores et on redonne des triminos aux joueurs
    global Tour
    Tour = 0
    trimino_selectionne = [[],0,0]
    affciher_trimino_selectionne(trimino_selectionne)
    Plateau.clear()
    creer_plateau(nombre_ligne,Height,Width)
    generer_pile()
    distribution()
    placer_trimino(None, x=Width/2,y=Height/2)
    Tour = random.randint(1,Nombre_Joueurs)
    LabelText.set("C'est au tour de " + str(Joueurs[Tour-1].name) + " de jouer")
    actualiser_mains()

def actualiser_mains(): #On actualise les mains des joueurs
    for i in range (0,Nombre_Joueurs):
        Joueurs[i].Actualiser_main()
    
def creer_plateau(ligne,hauteur,largeur): #Création des lignes du plateau de jeu
    canvas.create_rectangle(0,0,Width,Height, outline = "white", fill = "white")
    if largeur > hauteur:
        iteration = 2*int(largeur/cote_triangle)+1
    else:
        iteration = 2*int(hauteur/(Hauteur_triangle))+1
#creer_repere
    # for i in range(0,iteration):
    #     canvas.create_line(i*cote_triangle/2,hauteur-i*Hauteur_triangle,largeur,hauteur-i*Hauteur_triangle,fill = 'red',width = 5)
    #     canvas.create_line(i*cote_triangle,hauteur,nombre_ligne*0.5*cote_triangle + i*cote_triangle,0,fill = 'red',width = 5)
#creer_grille
    for i in range(0,ligne+1):
        canvas.create_line(0,i*hauteur/ligne,largeur,i*hauteur/ligne)
    for i in range(0,iteration):
        canvas.create_line(0,i*2*Hauteur_triangle - (nombre_ligne%2)*Hauteur_triangle,i*cote_triangle - (nombre_ligne%2)*cote_triangle/2,0)
        canvas.create_line(i*cote_triangle,hauteur,0,hauteur-i*2*Hauteur_triangle)
    canvas.create_rectangle(3,3,largeur,hauteur,width = 3) #contour plateau
    canvas_selection.create_rectangle(3,3,Width_canvas_selection,Height_canvas_selection,width = 3) #contour canvas_selection


canvas = Canvas(fenetre, width=Width, height=Height, bg="#ffffff") #création du plateau de jeu
canvas.pack(side = "left")
Label(fenetre, text = "Trimino séléctionné", font = font).pack(side = "top") #Affichage de texte
canvas_selection = Canvas(fenetre, width=Width_canvas_selection, height=Height_canvas_selection, bg="#ffffff")#création du tableau de sélection
canvas_selection.pack(side = "top")


Information = Label(fenetre,text = LabelText, textvariable = LabelText, font = font, foreground = "red").pack(side = "top") #Affichage de texte d'information
Button(fenetre, text = "Commencer une nouvelle partie", command = commencer_partie).pack(side = "bottom",pady=5) #Création bouton
Button(fenetre, text = "Piocher", command = piocher).pack(side = "bottom",pady=5) #Création bouton

## Définition Joueurs    
class Joueur:
    def __init__(self,numero, name): #determination des caractéristiques d'un joueur
        self.name = str(name)
        self.main = []
        self.numero = numero
        self.score = 0
        self.Label = StringVar()
        self.Label.set(str(self.name) + "    Score : " + str(self.score)) #affichage du nom et du score du joueur
        self.canvas = Canvas(fenetre, width=cote_triangle*Triminos_distribues, height = Hauteur_triangle*1.2, bg="#ffffff")
        self.name_text = Label(fenetre,textvariable = self.Label, font = font)
        self.canvas.bind("<Button 1>", self.selectionner_triminos_main) 
        
    def Presentation(self):
        print("\nJoueur " + str(self.name) +" numéro " + str(self.numero) + " a la main suivante:")
        print(self.main)
        
    def Afficher_canvas(self): #création de la case où la main s'affiche
        self.name_text.pack(side = "top")
        self.canvas.pack(side = "top")
        
    def Actualiser_main(self): #on efface l'ancienne main puis on affiche la nouvelle main
        self.canvas.create_rectangle(0,0,cote_triangle*Triminos_distribues,Hauteur_triangle*1.2, outline = "white", fill = "white")
        if len(self.main) <= Triminos_distribues:
            cote = cote_triangle
        else:
            cote = cote_triangle*Triminos_distribues/len(self.main)
        for i in range (0,len(self.main)):
            dessiner_triminos(1.5+cote/2 + i*cote,1.5+(Hauteur_triangle*1.2-Hauteur_triangle)/2 + cote_triangle*(3**0.5)/3,self.main[i],0,self.canvas,cote)
        if Tour == self.numero:
            self.canvas.create_rectangle(3,3,cote_triangle*Triminos_distribues,Hauteur_triangle*1.2,width = 3, outline = 'red') #contour plateau
        else:
            self.canvas.create_rectangle(3,3,cote_triangle*Triminos_distribues,Hauteur_triangle*1.2,width = 3)
            
    def numero_trimino_selectionne(self,x): #convertir l'endroit où on clique en numéro entre 0 et n pour savoir quel est le trimino que l'utilisateur veut choisir
        if len(self.main) >= Triminos_distribues:
            return int(x/(cote_triangle*Triminos_distribues/len(self.main)))
        else:
            return int(x/cote_triangle)
        
    def selectionner_triminos_main(self,event):
        global trimino_selectionne
        if Tour != self.numero: #si le joueur veut jouer mais que ce n'est pas son tour, aucun trimino n'est selectionné danns sa main
            return
        selection = self.numero_trimino_selectionne(event.x) #correspond au n-ième trimino qu'on a selectionné
        Taille_main = len(self.main)
        if trimino_selectionne[0] != []: #si on a déja selectionné un trimino et qu'on veut en choisir un autre
            self.main.append(trimino_selectionne[0]) #on remet le trimino dans la main du joueur
            trimino_selectionne[0] = [] #le trimino selectionné est remplacé par un blanc
            affciher_trimino_selectionne(trimino_selectionne) #on supprime le trimino dans la case
            self.Actualiser_main()
        if selection >= Taille_main: #si on selectionne un endroit où il n'y a pas de trimino
            LabelText.set(Erreur.c)
            return
        else:
            trimino_selectionne = [self.main.pop(selection),0,self.numero] #on retire le trimino choisi de la main du joueur
            affciher_trimino_selectionne(trimino_selectionne) #on l'affiche dans la case
            self.Actualiser_main()



Joueurs = list() #pas de joueur au début

def Creation_joueur(): #créée chaque joueur avec un nom et une main vide
    for j in range(0,Nombre_Joueurs):
        Nom = str(input("Entrez le nom du joueur " + str(j+1) + ":")) 
        Joueurs.append(Joueur(j+1,Nom))
        Joueurs[j].Afficher_canvas()
        Joueurs[j].Actualiser_main()

def distribution(): #distribution des triminos (main) à chaque joueur et attribution d'un score nul
    for j in range(0,Nombre_Joueurs):
        Joueurs[j].main = []
        for i in range (Triminos_distribues):
            Joueurs[j].score = 0
            Joueurs[j].Label.set(str(Joueurs[j].name) + "    Score : " + str(Joueurs[j].score))
            Joueurs[j].main.append(Pile.pop(0))
    Presenter_joueur()

def Presenter_joueur(): #affichage de tous les joueurs et de leur jeu
    for k in range(0,Nombre_Joueurs):
        Joueurs[k].Actualiser_main()

Creation_joueur()


##

class Erreur:
    a = "Impossible de placer le Trimino ici!"
    b = "Un trimino est déja placé ici!"
    c = "Aucun Trimino séléctionné!"
    d = "Les couleurs ne correspondent pas!"
    e = "Il faut d'abord commencer une nouvelle partie!"

##Paramètres fenetre
creer_plateau(nombre_ligne,Height,Width)
affciher_trimino_selectionne(trimino_selectionne)
canvas.bind("<Button 1>", placer_trimino)    
fenetre.bind("<Left>", rotation_gauche)
fenetre.bind("<Right>", rotation_droite)   

##
fenetre.mainloop()

print("\033[1;31;40m Thanks for playing! \033[0m")