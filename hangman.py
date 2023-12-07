 #pyinstaller Pendu.py --onefile --noconsole --add-data "ukenglish.txt;." --add-data "liste_francais.txt;." --add-data "the_icon.ico;." --icon=the_icon.ico --add-data "button_sound.mp3;." --add-data "keyboard_sound.mp3;." --add-data "lose_sound.mp3;." --add-data "win_sound.mp3;."

##----- Importation des Modules -----##
import random
from tkinter import *
from tkinter import Button
from pathlib import Path
import sys
import os
from pygame import mixer

mixer.init()

# Récupérer le chemin relatif de l'exécutable
if getattr(sys, 'frozen', False):
    # Si le script est empaqueté en tant qu'exécutable
    application_path = sys._MEIPASS
else:
    # Si le script est exécuté normalement
    application_path = os.path.dirname(os.path.abspath(__file__))

# Utiliser ce chemin pour accéder aux fichiers texte
path_to_liste_francais = os.path.join(application_path, "liste_francais.txt")
path_to_ukenglish = os.path.join(application_path, "ukenglish.txt")
Icon = Path(__file__).parent / "the_icon.ico"
button_sound_path = Path(__file__).parent / "button_sound.mp3"
button_sound = mixer.Sound(button_sound_path)
keyboard_sound_path = Path(__file__).parent / "keyboard_sound.mp3"
keyboard_sound = mixer.Sound(keyboard_sound_path)
win_sound_path = Path(__file__).parent / "win.mp3"
win_sound = mixer.Sound(win_sound_path)
lose_sound_path = Path(__file__).parent / "lose_sound.mp3"
lose_sound = mixer.Sound(lose_sound_path)


fen_accueil = None
fen = None
difficile_fen = None
moyen_fen = None
facile_fen = None
texte_reponse1 = None
texte_erreurs1 = None

##----- Création de la fenêtre -----##

fen = Tk()
fen.title('Pendu')
fen.iconbitmap(Icon)



