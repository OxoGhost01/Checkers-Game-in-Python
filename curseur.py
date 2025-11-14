"""
Jeu de dame - fichier de la classe du curseur
Auteurs : Timothée GAUCHER & Théo FOENKINOS
Date : créé le : 06/11/2023 (pas sur) - dernière modif le : 23/12/2023 (sur)
"""
import pygame


class Selector:

    def __init__(self, screen):
        """
        Constructeur blablabla flemme de tout écrire
        :param screen: l'écran pour l'affichage
        """
        self.screen = screen
        self.pixel_x = 0
        self.pixel_y = 0
        self.x = None
        self.y = None
        self.indice_selection = 0
        self.select = False
        self.cases_selection = []
        self.color = (0, 255, 0)

    def getx(self):
        """
        :return: x
        """
        return self.x

    def gety(self):
        """
        :return: y
        """
        return self.y

    def isselecting(self):
        """
        :return: True si on est en train de sélectionner un pion False sinon
        """
        return self.select

    def lien(self):
        """
        Calcule les coordonnées en pixel pour l'affichage
        :return: nothing
        """
        self.pixel_y = self.y * 40 + 100
        if self.y % 2:
            self.pixel_x = self.x * 80 + 100
        else:
            self.pixel_x = self.x * 80 + 140

    def afficher_cursor(self):
        """
        Affiche en vert les cases de déplacement d'un pion
        :return: nothing
        """
        if self.select:
            for i in range(len(self.cases_selection)):
                x = self.cases_selection[i][0][0]
                y = self.cases_selection[i][0][1]
                pixel_y = y * 40 + 100
                if y % 2:
                    pixel_x = x * 80 + 100
                else:
                    pixel_x = x * 80 + 140
                pygame.draw.rect(self.screen, self.color, (pixel_x, pixel_y, 40, 40), 2)

    def selectionner_pion(self, cases_possibles=None):
        """
        Sélectionne le pion choisi
        :param cases_possibles: les cases de déplacement du pion
        :return: x et y si on désélectionne
        """
        if cases_possibles and not self.select:
            self.select = True
            self.cases_selection = cases_possibles
        else:
            self.select = False
            return self.x, self.y

    def selectionner_case(self, x_mouse, y_mouse):
        """
        Sert à cliquer sur un case avec la souris
        Cette fonction va regarder si la case cliquée est une "bonne" case
        :param x_mouse: x de la souris
        :param y_mouse: y de la souris
        :return: True si la case est "bonne" sinon False
        """
        if 100 <= x_mouse <= 500 and 100 <= y_mouse <= 500:
            for b in range(10):
                y = 40 * b + 100
                if y <= y_mouse <= y + 40:
                    for a in range(5):
                        if b % 2:
                            x = a * 80 + 100
                        else:
                            x = a * 80 + 140
                        if x <= x_mouse <= x + 40:
                            self.x = a
                            self.y = b
                            return True
                    return False
