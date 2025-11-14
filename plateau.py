"""
Jeu de dame - la classe du plateau
Auteurs : Timothée GAUCHER & Théo FOENKINOS
Date : créé le : 06/11/2023 (pas sur) - dernière modif le : 29/12/2023 (sur)
"""
from pions import *


class Plateau:

    def __init__(self, screen):
        """
        Le constructeur blablabla
        :param screen: l'écran (pour pouvoir afficher le plateau)
        """
        self.black = (0, 0, 0)
        self.screen = screen
        self.pions = []
        self.cases_vides = []
        self.joueur = "blanc"
        self.autre_joueur = "noir"
        self.pion_attrape = None

    def __len__(self):
        return len(self.pions)

    def dessiner(self):
        """
        Gère l'affichage du plateau et crée la variable cases_vides
        :return: nothing
        """
        noir = 0
        pygame.draw.rect(self.screen, self.black, (100, 100, 400, 400), 2)
        for y in range(100, 461, 40):
            for x in range(100, 461, 40):
                if noir % 2:
                    pygame.draw.rect(self.screen, self.black, (x, y, 40, 40))
                noir += 1
            if noir == 10:
                noir = 1
            else:
                noir = 0

    def creer_pions(self):
        """
        Il y a juste à lire le nom de la fonction pour savoir ce qu'elle fait
        :return: nothing
        """

        for y in range(10):
            if y < 4:
                for x in range(5):
                    self.pions.append(Pion(x, y, "blanc", self.screen))
            elif 4 <= y < 6:
                for x in range(5):
                    self.cases_vides.append((x, y))
            else:
                for x in range(5):
                    self.pions.append(Pion(x, y, "noir", self.screen))

    def afficher_pions(self):
        """
        Affiche les pions
        :return: nothing
        """
        for i in self.pions:
            i.afficher()

    def changer_joueur(self):
        """
        Elle fait quoi ? - FEUR !
        Elle change le joueur
        :return: nothing
        """
        if self.joueur == "blanc":
            self.joueur = "noir"
            self.autre_joueur = "blanc"
        else:
            self.joueur = "blanc"
            self.autre_joueur = "noir"

    def chercher_pion(self, x, y):
        """
        Parcourt la liste des pions et regarde sr les paramètres x et y correspondent à un pion
        :param x: x du pion cherché
        :param y: y du pion cherché
        :return: l'indice du pion si pion trouvé sinon None
        """
        for i in range(len(self.pions)):
            if self.pions[i].get_coord() == (x, y):
                return i
        return None

    def isthereapion(self, x, y):
        """
        Regarde s'il y a un pion ou non
        :param x: x de la case
        :param y: y de la case
        :return: True si pion trouvé False sinon
        """
        return self.chercher_pion(x, y) if (self.chercher_pion(x, y) and
                                            self.pions[self.chercher_pion(x, y)].get_color() == self.joueur) else None

    def calculer_cases_vides(self):
        """
        LOGIQUE
        :return: nothing
        """
        self.cases_vides = []
        for y in range(10):
            for x in range(5):
                if not self.chercher_pion(x, y):
                    self.cases_vides.append((x, y))

    def attraper_pion(self, pion):
        """
        'Attrape un pion' et lance le calcul de ses possibilités de déplacement
        :param pion: le pion en question
        :return: les déplacements possibles du pion
        """
        self.pion_attrape = pion
        if self.pions[pion].isdame():
            cases = self.filtrer_cases_dame()
        else:
            cases = self.filtrer_cases_pion()
        return cases

    def filtrer_cases_pion(self, i_pion=None):
        """
        Un peu plus long... Elle récupère ce que 'calculer_déplacement_pion' renvoie et filtre ces dernières
        en fonction des cas. Le paramètre est utilisé seulement si on appelle la fonction pour savoir si un pion
        peut manger ou non
        :param i_pion: indice du pion
        :return: les cases possibles
        """
        pion_a_manger = []
        cases_pour_manger = []
        if i_pion is not None:
            cases = self.pions[i_pion].calculer_deplacement_pion()
            x, y = self.pions[i_pion].get_coord()
            color = self.pions[i_pion].get_color()
        else:
            cases = self.pions[self.pion_attrape].calculer_deplacement_pion()
            x = self.pions[self.pion_attrape].getx()
            y = self.pions[self.pion_attrape].gety()
            color = self.pions[self.pion_attrape].get_color()

        if y % 2:
            # En bas à droite
            if (x + 1, y + 2) in cases:
                if (x, y + 1) in self.cases_vides:
                    cases.remove((x + 1, y + 2))
                elif self.pions[self.chercher_pion(x, y + 1)].get_color() == self.joueur:
                    if self.joueur == "blanc":
                        cases.remove((x, y + 1))
                    cases.remove((x + 1, y + 2))
                else:
                    if (x + 1, y + 2) not in self.cases_vides:
                        cases.remove((x + 1, y + 2))
                        if color == "blanc":
                            cases.remove((x, y + 1))
                    else:
                        if self.pions[self.chercher_pion(x, y + 1)].get_color() == self.autre_joueur:
                            cases_pour_manger.append((x + 1, y + 2))
                            pion_a_manger.append((x, y + 1))
            else:
                if self.joueur == "blanc" and x == 4:
                    if (x, y + 1) not in self.cases_vides:
                        cases.remove((x, y + 1))
            # En bas à gauche
            if (x - 1, y + 2) in cases:
                if (x - 1, y + 1) in self.cases_vides:
                    cases.remove((x - 1, y + 2))
                elif self.pions[self.chercher_pion(x - 1, y + 1)].get_color() == self.joueur:
                    if self.joueur == "blanc":
                        cases.remove((x - 1, y + 1))
                    cases.remove((x - 1, y + 2))
                else:
                    if (x - 1, y + 2) not in self.cases_vides:
                        cases.remove((x - 1, y + 2))
                        if color == "blanc":
                            cases.remove((x - 1, y + 1))
                    else:
                        if self.pions[self.chercher_pion(x - 1, y + 1)].get_color() == self.autre_joueur:
                            cases_pour_manger.append((x - 1, y + 2))
                            pion_a_manger.append((x - 1, y + 1))
            # En haut à droite
            if (x + 1, y - 2) in cases:
                if (x, y - 1) in self.cases_vides:
                    cases.remove((x + 1, y - 2))
                elif self.pions[self.chercher_pion(x, y - 1)].get_color() == self.joueur:
                    if self.joueur == "noir":
                        cases.remove((x, y - 1))
                    cases.remove((x + 1, y - 2))
                else:
                    if (x + 1, y - 2) not in self.cases_vides:
                        cases.remove((x + 1, y - 2))
                        if color == "noir":
                            cases.remove((x, y - 1))
                    else:
                        if self.pions[self.chercher_pion(x, y - 1)].get_color() == self.autre_joueur:
                            cases_pour_manger.append((x + 1, y - 2))
                            pion_a_manger.append((x, y - 1))
            else:
                if self.joueur == "noir" and x == 4:
                    if (x, y - 1) not in self.cases_vides:
                        cases.remove((x, y - 1))
            # En haut à gauche
            if (x - 1, y - 2) in cases:
                if (x - 1, y - 1) in self.cases_vides:
                    cases.remove((x - 1, y - 2))
                elif self.pions[self.chercher_pion(x - 1, y - 1)].get_color() == self.joueur:
                    if self.joueur == "noir":
                        cases.remove((x - 1, y - 1))
                    cases.remove((x - 1, y - 2))
                else:
                    if (x - 1, y - 2) not in self.cases_vides:
                        cases.remove((x - 1, y - 2))
                        if color == "noir":
                            cases.remove((x - 1, y - 1))
                    else:
                        if self.pions[self.chercher_pion(x - 1, y - 1)].get_color() == self.autre_joueur:
                            cases_pour_manger.append((x - 1, y - 2))
                            pion_a_manger.append((x - 1, y - 1))
        else:
            # En bas à droite
            if (x + 1, y + 2) in cases:
                if (x + 1, y + 1) in self.cases_vides:
                    cases.remove((x + 1, y + 2))
                elif self.pions[self.chercher_pion(x + 1, y + 1)].get_color() == self.joueur:
                    if self.joueur == "blanc":
                        cases.remove((x + 1, y + 1))
                    cases.remove((x + 1, y + 2))
                else:
                    if (x + 1, y + 2) not in self.cases_vides:
                        cases.remove((x + 1, y + 2))
                        if color == "blanc":
                            cases.remove((x + 1, y + 1))
                    else:
                        if self.pions[self.chercher_pion(x + 1, y + 1)].get_color() == self.autre_joueur:
                            cases_pour_manger.append((x + 1, y + 2))
                            pion_a_manger.append((x + 1, y + 1))
            # En bas à gauche
            if (x - 1, y + 2) in cases:
                if (x, y + 1) in self.cases_vides:
                    cases.remove((x - 1, y + 2))
                elif self.pions[self.chercher_pion(x, y + 1)].get_color() == self.joueur:
                    if self.joueur == "blanc":
                        cases.remove((x, y + 1))
                    cases.remove((x - 1, y + 2))
                else:
                    if (x - 1, y + 2) not in self.cases_vides:
                        cases.remove((x - 1, y + 2))
                        if color == "blanc":
                            cases.remove((x, y + 1))
                    else:
                        if self.pions[self.chercher_pion(x, y + 1)].get_color() == self.autre_joueur:
                            cases_pour_manger.append((x - 1, y + 2))
                            pion_a_manger.append((x, y + 1))
            else:
                if self.joueur == "blanc" and x == 0:
                    if (x, y + 1) not in self.cases_vides:
                        cases.remove((x, y + 1))
            # En haut à droite
            if (x + 1, y - 2) in cases:
                if (x + 1, y - 1) in self.cases_vides:
                    cases.remove((x + 1, y - 2))
                elif self.pions[self.chercher_pion(x + 1, y - 1)].get_color() == self.joueur:
                    if self.joueur == "noir":
                        cases.remove((x + 1, y - 1))
                    cases.remove((x + 1, y - 2))
                else:
                    if (x + 1, y - 2) not in self.cases_vides:
                        cases.remove((x + 1, y - 2))
                        if color == "noir":
                            cases.remove((x + 1, y - 1))
                    else:
                        if self.pions[self.chercher_pion(x + 1, y - 1)].get_color() == self.autre_joueur:
                            cases_pour_manger.append((x + 1, y - 2))
                            pion_a_manger.append((x + 1, y - 1))
            # En haut à gauche
            if (x - 1, y - 2) in cases:
                if (x, y - 1) in self.cases_vides:
                    cases.remove((x - 1, y - 2))
                elif self.pions[self.chercher_pion(x, y - 1)].get_color() == self.joueur:
                    if self.joueur == "noir":
                        cases.remove((x, y - 1))
                    cases.remove((x - 1, y - 2))
                else:
                    if (x - 1, y - 2) not in self.cases_vides:
                        cases.remove((x - 1, y - 2))
                        if color == "noir":
                            cases.remove((x, y - 1))
                    else:
                        if self.pions[self.chercher_pion(x, y - 1)].get_color() == self.autre_joueur:
                            cases_pour_manger.append((x - 1, y - 2))
                            pion_a_manger.append((x, y - 1))
            else:
                if self.joueur == "noir" and x == 0:
                    if (x, y - 1) not in self.cases_vides:
                        cases.remove((x, y - 1))

        i = 0
        while i < len(cases):
            pion_dans_case = self.chercher_pion(cases[i][0], cases[i][1])
            if pion_dans_case:
                if self.pions[pion_dans_case].get_color() == self.joueur:
                    cases.remove(cases[i])
                    i -= 1
            i += 1

        if pion_a_manger:
            c = cases_pour_manger
            p = pion_a_manger
            cases = []
            for i in range(len(c)):
                cases.append((c[i], p[i]))
            return cases
        else:
            c = []
            for i in cases:
                c.append((i, None))
            return c

    def bouger_pion(self, newx, newy, cases):
        """
        Sert à déplacer un pion
        :param cases: les cases de déplacement possibles du pion
        :param newx: logique
        :param newy: toujours aussi logique
        :return: nothing
        """
        for i in cases:
            if (newx, newy) == i[0]:
                self.pions[self.pion_attrape].change_coord(newx, newy)
                if self.joueur == "blanc":
                    if newy == 9 and self.pions[self.pion_attrape].isdame() is False:
                        self.pions[self.pion_attrape].upgrade()
                elif self.joueur == "noir":
                    if newy == 0 and self.pions[self.pion_attrape].isdame() is False:
                        self.pions[self.pion_attrape].upgrade()
                self.pion_attrape = None
                return True
        return False

    def manger(self, x, y, indice, cases):
        """
        Mange un pion
        :param cases: les cases de déplacement possibles du pion
        :param x: x du pion mangé
        :param y: y du pion mangé
        :param indice: indice du pion mangé
        :return: nothing
        """
        if self.bouger_pion(x, y, cases):
            indice = self.chercher_pion(indice[0], indice[1])
            if self.pions[indice].isdame() is True:
                score = 2
            else:
                score = 1
            self.pions[indice].mourir()
            return score

    def jouer_ou_manger(self):
        """
        Sert à savoir si un pion peut manger ou non
        :return: une liste avec le nombre de pions à manger pour chaque pion
        """
        doit_manger = []
        for pion in range(len(self.pions)):
            peut_manger = False
            if self.pions[pion].get_color() == self.joueur:
                dame = True if self.pions[pion].isdame() is True else False
                if dame:
                    cases = self.filtrer_cases_dame(pion)
                else:
                    cases = self.filtrer_cases_pion(pion)
                for y in cases:
                    if y[1]:
                        peut_manger = True
                        break
                doit_manger.append(peut_manger)
            elif self.joueur == "noir":
                doit_manger.append(False)
        return doit_manger

    def filtrer_cases_dame(self, i_pion=None):
        """
        Comme pour les pions sauf que cette fois-ci c'est pour les dames. Le paramètre est utilisé seulement
        quand on veut savoir si une dame peut manger
        :param i_pion: l'indice de la dame
        :return: les cases après filtre
        """
        pion_a_manger = []
        cases_pour_manger = []
        if i_pion is not None:
            cases = self.pions[i_pion].calculer_deplacement_dame()
        else:
            cases = self.pions[self.pion_attrape].calculer_deplacement_dame()
        for d in range(len(cases)):
            i = 0
            while i < len(cases[d]):
                if self.chercher_pion(cases[d][i][0], cases[d][i][1]):
                    if self.pions[self.chercher_pion(cases[d][i][0], cases[d][i][1])].get_color() == self.joueur:
                        while i < len(cases[d]):
                            cases[d].remove(cases[d][i])
                        break
                    if (self.pions[self.chercher_pion(cases[d][i][0], cases[d][i][1])].get_color() ==
                            self.autre_joueur):
                        pion_a_manger.append(cases[d][i])
                        if i < len(cases[d]) - 1:
                            i += 1
                            while i < len(cases[d]):
                                if self.chercher_pion(cases[d][i][0], cases[d][i][1]):
                                    if (self.pions[self.chercher_pion(cases[d][i][0], cases[d][i][1])].get_color() ==
                                            self.autre_joueur):
                                        i -= 1
                                        while i < len(cases[d]):
                                            cases[d].remove(cases[d][i])
                                        break
                                else:
                                    cases_pour_manger.append((cases[d][i], pion_a_manger[len(pion_a_manger) - 1]))
                                i += 1
                        else:
                            cases[d].remove(cases[d][i])
                else:
                    cases[d][i] = (cases[d][i], None)
                i += 1

        if cases_pour_manger:
            return cases_pour_manger
        else:
            c = []
            for i in range(len(cases)):
                for y in range(len(cases[i])):
                    c.append(cases[i][y])
            return c

    def the_end(self):

        """
        Sert à savoir s'il reste des pions aux deux joueurs ou si un des 2 n'en n'a plus, dans ce cas, il a perdu
        :return: 2 booléens, un pour les blancs, un pour les noirs, True s'il a perdu, False s'il lui reste des pions
        """

        blanc = False
        noir = False
        for i in self.pions:
            if i.get_color() == "blanc":
                if not i.isalive():
                    blanc = True
                else:
                    blanc = False
                    break
            else:
                if not i.isalive():
                    noir = True
                else:
                    noir = False
                    break
        return blanc, noir
