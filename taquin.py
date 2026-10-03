import random
from tkinter import *

class Cellule :
    def __init__(self,valeur,suivant=None) :
        self.valeur=valeur
        self.suivant=suivant
class Pile :
    def __init__(self,valeur=None) :
        if valeur!=None :
            self.sommet=Cellule(valeur)
        else :
            self.sommet=None
    def est_vide(self) :
        return self.sommet==None
    def empiler(self,valeur) :
        self.sommet=Cellule(valeur,self.sommet)
    def depiler(self) :
        if not(self.est_vide()) :
            x=self.sommet
            self.sommet=x.suivant
            return x.valeur
        else :
            return None
class Taquin :
    def __init__(self) :
        self.tab=[0,1,2,3,4,5,6,7,8]
        self.mode_resolution=False
        self.pile=Pile()
    def est_gagnant(self) :
        return self.tab==[0,1,2,3,4,5,6,7,8]
    def indice(self,numero) :
        assert type(numero)==int,"numero doit être entier"
        assert numero<=8 and numero>=0, "numero de case non valide"
        i=0
        while self.tab[i]!=numero :
            i=i+1
        return i
    def __str__(self) :
        resultat=""
        for i in range(3) :
            for j in self.tab[i*3:i*3+3] :
                resultat+=f"{j} "
            resultat+="\n"
        return resultat


    def coups_possibles(self) :
        resultat=[]
        ligne1=self.tab[:3]
        ligne2=self.tab[3:6]
        ligne3=self.tab[6:]
        colonne1=self.tab[0:len(self.tab):3]
        colonne2=self.tab[1:len(self.tab):3]
        colonne3=self.tab[2:len(self.tab):3]
        tab2=[ligne1,ligne2,ligne3,colonne1,colonne2,colonne3]
        for i in tab2 :
            for j in range(len(i)-1) :
                if i[j+1]==0 :
                    resultat.append(i[j])
            for j in range(1,len(i)) :
                if i[j-1]==0 :
                    resultat.append(i[j])
        return resultat
    def est_possible(self,numero) :
        return (numero in self.coups_possibles())
    def jouer(self,numero) :
        if self.est_possible(numero) :
            i=self.indice(numero)
            j=self.indice(0)
            self.tab[j]=numero
            self.tab[i]=0
        if not(self.mode_resolution) :
            if not(self.pile.est_vide()) :
                x=self.pile.depiler()
                if x!=numero :
                    self.pile.empiler(x)
                    self.pile.empiler(numero)
            else :
                self.pile.empiler(numero)
    def melanger(self,n) :
        precedent=None
        i=0
        while i<n :
            possibilites=self.coups_possibles()
            choix=random.choice(possibilites)
            if choix!=precedent :
                self.jouer(choix)
                precedent=choix
                i+=1
    def resoudre(self) :
        self.mode_resolution=True
        while not(self.pile.est_vide()) :
            x=self.pile.depiler()
            self.jouer(x)
            self.afficher()
            #ou print(self) si onst dans le terminal
    def afficher(self) :
        cnv.delete("all")
        for i in range(3):
            for j in range(3):
                x, y=100*j, 100*i
                A, B, C=(x, y), (x+100, y+100), (x+50, y+50)
                if self.tab[3*i+j] != 0:
                    rect=cnv.create_rectangle(A, B, fill="royal blue")
                    txt=cnv.create_text(C, text=self.tab[3*i+j], fill="yellow")             
                else :
                    rect=cnv.create_rectangle(A, B, fill="gray")
def main_terminal() :
    T=Taquin()
    T.melanger(5)
    print(T)
    while not(T.est_gagnant()) :
        x=int(input("jouer un coup (1) ou resolution automatique(2) ou quitter le jeu(3) ?"))
        if x==2 :
            T.resoudre()
        elif x==1 :
            numero=int(input("quel numéro ?"))
            T.jouer(numero)
            print(T)
        elif x==3 :
            return
        else : 
            print("autre valeur que 1, 2 ou 3")


T=Taquin()
T.melanger(10)       
fenetre=Tk()
cnv=Canvas(fenetre, width=300, height=300, bg='gray70')
T.afficher()
bouton=Button(fenetre, text="Quitter", command=fenetre.quit)
bouton2=Button(fenetre, text="Resolution automatique", command=T.resoudre)
s = Spinbox(fenetre, from_=1, to=8)
def jouer_bouton_clavier(event) :
    numero=int(event.keysym)
    T.jouer(numero)
    T.afficher()
cnv.focus_set()
def jouer_bouton() :
    numero=int(s.get())
    T.jouer(numero)
    T.afficher()
bouton3=Button(fenetre, text="Jouer", command=jouer_bouton)
def nouveau() :
    T=Taquin()
    T.melanger(10)
    T.afficher()
bouton4=Button(fenetre, text="Nouveau", command=nouveau)
for i in range(1,9) :
    cnv.bind(f"<KeyPress-{i}>", jouer_bouton_clavier)
label = Label(fenetre, text="Texte par défaut", bg="yellow")
bouton.pack()
bouton2.pack()
bouton4.pack()
cnv.pack()
s.pack()
bouton3.pack()
if T.est_gagnant() :
    label.pack()

fenetre.mainloop()
