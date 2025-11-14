"""
Jeu de dame - fichier principal
Auteurs : Timothée GAUCHER & Théo FOENKINOS
Date : créé le : 06/11/2023 (pas sur) - dernière modif le : 29/12/2023 (sur)
"""

import pygame
import sys
import plateau
import curseur

from pygame.locals import *


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Jeu de dames v3.1")
sysFont = pygame.font.SysFont("None", 32)
black = (0, 0, 0)
white = (255, 255, 255)
grey2 = (127.5, 127.5, 127.5)
white_black = (10, 10, 10)
grey = (190, 190, 190)
black_grey = (80, 80, 80)
color_space = [0, 0, 0]
sens_color = 0.5  # Pour changer la couleur du texte d'accueil
debut_jeu = True  # Pour afficher les règles avant le début du jeu
cases = []  # Les cases de déplacement du pion qui est sélectionné
indice = 0  # La case sélectionnée pour manger
manger = False  # Saloir si un pion peut manger ou pas
remange = False  # Savoir si un pion a mangé ou pas
pion = None  # L'indice du pion sélectionné
joueur = None  # La variable qui va afficher la couleur du joueur qui a gagné à la fin de la partie
score_j1 = 0
score_j2 = 0
# Création du jeu : le sélecteur et le plateau (les pions sont créés dans la classe plateau)
selector = curseur.Selector(screen)
plateau1 = plateau.Plateau(screen)
plateau1.creer_pions()
# Les textes
aff_legende = sysFont.render("Légende :", 0, black)
dame = sysFont.render("Dame :", 0, black)
dame2 = sysFont.render("D", 0, black)
dame3 = sysFont.render("D", 0, black)
points = sysFont.render("Points :", 0, black)
sysFont2 = pygame.font.SysFont("None", 25)  # pour les sous-légendes
points_pion = sysFont2.render("1 point pour un pion mangé", 0, black)
points_dame = sysFont2.render("2 points pour une dame mangé", 0, black)
# Les textes pour les règles, affichage avant le début du jeu
regle1 = sysFont.render("Règles du jeu de dames : ", 0, black)
regle2 = sysFont2.render("Voir au lien suivant : https://www.regledujeu.fr/regle-jeu-de-dames/", 0, black)
regle3 = sysFont.render("Comment jouer : ", 0, black)
regle4 = sysFont2.render("Pour vous déplacer, cliquez sur un pion ;", 0, black)
regle5 = sysFont2.render("Les cases de déplacement possibles sont affichées en vert une fois le pion sélectionné",
                         0, black)
regle6 = sysFont2.render("Si un pion/dame est en position de manger, il est obligé", 0, black)
regle7 = sysFont2.render("Quand vous avez plusieurs possibilités pour manger,", 0, black)
regle8 = sysFont2.render("vous devez choisir celle qui vous rapporte le plus", 0, black)
regle9 = sysFont2.render("Si jamais vous sélectionnez un pion mais qu'aucune case ne s'affiche en vert,",
                         0, black)
regle10 = sysFont2.render("c'est qu'un autre de vos pions peut manger.", 0, black)

fin_jeu = sysFont.render(f"Le joueur {joueur} a gagné !", 0, black)


def afficher():
    """
    Sert à afficher les infos à l'écran (LOGIQUE)
    :return: nothing (le grand retour XD)
    """
    aff_joueur = sysFont.render("Au tour du joueur " + plateau1.joueur, 0,
                                white if plateau1.joueur == "blanc" else black)
    screen.blit(aff_joueur, (340, 40))
    screen.blit(aff_legende, (570, 200))
    screen.blit(dame, (590, 240))
    pygame.draw.circle(screen, white, (690, 250), 20)
    screen.blit(dame2, (682, 242))
    pygame.draw.circle(screen, black_grey, (740, 250), 20)
    screen.blit(dame3, (732, 242))
    screen.blit(points, (590, 280))
    screen.blit(points_pion, (530, 310))
    screen.blit(points_dame, (530, 330))
    score_J1 = sysFont.render(f"Score J1 : {score_j1}", 0, black)
    score_J2 = sysFont.render(f"Score J2 : {score_j2}", 0, black)
    screen.blit(score_J1, (20, 40))
    screen.blit(score_J2, (20, 550))