def facile():
    button_sound.play()
    global facile_fen
    global moyen_fen
    global difficile_fen
    global fen_accueil
    difficile_fen = False
    moyen_fen = False
    facile_fen = True
    fen_accueil = False

    ##----- Fonction -----##
    global mot_choisi
    global la_taille
    global liste
    global mot_cherche
    global mot_affiche
    global commence
    global erreurs
    global ancien_mot
    mot_choisi=''
    la_taille = 100
    liste = ''
    mot_cherche = ''
    mot_affiche = ''
    commence = False  # Variable pour suivre si le jeu a commencé
    erreurs = 0
    ancien_mot = []

    def aleatoire_mot(event):
        button_sound.play()
        dessin.delete("boutton_commencer")
        with open(path_to_liste_francais, 'r', encoding='iso-8859-1') as fichier:
            mots = fichier.readlines()
            global mot_choisi
            mot_choisi = random.choice(mots).strip()  # strip() pour supprimer les sauts de ligne
            for lettre in mot_choisi:
                if lettre == " ":
                    mot_choisi = random.choice(mots).strip()  # strip() pour supprimer les sauts de ligne
            global mot_cherche
            mot_cherche = mot_choisi.lower()
            global la_taille
            la_taille = taille_du_mot(mot_choisi)
            afficher_mot(mot_choisi.lower(), taille_du_mot(mot_choisi))  # Convertir le mot en minuscule pour l'affichage sinon ya probleme
        global commence
        commence = True
    path_to_liste_francais = os.path.join(application_path, "liste_francais.txt")
    path_to_ukenglish = os.path.join(application_path, "ukenglish.txt")

    def taille_du_mot(mot):
        longueur = len(mot)
        if longueur < 7:
            return 100
        if 11 > longueur > 9 :
            return 60
        if 12 >= longueur >= 11 :
            return 50
        if longueur > 12 :
            return 40
        else :
            return 70


    def afficher_mot(mot, taille):
        global mot_affiche, partie1
        mot_affiche = ''
        lettres_a_afficher = set()
        global mot_choisi
        if len(mot_choisi) < 4:
            for i, char in enumerate(mot):
                if char != ' ' and random.random() < 0.40:
                    lettres_a_afficher.add(i)  # Ajouter l'indice de la lettre à afficher

            for i, char in enumerate(mot):
                if i in lettres_a_afficher or char == ' ':
                    mot_affiche += char + ' '
                else:
                    mot_affiche += '_ '
        elif len(mot_choisi) > 10:
            for i, char in enumerate(mot):
                if char != ' ' and random.random() < 0.60:
                    lettres_a_afficher.add(i)  # Ajouter l'indice de la lettre à afficher

            for i, char in enumerate(mot):
                if i in lettres_a_afficher or char == ' ':
                    mot_affiche += char + ' '
                else:
                    mot_affiche += '_ '
        else:
            for i, char in enumerate(mot):
                if char != ' ' and random.random() < 0.50:
                    lettres_a_afficher.add(i)  # Ajouter l'indice de la lettre à afficher

            for i, char in enumerate(mot):
                if i in lettres_a_afficher or char == ' ':
                    mot_affiche += char + ' '
                else:
                    mot_affiche += '_ '
        if partie1:
            dessin.itemconfigure(texte_reponse, text=mot_affiche, font=('Arial', taille))
        else:
            dessin.itemconfigure(texte_reponse1, text=mot_affiche, font=('Arial', taille))



    def clavier_pressed(event):
        keyboard_sound.play()
        global liste
        global commence
        global erreurs, partie1

        if commence == True:
            lettre = event.char  # Convertir la lettre en minuscule
            #Ignorer la touche shift pour mettre des lettres en majuscules
            if event.keysym == 'Shift_R' or event.keysym == 'Shift_L':
                return 1
            global liste
            if event.char in liste :
                dessin.delete("lettre_deja_clique")
                message = dessin.create_text(400, 300, text='La lettre : ' + str(event.char) +  ' a déjà été cliqué !', fill='black', font=('Arial 20', 15), tags="lettre_deja_clique")
                erreurs +=1
                if partie1:
                    dessin.itemconfigure(texte_erreurs, text='Il vous reste : ' + str(11 - erreurs) + ' essais !')
                else:
                    dessin.itemconfigure(texte_erreurs1, text='Il vous reste : ' + str(11 - erreurs) + ' essais !')
                dessin_pendu(erreurs)
                return 1
            else :
                dessin.delete("lettre_clique")
                dessin.delete("lettre_deja_clique")
                liste = liste + str(event.char) + ' | '
                lettre_clique = dessin.create_text(400, 250, text='| '+ liste, fill='black', font=('Arial 20', 15), tags="lettre_clique")

                if lettre not in mot_choisi.lower():
                    erreurs +=1
                    if partie1:
                        dessin.itemconfigure(texte_erreurs, text='Il vous reste : ' + str(11 - erreurs)+ ' essais !')
                    else:
                        dessin.itemconfigure(texte_erreurs1, text='Il vous reste : ' + str(11 - erreurs) + ' essais !')
                    dessin_pendu(erreurs)
                return 2


    def lettre_dans_mot(event):
        global mot_cherche
        global mot_affiche
        global commence, partie1
        if commence == True:
            reponse_fonc = clavier_pressed(event)
            if reponse_fonc != 1:
                nouvelle_affiche = ''
                for i in range(len(mot_affiche) // 2):  # Ensure the loop doesn't exceed the length of mot_affiche
                    lettre = mot_cherche[i]
                    if lettre == event.char:
                        nouvelle_affiche += lettre + ' '
                    else:
                        if mot_choisi[i] == ' ':
                            nouvelle_affiche += ' '
                        else:
                            nouvelle_affiche += mot_affiche[i * 2] + ' '  # Update the index according to the new loop

                mot_affiche = nouvelle_affiche
                verifie(nouvelle_affiche)
                if partie1:
                    dessin.itemconfigure(texte_reponse, text=nouvelle_affiche)
                else:
                    dessin.itemconfigure(texte_reponse1, text=nouvelle_affiche)


    def verifie(mot):
        global mot_affiche
        global commence
        global mot_choisi
        global ancien_mot
        if '_' not in mot_affiche:
            win_sound.play()
            ancien_mot.append(mot_choisi)
            reponse = obtenir_definition(ancien_mot[-1])
            gagner = dessin.create_text(400, 400, text='Vous avez gagné(e)', fill='white', font='Arial 20')
            commence = False
            dessin.after(4000, reinitialiser_jeu)

    def lien_url(event):
        import webbrowser
        global mot_choisi
        webbrowser.open("https://fr.wiktionary.org/wiki/" + str(mot_choisi))

    def lien_url1(event):
        import webbrowser
        global mot_choisi
        global ancien_mot
        webbrowser.open("https://fr.wiktionary.org/wiki/" + str(ancien_mot[-1]))


    def obtenir_definition(mot):
        #parsing html
        boutton_def = dessin.create_line(600, 350, 700, 350, width=50, fill='#B882EE')
        dessin.tag_bind(boutton_def, '<Button-1>', lien_url)

        text_def = dessin.create_text(650, 350,  text="DÉFINITION", fill='white', font='Arial')
        dessin.tag_bind(text_def, '<Button-1>', lien_url)

    def dessin_pendu(nb):
        global commence
        if nb == 1 or nb > 1:
            pendu_1 = dessin.create_line(20, 500, 220, 500, width=5, fill='black')
            if nb == 2 or nb > 1:
                pendu_2 = dessin.create_line(70, 300, 70, 500, width=5, fill='black')
                if nb == 3 or nb > 2:
                    pendu_3 = dessin.create_line(70, 300, 170, 300, width=5, fill='black')
                    if nb == 4 or nb > 3:
                        pendu_4 = dessin.create_line(70, 350, 120, 300, width=5, fill='black')
                        if nb == 5 or nb > 4:
                            pendu_5 = dessin.create_line(170, 300, 170, 350, width=5, fill='black')
                            if nb == 6 or nb > 5:
                                pendu_6 = dessin.create_oval(150, 350, 190, 390, outline='black', width=5)
                                if nb == 7 or nb > 6:
                                    pendu_7 = dessin.create_line(170, 390, 170, 450, width=5, fill='black')
                                    if nb == 8 or nb > 7:
                                        # Bras gauche
                                        pendu_8 = dessin.create_line(170, 410, 140, 380, width=5, fill='black')
                                        if nb == 9 or nb > 8:
                                            # Bras droit
                                            pendu_9 = dessin.create_line(170, 410, 200, 380, width=5, fill='black')
                                            if nb == 10 or nb > 9:
                                                # Jambe gauche
                                                pendu_10 = dessin.create_line(170, 450, 140, 480, width=5, fill='black')
                                                if nb == 11 or nb > 10:
                                                    # Jambe droite
                                                    global ancien_mot
                                                    pendu_11 = dessin.create_line(170, 450, 200, 480, width=5, fill='black')
                                                    perdu = dessin.create_text(400, 400, text='Perdu ! le mot était : '+ str(mot_choisi), fill='white', font='Arial 20')
                                                    dessin.itemconfigure(perdu)
                                                    ancien_mot.append(mot_choisi)
                                                    reponse = obtenir_definition(ancien_mot[-1])
                                                    lose_sound.play()
                                                    commence = False
                                                    dessin.after(4000, reinitialiser_jeu)



    def reinitialiser_jeu():
        global mot_choisi, la_taille, liste, mot_cherche, mot_affiche, commence, erreurs, partie1
        partie1 = False
        mot_choisi = ''
        la_taille = 100
        liste = ''
        mot_cherche = ''
        mot_affiche = ''
        commence = False
        erreurs = 0

        # Supprimer tous les éléments du canevas
        dessin.delete("all")
        # Redessiner les éléments de base
        rectangle_boutton = dessin.create_line(500, 500, 300, 500, width=50, fill='#008900', tags="boutton_commencer")
        dessin.tag_bind(rectangle_boutton, '<Button-1>', aleatoire_mot)

        Commencer_boutton = dessin.create_text(400, 500, text='COMMENCER', fill='white', font='Arial 20', tags="boutton_commencer")
        dessin.tag_bind(Commencer_boutton, '<Button-1>', aleatoire_mot)

        dessin.create_rectangle(40, 30, 760, 190, fill="#c09b72")

        rectangle_boutton1 = dessin.create_line(750, 110, 50, 110, width=150, fill='#008900')
        dessin.tag_bind(rectangle_boutton1)

        global texte_reponse1
        texte_reponse1 = dessin.create_text(400, 100, text='', fill='black', font=('Arial', la_taille))

        rectangle_boutton = dessin.create_line(0, 0, 100, 0, width=50, fill='#014911')
        dessin.tag_bind(rectangle_boutton, '<Button-1>', accueil)

        Commencer_boutton = dessin.create_text(50, 15, text='RETOUR', fill='white', font='Arial')
        dessin.tag_bind(Commencer_boutton, '<Button-1>', accueil)

        global texte_erreurs1
        texte_erreurs1 = dessin.create_text(650, 450, text='Il vous reste : 11 essais !', fill='black', font='Arial 20')

        boutton_def = dessin.create_line(600, 350, 700, 350, width=50, fill='#B882EE')
        dessin.tag_bind(boutton_def, '<Button-1>', lien_url1)

        text_def = dessin.create_text(650, 350,  text="DÉFINITION", fill='white', font='Arial')
        dessin.tag_bind(text_def, '<Button-1>', lien_url1)


    global partie1
    partie1 = True
    ##----- Création de la fenêtre -----##

    fen.title('Pendu facile')

    ##----- Création des boutons -----##

    bouton_quitter = Button(fen, text='QUITTER/STOP', command=fen.destroy)
    bouton_quitter.grid(row = 15, column = 0, padx = 3, pady = 3, sticky=E)


    ##----- Création du canevas -----##

    dessin = Canvas(fen, width = 800, height = 600, bg = '#9897A9')
    dessin.grid(row = 0, column =0, rowspan = 15, sticky = N)

    if facile_fen == True or moyen_fen == True or difficile_fen == True or fen_accueil == True:
        # Efface tout le contenu existant sur le canevas
        dessin.delete("all")

    ##----- Retour accueil -----##

    rectangle_boutton = dessin.create_line(0, 0, 100, 0, width=50, fill='#014911')
    dessin.tag_bind(rectangle_boutton, '<Button-1>', accueil)

    Commencer_boutton = dessin.create_text(50, 15, text='RETOUR', fill='white', font='Arial')
    dessin.tag_bind(Commencer_boutton, '<Button-1>', accueil)

    ##----- Dessiner dans le canevas -----##

    rectangle_boutton = dessin.create_line(500, 500, 300, 500, width=50, fill='#008900', tags="boutton_commencer")
    dessin.tag_bind(rectangle_boutton, '<Button-1>', aleatoire_mot)

    Commencer_boutton = dessin.create_text(400, 500, text='COMMENCER', fill='white', font='Arial 20',tags="boutton_commencer")
    dessin.tag_bind(Commencer_boutton, '<Button-1>', aleatoire_mot)


    ##----- Mots a chercher -----##
    dessin.create_rectangle(40, 30, 760, 190, fill="#c09b72")

    rectangle_boutton1 = dessin.create_line(750, 110, 50, 110, width=150, fill='#008900')
    dessin.tag_bind(rectangle_boutton1)


    ##-----Création des zones de texte-----##
    texte_erreurs = dessin.create_text(650, 450, text='Il vous reste : 11 essais !', fill='black', font='Arial 20')
    texte_reponse = dessin.create_text(400, 100, text=str(mot_choisi), fill='black', font=('Arial 20', la_taille))


    ##-----Clavier-----##

    fen.bind("<Key>",lettre_dans_mot)

    ##----- Programme principal -----##

    # Boucle d'attente des événements

def moyen():
    button_sound.play()
    global facile_fen
    global moyen_fen
    global difficile_fen
    global fen_accueil
    difficile_fen = False
    moyen_fen = True
    facile_fen = False
    fen_accueil = False
    ##----- Fonction -----##
    global mot_choisi
    global la_taille
    global liste
    global mot_cherche
    global mot_affiche
    global commence
    global erreurs
    global ancien_mot
    mot_choisi=''
    la_taille = 100
    liste = ''
    mot_cherche = ''
    mot_affiche = ''
    commence = False  # Variable pour suivre si le jeu a commencé
    erreurs = 0
    ancien_mot = []

    def aleatoire_mot(event):
        button_sound.play()
        dessin.delete("boutton_commencer")
        with open(path_to_liste_francais, 'r', encoding='iso-8859-1') as fichier:
            mots = fichier.readlines()
            global mot_choisi
            mot_choisi = random.choice(mots).strip()  # strip() pour supprimer les sauts de ligne
            for lettre in mot_choisi:
                if lettre == " ":
                    mot_choisi = random.choice(mots).strip()  # strip() pour supprimer les sauts de ligne
            global mot_cherche
            mot_cherche = mot_choisi.lower()
            global la_taille
            la_taille = taille_du_mot(mot_choisi)
            afficher_mot(mot_choisi.lower(), taille_du_mot(mot_choisi))  # Convertir le mot en minuscule pour l'affichage sinon ya probleme
        global commence
        commence = True
    path_to_liste_francais = os.path.join(application_path, "liste_francais.txt")
    path_to_ukenglish = os.path.join(application_path, "ukenglish.txt")

    def taille_du_mot(mot):
        longueur = len(mot)
        if longueur < 7:
            return 100
        if 11 > longueur > 9 :
            return 60
        if 12 >= longueur >= 11 :
            return 50
        if longueur > 12 :
            return 40
        else :
            return 70


    def afficher_mot(mot, taille):
        global mot_affiche, partie1
        mot_affiche = ''
        lettres_a_afficher = set()

        for i, char in enumerate(mot):
            if char != ' ' and random.random() < 0.33:
                lettres_a_afficher.add(i)  # Ajouter l'indice de la lettre à afficher

        for i, char in enumerate(mot):
            if i in lettres_a_afficher or char == ' ':
                mot_affiche += char + ' '
            else:
                mot_affiche += '_ '
        if partie1:
            dessin.itemconfigure(texte_reponse, text=mot_affiche, font=('Arial', taille))
        else:
            dessin.itemconfigure(texte_reponse1, text=mot_affiche, font=('Arial', taille))



    def clavier_pressed(event):
        keyboard_sound.play()
        global liste
        global commence
        global erreurs, partie1

        if commence == True:
            lettre = event.char  # Convertir la lettre en minuscule
            #Ignorer la touche shift pour mettre des lettres en majuscules
            if event.keysym == 'Shift_R' or event.keysym == 'Shift_L':
                return 1
            global liste
            if event.char in liste :
                dessin.delete("lettre_deja_clique")
                message = dessin.create_text(400, 300, text='La lettre : ' + str(event.char) +  ' a déjà été cliqué !', fill='black', font=('Arial 20', 15), tags="lettre_deja_clique")
                erreurs += 1
                if partie1:
                    dessin.itemconfigure(texte_erreurs, text='Il vous reste : ' + str(11 - erreurs) + ' essais !')
                else:
                    dessin.itemconfigure(texte_erreurs1, text='Il vous reste : ' + str(11 - erreurs) + ' essais !')
                dessin_pendu(erreurs)
                return 1
            else :
                dessin.delete("lettre_clique")
                dessin.delete("lettre_deja_clique")
                liste = liste + str(event.char) + ' | '
                lettre_clique = dessin.create_text(400, 250, text='| '+ liste, fill='black', font=('Arial 20', 15), tags="lettre_clique")

                if lettre not in mot_choisi.lower():
                    erreurs +=1
                    if partie1:
                        dessin.itemconfigure(texte_erreurs, text='Il vous reste : ' + str(11 - erreurs)+ ' essais !')
                    else:
                        dessin.itemconfigure(texte_erreurs1, text='Il vous reste : ' + str(11 - erreurs) + ' essais !')
                    dessin_pendu(erreurs)
                return 2


    def lettre_dans_mot(event):
        global mot_cherche
        global mot_affiche
        global commence, partie1
        if commence == True:
            reponse_fonc = clavier_pressed(event)
            if reponse_fonc != 1:
                nouvelle_affiche = ''
                for i in range(len(mot_affiche) // 2):  # Ensure the loop doesn't exceed the length of mot_affiche
                    lettre = mot_cherche[i]
                    if lettre == event.char:
                        nouvelle_affiche += lettre + ' '
                    else:
                        if mot_choisi[i] == ' ':
                            nouvelle_affiche += ' '
                        else:
                            nouvelle_affiche += mot_affiche[i * 2] + ' '  # Update the index according to the new loop

                mot_affiche = nouvelle_affiche
                verifie(nouvelle_affiche)
                if partie1:
                    dessin.itemconfigure(texte_reponse, text=nouvelle_affiche)
                else:
                    dessin.itemconfigure(texte_reponse1, text=nouvelle_affiche)


    def verifie(mot):
        global mot_affiche
        global commence
        global mot_choisi
        global ancien_mot
        if '_' not in mot_affiche:
            win_sound.play()
            ancien_mot.append(mot_choisi)
            reponse = obtenir_definition(ancien_mot[-1])
            gagner = dessin.create_text(400, 400, text='Vous avez gagné(e)', fill='white', font='Arial 20')
            commence = False
            dessin.after(4000, reinitialiser_jeu)

    def lien_url(event):
        import webbrowser
        global mot_choisi
        webbrowser.open("https://fr.wiktionary.org/wiki/" + str(mot_choisi))

    def lien_url1(event):
        import webbrowser
        global mot_choisi
        global ancien_mot
        webbrowser.open("https://fr.wiktionary.org/wiki/" + str(ancien_mot[-1]))


    def obtenir_definition(mot):
        #parsing html
        boutton_def = dessin.create_line(600, 350, 700, 350, width=50, fill='#B882EE')
        dessin.tag_bind(boutton_def, '<Button-1>', lien_url)

        text_def = dessin.create_text(650, 350,  text="DÉFINITION", fill='white', font='Arial')
        dessin.tag_bind(text_def, '<Button-1>', lien_url)


    def dessin_pendu(nb):
        global commence
        if nb == 1 or nb > 1:
            pendu_1 = dessin.create_line(20, 500, 220, 500, width=5, fill='black')
            if nb == 2 or nb > 1:
                pendu_2 = dessin.create_line(70, 300, 70, 500, width=5, fill='black')
                if nb == 3 or nb > 2:
                    pendu_3 = dessin.create_line(70, 300, 170, 300, width=5, fill='black')
                    if nb == 4 or nb > 3:
                        pendu_4 = dessin.create_line(70, 350, 120, 300, width=5, fill='black')
                        if nb == 5 or nb > 4:
                            pendu_5 = dessin.create_line(170, 300, 170, 350, width=5, fill='black')
                            if nb == 6 or nb > 5:
                                pendu_6 = dessin.create_oval(150, 350, 190, 390, outline='black', width=5)
                                if nb == 7 or nb > 6:
                                    pendu_7 = dessin.create_line(170, 390, 170, 450, width=5, fill='black')
                                    if nb == 8 or nb > 7:
                                        # Bras gauche
                                        pendu_8 = dessin.create_line(170, 410, 140, 380, width=5, fill='black')
                                        if nb == 9 or nb > 8:
                                            # Bras droit
                                            pendu_9 = dessin.create_line(170, 410, 200, 380, width=5, fill='black')
                                            if nb == 10 or nb > 9:
                                                # Jambe gauche
                                                pendu_10 = dessin.create_line(170, 450, 140, 480, width=5, fill='black')
                                                if nb == 11 or nb > 10:
                                                    # Jambe droite
                                                    global ancien_mot
                                                    pendu_11 = dessin.create_line(170, 450, 200, 480, width=5, fill='black')
                                                    perdu = dessin.create_text(400, 400, text='Perdu ! le mot était : '+ str(mot_choisi), fill='white', font='Arial 20')
                                                    dessin.itemconfigure(perdu)
                                                    ancien_mot.append(mot_choisi)
                                                    reponse = obtenir_definition(ancien_mot[-1])
                                                    lose_sound.play()
                                                    commence = False
                                                    dessin.after(4000, reinitialiser_jeu)



    def reinitialiser_jeu():
        global mot_choisi, la_taille, liste, mot_cherche, mot_affiche, commence, erreurs, ancien_mot, partie1
        partie1 = False
        mot_choisi = ''
        la_taille = 100
        liste = ''
        mot_cherche = ''
        mot_affiche = ''
        commence = False
        erreurs = 0

        # Supprimer tous les éléments du canevas
        dessin.delete("all")

        # Redessiner les éléments de base
        rectangle_boutton = dessin.create_line(500, 500, 300, 500, width=50, fill='#d47904', tags="boutton_commencer")
        dessin.tag_bind(rectangle_boutton, '<Button-1>', aleatoire_mot)

        Commencer_boutton = dessin.create_text(400, 500, text='COMMENCER', fill='white', font='Arial 20', tags="boutton_commencer")
        dessin.tag_bind(Commencer_boutton, '<Button-1>', aleatoire_mot)

        dessin.create_rectangle(40, 30, 760, 190, fill="#c09b72")

        rectangle_boutton1 = dessin.create_line(750, 110, 50, 110, width=150, fill='#d47904')
        dessin.tag_bind(rectangle_boutton1)

        global texte_reponse1
        texte_reponse1 = dessin.create_text(400, 100, text='', fill='black', font=('Arial', la_taille))

        rectangle_boutton = dessin.create_line(0, 0, 100, 0, width=50, fill='#014911')
        dessin.tag_bind(rectangle_boutton, '<Button-1>', accueil)

        Commencer_boutton = dessin.create_text(50, 15, text='RETOUR', fill='white', font='Arial')
        dessin.tag_bind(Commencer_boutton, '<Button-1>', accueil)
        global texte_erreurs1
        texte_erreurs1 = dessin.create_text(650, 450, text='Il vous reste : 11 essais !', fill='black', font='Arial 20')

        boutton_def = dessin.create_line(600, 350, 700, 350, width=50, fill='#B882EE')
        dessin.tag_bind(boutton_def, '<Button-1>', lien_url1)

        text_def = dessin.create_text(650, 350,  text="DÉFINITION", fill='white', font='Arial')
        dessin.tag_bind(text_def, '<Button-1>', lien_url1)


    global partie1
    partie1 = True
    ##----- Création de la fenêtre -----##

    fen.title('Pendu moyen')

    ##----- Création des boutons -----##

    bouton_quitter = Button(fen, text='QUITTER/STOP', command=fen.destroy)
    bouton_quitter.grid(row = 15, column = 0, padx = 3, pady = 3, sticky=E)


    ##----- Création du canevas -----##

    dessin = Canvas(fen, width = 800, height = 600, bg = '#9897A9')
    dessin.grid(row = 0, column =0, rowspan = 15, sticky = N)

    if facile_fen == True or moyen_fen == True or difficile_fen == True or fen_accueil == True:
        # Efface tout le contenu existant sur le canevas
        dessin.delete("all")

    ##----- Retour accueil -----##

    rectangle_boutton = dessin.create_line(0, 0, 100, 0, width=50, fill='#014911')
    dessin.tag_bind(rectangle_boutton, '<Button-1>', accueil)

    Commencer_boutton = dessin.create_text(50, 15, text='RETOUR', fill='white', font='Arial')
    dessin.tag_bind(Commencer_boutton, '<Button-1>', accueil)

    ##----- Dessiner dans le canevas -----##

    rectangle_boutton = dessin.create_line(500, 500, 300, 500, width=50, fill='#d47904', tags="boutton_commencer")
    dessin.tag_bind(rectangle_boutton, '<Button-1>', aleatoire_mot)

    Commencer_boutton = dessin.create_text(400, 500, text='COMMENCER', fill='white', font='Arial 20',tags="boutton_commencer")
    dessin.tag_bind(Commencer_boutton, '<Button-1>', aleatoire_mot)


    ##----- Mots a chercher -----##
    dessin.create_rectangle(40, 30, 760, 190, fill="#c09b72")

    rectangle_boutton1 = dessin.create_line(750, 110, 50, 110, width=150, fill='#d47904')
    dessin.tag_bind(rectangle_boutton1)


    ##-----Création des zones de texte-----##
    texte_erreurs = dessin.create_text(650, 450, text='Il vous reste : 11 essais !', fill='black', font='Arial 20')
    texte_reponse = dessin.create_text(400, 100, text=str(mot_choisi), fill='black', font=('Arial 20', la_taille))


    ##-----Clavier-----##

    fen.bind("<Key>",lettre_dans_mot)

    ##----- Programme principal -----##

    # Boucle d'attente des événements

def difficile():
    button_sound.play()
    global facile_fen
    global moyen_fen
    global difficile_fen
    global fen_accueil
    difficile_fen = True
    moyen_fen = False
    facile_fen = False
    fen_accueil = False


    ##----- Fonction -----##
    global mot_choisi
    global la_taille
    global liste
    global mot_cherche
    global mot_affiche
    global commence
    global erreurs
    global ancien_mot
    mot_choisi=''
    la_taille = 100
    liste = ''
    mot_cherche = ''
    mot_affiche = ''
    commence = False  # Variable pour suivre si le jeu a commencé
    erreurs = 0
    ancien_mot = []

    def aleatoire_mot(event):
        button_sound.play()
        dessin.delete("boutton_commencer")
        with open(path_to_liste_francais, 'r', encoding='iso-8859-1') as fichier:
            mots = fichier.readlines()
            global mot_choisi
            mot_choisi = random.choice(mots).strip()  # strip() pour supprimer les sauts de ligne
            for lettre in mot_choisi:
                if lettre == " ":
                    mot_choisi = random.choice(mots).strip()  # strip() pour supprimer les sauts de ligne
            global mot_cherche
            mot_cherche = mot_choisi
            global la_taille
            la_taille = taille_du_mot(mot_choisi)
            afficher_mot(mot_choisi.lower(), taille_du_mot(mot_choisi))  # Convertir le mot en minuscule pour l'affichage sinon ya probleme
        global commence
        commence = True
    path_to_liste_francais = os.path.join(application_path, "liste_francais.txt")
    path_to_ukenglish = os.path.join(application_path, "ukenglish.txt")

    def taille_du_mot(mot):
        longueur = len(mot)
        if longueur < 7:
            return 100
        if 11 > longueur > 9 :
            return 60
        if 12 >= longueur >= 11 :
            return 50
        if longueur > 12 :
            return 40
        else :
            return 70


    def afficher_mot(mot, taille):
        global mot_affiche, partie1
        mot_affiche = ''

        for char in mot:
            if char == ' ':
                mot_affiche += ' '
            else:
                mot_affiche += '_ '
        if partie1:
            dessin.itemconfigure(texte_reponse, text=mot_affiche, font=('Arial', taille))
        else:
            dessin.itemconfigure(texte_reponse1, text=mot_affiche, font=('Arial', taille))



    def clavier_pressed(event):
        keyboard_sound.play()
        global liste
        global commence
        global erreurs, partie1

        if commence == True:
            lettre = event.char  # Convertir la lettre en minuscule
            #Ignorer la touche shift pour mettre des lettres en majuscules
            if event.keysym == 'Shift_R' or event.keysym == 'Shift_L':
                return 1
            global liste
            if event.char in liste :
                dessin.delete("lettre_deja_clique")
                message = dessin.create_text(400, 300, text='La lettre : ' + str(event.char) +  ' a déjà été cliqué !', fill='black', font=('Arial 20', 15), tags="lettre_deja_clique")
                erreurs +=1
                if partie1:
                    dessin.itemconfigure(texte_erreurs, text='Il vous reste : ' + str(6 - erreurs) + ' essais !')
                else:
                    dessin.itemconfigure(texte_erreurs1, text='Il vous reste : ' + str(6 - erreurs) + ' essais !')
                dessin_pendu(erreurs)
                return 1
            else :
                dessin.delete("lettre_clique")
                dessin.delete("lettre_deja_clique")
                liste = liste + str(event.char) + ' | '
                lettre_clique = dessin.create_text(400, 250, text='| '+ liste, fill='black', font=('Arial 20', 15), tags="lettre_clique")

                if lettre not in mot_choisi.lower():
                    erreurs +=1
                    if partie1:
                        dessin.itemconfigure(texte_erreurs, text='Il vous reste : ' + str(6 - erreurs)+ ' essais !')
                    else:
                        dessin.itemconfigure(texte_erreurs1, text='Il vous reste : ' + str(6 - erreurs) + ' essais !')
                    dessin_pendu(erreurs)
                return 2


    def lettre_dans_mot(event):
        global mot_cherche
        global mot_affiche
        global commence, partie1
        if commence == True:
            reponse_fonc = clavier_pressed(event)
            if reponse_fonc != 1:
                nouvelle_affiche = ''
                for i in range(len(mot_affiche) // 2):  # Ensure the loop doesn't exceed the length of mot_affiche
                    lettre = mot_cherche[i]
                    if lettre == event.char:
                        nouvelle_affiche += lettre + ' '
                    else:
                        if mot_choisi[i] == ' ':
                            nouvelle_affiche += ' '
                        else:
                            nouvelle_affiche += mot_affiche[i * 2] + ' '  # Update the index according to the new loop

                mot_affiche = nouvelle_affiche
                verifie(nouvelle_affiche)
                if partie1:
                    dessin.itemconfigure(texte_reponse, text=nouvelle_affiche)
                else:
                    dessin.itemconfigure(texte_reponse1, text=nouvelle_affiche)


    def verifie(mot):
        global mot_affiche
        global commence
        
        global mot_choisi
        global ancien_mot
        if '_' not in mot_affiche:
            ancien_mot.append(mot_choisi)
            win_sound.play()
            reponse = obtenir_definition(ancien_mot[-1])
            gagner = dessin.create_text(400, 400, text='Vous avez gagné(e)', fill='white', font='Arial 20')
            commence = False
            dessin.after(4000, reinitialiser_jeu)

    def lien_url(event):
        import webbrowser
        global mot_choisi
        webbrowser.open("https://fr.wiktionary.org/wiki/" + str(mot_choisi))

    def lien_url1(event):
        import webbrowser
        global mot_choisi
        webbrowser.open("https://fr.wiktionary.org/wiki/" + str(ancien_mot[-1]))


    def obtenir_definition(mot):
        #parsing html
        boutton_def = dessin.create_line(600, 350, 700, 350, width=50, fill='#B882EE')
        dessin.tag_bind(boutton_def, '<Button-1>', lien_url)

        text_def = dessin.create_text(650, 350,  text="DÉFINITION", fill='white', font='Arial')
        dessin.tag_bind(text_def, '<Button-1>', lien_url)


    def dessin_pendu(nb):
        global commence
        global mot_choisi
        if nb == 1 or nb > 1:
            pendu_1 = dessin.create_line(20, 500, 220, 500, width=5, fill='black')
            pendu_2 = dessin.create_line(70, 300, 70, 500, width=5, fill='black')
            if nb == 2 or nb > 1:
                pendu_3 = dessin.create_line(70, 300, 170, 300, width=5, fill='black')
                pendu_4 = dessin.create_line(70, 350, 120, 300, width=5, fill='black')
                if nb == 3 or nb > 2:
                    pendu_5 = dessin.create_line(170, 300, 170, 350, width=5, fill='black')
                    pendu_6 = dessin.create_oval(150, 350, 190, 390, outline='black', width=5)
                    if nb == 4 or nb > 3:
                        pendu_7 = dessin.create_line(170, 390, 170, 450, width=5, fill='black')
                        # Bras gauche
                        pendu_8 = dessin.create_line(170, 410, 140, 380, width=5, fill='black')
                        if nb == 5 or nb > 4:
                            # Bras droit
                            pendu_9 = dessin.create_line(170, 410, 200, 380, width=5, fill='black')
                            # Jambe gauche
                            pendu_10 = dessin.create_line(170, 450, 140, 480, width=5, fill='black')
                            if nb == 6 or nb > 5:
                                # Jambe droite
                                global ancien_mot
                                pendu_11 = dessin.create_line(170, 450, 200, 480, width=5, fill='black')
                                lose_sound.play()
                                perdu = dessin.create_text(400, 400, text='Perdu ! le mot était : '+ str(mot_choisi), fill='white', font='Arial 20')
                                dessin.itemconfigure(perdu)
                                ancien_mot.append(mot_choisi)
                                reponse = obtenir_definition(ancien_mot[-1])
                                commence = False
                                dessin.after(4000, reinitialiser_jeu)



    def reinitialiser_jeu():
        global mot_choisi, la_taille, liste, mot_cherche, mot_affiche, commence, erreurs, partie1
        partie1 = False
        mot_choisi = ''
        la_taille = 100
        liste = ''
        mot_cherche = ''
        mot_affiche = ''
        commence = False
        erreurs = 0

        # Supprimer tous les éléments du canevas
        dessin.delete("all")

        # Redessiner les éléments de base
        rectangle_boutton = dessin.create_line(500, 500, 300, 500, width=50, fill='#cc0e00', tags="boutton_commencer")
        dessin.tag_bind(rectangle_boutton, '<Button-1>', aleatoire_mot)

        Commencer_boutton = dessin.create_text(400, 500, text='COMMENCER', fill='white', font='Arial 20', tags="boutton_commencer")
        dessin.tag_bind(Commencer_boutton, '<Button-1>', aleatoire_mot)

        dessin.create_rectangle(40, 30, 760, 190, fill="#c09b72")

        rectangle_boutton1 = dessin.create_line(750, 110, 50, 110, width=150, fill='#cc0e00')
        dessin.tag_bind(rectangle_boutton1)

        global texte_reponse1
        texte_reponse1 = dessin.create_text(400, 100, text='', fill='black', font=('Arial', la_taille))

        rectangle_boutton = dessin.create_line(0, 0, 100, 0, width=50, fill='#014911')
        dessin.tag_bind(rectangle_boutton, '<Button-1>', accueil)

        Commencer_boutton = dessin.create_text(50, 15, text='RETOUR', fill='white', font='Arial')
        dessin.tag_bind(Commencer_boutton, '<Button-1>', accueil)

        global texte_erreurs1
        texte_erreurs1 = dessin.create_text(650, 450, text='Il vous reste : 6 essais !', fill='black', font='Arial 20')


        boutton_def = dessin.create_line(600, 350, 700, 350, width=50, fill='#B882EE')
        dessin.tag_bind(boutton_def, '<Button-1>', lien_url1)

        text_def = dessin.create_text(650, 350,  text="DÉFINITION", fill='white', font='Arial')
        dessin.tag_bind(text_def, '<Button-1>', lien_url1)


    global partie1
    partie1 = True
    ##----- Création de la fenêtre -----##

    fen.title('Pendu difficile')

    ##----- Création des boutons -----##

    bouton_quitter = Button(fen, text='QUITTER/STOP', command=fen.destroy)
    bouton_quitter.grid(row = 15, column = 0, padx = 3, pady = 3, sticky=E)


    ##----- Création du canevas -----##

    dessin = Canvas(fen, width = 800, height = 600, bg = '#9897A9')
    dessin.grid(row = 0, column =0, rowspan = 15, sticky = N)

    if facile_fen == True or moyen_fen == True or difficile_fen == True or fen_accueil == True:
        # Efface tout le contenu existant sur le canevas
        dessin.delete("all")

    ##----- Retour accueil -----##

    rectangle_boutton = dessin.create_line(0, 0, 100, 0, width=50, fill='#014911')
    dessin.tag_bind(rectangle_boutton, '<Button-1>', accueil)

    Commencer_boutton = dessin.create_text(50, 15, text='RETOUR', fill='white', font='Arial')
    dessin.tag_bind(Commencer_boutton, '<Button-1>', accueil)

    ##----- Dessiner dans le canevas -----##

    rectangle_boutton = dessin.create_line(500, 500, 300, 500, width=50, fill='#cc0e00', tags="boutton_commencer")
    dessin.tag_bind(rectangle_boutton, '<Button-1>', aleatoire_mot)

    Commencer_boutton = dessin.create_text(400, 500, text='COMMENCER', fill='white', font='Arial 20',tags="boutton_commencer")
    dessin.tag_bind(Commencer_boutton, '<Button-1>', aleatoire_mot)


    ##----- Mots a chercher -----##
    dessin.create_rectangle(40, 30, 760, 190, fill="#c09b72")

    rectangle_boutton1 = dessin.create_line(750, 110, 50, 110, width=150, fill='#cc0e00')
    dessin.tag_bind(rectangle_boutton1)


    ##-----Création des zones de texte-----##
    texte_erreurs = dessin.create_text(650, 450, text='Il vous reste : 6 essais !', fill='black', font='Arial 20')
    texte_reponse = dessin.create_text(400, 100, text=str(mot_choisi), fill='black', font=('Arial 20', la_taille))


    ##-----Clavier-----##

    fen.bind("<Key>",lettre_dans_mot)

    ##----- Programme principal -----##

    # Boucle d'attente des événements


def les_regles():
    button_sound.play()
    global facile_fen
    global moyen_fen
    global difficile_fen
    global fen_accueil
    difficile_fen = True
    moyen_fen = False
    facile_fen = False
    fen_accueil = True

    ##----- Création de la fenêtre -----##

    fen.title('Les règles')

    ##----- Création du canevas -----##
    global dessin

    dessin = Canvas(fen, width = 800, height = 600, bg = '#9897A9')
    dessin.grid(row = 0, column =0, rowspan = 15, sticky = N)

    if facile_fen == True or moyen_fen == True or difficile_fen == True or fen_accueil == True:
        # Efface tout le contenu existant sur le canevas
        dessin.delete("all")
    texte_regles = """

Fonctionnement :
        - Le jeu va commencer lorsque l'utilisateur (vous) cliquera sur le bouton "Commencer".
        Des _ vont s'afficher en fonction du niveau de difficulté choisi.
        - L'objectif est de trouver les lettres manquantes en appuyant sur les touches du
        clavier correspondantes.
        - La partie se termine lorsque l'utilisateur n'a plus d'essais (le pendu est alors
        complètement dessiné) ou lorsqu'il a trouvé toutes les lettres. À ce moment-là,
        l'utilisateur (vous) pourra trouver la définition du mot recherché en appuyant sur
        le bouton "Définition".

 Attention :
        - Il est possible de rechercher un mot séparé par un tiret (-), ou même de
        rechercher deux mots donc il faut appuyer sur la touche espace.
        - Si l'utilisateur choisit le mode Difficile : Les lettres majuscules (M) et les
        lettres minuscules (m) ne sont pas considérées comme étant les mêmes lettres.
        - Lorsque l'utilisateur commence une partie dans les niveaux de difficulté "Facile"
        ou "Moyen", quelques lettres vont être affichées. Il est possible qu'il faille
        chercher une même lettre qui était déjà affichée lorsque le mot s'est affiché
        pour la première fois. Par exemple, si le mot est "arbre" et que le programme
        affiche : _ r b _ e, il faut quand même trouver la lettre "r" bien qu'elle
        soit déjà affichée.
        - Lorsque l'utilisateur commence une partie dans les niveaux de difficulté
        "Facile" ou "Moyen", quelques lettres vont être affichées. Si l'utilisateur
        clique sur une lettre qui était déjà affichée et qu'elle n'apparaît qu'une seule fois
        dans le mot, alors la faute ne sera pas comptabilisée exceptionnellement.
        Par exemple, si le mot est 'arbre' et que le programme affiche : _ r _ r _, et que
        l'utilisateur appuie sur la lettre 'r', cela ne sera pas compté comme une erreur.
        Cependant, si l'utilisateur appuie une deuxième fois, alors cela sera considéré
        comme une erreur.
        - L'utilisateur peut perdre des essais s'il appuie plusieurs fois sur une
        touche qui a déjà été cliquée ou si la touche cliquée ne fait pas partie
        du mot à deviner.


    """
    dessin.create_text(420, 310, text=str(texte_regles), fill='black', font=('Arial', 12))


    rectangle_boutton = dessin.create_line(0, 0, 100, 0, width=50, fill='#014911')
    dessin.tag_bind(rectangle_boutton, '<Button-1>', accueil)

    Commencer_boutton = dessin.create_text(50, 15, text='RETOUR', fill='white', font='Arial')
    dessin.tag_bind(Commencer_boutton, '<Button-1>', accueil)

def accueil(event):
    button_sound.play()
    global facile_fen
    global moyen_fen
    global difficile_fen
    global fen_accueil
    difficile_fen = False
    moyen_fen = False
    facile_fen = False
    fen_accueil = True


    ##----- Fonctions -----##


    def langue_anglais():
        principal_menu(1)

    def grossir(event, btn, taille, aaa):
        btn.configure(width=aaa+2,font=("Arial", taille+2))

    def petit(event, btn, taille, aaa):
        btn.configure(width=aaa,font=("Arial", taille))

    ##----- Création de la fenêtre -----##



    fen.title("Page d'Accueil")


    ##----- Création du canevas -----##
    global dessin

    dessin = Canvas(fen, width = 800, height = 600, bg = '#9897A9')
    dessin.grid(row = 0, column =0, rowspan = 15, sticky = N)

    if facile_fen == True or moyen_fen == True or difficile_fen == True or fen_accueil == True:
        # Efface tout le contenu existant sur le canevas
        dessin.delete("all")
    ##----- behind buttons-----##
    dessin.create_rectangle(570, 200, 790, 560, fill="#c09b72") # droite
    dessin.create_rectangle(580, 210, 780, 550, fill="#d8cdc1")

    dessin.create_rectangle(10, 200, 230, 560, fill="#c09b72") # gauche
    dessin.create_rectangle(20, 210, 220, 550, fill="#d8cdc1")

    dessin.create_rectangle(220, 170, 580, 590, fill="#c09b72") # milieu
    dessin.create_rectangle(230, 180, 570, 580, fill="#d8cdc1")

    ##----- title behind buttons-----##

    dessin.create_rectangle(610, 180, 750, 230, fill="#d1d72d") # droite

    dessin.create_rectangle(50, 180, 190, 230, fill="#d1d72d") # gauche

    dessin.create_rectangle(260, 140, 540, 210, fill="#d1d72d") # milieu

    ##----- title -----##

    dessin.create_text(400, 50, text="Le Pendu", fill='white', font=('Arial', 70))
    dessin.create_text(400, 115, text="Par Yuri DENIS", fill='white', font=('Arial', 25))

    ##----- title frame -----##

    dessin.create_text(125, 205, text="Language :", fill='black', font=('Arial', 15, 'underline'))
    dessin.create_text(405, 175, text="Difficultés :", fill='black', font=('Arial', 25, 'underline'))
    dessin.create_text(680, 205, text="Les Règles :", fill='black', font=('Arial', 15, 'underline'))

    ##----- Boutton levels-----##

    rectangle_boutton_facile = Button(fen, text="FACILE", command=facile, width=22, height = 3, font=("Arial", 11), bg="#008900",fg="white")
    rectangle_boutton_facile.grid(row = 9, padx = 0, sticky=N)
    rectangle_boutton_facile.bind('<Motion>', lambda event,width = 22, taille = 11, btn = rectangle_boutton_facile: grossir(event,btn, taille,width))
    rectangle_boutton_facile.bind('<Leave>', lambda event,width = 22, taille = 11, btn = rectangle_boutton_facile: petit(event,btn, taille,width))

    rectangle_boutton_moyen = Button(fen, text="MOYEN", command=moyen, width=22, height = 3, font=("Arial", 11), bg="#d47904",fg="white")
    rectangle_boutton_moyen.grid(row = 11, padx = 0, sticky=N)
    rectangle_boutton_moyen.bind('<Motion>', lambda event,width = 22, taille = 11, btn = rectangle_boutton_moyen: grossir(event,btn, taille,width))
    rectangle_boutton_moyen.bind('<Leave>', lambda event,width = 22, taille = 11, btn = rectangle_boutton_moyen: petit(event,btn, taille,width))

    rectangle_boutton_difficile = Button(fen, text="DIFFICILE", command=difficile, width=22, height = 3, font=("Arial", 11), bg="#cc0e00",fg="white")
    rectangle_boutton_difficile.grid(row = 13, padx = 0, sticky=N)
    rectangle_boutton_difficile.bind('<Motion>', lambda event,width = 22, taille = 11, btn = rectangle_boutton_difficile: grossir(event,btn, taille,width))
    rectangle_boutton_difficile.bind('<Leave>', lambda event,width = 22, taille = 11, btn = rectangle_boutton_difficile: petit(event,btn, taille,width))

    ##----- Boutton règles -----##

    rules_button = Button(fen, text="Clique ici", command=les_regles, width=17, height = 3, font=("Arial", 11), bg="#1567b5",fg="white")
    rules_button.grid(row = 11, padx= 40, sticky=E)
    rules_button.bind('<Motion>', lambda event, taille = 10,width = 16, btn = rules_button: grossir(event,btn, taille,width))
    rules_button.bind('<Leave>', lambda event, taille = 11,width = 17, btn = rules_button: petit(event,btn, taille, width))

    ##----- Boutton langue  -----##


    rectangle_boutton_francais = Button(fen, text="English", command=langue_anglais, width=17, height = 3, font=("Arial", 11), bg="#1567b5",fg="white")
    rectangle_boutton_francais.grid(row = 11, padx= 40, sticky=W)
    rectangle_boutton_francais.bind('<Motion>', lambda event, taille = 10,width = 16, btn = rectangle_boutton_francais: grossir(event,btn, taille,width))
    rectangle_boutton_francais.bind('<Leave>', lambda event, taille = 11,width = 17, btn = rectangle_boutton_francais: petit(event,btn, taille, width))




def easy():
    button_sound.play()
    global facile_fen
    global moyen_fen
    global difficile_fen
    global fen_accueil
    difficile_fen = False
    moyen_fen = False
    facile_fen = True
    fen_accueil = False

    ##----- Fonction -----##
    global mot_choisi
    global la_taille
    global liste
    global mot_cherche
    global mot_affiche
    global commence
    global erreurs
    global ancien_mot
    mot_choisi=''
    la_taille = 100
    liste = ''
    mot_cherche = ''
    mot_affiche = ''
    commence = False  # Variable pour suivre si le jeu a commencé
    erreurs = 0
    ancien_mot = []

    def aleatoire_mot(event):
        button_sound.play()
        dessin.delete("boutton_commencer")
        with open(path_to_ukenglish, 'r', encoding='latin-1') as fichier:
            mots = fichier.readlines()
            global mot_choisi
            mot_choisi = random.choice(mots).strip()  # strip() pour supprimer les sauts de ligne
            for lettre in mot_choisi:
                if lettre == " ":
                    mot_choisi = random.choice(mots).strip()  # strip() pour supprimer les sauts de ligne
            global mot_cherche
            mot_cherche = mot_choisi.lower()
            global la_taille
            la_taille = taille_du_mot(mot_choisi)
            afficher_mot(mot_choisi.lower(), taille_du_mot(mot_choisi))  # Convertir le mot en minuscule pour l'affichage sinon ya probleme
        global commence
        commence = True

    path_to_liste_francais = os.path.join(application_path, "liste_francais.txt")
    path_to_ukenglish = os.path.join(application_path, "ukenglish.txt")
    def taille_du_mot(mot):
        longueur = len(mot)
        if longueur < 7:
            return 100
        if 11 > longueur > 9 :
            return 60
        if 12 >= longueur >= 11 :
            return 50
        if longueur > 12 :
            return 40
        else :
            return 70


    def afficher_mot(mot, taille):
        global mot_affiche, partie1
        mot_affiche = ''
        lettres_a_afficher = set()
        global mot_choisi
        if len(mot_choisi) < 4:
            for i, char in enumerate(mot):
                if char != ' ' and random.random() < 0.40:
                    lettres_a_afficher.add(i)  # Ajouter l'indice de la lettre à afficher

            for i, char in enumerate(mot):
                if i in lettres_a_afficher or char == ' ':
                    mot_affiche += char + ' '
                else:
                    mot_affiche += '_ '
        elif len(mot_choisi) > 10:
            for i, char in enumerate(mot):
                if char != ' ' and random.random() < 0.60:
                    lettres_a_afficher.add(i)  # Ajouter l'indice de la lettre à afficher

            for i, char in enumerate(mot):
                if i in lettres_a_afficher or char == ' ':
                    mot_affiche += char + ' '
                else:
                    mot_affiche += '_ '
        else:
            for i, char in enumerate(mot):
                if char != ' ' and random.random() < 0.50:
                    lettres_a_afficher.add(i)  # Ajouter l'indice de la lettre à afficher

            for i, char in enumerate(mot):
                if i in lettres_a_afficher or char == ' ':
                    mot_affiche += char + ' '
                else:
                    mot_affiche += '_ '
        if partie1:
            dessin.itemconfigure(texte_reponse, text=mot_affiche, font=('Arial', taille))
        else:
            dessin.itemconfigure(texte_reponse1, text=mot_affiche, font=('Arial', taille))



    def clavier_pressed(event):
        keyboard_sound.play()
        global liste
        global commence
        global erreurs, partie1

        if commence == True:
            lettre = event.char  # Convertir la lettre en minuscule
            #Ignorer la touche shift pour mettre des lettres en majuscules
            if event.keysym == 'Shift_R' or event.keysym == 'Shift_L':
                return 1
            global liste
            if event.char in liste :
                dessin.delete("lettre_deja_clique")
                message = dessin.create_text(400, 300, text='The letter : ' + str(event.char) +  ' has already been clicked !', fill='black', font=('Arial 20', 15), tags="lettre_deja_clique")
                erreurs +=1
                if partie1:
                    dessin.itemconfigure(texte_erreurs, text='You have : ' + str(11 - erreurs) + ' attemps left !')
                else:
                    dessin.itemconfigure(texte_erreurs1, text='You have : ' + str(11 - erreurs) + ' attemps left !')
                dessin_pendu(erreurs)
                return 1
            else :
                dessin.delete("lettre_clique")
                dessin.delete("lettre_deja_clique")
                liste = liste + str(event.char) + ' | '
                lettre_clique = dessin.create_text(400, 250, text='| '+ liste, fill='black', font=('Arial 20', 15), tags="lettre_clique")

                if lettre not in mot_choisi.lower():
                    erreurs +=1
                    if partie1:
                        dessin.itemconfigure(texte_erreurs, text='You have : ' + str(11 - erreurs)+ ' attemps left !')
                    else:
                        dessin.itemconfigure(texte_erreurs1, text='You have : ' + str(11 - erreurs) + ' attemps left !')
                    dessin_pendu(erreurs)
                return 2


    def lettre_dans_mot(event):
        global mot_cherche
        global mot_affiche
        global commence, partie1
        if commence == True:
            reponse_fonc = clavier_pressed(event)
            if reponse_fonc != 1:
                nouvelle_affiche = ''
                for i in range(len(mot_affiche) // 2):  # Ensure the loop doesn't exceed the length of mot_affiche
                    lettre = mot_cherche[i]
                    if lettre == event.char:
                        nouvelle_affiche += lettre + ' '
                    else:
                        if mot_choisi[i] == ' ':
                            nouvelle_affiche += ' '
                        else:
                            nouvelle_affiche += mot_affiche[i * 2] + ' '  # Update the index according to the new loop

                mot_affiche = nouvelle_affiche
                verifie(nouvelle_affiche)
                if partie1:
                    dessin.itemconfigure(texte_reponse, text=nouvelle_affiche)
                else:
                    dessin.itemconfigure(texte_reponse1, text=nouvelle_affiche)


    def verifie(mot):
        global mot_affiche
        global commence
        
        global mot_choisi
        global ancien_mot
        if '_' not in mot_affiche:
            win_sound.play()
            ancien_mot.append(mot_choisi)
            reponse = obtenir_definition(ancien_mot[-1])
            gagner = dessin.create_text(400, 400, text='You WON !!', fill='white', font='Arial 20')
            commence = False
            dessin.after(4000, reinitialiser_jeu)

    def lien_url(event):
        import webbrowser
        global mot_choisi
        webbrowser.open("https://dictionary.cambridge.org/dictionary/english/" + str(mot_choisi))

    def lien_url1(event):
        import webbrowser
        global mot_choisi
        webbrowser.open("https://dictionary.cambridge.org/dictionary/english/" + str(ancien_mot[-1]))


    def obtenir_definition(mot):
        #parsing html
        boutton_def = dessin.create_line(600, 350, 700, 350, width=50, fill='#B882EE')
        dessin.tag_bind(boutton_def, '<Button-1>', lien_url)

        text_def = dessin.create_text(650, 350,  text="DEFINITION", fill='white', font='Arial')
        dessin.tag_bind(text_def, '<Button-1>', lien_url)


    def dessin_pendu(nb):
        global commence
        if nb == 1 or nb > 1:
            pendu_1 = dessin.create_line(20, 500, 220, 500, width=5, fill='black')
            if nb == 2 or nb > 1:
                pendu_2 = dessin.create_line(70, 300, 70, 500, width=5, fill='black')
                if nb == 3 or nb > 2:
                    pendu_3 = dessin.create_line(70, 300, 170, 300, width=5, fill='black')
                    if nb == 4 or nb > 3:
                        pendu_4 = dessin.create_line(70, 350, 120, 300, width=5, fill='black')
                        if nb == 5 or nb > 4:
                            pendu_5 = dessin.create_line(170, 300, 170, 350, width=5, fill='black')
                            if nb == 6 or nb > 5:
                                pendu_6 = dessin.create_oval(150, 350, 190, 390, outline='black', width=5)
                                if nb == 7 or nb > 6:
                                    pendu_7 = dessin.create_line(170, 390, 170, 450, width=5, fill='black')
                                    if nb == 8 or nb > 7:
                                        # Bras gauche
                                        pendu_8 = dessin.create_line(170, 410, 140, 380, width=5, fill='black')
                                        if nb == 9 or nb > 8:
                                            # Bras droit
                                            pendu_9 = dessin.create_line(170, 410, 200, 380, width=5, fill='black')
                                            if nb == 10 or nb > 9:
                                                # Jambe gauche
                                                pendu_10 = dessin.create_line(170, 450, 140, 480, width=5, fill='black')
                                                if nb == 11 or nb > 10:
                                                    # Jambe droite
                                                    global ancien_mot
                                                    lose_sound.play()
                                                    pendu_11 = dessin.create_line(170, 450, 200, 480, width=5, fill='black')
                                                    perdu = dessin.create_text(400, 400, text='You lose ! The word was : '+ str(mot_choisi), fill='white', font='Arial 20')
                                                    dessin.itemconfigure(perdu)
                                                    ancien_mot.append(mot_choisi)
                                                    reponse = obtenir_definition(ancien_mot[-1])
                                                    commence = False
                                                    dessin.after(4000, reinitialiser_jeu)



    def reinitialiser_jeu():
        global mot_choisi, la_taille, liste, mot_cherche, mot_affiche, commence, erreurs, partie1
        partie1= False
        mot_choisi = ''
        la_taille = 100
        liste = ''
        mot_cherche = ''
        mot_affiche = ''
        commence = False
        erreurs = 0

        # Supprimer tous les éléments du canevas
        dessin.delete("all")

        # Redessiner les éléments de base
        rectangle_boutton = dessin.create_line(500, 500, 300, 500, width=50, fill='#008900', tags="boutton_commencer")
        dessin.tag_bind(rectangle_boutton, '<Button-1>', aleatoire_mot)

        Commencer_boutton = dessin.create_text(400, 500, text='START', fill='white', font='Arial 20', tags="boutton_commencer")
        dessin.tag_bind(Commencer_boutton, '<Button-1>', aleatoire_mot)

        dessin.create_rectangle(40, 30, 760, 190, fill="#c09b72")

        rectangle_boutton1 = dessin.create_line(750, 110, 50, 110, width=150, fill='#008900')
        dessin.tag_bind(rectangle_boutton1)

        global texte_reponse1
        texte_reponse1 = dessin.create_text(400, 100, text='', fill='black', font=('Arial', la_taille))

        rectangle_boutton = dessin.create_line(0, 0, 100, 0, width=50, fill='#014911')
        dessin.tag_bind(rectangle_boutton, '<Button-1>', principal_menu)

        Commencer_boutton = dessin.create_text(50, 15, text='BACK', fill='white', font='Arial')
        dessin.tag_bind(Commencer_boutton, '<Button-1>', principal_menu)

        global texte_erreurs1
        texte_erreurs1 = dessin.create_text(650, 450, text='You have : 11 attemps left !', fill='black', font='Arial 20')


        boutton_def = dessin.create_line(600, 350, 700, 350, width=50, fill='#B882EE')
        dessin.tag_bind(boutton_def, '<Button-1>', lien_url1)

        text_def = dessin.create_text(650, 350,  text="DÉFINITION", fill='white', font='Arial')
        dessin.tag_bind(text_def, '<Button-1>', lien_url1)


    global partie1
    partie1= True
    ##----- Création de la fenêtre -----##

    fen.title('Hangman easy')

    ##----- Création des boutons -----##

    bouton_quitter = Button(fen, text='QUITTER/STOP', command=fen.destroy)
    bouton_quitter.grid(row = 15, column = 0, padx = 3, pady = 3, sticky=E)


    ##----- Création du canevas -----##

    dessin = Canvas(fen, width = 800, height = 600, bg = '#9897A9')
    dessin.grid(row = 0, column =0, rowspan = 15, sticky = N)

    if facile_fen == True or moyen_fen == True or difficile_fen == True or fen_accueil == True:
        # Efface tout le contenu existant sur le canevas
        dessin.delete("all")

    ##----- Retour accueil -----##

    rectangle_boutton = dessin.create_line(0, 0, 100, 0, width=50, fill='#014911')
    dessin.tag_bind(rectangle_boutton, '<Button-1>', principal_menu)

    Commencer_boutton = dessin.create_text(50, 15, text='BACK', fill='white', font='Arial')
    dessin.tag_bind(Commencer_boutton, '<Button-1>', principal_menu)

    ##----- Dessiner dans le canevas -----##

    rectangle_boutton = dessin.create_line(500, 500, 300, 500, width=50, fill='#008900', tags="boutton_commencer")
    dessin.tag_bind(rectangle_boutton, '<Button-1>', aleatoire_mot)

    Commencer_boutton = dessin.create_text(400, 500, text='START', fill='white', font='Arial 20',tags="boutton_commencer")
    dessin.tag_bind(Commencer_boutton, '<Button-1>', aleatoire_mot)


    ##----- Mots a chercher -----##
    dessin.create_rectangle(40, 30, 760, 190, fill="#c09b72")

    rectangle_boutton1 = dessin.create_line(750, 110, 50, 110, width=150, fill='#008900')
    dessin.tag_bind(rectangle_boutton1)


    ##-----Création des zones de texte-----##
    texte_erreurs = dessin.create_text(650, 450, text='You have : 11 attemps left !', fill='black', font='Arial 20')
    texte_reponse = dessin.create_text(400, 100, text=str(mot_choisi), fill='black', font=('Arial 20', la_taille))


    ##-----Clavier-----##

    fen.bind("<Key>",lettre_dans_mot)

    ##----- Programme principal -----##

    # Boucle d'attente des événements


def medium():
    button_sound.play()
    global facile_fen
    global moyen_fen
    global difficile_fen
    global fen_accueil
    difficile_fen = False
    moyen_fen = True
    facile_fen = False
    fen_accueil = False
    ##----- Fonction -----##
    global mot_choisi
    global la_taille
    global liste
    global mot_cherche
    global mot_affiche
    global commence
    global erreurs
    global ancien_mot
    mot_choisi=''
    la_taille = 100
    liste = ''
    mot_cherche = ''
    mot_affiche = ''
    commence = False  # Variable pour suivre si le jeu a commencé
    erreurs = 0
    ancien_mot = []

    def aleatoire_mot(event):
        button_sound.play()
        dessin.delete("boutton_commencer")
        with open(path_to_ukenglish, 'r', encoding='latin-1') as fichier:
            mots = fichier.readlines()
            global mot_choisi
            mot_choisi = random.choice(mots).strip()  # strip() pour supprimer les sauts de ligne
            for lettre in mot_choisi:
                if lettre == " ":
                    mot_choisi = random.choice(mots).strip()  # strip() pour supprimer les sauts de ligne
            global mot_cherche
            mot_cherche = mot_choisi.lower()
            global la_taille
            la_taille = taille_du_mot(mot_choisi)
            afficher_mot(mot_choisi.lower(), taille_du_mot(mot_choisi))  # Convertir le mot en minuscule pour l'affichage sinon ya probleme
        global commence
        commence = True
    path_to_liste_francais = os.path.join(application_path, "liste_francais.txt")
    path_to_ukenglish = os.path.join(application_path, "ukenglish.txt")

    def taille_du_mot(mot):
        longueur = len(mot)
        if longueur < 7:
            return 100
        if 11 > longueur > 9 :
            return 60
        if 12 >= longueur >= 11 :
            return 50
        if longueur > 12 :
            return 40
        else :
            return 70


    def afficher_mot(mot, taille):
        global mot_affiche, partie1
        mot_affiche = ''
        lettres_a_afficher = set()

        for i, char in enumerate(mot):
            if char != ' ' and random.random() < 0.33:
                lettres_a_afficher.add(i)  # Ajouter l'indice de la lettre à afficher

        for i, char in enumerate(mot):
            if i in lettres_a_afficher or char == ' ':
                mot_affiche += char + ' '
            else:
                mot_affiche += '_ '
        if partie1:
            dessin.itemconfigure(texte_reponse, text=mot_affiche, font=('Arial', taille))
        else:
            dessin.itemconfigure(texte_reponse1, text=mot_affiche, font=('Arial', taille))



    def clavier_pressed(event):
        keyboard_sound.play()
        global liste
        global commence
        global erreurs, partie1

        if commence == True:
            lettre = event.char  # Convertir la lettre en minuscule
            #Ignorer la touche shift pour mettre des lettres en majuscules
            if event.keysym == 'Shift_R' or event.keysym == 'Shift_L':
                return 1
            global liste
            if event.char in liste :
                dessin.delete("lettre_deja_clique")
                message = dessin.create_text(400, 300, text='The letter : ' + str(event.char) +  ' has already been clicked !', fill='black', font=('Arial 20', 15), tags="lettre_deja_clique")
                erreurs +=1
                if partie1:
                    dessin.itemconfigure(texte_erreurs, text='You have : ' + str(11 - erreurs) + ' attemps left !')
                else:
                    dessin.itemconfigure(texte_erreurs1, text='You have : ' + str(11 - erreurs) + ' attemps left !')
                dessin_pendu(erreurs)
                return 1
            else :
                dessin.delete("lettre_clique")
                dessin.delete("lettre_deja_clique")
                liste = liste + str(event.char) + ' | '
                lettre_clique = dessin.create_text(400, 250, text='| '+ liste, fill='black', font=('Arial 20', 15), tags="lettre_clique")

                if lettre not in mot_choisi.lower():
                    erreurs +=1
                    if partie1:
                        dessin.itemconfigure(texte_erreurs, text='You have : ' + str(11 - erreurs) + ' attemps left !')
                    else:
                        dessin.itemconfigure(texte_erreurs1, text='You have : ' + str(11 - erreurs) + ' attemps left !')
                    dessin_pendu(erreurs)
                return 2


    def lettre_dans_mot(event):
        global mot_cherche
        global mot_affiche
        global commence, partie1
        if commence == True:
            reponse_fonc = clavier_pressed(event)
            if reponse_fonc != 1:
                nouvelle_affiche = ''
                for i in range(len(mot_affiche) // 2):  # Ensure the loop doesn't exceed the length of mot_affiche
                    lettre = mot_cherche[i]
                    if lettre == event.char:
                        nouvelle_affiche += lettre + ' '
                    else:
                        if mot_choisi[i] == ' ':
                            nouvelle_affiche += ' '
                        else:
                            nouvelle_affiche += mot_affiche[i * 2] + ' '  # Update the index according to the new loop

                mot_affiche = nouvelle_affiche
                verifie(nouvelle_affiche)
                if partie1:
                    dessin.itemconfigure(texte_reponse, text=nouvelle_affiche)
                else:
                    dessin.itemconfigure(texte_reponse1, text=nouvelle_affiche)


    def verifie(mot):
        global mot_affiche
        global commence
        
        global mot_choisi
        global ancien_mot
        if '_' not in mot_affiche:
            ancien_mot.append(mot_choisi)
            reponse = obtenir_definition(ancien_mot[-1])
            win_sound.play()
            gagner = dessin.create_text(400, 400, text='You WON !!', fill='white', font='Arial 20')
            commence = False
            dessin.after(4000, reinitialiser_jeu)

    def lien_url(event):
        import webbrowser
        global mot_choisi
        webbrowser.open("https://dictionary.cambridge.org/dictionary/english/" + str(mot_choisi))

    def lien_url1(event):
        import webbrowser
        global mot_choisi
        webbrowser.open("https://dictionary.cambridge.org/dictionary/english/" + str(ancien_mot[-1]))


    def obtenir_definition(mot):
        #parsing html
        boutton_def = dessin.create_line(600, 350, 700, 350, width=50, fill='#B882EE')
        dessin.tag_bind(boutton_def, '<Button-1>', lien_url)

        text_def = dessin.create_text(650, 350,  text="DEFINITION", fill='white', font='Arial')
        dessin.tag_bind(text_def, '<Button-1>', lien_url)


    def dessin_pendu(nb):
        global commence
        if nb == 1 or nb > 1:
            pendu_1 = dessin.create_line(20, 500, 220, 500, width=5, fill='black')
            if nb == 2 or nb > 1:
                pendu_2 = dessin.create_line(70, 300, 70, 500, width=5, fill='black')
                if nb == 3 or nb > 2:
                    pendu_3 = dessin.create_line(70, 300, 170, 300, width=5, fill='black')
                    if nb == 4 or nb > 3:
                        pendu_4 = dessin.create_line(70, 350, 120, 300, width=5, fill='black')
                        if nb == 5 or nb > 4:
                            pendu_5 = dessin.create_line(170, 300, 170, 350, width=5, fill='black')
                            if nb == 6 or nb > 5:
                                pendu_6 = dessin.create_oval(150, 350, 190, 390, outline='black', width=5)
                                if nb == 7 or nb > 6:
                                    pendu_7 = dessin.create_line(170, 390, 170, 450, width=5, fill='black')
                                    if nb == 8 or nb > 7:
                                        # Bras gauche
                                        pendu_8 = dessin.create_line(170, 410, 140, 380, width=5, fill='black')
                                        if nb == 9 or nb > 8:
                                            # Bras droit
                                            pendu_9 = dessin.create_line(170, 410, 200, 380, width=5, fill='black')
                                            if nb == 10 or nb > 9:
                                                # Jambe gauche
                                                pendu_10 = dessin.create_line(170, 450, 140, 480, width=5, fill='black')
                                                if nb == 11 or nb > 10:
                                                    # Jambe droite
                                                    global ancien_mot
                                                    pendu_11 = dessin.create_line(170, 450, 200, 480, width=5, fill='black')
                                                    perdu = dessin.create_text(400, 400, text='You lose ! The word was : '+ str(mot_choisi), fill='white', font='Arial 20')
                                                    dessin.itemconfigure(perdu)
                                                    ancien_mot.append(mot_choisi)
                                                    lose_sound.play()
                                                    reponse = obtenir_definition(ancien_mot[-1])
                                                    commence = False
                                                    dessin.after(4000, reinitialiser_jeu)



    def reinitialiser_jeu():
        global mot_choisi, la_taille, liste, mot_cherche, mot_affiche, commence, erreurs, partie1
        partie1= False
        mot_choisi = ''
        la_taille = 100
        liste = ''
        mot_cherche = ''
        mot_affiche = ''
        commence = False
        erreurs = 0

        # Supprimer tous les éléments du canevas
        dessin.delete("all")

        # Redessiner les éléments de base
        rectangle_boutton = dessin.create_line(500, 500, 300, 500, width=50, fill='#d47904', tags="boutton_commencer")
        dessin.tag_bind(rectangle_boutton, '<Button-1>', aleatoire_mot)

        Commencer_boutton = dessin.create_text(400, 500, text='START', fill='white', font='Arial 20', tags="boutton_commencer")
        dessin.tag_bind(Commencer_boutton, '<Button-1>', aleatoire_mot)

        dessin.create_rectangle(40, 30, 760, 190, fill="#c09b72")

        rectangle_boutton1 = dessin.create_line(750, 110, 50, 110, width=150, fill='#d47904')
        dessin.tag_bind(rectangle_boutton1)

        global texte_reponse1
        texte_reponse1 = dessin.create_text(400, 100, text='', fill='black', font=('Arial', la_taille))

        rectangle_boutton = dessin.create_line(0, 0, 100, 0, width=50, fill='#014911')
        dessin.tag_bind(rectangle_boutton, '<Button-1>', principal_menu)

        Commencer_boutton = dessin.create_text(50, 15, text='BACK', fill='white', font='Arial')
        dessin.tag_bind(Commencer_boutton, '<Button-1>', principal_menu)
        global texte_erreurs1
        texte_erreurs1 = dessin.create_text(650, 450, text='You have 11 attemps left!', fill='black', font='Arial 20')


        boutton_def = dessin.create_line(600, 350, 700, 350, width=50, fill='#B882EE')
        dessin.tag_bind(boutton_def, '<Button-1>', lien_url1)

        text_def = dessin.create_text(650, 350,  text="DÉFINITION", fill='white', font='Arial')
        dessin.tag_bind(text_def, '<Button-1>', lien_url1)


    global partie1
    partie1 = True
    ##----- Création de la fenêtre -----##

    fen.title('Hangman medium')

    ##----- Création des boutons -----##

    bouton_quitter = Button(fen, text='QUITTER/STOP', command=fen.destroy)
    bouton_quitter.grid(row = 15, column = 0, padx = 3, pady = 3, sticky=E)


    ##----- Création du canevas -----##

    dessin = Canvas(fen, width = 800, height = 600, bg = '#9897A9')
    dessin.grid(row = 0, column =0, rowspan = 15, sticky = N)

    if facile_fen == True or moyen_fen == True or difficile_fen == True or fen_accueil == True:
        # Efface tout le contenu existant sur le canevas
        dessin.delete("all")

    ##----- Retour accueil -----##

    rectangle_boutton = dessin.create_line(0, 0, 100, 0, width=50, fill='#014911')
    dessin.tag_bind(rectangle_boutton, '<Button-1>', principal_menu)

    Commencer_boutton = dessin.create_text(50, 15, text='BACK', fill='white', font='Arial')
    dessin.tag_bind(Commencer_boutton, '<Button-1>', principal_menu)

    ##----- Dessiner dans le canevas -----##

    rectangle_boutton = dessin.create_line(500, 500, 300, 500, width=50, fill='#d47904', tags="boutton_commencer")
    dessin.tag_bind(rectangle_boutton, '<Button-1>', aleatoire_mot)

    Commencer_boutton = dessin.create_text(400, 500, text='START', fill='white', font='Arial 20',tags="boutton_commencer")
    dessin.tag_bind(Commencer_boutton, '<Button-1>', aleatoire_mot)


    ##----- Mots a chercher -----##
    dessin.create_rectangle(40, 30, 760, 190, fill="#c09b72")

    rectangle_boutton1 = dessin.create_line(750, 110, 50, 110, width=150, fill='#d47904')
    dessin.tag_bind(rectangle_boutton1)


    ##-----Création des zones de texte-----##
    texte_erreurs = dessin.create_text(650, 450, text='You have 11 attemps left !', fill='black', font='Arial 20')
    texte_reponse = dessin.create_text(400, 100, text=str(mot_choisi), fill='black', font=('Arial 20', la_taille))


    ##-----Clavier-----##

    fen.bind("<Key>",lettre_dans_mot)

    ##----- Programme principal -----##

    # Boucle d'attente des événements

def hard():
    button_sound.play()
    global facile_fen
    global moyen_fen
    global difficile_fen
    global fen_accueil
    difficile_fen = True
    moyen_fen = False
    facile_fen = False
    fen_accueil = False


    ##----- Fonction -----##
    global mot_choisi
    global la_taille
    global liste
    global mot_cherche
    global mot_affiche
    global commence
    global erreurs
    global ancien_mot
    mot_choisi=''
    la_taille = 100
    liste = ''
    mot_cherche = ''
    mot_affiche = ''
    commence = False  # Variable pour suivre si le jeu a commencé
    erreurs = 0
    ancien_mot = []

    def aleatoire_mot(event):
        button_sound.play()
        dessin.delete("boutton_commencer")
        with open(path_to_ukenglish, 'r', encoding='latin-1') as fichier:
            mots = fichier.readlines()
            global mot_choisi
            mot_choisi = random.choice(mots).strip()  # strip() pour supprimer les sauts de ligne
            for lettre in mot_choisi:
                if lettre == " ":
                    mot_choisi = random.choice(mots).strip()  # strip() pour supprimer les sauts de ligne
            global mot_cherche
            mot_cherche = mot_choisi
            global la_taille
            la_taille = taille_du_mot(mot_choisi)
            afficher_mot(mot_choisi.lower(), taille_du_mot(mot_choisi))  # Convertir le mot en minuscule pour l'affichage sinon ya probleme
        global commence
        commence = True
    path_to_liste_francais = os.path.join(application_path, "liste_francais.txt")
    path_to_ukenglish = os.path.join(application_path, "ukenglish.txt")

    def taille_du_mot(mot):
        longueur = len(mot)
        if longueur < 7:
            return 100
        if 11 > longueur > 9 :
            return 60
        if 12 >= longueur >= 11 :
            return 50
        if longueur > 12 :
            return 40
        else :
            return 70


    def afficher_mot(mot, taille):
        global mot_affiche, partie1
        mot_affiche = ''

        for char in mot:
            if char == ' ':
                mot_affiche += ' '
            else:
                mot_affiche += '_ '
        if partie1:
            dessin.itemconfigure(texte_reponse, text=mot_affiche, font=('Arial', taille))
        else:
            dessin.itemconfigure(texte_reponse1, text=mot_affiche, font=('Arial', taille))



    def clavier_pressed(event):
        keyboard_sound.play()
        global liste
        global commence
        global erreurs, partie1

        if commence == True:
            lettre = event.char  # Convertir la lettre en minuscule
            #Ignorer la touche shift pour mettre des lettres en majuscules
            if event.keysym == 'Shift_R' or event.keysym == 'Shift_L':
                return 1
            global liste
            if event.char in liste :
                dessin.delete("lettre_deja_clique")
                message = dessin.create_text(400, 300, text='The letter : ' + str(event.char) +  ' has been already clicked!', fill='black', font=('Arial 20', 15), tags="lettre_deja_clique")
                erreurs +=1
                if partie1:
                    dessin.itemconfigure(texte_erreurs, text='You have : ' + str(6 - erreurs) + ' attemps left !')
                else:
                    dessin.itemconfigure(texte_erreurs1, text='You have : ' + str(6 - erreurs) + ' attemps left !')
                dessin_pendu(erreurs)
                return 1
            else :
                dessin.delete("lettre_clique")
                dessin.delete("lettre_deja_clique")
                liste = liste + str(event.char) + ' | '
                lettre_clique = dessin.create_text(400, 250, text='| '+ liste, fill='black', font=('Arial 20', 15), tags="lettre_clique")

                if lettre not in mot_choisi.lower():
                    erreurs +=1
                    if partie1:
                        dessin.itemconfigure(texte_erreurs, text='You have : ' + str(6 - erreurs) + ' attemps left !')
                    else:
                        dessin.itemconfigure(texte_erreurs1, text='You have : ' + str(6 - erreurs) + ' attemps left !')
                    dessin_pendu(erreurs)
                return 2


    def lettre_dans_mot(event):
        global mot_cherche
        global mot_affiche
        global commence, partie1
        if commence == True:
            reponse_fonc = clavier_pressed(event)
            if reponse_fonc != 1:
                nouvelle_affiche = ''
                for i in range(len(mot_affiche) // 2):  # Ensure the loop doesn't exceed the length of mot_affiche
                    lettre = mot_cherche[i]
                    if lettre == event.char:
                        nouvelle_affiche += lettre + ' '
                    else:
                        if mot_choisi[i] == ' ':
                            nouvelle_affiche += ' '
                        else:
                            nouvelle_affiche += mot_affiche[i * 2] + ' '  # Update the index according to the new loop

                mot_affiche = nouvelle_affiche
                verifie(nouvelle_affiche)
                if partie1 :
                    dessin.itemconfigure(texte_reponse, text=nouvelle_affiche)
                else:
                    dessin.itemconfigure(texte_reponse1, text=nouvelle_affiche)


    def verifie(mot):
        global mot_affiche
        global commence
        
        global mot_choisi
        global ancien_mot
        if '_' not in mot_affiche:
            ancien_mot.append(mot_choisi)
            win_sound.play()
            reponse = obtenir_definition(ancien_mot[-1])
            gagner = dessin.create_text(400, 400, text='You WON !!', fill='white', font='Arial 20')
            commence = False
            dessin.after(4000, reinitialiser_jeu)

    def lien_url(event):
        import webbrowser
        global mot_choisi
        webbrowser.open("https://dictionary.cambridge.org/dictionary/english/" + str(mot_choisi))

    def lien_url1(event):
        import webbrowser
        global mot_choisi
        global ancien_mot
        webbrowser.open("https://dictionary.cambridge.org/dictionary/english/" + str(ancien_mot[-1]))


    def obtenir_definition(mot):
        #parsing html
        boutton_def = dessin.create_line(600, 350, 700, 350, width=50, fill='#B882EE')
        dessin.tag_bind(boutton_def, '<Button-1>', lien_url)

        text_def = dessin.create_text(650, 350,  text="DEFINITION", fill='white', font='Arial')
        dessin.tag_bind(text_def, '<Button-1>', lien_url)


    def dessin_pendu(nb):
        global commence
        global mot_choisi
        if nb == 1 or nb > 1:
            pendu_1 = dessin.create_line(20, 500, 220, 500, width=5, fill='black')
            pendu_2 = dessin.create_line(70, 300, 70, 500, width=5, fill='black')
            if nb == 2 or nb > 1:
                pendu_3 = dessin.create_line(70, 300, 170, 300, width=5, fill='black')
                pendu_4 = dessin.create_line(70, 350, 120, 300, width=5, fill='black')
                if nb == 3 or nb > 2:
                    pendu_5 = dessin.create_line(170, 300, 170, 350, width=5, fill='black')
                    pendu_6 = dessin.create_oval(150, 350, 190, 390, outline='black', width=5)
                    if nb == 4 or nb > 3:
                        pendu_7 = dessin.create_line(170, 390, 170, 450, width=5, fill='black')
                        # Bras gauche
                        pendu_8 = dessin.create_line(170, 410, 140, 380, width=5, fill='black')
                        if nb == 5 or nb > 4:
                            # Bras droit
                            pendu_9 = dessin.create_line(170, 410, 200, 380, width=5, fill='black')
                            # Jambe gauche
                            pendu_10 = dessin.create_line(170, 450, 140, 480, width=5, fill='black')
                            if nb == 6 or nb > 5:
                                # Jambe droite
                                global ancien_mot
                                pendu_11 = dessin.create_line(170, 450, 200, 480, width=5, fill='black')
                                perdu = dessin.create_text(400, 400, text='You Lose ! The word was : '+ str(mot_choisi), fill='white', font='Arial 20')
                                dessin.itemconfigure(perdu)
                                lose_sound.play()
                                ancien_mot.append(mot_choisi)
                                reponse = obtenir_definition(ancien_mot[-1])
                                commence = False
                                dessin.after(4000, reinitialiser_jeu)



    def reinitialiser_jeu():
        global partie1
        partie1 = False
        global mot_choisi, la_taille, liste, mot_cherche, mot_affiche, commence, erreurs, ancien_mot
        mot_choisi = ''
        la_taille = 100
        liste = ''
        mot_cherche = ''
        mot_affiche = ''
        commence = False
        erreurs = 0

        # Supprimer tous les éléments du canevas
        dessin.delete("all")

        # Redessiner les éléments de base
        rectangle_boutton = dessin.create_line(500, 500, 300, 500, width=50, fill='#cc0e00', tags="boutton_commencer")
        dessin.tag_bind(rectangle_boutton, '<Button-1>', aleatoire_mot)

        Commencer_boutton = dessin.create_text(400, 500, text='START', fill='white', font='Arial 20', tags="boutton_commencer")
        dessin.tag_bind(Commencer_boutton, '<Button-1>', aleatoire_mot)

        dessin.create_rectangle(40, 30, 760, 190, fill="#c09b72")

        rectangle_boutton1 = dessin.create_line(750, 110, 50, 110, width=150, fill='#cc0e00')
        dessin.tag_bind(rectangle_boutton1)

        global texte_reponse1
        texte_reponse1 = dessin.create_text(400, 100, text='', fill='black', font=('Arial', la_taille))

        rectangle_boutton = dessin.create_line(0, 0, 100, 0, width=50, fill='#014911')
        dessin.tag_bind(rectangle_boutton, '<Button-1>', principal_menu)

        Commencer_boutton = dessin.create_text(50, 15, text='BACK', fill='white', font='Arial')
        dessin.tag_bind(Commencer_boutton, '<Button-1>', principal_menu)

        global texte_erreurs1
        texte_erreurs1 = dessin.create_text(650, 450, text='You have : 6 attemps left !', fill='black', font='Arial 20')

        boutton_def = dessin.create_line(600, 350, 700, 350, width=50, fill='#B882EE')
        dessin.tag_bind(boutton_def, '<Button-1>', lien_url1)

        text_def = dessin.create_text(650, 350,  text="DÉFINITION", fill='white', font='Arial')
        dessin.tag_bind(text_def, '<Button-1>', lien_url1)

    global partie1
    partie1 = True
    ##----- Création de la fenêtre -----##

    fen.title('Hangman hard')

    ##----- Création des boutons -----##

    bouton_quitter = Button(fen, text='QUITTER/STOP', command=fen.destroy)
    bouton_quitter.grid(row = 15, column = 0, padx = 3, pady = 3, sticky=E)


    ##----- Création du canevas -----##

    dessin = Canvas(fen, width = 800, height = 600, bg = '#9897A9')
    dessin.grid(row = 0, column =0, rowspan = 15, sticky = N)

    if facile_fen == True or moyen_fen == True or difficile_fen == True or fen_accueil == True:
        # Efface tout le contenu existant sur le canevas
        dessin.delete("all")

    ##----- Retour accueil -----##

    rectangle_boutton = dessin.create_line(0, 0, 100, 0, width=50, fill='#014911')
    dessin.tag_bind(rectangle_boutton, '<Button-1>', principal_menu)

    Commencer_boutton = dessin.create_text(50, 15, text='BACK', fill='white', font='Arial')
    dessin.tag_bind(Commencer_boutton, '<Button-1>', principal_menu)

    ##----- Dessiner dans le canevas -----##

    rectangle_boutton = dessin.create_line(500, 500, 300, 500, width=50, fill='#cc0e00', tags="boutton_commencer")
    dessin.tag_bind(rectangle_boutton, '<Button-1>', aleatoire_mot)

    Commencer_boutton = dessin.create_text(400, 500, text='START', fill='white', font='Arial 20',tags="boutton_commencer")
    dessin.tag_bind(Commencer_boutton, '<Button-1>', aleatoire_mot)


    ##----- Mots a chercher -----##
    dessin.create_rectangle(40, 30, 760, 190, fill="#c09b72")

    rectangle_boutton1 = dessin.create_line(750, 110, 50, 110, width=150, fill='#cc0e00')
    dessin.tag_bind(rectangle_boutton1)


    ##-----Création des zones de texte-----##
    texte_erreurs = dessin.create_text(650, 450, text='You have : 6 attemps left !', fill='black', font='Arial 20')
    texte_reponse = dessin.create_text(400, 100, text=str(mot_choisi), fill='black', font=('Arial 20', la_taille))


    ##-----Clavier-----##

    fen.bind("<Key>",lettre_dans_mot)

    ##----- Programme principal -----##

    # Boucle d'attente des événements

def the_rules():
    button_sound.play()
    global facile_fen
    global moyen_fen
    global difficile_fen
    global fen_accueil
    difficile_fen = True
    moyen_fen = False
    facile_fen = False
    fen_accueil = True

    ##----- Création de la fenêtre -----##

    fen.title('The rules')

    ##----- Création du canevas -----##
    global dessin

    dessin = Canvas(fen, width = 800, height = 600, bg = '#9897A9')
    dessin.grid(row = 0, column =0, rowspan = 15, sticky = N)

    if facile_fen == True or moyen_fen == True or difficile_fen == True or fen_accueil == True:
        # Efface tout le contenu existant sur le canevas
        dessin.delete("all")

    texte_regles = """

Operation:
        - The game will start when the user (you) clicks on the "Start" button. _ will be
        displayed based on the chosen difficulty level.
        - The objective is to find the missing letters by pressing the corresponding keys
        on the keyboard.
        - The game ends when the user runs out of attempts (the hangman is completely drawn)
        or when all the letters are found. At that point, the user (you) can find the
        definition of the searched word by pressing the "Definition" button.

Attention:
        - It is possible to search for a word separated by a hyphen (-), or even to search
        for two words, in which case you need to press the space bar.
        - If the user selects the Hard mode :Uppercase letters (M) and lowercase letters
        (m) are not considered the same.
        - When the user starts a game in the "Easy" or "Medium" difficulty levels, a
        few letters will be displayed. It might be possible to search for a letter that
        was already displayed when the word was first shown. For example, if the word
        is "tree" and the program displays: _ r _ e, the user still need to find the letter
        "e" even though it's already displayed.
        - When the user starts a game in the 'Easy' or 'Medium' difficulty levels, a
        few letters will be displayed. If the user clicks on a letter that was already shown
        and it appears only once in the word, then the mistake will not be counted,
        exceptionally. For example, if the word is 'tree' and the program displays: _ _ e e,
        and the user presses the letter 'e', it will not count as an error.
        However, if the user presses it a second time, then it will count as an error.
        - The user can lose attempts by pressing a key multiple times that has already been
        clicked or if the clicked key is not part of the word to guess.


    """
    dessin.create_text(400, 310, text=str(texte_regles), fill='black', font=('Arial', 13))



    rectangle_boutton = dessin.create_line(0, 0, 100, 0, width=50, fill='#014911')
    dessin.tag_bind(rectangle_boutton, '<Button-1>', principal_menu)

    Commencer_boutton = dessin.create_text(50, 15, text='BACK', fill='white', font='Arial')
    dessin.tag_bind(Commencer_boutton, '<Button-1>', principal_menu)


def principal_menu(event):
    button_sound.play()
    global facile_fen
    global moyen_fen
    global difficile_fen
    global fen_accueil
    difficile_fen = False
    moyen_fen = False
    facile_fen = False
    fen_accueil = True


    ##----- Fonctions -----##

    def langue_francais():
        accueil(1)



    def grossir(event, btn, taille, aaa):
        btn.configure(width=aaa+2,font=("Arial", taille+2))

    def petit(event, btn, taille, aaa):
        btn.configure(width=aaa,font=("Arial", taille))

    ##----- Création de la fenêtre -----##



    fen.title('Home Page')


    ##----- Création du canevas -----##
    global dessin

    dessin = Canvas(fen, width = 800, height = 600, bg = '#9897A9')
    dessin.grid(row = 0, column =0, rowspan = 15, sticky = N)

    if facile_fen == True or moyen_fen == True or difficile_fen == True or fen_accueil == True:
        # Efface tout le contenu existant sur le canevas
        dessin.delete("all")
    ##----- behind buttons-----##
    dessin.create_rectangle(570, 200, 790, 560, fill="#c09b72") # droite
    dessin.create_rectangle(580, 210, 780, 550, fill="#d8cdc1")

    dessin.create_rectangle(10, 200, 230, 560, fill="#c09b72") # gauche
    dessin.create_rectangle(20, 210, 220, 550, fill="#d8cdc1")

    dessin.create_rectangle(220, 170, 580, 590, fill="#c09b72") # milieu
    dessin.create_rectangle(230, 180, 570, 580, fill="#d8cdc1")

    ##----- title behind buttons-----##

    dessin.create_rectangle(610, 180, 750, 230, fill="#d1d72d") # droite

    dessin.create_rectangle(50, 180, 190, 230, fill="#d1d72d") # gauche

    dessin.create_rectangle(260, 140, 540, 210, fill="#d1d72d") # milieu

    ##----- title -----##

    dessin.create_text(400, 50, text="The Hangman", fill='white', font=('Arial', 70))
    dessin.create_text(400, 115, text="Done by Yuri DENIS", fill='white', font=('Arial', 25))

    ##----- title frame -----##

    dessin.create_text(125, 205, text="Langue :", fill='black', font=('Arial', 15, 'underline'))
    dessin.create_text(405, 175, text="Difficulty Levels :", fill='black', font=('Arial', 25, 'underline'))
    dessin.create_text(680, 205, text="The Rules :", fill='black', font=('Arial', 15, 'underline'))

    ##----- Boutton levels-----##

    rectangle_boutton_facile = Button(fen, text="EASY", command=easy, width=22, height = 3, font=("Arial", 11), bg="#008900",fg="white")
    rectangle_boutton_facile.grid(row = 9, padx = 0, sticky=N)
    rectangle_boutton_facile.bind('<Motion>', lambda event,width = 22, taille = 11, btn = rectangle_boutton_facile: grossir(event,btn, taille,width))
    rectangle_boutton_facile.bind('<Leave>', lambda event,width = 22, taille = 11, btn = rectangle_boutton_facile: petit(event,btn, taille,width))

    rectangle_boutton_moyen = Button(fen, text="MEDIUM", command=medium, width=22, height = 3, font=("Arial", 11), bg="#d47904",fg="white")
    rectangle_boutton_moyen.grid(row = 11, padx = 0, sticky=N)
    rectangle_boutton_moyen.bind('<Motion>', lambda event,width = 22, taille = 11, btn = rectangle_boutton_moyen: grossir(event,btn, taille,width))
    rectangle_boutton_moyen.bind('<Leave>', lambda event,width = 22, taille = 11, btn = rectangle_boutton_moyen: petit(event,btn, taille,width))

    rectangle_boutton_difficile = Button(fen, text="HARD", command=hard, width=22, height = 3, font=("Arial", 11), bg="#cc0e00",fg="white")
    rectangle_boutton_difficile.grid(row = 13, padx = 0, sticky=N)
    rectangle_boutton_difficile.bind('<Motion>', lambda event,width = 22, taille = 11, btn = rectangle_boutton_difficile: grossir(event,btn, taille,width))
    rectangle_boutton_difficile.bind('<Leave>', lambda event,width = 22, taille = 11, btn = rectangle_boutton_difficile: petit(event,btn, taille,width))

    ##----- Boutton règles -----##

    rules_button = Button(fen, text="Click here", command=the_rules, width=17, height = 3, font=("Arial", 11), bg="#1567b5",fg="white")
    rules_button.grid(row = 11, padx= 40, sticky=E)
    rules_button.bind('<Motion>', lambda event, taille = 10,width = 16, btn = rules_button: grossir(event,btn, taille,width))
    rules_button.bind('<Leave>', lambda event, taille = 11,width = 17, btn = rules_button: petit(event,btn, taille, width))

    ##----- Boutton langue  -----##


    rectangle_boutton_francais = Button(fen, text="Français", command=langue_francais, width=17, height = 3, font=("Arial", 11), bg="#1567b5",fg="white")
    rectangle_boutton_francais.grid(row = 11, padx= 40, sticky=W)
    rectangle_boutton_francais.bind('<Motion>', lambda event, taille = 10,width = 16, btn = rectangle_boutton_francais: grossir(event,btn, taille,width))
    rectangle_boutton_francais.bind('<Leave>', lambda event, taille = 11,width = 17, btn = rectangle_boutton_francais: petit(event,btn, taille, width))







##----- Programme principal -----##
accueil(1) # démarre accueil, page principal du pendu



fen.mainloop() # Boucle d'attente des événements











#Figma application design