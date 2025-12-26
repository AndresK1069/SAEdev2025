from tkinter import simpledialog

from data.constante import COUT_PONTE, NCASES


class GameController:
    def __init__(self, gm, hives, hive_coords, view, time_out):
        self.gm = gm
        self.hives = hives
        self.hive_coords = hive_coords
        self.view = view
        self.time_out = time_out

    def run(self):
        while self.time_out > 0:

            if self.check_end():
                return

            for hive in self.hives:
                self.play_turn(hive)

            self.end_round()
            self.time_out -= 1

    def play_turn(self, hive):
        self.view.render()
        self.view.show_player(hive)
        self.view.show_menu()
        choice = self.view.ask_choice()

        if choice == 1:
            self.spawn_bee(hive)
        elif choice == 2:
            self.move_bees(hive)
        elif choice == 3:
            pass

    def spawn_bee(self, hive):
        from core.utilities import getBeeStats
        index = self.hives.index(hive)
        row, col = self.hive_coords[index]
        if not isinstance(self.gm.data[row][col], list):
            if hive.currentNectar < COUT_PONTE :
                return

            bee_type = simpledialog.askstring(
                f"{hive.owner.playerName} Spawn Bee",
                "Nom de L'aibeille",
            )
            DummyObjectbeeData = getBeeStats(bee_type)



            self.gm.data[row][col] = self.gm.cellToList(row, col)

            if len(self.gm.data[row][col]) == 1:
                hive.currentNectar -= COUT_PONTE
                bee = hive.spawnBee(bee_type)
                self.gm.data[row][col].append(bee)

                self.view.clearCanva()
                self.view.render()
                del DummyObjectbeeData
                self.move_bees(hive)
        else:
            self.move_bees(hive)


    def move_bees(self, hive):
        for bee in hive.beeList:
            if bee.isStun:
                bee.stunCounter -= 1
                continue

            move  = simpledialog.askinteger(
            f"{hive.owner.playerName}Action",
            f"Bouger {bee}? (1 oui / 0 non)",
            minvalue=0,
            maxvalue=1
        )

            if move == 1:
                #get bee mobility to put in valid spot
                r,c = self.view.window.waitForClick()
                self.gm.moveObject(bee, c, r)
                self.gm.cleanGrid()

                self.view.clearCanva()
                self.view.render()

    def end_round(self):
        arr_f = self.gm.recupFleur()
        self.gm.getBeePos()
        self.gm.flowerButinage(arr_f)
        self.gm.emptyBeeNectar(self.hive_coords)
        self.gm.checkEscarmouche()
        self.gm.checkBeeHealth()

    def check_end(self):
        is_winner, r, c = self.gm.isWinner(self.hive_coords)
        if is_winner:
            self.view.show_winner(self.gm.data[r][c].owner.playerName)
            return True
        return False
