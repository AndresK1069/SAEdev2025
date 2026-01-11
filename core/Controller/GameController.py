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
        if len(hive.beeList) == 0:
            #fixme
            noBeeSpawn = messagebox.askyesno(
                f"{hive.owner.playerName} Action",
                "Vous n'avez pas d'abeille actuellement. Voulez-vous en pondre une ?"
            )


            # Convert True/False to 1/0 if you need
            noBeeSpawn_int = 1 if noBeeSpawn else 0
            if noBeeSpawn == 1:
                return self.spawn_bee(hive)
            else:
                return

        for bee in reversed(hive.beeList):
            if bee.isStun:
                continue


            #fixme
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
        self.gm.checkStunBee()
        arr_f = self.gm.recupFleur()
        self.gm.getBeePos()
        self.gm.flowerButinage(arr_f)
        self.gm.emptyBeeNectar(self.hive_coords)
        self.gm.checkEscarmouche()


    def check_end(self):
        is_winner, r, c = self.gm.isWinner(self.hive_coords)
        if is_winner:
            print(f"{self.gm.data[r][c].owner.playerName} is The Winner!")
            exit()
        return False