def regles(color, sens):
    """
    Sert à afficher l'aide à l'utilisation du jeu au départ
    :param color: la couleur du texte en bas de l'écran
    :param sens: le sens de variation de la couleur
    :return: le paramètre sens, pour qu'il soit "sauvegardé", et puisse correctement être réutilisé au prochain tour
    """
    if color[0] == 255 and sens == 0.5:
        sens = -0.5
    if color[0] == 0 and sens == -0.5:
        sens = 0.5
    for i in range(3):
        color[i] += sens
    espace_pour_continuer = sysFont2.render("[Appuyer sur la touche espace pour continuer]", 0, color)
    screen.blit(espace_pour_continuer, (210, 500))
    screen.blit(regle1, (250, 40))
    screen.blit(regle2, (110, 70))
    screen.blit(regle3, (300, 120))
    screen.blit(regle4, (230, 160))
    screen.blit(regle5, (50, 190))
    screen.blit(regle6, (160, 220))
    screen.blit(regle7, (180, 250))
    screen.blit(regle8, (190, 280))
    screen.blit(regle9, (80, 310))
    screen.blit(regle10, (220, 340))

    return sens


# La boucle principale et indispensable du jeu
while True:
    screen.fill((150, 150, 150))
    x_mouse, y_mouse = pygame.mouse.get_pos()
    j_blanc, j_noir = plateau1.the_end()
    if not debut_jeu and not j_blanc and not j_noir:
        plateau1.dessiner()
        plateau1.afficher_pions()
        plateau1.calculer_cases_vides()
        selector.afficher_cursor()

        # affichage de tous les textes générés avant le début de la boucle, sur l'écran
        afficher()

    # La fin du jeu
    elif not debut_jeu and (j_blanc or j_noir):
        plateau1.dessiner()
        plateau1.afficher_pions()
        joueur = "blanc" if j_blanc else "noir"
        screen.blit(fin_jeu, (200, 40))
    else:
        sens_color = regles(color_space, sens_color)

    # Boucle des évènements du jeu
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                debut_jeu = False

        # La sélection du pion / le déplacement du pion
        if event.type == pygame.MOUSEBUTTONDOWN and not debut_jeu and not j_blanc and not j_noir:
            if selector.selectionner_case(x_mouse, y_mouse):
                if selector.isselecting():
                    x, y = selector.selectionner_pion()
                    if not manger:
                        if plateau1.bouger_pion(x, y, cases):
                            plateau1.changer_joueur()
                    else:
                        for i in range(len(cases)):
                            if cases[i][0] == (x, y):
                                indice = i
                                break
                        if plateau1.joueur == "blanc":
                            score_j1 += plateau1.manger(x, y, cases[indice][1], cases)
                        else:
                            score_j2 += plateau1.manger(x, y, cases[indice][1], cases)
                        plateau1.calculer_cases_vides()
                        cases = plateau1.attraper_pion(pion)
                        if cases:
                            if cases[0][1] is None:
                                plateau1.changer_joueur()
                        elif not cases:
                            plateau1.changer_joueur()
                else:
                    pion = plateau1.isthereapion(selector.getx(), selector.gety())
                    if pion:
                        devoir_de_manger = plateau1.jouer_ou_manger()
                        manger = False
                        for i in devoir_de_manger:
                            if i:
                                manger = True
                                break
                        if manger:
                            if devoir_de_manger[pion]:
                                cases = plateau1.attraper_pion(pion)
                                selector.selectionner_pion(cases)

                        else:
                            cases = plateau1.attraper_pion(pion)
                            selector.selectionner_pion(cases)

    pygame.display.update()
