from random import choice
from tkinter import simpledialog, messagebox
from tkinter.colorchooser import Chooser

from data.constante import COUT_PONTE, NCASES
from core.utilities import randomName


class GameController:
    def __init__(self, gm, hives, hive_coords, view, time_out):
        self.gm = gm
        self.hives = hives
        self.hive_coords = hive_coords
        self.view = view
        self.time_out = time_out

    def run(self):
        """
            Exécute la boucle principale du jeu jusqu'à ce que le temps imparti soit écoulé ou que la partie se termine.

            Cette méthode gère le déroulement des tours de jeu pour chaque ruche (hive) :
            - Vérifie si la partie est terminée avec `check_end()`.
            - Pour chaque ruche :
                - Si le propriétaire n'est pas une IA, exécute `play_turn`.
                - Si le propriétaire est une IA, exécute `aiTurn`.
            - Termine le tour avec `end_round`.
            - Décrémente le compteur de temps `time_out`.

            La boucle continue tant que `time_out > 0` et que la partie n'est pas terminée.

            Retours
            -------
            None
                La méthode modifie l'état du jeu mais ne retourne rien.
        """
        while self.time_out > 0:
            print(self.time_out)

            if self.check_end():
                return

            for hive in self.hives:
                if not hive.owner.isAI:
                    self.play_turn(hive)
                else:
                    self.aiTurn(hive)

            self.end_round()
            self.time_out -= 1

    def aiTurn(self, hive):
        """
            Exécute le tour d'une ruche contrôlée par l'IA.

            La méthode effectue les actions suivantes :
            1. Efface et redessine le canevas via `self.view.clearCanva()` et `self.view.render()`.
            2. Vérifie si le propriétaire de la ruche est bien une IA.
            3. Détermine l'action de l'IA en appelant `shouldPlay` avec le nectar actuel de la ruche.
               - Si la ruche n'a pas assez de nectar pour pondre (`COUT_PONTE`), la décision est forcée
                 pour effectuer un déplacement (`choice = 2`).
            4. Exécute l'action choisie par l'IA :
               - `choice == 1` : pondre une abeille avec `aiSpawnBee`.
               - `choice == 2` : déplacer les abeilles avec `aiMoveBees`.
               - `choice == 3` : ne rien faire (option disponible mais non implémentée ici).

            Paramètres
            ----------
            hive : Hive
                La ruche dont le tour est géré par l'IA.

            Retours
            -------
            None
                La méthode agit sur l'état du jeu et met à jour l'affichage, mais ne retourne rien.
        """
        self.view.clearCanva()
        self.view.render()
        if hive.owner.isAI:
            choice = hive.owner.shouldPlay(hive.currentNectar)
            if hive.currentNectar < COUT_PONTE:
                choice = 2

            if choice == 1:
                self.aiSpawnBee(hive,hive.owner.getBee())
            if choice == 2:
                self.aiMoveBees(hive)
                pass
            if choice == 3:
                pass


    def play_turn(self, hive):
        """
            Exécute le tour d'une ruche contrôlée par un joueur humain.

            La méthode effectue les actions suivantes :
            1. Efface et redessine le canevas via `self.view.clearCanva()` et `self.view.render()`.
            2. Affiche les informations du joueur actif avec `show_player`.
            3. Affiche le menu des actions disponibles avec `show_menu`.
            4. Récupère le choix du joueur via `ask_choice2`.
            5. Exécute l'action choisie :
               - `choice == 1` : pondre une abeille avec `spawn_bee`.
               - `choice == 2` : déplacer les abeilles avec `move_bees`.
               - `choice == 3` : ne rien faire.

            Paramètres
            ----------
            hive : Hive
                La ruche du joueur dont le tour est exécuté.

            Retours
            -------
            None
                La méthode agit directement sur l'état du jeu et l'affichage, sans retourner de valeur.
        """
        self.view.clearCanva()
        self.view.render()
        self.view.show_player(hive)
        self.view.show_menu()
        choice = self.view.ask_choice2(hive)

        if choice == 1:
            self.spawn_bee(hive)
        elif choice == 2:
            self.move_bees(hive)
        elif choice == 3:
            pass

    def spawn_bee(self, hive):
        """
            Pond une abeille pour la ruche spécifiée.

            Cette méthode effectue les étapes suivantes :
            1. Récupère les coordonnées de la ruche dans la grille.
            2. Transforme la cellule en liste si nécessaire pour contenir plusieurs objets.
            3. Vérifie si la ruche dispose de suffisamment de nectar (`COUT_PONTE`) :
               - Si le nectar est insuffisant, la méthode déclenche directement le déplacement des abeilles via `move_bees`.
            4. Sinon, demande au joueur de choisir le type d’abeille à pondre via `choose_bee`.
            5. Réduit le nectar de la ruche du coût de ponte (`COUT_PONTE`).
            6. Crée l’abeille et lui assigne un propriétaire et un nom aléatoire.
            7. Ajoute l’abeille à la cellule correspondante dans la grille.
            8. Met à jour l’affichage via `clearCanva` et `render`.
            9. Déclenche le déplacement des abeilles via `move_bees`.

            Paramètres
            ----------
            hive : Hive
                La ruche qui pond l’abeille.

            Retours
            -------
            None
                La méthode modifie directement la grille et l’état du jeu, sans retourner de valeur.
        """
        index = self.hives.index(hive)
        row, col = self.hive_coords[index]

        if not isinstance(self.gm.data[row][col], list):
            self.gm.data[row][col] = [hive]

        if hive.currentNectar < COUT_PONTE:
            return self.move_bees(hive)

        bee_type=self.view.choose_bee(hive)

        hive.reduceNectar(COUT_PONTE)
        bee = hive.spawnBee(bee_type)
        bee.owner = hive.owner
        bee.name = randomName()
        self.gm.data[row][col].append(bee)

        self.view.clearCanva()
        self.view.render()
        self.move_bees(hive)

    def move_bees(self, hive):
        """
           Permet au joueur de déplacer les abeilles de sa ruche.

           Cette méthode effectue les étapes suivantes :
           1. Vérifie si la ruche possède des abeilles (`beeList`) :
              - Si aucune abeille n’est présente, propose au joueur de pondre une nouvelle abeille
                via une boîte de dialogue `messagebox.askyesno`.
              - Si le joueur accepte, appelle `spawn_bee`; sinon, termine l’action.
           2. Parcourt toutes les abeilles de la ruche dans l’ordre inverse pour permettre les déplacements récents en priorité.
           3. Ignore les abeilles étourdies (`isStun`).
           4. Pour chaque abeille non étourdie, demande au joueur via `messagebox.askyesno` s’il souhaite déplacer cette abeille.
           5. Si le joueur choisit de déplacer l’abeille :
              - Attend un clic sur la grille avec `waitForClick`.
              - Vérifie que la cellule cliquée appartient à la zone du joueur ou est libre.
              - Déplace l’abeille vers la cellule choisie avec `moveObject`.
              - Met à jour la grille et l’affichage (`cleanGrid`, `clearCanva`, `render`).
              - En cas de déplacement invalide, affiche un message d’erreur et redemande au joueur de cliquer.

           Paramètres
           ----------
           hive : Hive
               La ruche du joueur dont les abeilles doivent être déplacées.

           Retours
           -------
           None
               La méthode agit directement sur l’état de la grille et l’affichage, sans retourner de valeur.
        """
        if len(hive.beeList) == 0:

            noBeeSpawn = messagebox.askyesno(
                f"{hive.owner.playerName} Action",
                "Vous n'avez pas d'abeille actuellement. Voulez-vous en pondre une ?"
            )

            noBeeSpawn_int = 1 if noBeeSpawn else 0
            if noBeeSpawn == 1:
                return self.spawn_bee(hive)
            else:
                return

        for bee in reversed(hive.beeList):
            if bee.isStun:
                continue



            move = messagebox.askyesno(
                f"{hive.owner.playerName} Action",
                f"Bouger {bee.name}?"
            )

            move = 1 if move else 0

            if move == 1:
                while True:
                    try:
                        r, c = self.view.window.waitForClick()
                        areaOwner = self.gm.getAreaOwner(self.hives, r, c)
                        if areaOwner != bee.owner and areaOwner is not None:
                            raise ValueError("It's not your zone")
                        self.gm.moveObject(bee, r, c)

                        self.gm.cleanGrid()
                        self.view.clearCanva()
                        self.view.render()
                        break
                    except Exception as e:
                        print(f"Invalid move: {e}. Please try again.")

    def aiSpawnBee(self, hive ,beeType):
        """
            Pond une abeille pour une ruche contrôlée par l'IA.

            Cette méthode effectue les étapes suivantes :
            1. Récupère les coordonnées de la ruche dans la grille.
            2. Transforme la cellule en liste si nécessaire pour contenir plusieurs objets.
            3. Vérifie si la ruche dispose de suffisamment de nectar (`COUT_PONTE`) :
               - Si le nectar est insuffisant, l'IA déclenche directement le déplacement des abeilles via `aiMoveBees`.
            4. Sinon :
               - Réduit le nectar de la ruche du coût de ponte (`COUT_PONTE`).
               - Crée l’abeille du type spécifié (`beeType`).
               - Assigne l’abeille à son propriétaire et lui donne un nom aléatoire.
               - Ajoute l’abeille à la cellule correspondante dans la grille.
            5. Met à jour l’affichage via `clearCanva` et `render`.
            6. Déclenche le déplacement des abeilles de l’IA via `aiMoveBees`.

            Paramètres
            ----------
            hive : Hive
                La ruche contrôlée par l'IA qui pond l’abeille.
            beeType : type
                Le type d’abeille à créer pour la ruche.

            Retours
            -------
            None
                La méthode modifie directement la grille et l’état du jeu, sans retourner de valeur.
        """
        index = self.hives.index(hive)
        row, col = self.hive_coords[index]

        if not isinstance(self.gm.data[row][col], list):
            self.gm.data[row][col] = [hive]

        if hive.currentNectar < COUT_PONTE:
            return self.aiMoveBees(hive)

        hive.reduceNectar(COUT_PONTE)
        bee = hive.spawnBee(beeType)
        bee.owner = hive.owner
        bee.name = randomName()
        self.gm.data[row][col].append(bee)

        self.view.clearCanva()
        self.view.render()
        self.aiMoveBees(hive)

    def aiMoveBees(self, hive):
        """
            Déplace automatiquement les abeilles d'une ruche contrôlée par l'IA.

            Cette méthode effectue les étapes suivantes pour chaque abeille de la ruche :
            1. Parcourt les abeilles de la ruche dans l’ordre inverse pour traiter les déplacements récents en priorité.
            2. Ignore les abeilles étourdies (`isStun`).
            3. Pour chaque abeille non étourdie, effectue un déplacement automatique :
               - Récupère les coordonnées actuelles de l’abeille dans la grille avec `getItemCoord`.
               - Si l’abeille n’est pas trouvée, récupère la position de la ruche.
               - Demande à l’IA de générer de nouvelles coordonnées avec `aiMoveBee`.
               - Vérifie que la cellule de destination appartient à la zone du joueur ou est libre.
               - Déplace l’abeille vers la cellule choisie avec `moveObject`.
               - Nettoie la grille et met à jour l’affichage via `cleanGrid`, `clearCanva` et `render`.
               - En cas de déplacement invalide, réessaie jusqu’à ce qu’un déplacement valide soit effectué.

            Paramètres
            ----------
            hive : Hive
                La ruche contrôlée par l’IA dont les abeilles doivent être déplacées.

            Retours
            -------
            None
                La méthode modifie directement la grille et l’affichage, sans retourner de valeur.
        """
        for bee in reversed(hive.beeList):
            if bee.isStun:
                continue

            while True:
                try:
                    bee_r, bee_c = self.gm.getItemCoord(bee)
                    if bee_r is None or bee_c is None:
                        bee_r, bee_c = self.gm.getItemCoord(hive)
                    r, c = hive.owner.aiMoveBee(bee, bee_r, bee_c)
                    areaOwner = self.gm.getAreaOwner(self.hives, r, c)
                    if areaOwner != bee.owner and areaOwner is not None:
                        raise ValueError("It's not your zone")
                    self.gm.moveObject(bee, r, c)
                    self.gm.cleanGrid()
                    self.view.clearCanva()
                    self.view.render()
                    break
                except Exception as e:
                    print(f"Move failed for bee {bee}: {e}. Retrying...")



    def end_round(self):
        """
           Exécute les actions de fin de tour pour toutes les entités de la grille.

           Cette méthode effectue les opérations suivantes dans l'ordre :
           1. Vérifie les abeilles étourdies et met à jour leur compteur de stun avec `checkStunBee`.
           2. Récupère toutes les fleurs présentes sur la grille avec `recupFleur`.
           3. Met à jour la position de toutes les abeilles avec `getBeePos`.
           4. Effectue le butinage des fleurs par les abeilles avec `flowerButinage`.
           5. Transfère le nectar des abeilles vers les ruches avec `emptyBeeNectar`.
           6. Vérifie les escarmouches entre abeilles ennemies et applique les dégâts éventuels avec `checkEscarmouche`.

           Paramètres
           ----------
           Aucun

           Retours
           -------
           None
               La méthode agit directement sur l'état de la grille, les ruches, les abeilles et l'affichage, sans retourner de valeur.
        """
        self.gm.checkStunBee()
        arr_f = self.gm.recupFleur()
        self.gm.getBeePos()
        self.gm.flowerButinage(arr_f)
        self.gm.emptyBeeNectar(self.hive_coords)
        self.gm.checkEscarmouche()


    def check_end(self):
        """
            Vérifie si une ruche a atteint la condition de victoire et termine le jeu si c'est le cas.

            Cette méthode effectue les étapes suivantes :
            1. Appelle `isWinner` sur la grille pour vérifier si l'une des ruches a atteint le nectar maximum (`MAX_NECTAR`).
            2. Si une ruche gagnante est détectée :
               - Affiche le nom du joueur gagnant.
               - Termine immédiatement le programme avec `exit()`.
            3. Sinon, retourne `False` pour indiquer qu'aucune condition de fin n'est remplie.

            Paramètres
            ----------
            Aucun

            Retours
            -------
            bool
                False si le jeu continue (aucune ruche n'a encore gagné).
            """
        is_winner, r, c = self.gm.isWinner(self.hive_coords)
        if is_winner:
            print(f"{self.gm.data[r][c].owner.playerName} is The Winner!")
            exit()
        return False
