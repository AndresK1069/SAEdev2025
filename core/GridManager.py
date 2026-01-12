from core.Component.Wall import Wall
from core.Component.Hive import Hive
from core.Component.Flower import Flower
from random import randint, random

from core.utilities import evenSplit
from data.constante import MAX_NECTAR, NFLEURS
import copy


class GridManager():

    def __init__(self, size: int):
        if size %3 !=0:
            raise Exception('Invalid grid size , size should be a multiple of 3')
        if size <3:
            raise Exception('Size must be greater than 3')
        self.size = size
        self.data = [[None for _ in range(size)] for _ in range(size)]

    def addObject(self, wall: Wall,player1_hive: Hive, player2_hive: Hive,player3_hive: Hive, player4_hive: Hive) -> list[list]:
        """
            Ajoute les murs et les ruches des joueurs sur la carte.

            Cette méthode place :
            - des murs (`wall`) tout autour de la bordure de la grille,
            - une ruche pour chaque joueur dans les quatre coins internes de la carte.

            Les positions des ruches sont également stockées et retournées.

            Paramètres
            ----------
            wall : Wall
                Objet représentant un mur à placer sur les bordures de la carte.
            player1_hive : Hive
                Ruche du joueur 1 (coin supérieur gauche).
            player2_hive : Hive
                Ruche du joueur 2 (coin supérieur droit).
            player3_hive : Hive
                Ruche du joueur 3 (coin inférieur gauche).
            player4_hive : Hive
                Ruche du joueur 4 (coin inférieur droit).

            Retours
            -------
            tuple[list[list], list[tuple[int, int]]]
                - La grille mise à jour contenant les murs et les ruches.
                - Une liste de coordonnées (ligne, colonne) correspondant
                  aux positions des ruches sur la carte.
        """
        rows = len(self.data)
        cols = len(self.data[0])

        coord_hive = []

        for r in range(rows):
            for c in range(cols):

                # Set walls around the border
                if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                    self.data[r][c] = wall

                # add the hives on the map
                if r == 1 and c == 1:
                    self.data[r][c] = player1_hive
                    coord_hive.append((r,c))
                if r == 1 and c == cols - 2:
                    self.data[r][c] = player2_hive
                    coord_hive.append((r, c))
                if r == rows-2 and c == 1:
                    self.data[r][c] = player3_hive
                    coord_hive.append((r, c))
                if r == rows-2 and c == cols - 2:
                    self.data[r][c] = player4_hive
                    coord_hive.append((r, c))

        return self.data , coord_hive

    def spawnFlower(self, numberFlower: int) -> list[list]:
        """
            Génère et place des fleurs sur la carte de manière symétrique.

            Cette méthode sélectionne des cellules valides dans une zone définie
            de la carte, puis y place des fleurs (`Flower`).
            Pour chaque fleur placée, trois autres fleurs sont générées par symétrie
            horizontale et verticale afin de garantir une répartition équilibrée.

            Le nombre de fleurs demandé doit être un multiple de 2, sinon une
            exception est levée.

            Paramètres
            ----------
            numberFlower : int
                Nombre de positions de base à utiliser pour générer les fleurs.
                Chaque position engendre 4 fleurs par symétrie.

            Retours
            -------
            list[list]
                La grille de la carte mise à jour avec les fleurs ajoutées.

            Exceptions
            ----------
            Exception
                Levée si `numberFlower` n'est pas un multiple de 2.
        """
        rows = len(self.data)
        cols = len(self.data[0])

        chunk = cols // 3
        middle_line = rows // 2
        possible_cells = []

        for r in range(rows):
            for c in range(cols):

                if r <= 1: #out of bound safety
                    continue

                if r != 0 and c != 0 and c != rows - 1:
                    if chunk - 1 < c < cols - chunk and r < middle_line and c < middle_line:
                        possible_cells.append((r, c))
                    if chunk < r < middle_line and c < middle_line:
                        possible_cells.append((r, c))


        if numberFlower %2 != 0:
            raise Exception('numberFlower should be a multiple of 2')

        for _ in range(numberFlower):
            i = randint(0, len(possible_cells)-1)
            flower_row , flower_col = possible_cells.pop(i)
            self.data[flower_row][flower_col] = Flower("f",evenSplit(NFLEURS,MAX_NECTAR))

            mirrored_row = 2 * middle_line - flower_row
            self.data[mirrored_row][flower_col] = Flower("f",evenSplit(NFLEURS,MAX_NECTAR))
            mirrored_col = 2 * middle_line - flower_col
            self.data[flower_row][mirrored_col] = Flower("f",evenSplit(NFLEURS,MAX_NECTAR))
            self.data[mirrored_row][mirrored_col] = Flower("f",evenSplit(NFLEURS,MAX_NECTAR))

        return self.data


    def getBattleZone(self, wall) -> list[list]:
        """
            Définit une zone de combat centrale sur la carte en y plaçant des murs.

            Cette méthode crée une zone délimitée par des murs au centre de la grille.
            Les murs sont placés sur des bandes verticales et horizontales calculées
            à partir de la taille de la carte, formant ainsi une zone de bataille
            centrale.

            Paramètres
            ----------
            wall : Wall
                Objet représentant un mur à placer dans la zone de combat.

            Retours
            -------
            list[list]
                La grille de la carte mise à jour avec la zone de combat définie.
        """
        rows = len(self.data)
        cols = len(self.data[0])

        chunk = cols // 3

        for r in range(rows):
            for c in range(cols):
                if chunk - 1 < c < cols - chunk:
                    self.data[r][c] = wall
                if chunk -1 < r < cols-chunk  :
                    self.data[r][c] = wall
        return self.data


    def cellToList(self, row: int, col: int) -> list:
        """
            Convertit le contenu d'une cellule de la grille en liste.

            Cette méthode récupère l'objet stocké à la position donnée
            (ligne, colonne) dans la grille et en retourne une copie
            encapsulée dans une liste.

            Paramètres
            ----------
            row : int
                Indice de la ligne de la cellule.
            col : int
                Indice de la colonne de la cellule.

            Retours
            -------
            list
                Une liste contenant une copie de l'objet présent dans la cellule.
        """
        varObject = self.data[row][col]
        return [copy.copy(varObject)]

    def cleanGrid(self):
        """
           Nettoie la grille en supprimant les listes contenant un seul élément.

           Cette méthode parcourt l'ensemble de la grille et remplace toute cellule
           contenant une liste d'un seul objet (généralement une ruche) par
           l'objet lui-même.
           Cela permet de simplifier la structure de la grille après certaines
           opérations où des objets ont été temporairement stockés dans des listes.

           Retours
           -------
           None
               La méthode modifie la grille directement et ne retourne aucune valeur.
        """
        rows = len(self.data)
        cols = len(self.data[0])

        for r in range(rows):
            for c in range(cols):
                if isinstance(self.data[r][c], list) and len(self.data[r][c]) ==  1:
                    for hive in self.data[r][c]:
                        hive_ = hive
                    self.data[r][c] = hive_


        return

    def is_valid_cell(self, bee, r: int, c: int, nRow: int, nCol: int) -> bool:
        """
            Vérifie si un déplacement vers une cellule cible est valide pour une abeille.

            Cette méthode contrôle :
            - que la cellule cible est dans les limites de la grille,
            - que la cellule de destination est vide,
            - que le déplacement n'est pas nul,
            - que la distance du déplacement respecte l'agilité de l'abeille,
            - que le type de déplacement autorisé est respecté
              (orthogonal uniquement ou type reine : horizontal, vertical, diagonal),
            - que le chemin entre la cellule de départ et la cellule d'arrivée
              n'est pas bloqué par un autre objet.

            Paramètres
            ----------
            bee : Bee
                Abeille effectuant le déplacement. Ses attributs `beeAgility`
                et `simpleMovement` déterminent les règles de déplacement.
            r : int
                Indice de ligne de la cellule de départ.
            c : int
                Indice de colonne de la cellule de départ.
            nRow : int
                Indice de ligne de la cellule de destination.
            nCol : int
                Indice de colonne de la cellule de destination.

            Retours
            -------
            bool
                `True` si le déplacement est valide.

            Exceptions
            ----------
            Exception
                Levée si l'une des règles de déplacement est violée
                (sortie de la grille, cellule occupée, mouvement invalide,
                agilité dépassée ou chemin bloqué).
        """
        rows = len(self.data)
        cols = len(self.data[0])

        # bounds
        if not (0 <= nRow < rows and 0 <= nCol < cols):
            raise Exception("Target cell out of bounds")

        # destination must be empty
        if self.data[nRow][nCol] is not None:
            raise Exception("Target cell is not empty")

        dr = nRow - r
        dc = nCol - c

        if dr == 0 and dc == 0:
            raise Exception("No movement")

        if abs(dr) > bee.beeAgility or abs(dc) > bee.beeAgility:
            raise Exception("Move exceeds agility")


        if bee.simpleMovement:
            if dr != 0 and dc != 0:
                raise Exception("Diagonal movement not allowed")
        else:
            if not (dr == 0 or dc == 0 or abs(dr) == abs(dc)):
                raise Exception("Invalid queen-like movement")


        step_r = 0 if dr == 0 else (1 if dr > 0 else -1)
        step_c = 0 if dc == 0 else (1 if dc > 0 else -1)

        curr_r = r + step_r
        curr_c = c + step_c

        while curr_r != nRow or curr_c != nCol:
            if self.data[curr_r][curr_c] is not None:
                raise Exception("Path blocked")

            curr_r += step_r
            curr_c += step_c

        return True

    def moveObject(self, bee, nRow: int, nCol: int) -> None:
        """
            Déplace une abeille vers une nouvelle cellule de la grille.

            Cette méthode recherche l’abeille dans la grille, puis vérifie si le
            déplacement vers la cellule cible est valide à l’aide de `is_valid_cell`.
            L’abeille peut être stockée directement dans une cellule ou à l’intérieur
            d’une liste contenue dans une cellule.

            Si le déplacement est valide, l’abeille est retirée de sa position actuelle
            et placée dans la cellule de destination.

            Paramètres
            ----------
            bee : Bee
                L’abeille à déplacer.
            nRow : int
                Indice de ligne de la cellule de destination.
            nCol : int
                Indice de colonne de la cellule de destination.

            Retours
            -------
            None
                La grille est modifiée directement. La méthode retourne la grille
                uniquement en cas de sortie anticipée.

            Exceptions
            ----------
            Exception
                Levée si l’abeille n’est pas trouvée dans la grille ou si le déplacement
                est invalide (propagé depuis `is_valid_cell`).
        """
        from core.Component.Bee import Bee

        if not isinstance(bee, Bee):
            return self.data

        rows = len(self.data)
        cols = len(self.data[0])

        for r in range(rows):
            for c in range(cols):

                cell = self.data[r][c]

                # bee inside a list
                if isinstance(cell, list) and bee in cell:
                    self.is_valid_cell(bee, r, c, nRow, nCol)

                    self.data[nRow][nCol] = bee
                    cell.remove(bee)
                    return self.data

                if cell is bee:
                    self.is_valid_cell(bee, r, c, nRow, nCol)

                    self.data[nRow][nCol] = bee
                    self.data[r][c] = None
                    return self.data


        raise Exception("Bee not found in matrix")


    def recupFleur(self) -> list[(int ,int)]:
        """
            Récupère les coordonnées de toutes les fleurs présentes sur la grille.

            Cette méthode parcourt chaque cellule de la grille et ajoute à une liste
            les positions (ligne, colonne) où se trouvent des objets de type `Flower`.

            Retours
            -------
            list[tuple[int, int]]
                Une liste de tuples représentant les coordonnées de chaque fleur.
                Chaque tuple contient (ligne, colonne).
        """
        flower_array = []
        rows = len(self.data)
        cols = len(self.data[0])

        for r in range(rows):
            for c in range(cols):
                if isinstance(self.data[r][c], Flower):
                    flower_array.append((r, c))
        return flower_array

    def flowerButinage(self, arrFlower:list) -> None:
        """
          Gère le butinage des abeilles sur les fleurs spécifiées.

          Pour chaque fleur de la liste, cette méthode examine la zone 3x3
          centrée sur la fleur. Si une abeille (`Bee`) se trouve dans cette
          zone et que ses deux derniers déplacements sont identiques,
          elle butine la fleur et reçoit le nectar correspondant.

          Paramètres
          ----------
          arrFlower : list[tuple[int, int]]
              Liste des coordonnées (ligne, colonne) des fleurs à butiner.

          Retours
          -------
          None
              La méthode modifie directement l'état des abeilles et des fleurs
              sur la grille.
        """
        from core.Component.Bee import Bee
        for f in arrFlower:
            r, c = f
            reel_row, reel_col = r, c
            r -= 1
            c -= 1
            for row in range(3):
                for col in range(3):
                    obj = self.data[r + row][c + col]
                    if isinstance(obj, Bee):
                        if len(obj.moveList) == 1:
                            continue
                        move1, move2 = obj.moveList[-2:]
                        if move1 == move2:
                            varNectar = self.data[reel_row][reel_col].reduceNectar()
                            obj.currentNectar += varNectar
                            obj.checkOverFlow()

    def getBeePos(self) -> None:
        """
            Enregistre la position actuelle de chaque abeille dans sa liste de mouvements.

            Cette méthode parcourt la grille et, pour chaque objet de type `Bee`,
            ajoute ses coordonnées actuelles (ligne, colonne) à son attribut `moveList`.
            Cela permet de suivre l'historique des positions de chaque abeille.

            Retours
            -------
            None
                La méthode modifie directement les objets `Bee` dans la grille.
        """
        from core.Component.Bee import Bee
        rows = len(self.data)
        cols = len(self.data[0])
        for r in range(rows):
            for c in range(cols):
                if isinstance(self.data[r][c], Bee):
                    self.data[r][c].moveList.append((r,c))

    def emptyBeeNectar(self, arrayhive: list) -> None:
        """
            Transfère le nectar des abeilles vers les ruches voisines.

            Pour chaque ruche dont les coordonnées sont dans `arrayhive`, la méthode
            parcourt la zone 3x3 centrée sur la ruche. Si une abeille (`Bee`) y est
            présente et possède du nectar (`currentNectar > 0`), le nectar est ajouté
            à la ruche et l’abeille est vidée de son nectar.

            Paramètres
            ----------
            arrayhive : list[tuple[int, int]]
                Liste des coordonnées (ligne, colonne) des ruches à remplir.

            Retours
            -------
            None
                La méthode modifie directement l’état des ruches et des abeilles sur la grille.
        """
        from core.Component.Bee import Bee
        print(arrayhive)
        for r, c in arrayhive:
            hive = self.data[r][c]
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr = r + dr
                    nc = c + dc
                    if 0 <= nr < len(self.data) and 0 <= nc < len(self.data[0]):
                        cell = self.data[nr][nc]
                        if isinstance(cell, Bee) and cell.currentNectar > 0:
                            hive.addNectar(cell.currentNectar)
                            cell.currentNectar = 0


    def checkEscarmouche(self) -> None:
        """
            Vérifie et applique les escarmouches entre abeilles ennemies voisines.

            Pour chaque abeille (`Bee`) sur la grille, cette méthode inspecte les
            cellules adjacentes (zone 3x3 autour de l'abeille). Si une abeille
            voisine appartient à un propriétaire différent et n'est pas étourdie
            (`isStun`), une escarmouche est déclenchée.

            Le calcul des dégâts prend en compte :
            - le nombre d'ennemis autour de l'abeille,
            - la force de l'abeille (`beeStrength`),
            - la probabilité d'esquive calculée via `did_dodge`.

            Si l'abeille ennemie ne parvient pas à esquiver, ses points de vie
            (`currenthealth`) sont réduits et elle est étourdie si sa santé tombe
            à zéro ou moins.

            Retours
            -------
            None
                La méthode modifie directement l’état des abeilles sur la grille.
        """
        from core.Component.Bee import Bee
        print("checking for Escarmouche ... ")
        rows = len(self.data)
        cols = len(self.data[0])

        for r in range(rows):
            for c in range(cols):
                bee = self.data[r][c]
                if isinstance(bee, Bee):
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            nr = r + dr
                            nc = c + dc
                            if 0 <= nr < rows and 0 <= nc < cols:
                                neighbor = self.data[nr][nc]
                                if (nr, nc) == (r, c):
                                    continue

                                if isinstance(neighbor, Bee):
                                    if bee.owner != neighbor.owner:
                                        if not neighbor.isStun:

                                            print(f"found escarmouche between ({bee.name}) and ({neighbor.name})")
                                            numEnemy =self.getBeeAround(r,c)
                                            dodgeProba = self.calFE(r ,c , numEnemy)
                                            FE = bee.beeStrength // numEnemy
                                            didDamege = self.did_dodge(dodgeProba)
                                            if not didDamege:
                                                neighbor.currenthealth -= FE
                                                if neighbor.currenthealth <= 0:
                                                    neighbor.stun()

    def did_dodge(self,dodgeProba: int) -> bool:
        """
            Détermine si une abeille esquive une attaque en fonction d'une probabilité.

            La méthode génère un nombre aléatoire et compare avec la probabilité
            d'esquive (`dodgeProba`) fournie en pourcentage.

            Paramètres
            ----------
            dodgeProba : int
                Probabilité d'esquive de l'abeille en pourcentage (0 à 100).

            Retours
            -------
            bool
                True si l'abeille esquive l'attaque, False sinon.
        """
        return random() < dodgeProba / 100

    def getBeeAround(self, r, c) -> int:
        """
           Compte le nombre d'abeilles ennemies autour d'une abeille donnée.

           La méthode vérifie les cellules adjacentes (zone 3x3 autour de la
           position (r, c)) et compte le nombre d'abeilles (`Bee`) appartenant à
           un propriétaire différent de l'abeille centrale.

           Paramètres
           ----------
           r : int
               Indice de ligne de l'abeille centrale.
           c : int
               Indice de colonne de l'abeille centrale.

           Retours
           -------
           int
               Nombre d'abeilles ennemies autour de l'abeille centrale. Retourne 0
               si la cellule centrale ne contient pas une abeille.
        """
        from core.Component.Bee import Bee
        beeNum = 0

        if not isinstance(self.data[r][c], Bee):
            return 0

        rows = len(self.data)
        cols = len(self.data[0])
        center_bee = self.data[r][c]

        for dr in range(r - 1, r + 2):
            for dc in range(c - 1, c + 2):
                if dr < 0 or dr >= rows or dc < 0 or dc >= cols:
                    continue
                if dr == r and dc == c:
                    continue

                cell = self.data[dr][dc]
                if isinstance(cell, Bee) and cell.owner != center_bee.owner:
                    beeNum += 1

        return beeNum

    def calFE(self,r :int,c :int, beeNum:int)-> int:
        """
            Calcule la force d'attaque (FE) d'une abeille contre les ennemies autour.

            Pour l'abeille située à la position (r, c), cette méthode somme la
            force (`beeStrength`) de toutes les abeilles ennemies dans la zone 3x3
            autour de l'abeille centrale, puis divise cette somme par le nombre
            d'ennemis (`beeNum`) pour obtenir la force moyenne d'attaque.

            Paramètres
            ----------
            r : int
                Indice de ligne de l'abeille centrale.
            c : int
                Indice de colonne de l'abeille centrale.
            beeNum : int
                Nombre d'abeilles ennemies autour de l'abeille centrale.

            Retours
            -------
            int
                La force d'attaque moyenne contre les abeilles ennemies. Retourne 0
                si la cellule centrale ne contient pas une abeille.
        """
        from core.Component.Bee import Bee
        sumBeeStrenght = 0

        if not isinstance(self.data[r][c], Bee):
            return 0

        rows = len(self.data)
        cols = len(self.data[0])
        center_bee = self.data[r][c]

        for dr in range(r - 1, r + 2):
            for dc in range(c - 1, c + 2):
                if dr < 0 or dr >= rows or dc < 0 or dc >= cols:
                    continue
                if dr == r and dc == c:
                    continue

                cell = self.data[dr][dc]
                if isinstance(cell, Bee) and cell.owner != center_bee.owner:
                    sumBeeStrenght+= cell.beeStrength
        return sumBeeStrenght // beeNum


    def checkStunBee(self) -> None:
        """
            Met à jour l'état d'étourdissement (`stun`) des abeilles sur la grille.

            La méthode parcourt toutes les cellules de la grille et pour chaque abeille
            (`Bee`) étourdie (`isStun == True`), elle décrémente son compteur
            `stunCounter`. Si le compteur atteint 0 ou moins, l'abeille est libérée
            de l'état d'étourdissement (`isStun = False`).

            Retours
            -------
            None
                La méthode modifie directement l'état des abeilles sur la grille.
        """
        from core.Component.Bee import Bee
        rows = len(self.data)
        cols = len(self.data[0])
        for r in range(rows):
            for c in range(cols):
                cell = self.data[r][c]
                if isinstance(cell, Bee) and cell.isStun:
                    if cell.stunCounter <= 0:
                        cell.isStun = False
                        continue
                    cell.stunCounter -= 1



    def getFlowerNectar(self) -> int:
        """
            Calcule le total de nectar disponible dans toutes les fleurs de la grille.

            La méthode parcourt chaque cellule de la grille et additionne
            la quantité de nectar (`flowerNectar`) de chaque objet de type `Flower`.

            Retours
            -------
            int
                Le total de nectar disponible dans toutes les fleurs de la grille.
        """
        nectar = 0
        rows = len(self.data)
        cols = len(self.data[0])
        for r in range(rows):
            for c in range(cols):
                if isinstance(self.data[r][c], Flower):
                    nectar +=  self.data[r][c].flowerNectar
        return nectar

    def getBeeNectar(self) -> int:
        """
           Calcule le total de nectar possédé par toutes les abeilles sur la grille.

           La méthode parcourt chaque cellule de la grille et additionne
           la quantité de nectar (`currentNectar`) de chaque objet de type `Bee`.

           Retours
           -------
           int
               Le total de nectar possédé par toutes les abeilles sur la grille.
        """
        nectar = 0
        from core.Component.Bee import Bee
        rows = len(self.data)
        cols = len(self.data[0])
        for r in range(rows):
            for c in range(cols):
                if isinstance(self.data[r][c], Bee):
                    nectar += self.data[r][c].currentNectar
        return nectar

    def isWinner(self, arrayhive: list):
        """
            Vérifie si une ruche a atteint la condition de victoire.

            La méthode parcourt les ruches listées dans `arrayhive` et détermine
            si l'une d'entre elles a accumulé suffisamment de nectar pour gagner.
            Selon la structure de `arrayhive`, chaque élément peut être soit :
            - une liste contenant un objet `Hive`, soit
            - un tuple de coordonnées pointant directement vers une ruche dans la grille.

            La victoire est déclarée si :
            - la ruche a atteint le nectar maximal (`MAX_NECTAR`), ou
            - la ruche a au moins la moitié du nectar maximal (dans certains cas).

            Paramètres
            ----------
            arrayhive : list
                Liste des ruches à vérifier. Chaque élément peut être soit une liste
                contenant une ruche, soit un tuple de coordonnées (ligne, colonne).

            Retours
            -------
            tuple[bool, int, int]
                - `won` : True si une ruche a gagné, False sinon.
                - `winning_hive_row` : indice de ligne de la ruche gagnante.
                - `winning_hive_col` : indice de colonne de la ruche gagnante.
        """
        won = False
        winning_hive_row = 0
        winning_hive_col = 0

        for x in arrayhive:
            if isinstance(x, list):
                hive = next((y for y in x if isinstance(y, Hive)), None)
                if hive is None:
                    continue
                r, c = getattr(hive, "row", None), getattr(hive, "col", None)
                if r is None or c is None:
                    continue
                if hive.currentNectar >= MAX_NECTAR:
                    won = True
                    winning_hive_row = r
                    winning_hive_col = c
                    break
            else:
                r, c = x
                cell = self.data[r][c]
                if hasattr(cell, "currentNectar") and cell.currentNectar >= MAX_NECTAR or cell.currentNectar >= MAX_NECTAR//2:
                    won = True
                    winning_hive_row = r
                    winning_hive_col = c
                    break

        return won, winning_hive_row, winning_hive_col

    def maxNectar(self, arrayhive: list) -> tuple[int, int]:
        """
            Détermine la ruche qui possède le plus de nectar sur la grille.

            La méthode parcourt la liste `arrayhive` et compare la quantité
            de nectar (`currentNectar`) de chaque ruche. Chaque élément de
            `arrayhive` peut être soit :
            - une liste contenant un objet `Hive`, soit
            - un tuple de coordonnées pointant directement vers une ruche.

            Le résultat indique les coordonnées de la ruche ayant accumulé
            le nectar maximal.

            Paramètres
            ----------
            arrayhive : list
                Liste des ruches à vérifier. Chaque élément peut être une liste
                contenant une ruche ou un tuple (ligne, colonne).

            Retours
            -------
            tuple[int, int]
                Coordonnées (ligne, colonne) de la ruche possédant le nectar maximum.
        """
        max_nectar = 0
        winning_hive_row = 0
        winning_hive_col = 0

        for x in arrayhive:
            if isinstance(x, list):
                hive = next((y for y in x if isinstance(y, Hive)), None)
                if hive is None:
                    continue
                if hive.currentNectar > max_nectar:
                    max_nectar = hive.currentNectar
                    idx = arrayhive.index(x)
                    r, c = arrayhive[idx] if not isinstance(arrayhive[idx], list) else (0, 0)
                    winning_hive_row = r
                    winning_hive_col = c
            else:
                r, c = x
                cell = self.data[r][c]
                if hasattr(cell, "currentNectar") and cell.currentNectar > max_nectar:
                    max_nectar = cell.currentNectar
                    winning_hive_row = r
                    winning_hive_col = c

        return winning_hive_row, winning_hive_col

    def getItemCoord(self,x):
        """
            Récupère les coordonnées d'un objet dans la grille.

            La méthode parcourt toutes les cellules de la grille et retourne
            les indices (ligne, colonne) de la cellule contenant l'objet `x`.
            L'objet peut être soit directement dans la cellule, soit dans
            une liste d'objets stockée dans la cellule.

            Paramètres
            ----------
            x : object
                L'objet dont on veut connaître la position dans la grille.

            Retours
            -------
            tuple[int, int] | None
                Les coordonnées (ligne, colonne) de l'objet si trouvé, sinon None.
        """
        rows = len(self.data)
        cols = len(self.data[0])
        for r in range(rows):
            for c in range(cols):
                if isinstance(self.data[r][c], list):
                    for item in self.data[r][c]:
                        if id(item) == id(x):
                            return r, c

                if id(self.data[r][c]) == id(x):
                    return (r, c)

    def setSafeZone(self, hive_array:list) -> None:
        """
            Définit des zones de sécurité pour chaque ruche sur la grille.

            La méthode crée quatre zones de sécurité prédéfinies correspondant
            aux coins de la grille et les associe à chaque ruche. Ces zones
            peuvent être utilisées pour protéger les ruches ou limiter les
            déplacements ennemis à proximité.

            Paramètres
            ----------
            hive_array : list
                Liste des 4 ruches pour lesquelles les zones de sécurité doivent être définies.
                Chaque ruche reçoit une zone correspondant à un coin de la grille.

            Retours
            -------
            None
                La méthode modifie directement les ruches en ajoutant la zone à
                leur attribut `baseList`.

            Exceptions
            ----------
            ValueError
                Levée si `hive_array` ne contient pas exactement 4 ruches.
        """
        if len(hive_array) != 4:
            raise ValueError("Expected at least 4 hives")
        tmpSize=self.size
        chunk = tmpSize//3
        zones = [
            ((0, chunk), (0, chunk)),
            ((0, chunk), (chunk * 2, tmpSize)),
            ((chunk * 2, tmpSize), (0, chunk)),
            ((chunk * 2, tmpSize), (chunk * 2, tmpSize))
        ]
        for hive , zones in zip(hive_array, zones):
            hive.baseList.append( (hive.owner, zones) )

    def getAreaOwner(self, hive_list: list, r: int, c: int) -> str | None:
        """
            Détermine le propriétaire d'une cellule située dans une zone de sécurité.

            La méthode parcourt la liste des ruches et leurs zones de sécurité
            (`baseList`). Si la cellule (r, c) se trouve dans l'une des zones
            d'une ruche, le propriétaire de cette ruche est retourné.

            Paramètres
            ----------
            hive_list : list
                Liste des ruches à vérifier. Chaque ruche doit posséder un attribut `baseList`,
                contenant des tuples de la forme (owner, ((r1, r2), (c1, c2))).
            r : int
                Indice de ligne de la cellule.
            c : int
                Indice de colonne de la cellule.

            Retours
            -------
            str | None
                Le propriétaire de la zone si la cellule se trouve dans une zone de sécurité,
                sinon None.
        """
        for hive in hive_list:
            for owner, ((r1, r2), (c1, c2)) in hive.baseList:
                if r1 <= r < r2 and c1 <= c < c2:
                    return owner
        return None


    def render(self)->None:
        """
            Affiche la grille du jeu dans la console.

            La méthode parcourt chaque cellule de la grille et construit une
            représentation textuelle ligne par ligne. Les règles de rendu sont :
            - Les cellules `None` sont représentées par un point `.`.
            - Les cellules contenant une liste sont représentées par `L`.
            - Les autres cellules affichent l'attribut `displayObject` de l'objet.

            Retours
            -------
            None
                La méthode affiche la grille directement dans la console.
        """
        for row in self.data:
            line = ""
            for cell in row:

                #Change with render priority system
                if isinstance(cell,list):
                    line += "L "
                    continue

                if cell is None:
                    line += ". "
                else:
                    line += str(cell.displayObject) + " "
            print(line)
