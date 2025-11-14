"""
Jeu de dame - fichier de la classe du pion
Auteurs : Timothée GAUCHER & Théo FOENKINOS
Date : créé le : 06/11/2023 (pas sur) - dernière modif le : 23/12/2023 (sur)
"""
import pygame


class Pion:

    def __init__(self, x, y, color, screen, dame=False, vivant=True):
        """
        Le constructeur blablabla ça ne change pas de d'habitude...
        :param x: Coordonnée x
        :param y: Coordonnée y
        :param color: noir/blanc (la couleur du pion)
        :param screen: l'écran, pour pouvoir afficher les pions
        :param dame: savoir si un pion est une dame ou non
        :param vivant: savoir si le pion est vivant (LOGIQUE)
        """
        self.x = x
        self.y = y
        self.pixel_x = 0
        self.pixel_y = 0
        self.color = color
        self.screen = screen
        self.dame = dame
        self.vivant = vivant

    def change_coord(self, newx, newy):
        """
        Pour changer les coordonnées
        :param newx: est-ce que j'ai vraiment besoin de détailler cela ?
        :param newy: je ne pense pas
        :return: nothing
        """
        self.x = newx
        self.y = newy

    def upgrade(self):
        """
        Transforme le pion en dame
        :return: nothing
        """
        self.dame = True

    def isdame(self):
        """
        :return: self.dame (true si le pion est une dame false sinon)
        """
        return self.dame

    def mourir(self):
        """
        Pour tuer un pion, on va également changer ses coordonnées pour éviter des bugs
        :return: nothing
        """
        self.vivant = False
        self.x = 20
        self.y = 20

    def get_coord(self):
        """
        :return: x, y
        """
        return self.x, self.y

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

    def get_color(self):
        """
        :return: la couleur du pion
        """
        return self.color

    def isalive(self):
        """
        Sert à savoir si un pion est vivant ou non
        :return: True si le pion est vivant, False sinon
        """
        return self.vivant

    def lien_pions(self):
        """
        Sert à calculer les coordonnées en pixel pour l'affichage
        :return: nothing
        """
        self.pixel_y = self.y * 40 + 120
        if self.y % 2:
            self.pixel_x = self.x * 80 + 120
        else:
            self.pixel_x = self.x * 80 + 160

    def afficher(self):
        """
        Affiche les pions (toujours aussi logique, il suffit de regarder le nom de la fonction XD)
        :return: nothing
        """
        self.lien_pions()
        if self.vivant:
            if self.color == "noir":
                pygame.draw.circle(self.screen, (80, 80, 80), (self.pixel_x, self.pixel_y), 15)
            else:
                pygame.draw.circle(self.screen, (220, 220, 220), (self.pixel_x, self.pixel_y), 15)
            if self.dame:
                sysFont = pygame.font.SysFont("None", 25)
                d = sysFont.render("D", 0, (0, 0, 0))
                self.screen.blit(d, (self.pixel_x - 5, self.pixel_y - 7))

    def calculer_deplacement_pion(self):
        """
        Sert à calculer TOUS les déplacements possibles d'un pion
        :return: les déplacements possibles
        """
        cases = []
        for a in range(1, 3):
            if self.y % 2:
                # En bas à droite
                if 0 <= self.x + (a - 1) <= 4 and 0 <= self.y + a <= 9 and (self.color == "blanc" or a == 2):
                    cases.append((self.x + (a - 1), self.y + a))
                # En bas à gauche
                if 0 <= self.x - 1 <= 4 and 0 <= self.y + a <= 9 and (self.color == "blanc" or a == 2):
                    cases.append((self.x - 1, self.y + a))
                # En haut à droite
                if 0 <= self.x + (a - 1) <= 4 and 0 <= self.y - a <= 9 and (self.color == "noir" or a == 2):
                    cases.append((self.x + (a - 1), self.y - a))
                # En haut à gauche
                if 0 <= self.x - 1 <= 4 and 0 <= self.y - a <= 9 and (self.color == "noir" or a == 2):
                    cases.append((self.x - 1, self.y - a))
            else:
                # En bas à droite
                if 0 <= self.x + 1 <= 4 and 0 <= self.y + a <= 9 and (self.color == "blanc" or a == 2):
                    cases.append((self.x + 1, self.y + a))
                # En bas à gauche
                if 0 <= self.x - (a - 1) <= 4 and 0 <= self.y + a <= 9 and (self.color == "blanc" or a == 2):
                    cases.append((self.x - (a - 1), self.y + a))
                # En haut à droite
                if 0 <= self.x + 1 <= 4 and 0 <= self.y - a <= 9 and (self.color == "noir" or a == 2):
                    cases.append((self.x + 1, self.y - a))
                # En haut à gauche
                if 0 <= self.x - (a - 1) <= 4 and 0 <= self.y - a <= 9 and (self.color == "noir" or a == 2):
                    cases.append((self.x - (a - 1), self.y - a))
        return cases

    def calculer_deplacement_dame(self):
        """
        Sert à calculer TOUS les déplacements possibles d'une dame
        :return: les déplacements possibles
        """
        haut_droite = []
        haut_gauche = []
        bas_droite = []
        bas_gauche = []
        if self.y % 2:
            booool = False
        else:
            booool = True
        x1 = 0
        x2 = 0
        for y in range(1, 10):
            # en bas à droite
            if booool:
                x1 += 1
                booool = False
            else:
                booool = True
            if 0 <= self.x + x1 <= 4 and 0 <= self.y + y <= 9:
                bas_droite.append((self.x + x1, self.y + y))

            # en bas à gauche
            if booool:
                x2 += 1
            if 0 <= self.x - x2 <= 4 and 0 <= self.y + y <= 9:
                bas_gauche.append((self.x - x2, self.y + y))

            # en haut à droite
            if 0 <= self.x + x1 <= 4 and 0 <= self.y - y <= 9:
                haut_droite.append((self.x + x1, self.y - y))

            # en bas à gauche
            if 0 <= self.x - x2 <= 4 and 0 <= self.y - y <= 9:
                haut_gauche.append((self.x - x2, self.y - y))
        return [bas_droite, bas_gauche, haut_droite, haut_gauche]
