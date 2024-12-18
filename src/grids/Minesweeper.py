from Grids import Grid
import time


class Minesweeper:

    def __init__(self, x: int, y: int, amt: int, lock: bool = False, mines: list = [], front_end: list = [], back_end: list = []):
        """
        :param x: how wide the board is
        :param y: how tall the board is
        :param amt: how many mines should be in the board
        :param lock: should it generate a new board if it cannot initiate, optional
        :param mines: allows direct control of the positions of the mines, optional
        :param front_end: "the interface", optional
        :param back_end: "the answer", if inputted, backend will be default as mines, optional
        """
        from random import randint

        # blueprint?
        self.backgrid = Grid(x, y, " ")
        self.b = Grid(x, y, "=")
        self.lock = lock
        self.sudo_open = []
        # randomly generate mines

        if not lock:
            self.mines = []
            while len(self.mines) < amt:
                l, n = randint(1, x), randint(1,y)
                if (l, n) not in self.mines:
                    self.mines.append((l, n))
        else:
            self.mines = mines

        # only uses preset board if locked and backend offered
        if not back_end or not lock:
            # tally up the amount of mines surrounding each square/tile
            for x in self.mines:
                for y in self.backgrid.is_neighbor(x):
                    value = self.backgrid.grid_value(y)
                    if value == " ":
                        self.backgrid.change_grid([y], "1")
                        continue
                    self.backgrid.change_grid([y], str(int(value)+1))
            # change the mined tiles' labels
            self.backgrid.change_grid(self.mines, "M")
        elif back_end and lock:
            self.backgrid.grid = list(back_end)
            if front_end:
                self.b.grid = list(front_end)

    def amt_empty(self, coord: tuple) -> tuple:
        if self.backgrid.grid_value(coord) != " ":
            return tuple([coord]), 0
        else:
            been_in = []
            empty_squares = []
            edge_list = []
            next_list = [coord]
            while next_list:
                nex = next_list.pop(0)
                for x in self.backgrid.is_neighbor(nex):
                    if x not in been_in:
                        been_in.append(x)
                        if self.backgrid.grid_value(x) == " ":
                            empty_squares.append(x)
                            next_list.append(x)
                        elif self.backgrid.grid_value(x).isdigit() and x not in edge_list:
                            edge_list.append(x)
            return tuple(empty_squares), len(edge_list)


    @staticmethod
    def expose_empty_squares(a, b, guess: tuple) -> None:
        b.change_grid([guess], " ")
        next_list = [guess]
        been_in = []
        while next_list:
            nex = next_list.pop(0)
            for x in b.is_neighbor(nex):
                if x not in been_in:
                    been_in.append(x)
                    # if it's next to a mine stop
                    value = a.grid_value(x)
                    if value != " ":
                        b.change_grid([x], value)
                    elif value == " ":
                        next_list.append(x)
                        b.change_grid([x], " ")

    def startupcheck(self, coord: tuple = (0, 0)) -> bool:
        """
        :param coord: the coordinate you want to start with
        :return: False if it cannot find a map in 10 tries, True if it succeds
        """
        if coord == (0, 0):
            blank_list = []
            blobs = {}
            for l in range(self.b.x):
                for n in range(self.b.y):
                    if (l+1, n+1) not in blank_list:
                        temp_tup = self.amt_empty((l+1, n+1))
                        blank_list += list(temp_tup[0])
                        if temp_tup[0]:
                            blobs[temp_tup[0]] = temp_tup[1]
            for l in blobs:
                if max(blobs.values()) == blobs[l]:
                    self.expose_empty_squares(self.backgrid, self.b, l[0])
                    return True
        tally = 0
        while self.backgrid.grid_value(coord) != " " and tally < 11:
            self.__init__(self.backgrid.x, self.backgrid.y, len(self.mines), self.lock, self.mines)
            tally += 1
        if tally >= 10:
            return False
        else:
            self.expose_empty_squares(self.backgrid, self.b, coord)
            return True

    def game_end_check(self) -> bool:
        """
        :return: True if you have won, and False if you haven't
        """
        # check if there are undiscovered squares remaining
        end = 0
        for x in self.b.grid:
            for y in x:
                if y in "?F▩=":
                    end += 1
        if end == len(self.mines):
            print("you dug out all the other squares!")
            for x in range(self.b.x):
                for y in range(self.b.y):
                    if self.b.grid_value((x+1, y+1)) == "=":
                        self.b.change_grid([(x+1, y+1)], "F")
            return True

        end = 0
        for x in range(self.b.y):
            for y in range(self.b.x):
                if self.backgrid.grid_value((y, x)) == "M":
                    end += 2
                    if self.b.grid_value((y, x)) == "F":
                        end -= 1
        if end == len(self.mines):
            print("you flagged all the mines!")
            for x in range(self.b.x):
                for y in range(self.b.y):
                    if self.b.grid_value((x+1, y+1)) == "=":
                        self.discover((x+1, y+1))
            return True
        return False

    def flag(self, guess: tuple) -> None:
        """
        :param guess: the coordinates you want to flag
        :return: nothing
        """
        value = self.b.grid_value(guess)
        if value == "?" or value == "▩" or value == "=":
            self.b.change_grid([guess], "F")
        elif value == "F":
            self.b.change_grid([guess], "=")
        else:
            print("you've explored this square")

    def discover(self, guess: tuple, temp: bool = False) -> bool:
        """
        :param guess: the coordinates you want to open
        :param temp: just to open that one square
        :return: True if you stepped on a mine, False if nothing happens
        """
        # to stop and reconsider
        if self.b.grid_value(guess) == "M":
            print(input("it's was a mine"))

        if self.b.grid_value(guess) == "F":
            print("you flagged this square")

        elif self.backgrid.grid_value(guess) == "M":
            self.b.change_grid([guess], "M")
            print("game over\nyou stepped on a mine")
            return True

        elif self.backgrid.grid_value(guess) == " ":
            if temp:
                self.b.change_grid([guess], "O")
                self.sudo_open.append(guess)
            else:
                self.expose_empty_squares(self.backgrid, self.b, guess)

        else:
            if temp and self.b.grid_value(guess) != "O":
                self.b.change_grid([guess], "O")
                self.sudo_open.append(guess)
            else:
                self.b.change_grid([guess], self.backgrid.grid_value(guess))
        return False

    def game(self) -> None:
        """
        game interface for users
        :return: nothing
        """
        self.b.display()
        guess = Grid.coords()
        if not self.startupcheck(guess):
            print("something might be wrong")
            return
        self.backgrid.display()
        print(self.mines)

        # game loop
        while not self.game_end_check():
            f = input("flag or open?: (f / g)")
            if f == "g":
                if self.discover(Grid.coords()):
                    break
            elif f == "f":
                self.flag(Grid.coords())
            self.b.display()
        return

    def ai(self, through: int, dis :bool = True, step: bool = False) -> tuple:
        """
        :return: front end, back end, if it has solved it
        """

        def all_combo(source: list, parent_branch: list = [], tar_len: int = 0) -> list:
            if not tar_len:
                return parent_branch
            result = []
            while source:
                on = source.pop(0)

                returned = all_combo(list(source), parent_branch + [on], tar_len - 1)

                if not returned:
                    pass
                elif type(returned[0]) != list:
                    result.append(returned)
                else:
                    result += returned
            return result

        self.b.display()
        cleared_list = []
        prev_grid = []
        tally = 0
        priority_copy = []
        priority = []
        while not self.game_end_check():
            if dis:
                time.sleep(0.7)
            # goes through every square
            for x in range(self.b.x):
                for y in range(self.b.y):
                    coord = (x + 1, y + 1)

                    if self.b.grid_value(coord) == " ":
                        if step:
                            for l in self.b.is_neighbor(coord):
                                if self.b.grid_value(l) == "=":
                                    self.discover(l, step)
                        cleared_list.append(coord)

                    states = {"flag":[],"unknown":[]}
                    # if the square has a number on it
                    if not self.b.grid_value(coord).isdigit() or coord in cleared_list:
                        continue
                    if dis:
                        self.b.blip("#", coord)
                    # print(cleared_list)
                    #for z in m.b.is_neighbor(a):
                    #    if m.b.grid_value(z).isdigit():
                    #        priority_copy.insert(0,z)

                    amount = int(self.b.grid_value(coord))
                    neighbors = self.b.is_neighbor(coord)
                    # sorts the squares neighboring the square
                    for z, g in [(self.b.grid_value(z), z) for z in neighbors]:
                        if z == "F":
                            states["flag"].append(g)
                        elif z in "?▩=":
                            states["unknown"].append(g)

                    # open all other squares if the amount of mines are the same as the number on the square
                    if len(states["flag"]) == amount:
                        # print("clearing everything\n\n")
                        cleared_list.append(coord)
                        for z in states["unknown"]:
                            self.discover(z, step)
                        states["unknown"] = []

                    # if unknown matches the number
                    elif len(states["unknown"]) + len(states["flag"]) == amount:
                        # print("flagging everything\n\n")
                        for z in states["unknown"]:
                            self.flag(z)
                            states["flag"].append(z)
                        states["unknown"] = []

                    # big brain
                    elif prev_grid == self.b.grid:
                        # print("yeah, it's big brain time\n\n")
                        possibilities = amount - len(states["flag"])

                        possible_combos = all_combo(list(states["unknown"]), [], possibilities)
                        # print(possible_combos, "possible combos")
                        possible_combos_fin = list(possible_combos)
                        # see if combo can be obviously denied
                        for z in possible_combos:
                            surrounding_possible = []
                            # for every flagged option
                            for n in z:
                                # surrounding_possible is all the surrounding squares with numbers on them
                                surrounding_possible += [d for d in self.b.is_neighbor(n) if self.b.grid_value(d).isdigit()]
                            # print(surrounding_possible, "surrounding possible squares")

                            # see if the possible combo surrounding a square is bigger than the actual square's value
                            for o in set(surrounding_possible):
                                # print(o, m.b.grid_value(o), "checking square")
                                total = 0
                                for p in self.b.is_neighbor(o):
                                    if self.b.grid_value(p) == "F" or p in z:
                                        total += 1
                                if total > int(self.b.grid_value(o)):
                                    # print("remove", z)
                                    possible_combos_fin.remove(z)
                                    break
                             # print(surrounding_possible, "surrounding possible numbers after")
                        # print(states["unknown"], "unknown squares")
                        # print(possible_combos_fin, "final possible combinations")
                        record = {x:0 for x in states["unknown"]}
                        # counting how often each squares appear in possible combos
                        for z in possible_combos_fin:
                            for n in z:
                                record[n] += 1
                        # print(record, "number of possible positions")
                        for z in record:
                            if record[z] == len(possible_combos_fin):
                                self.flag(z)
                                states["flag"].append(z)
                                states["unknown"].remove(z)
                            elif record[z] == 0:
                                self.discover(z, step)
                                states["unknown"].remove(z)

                        surrounding_possible = []
                        for l in possible_combos_fin:
                            for n in l:
                                for z in self.b.is_neighbor(n):
                                    if z not in surrounding_possible and self.b.grid_value(z).isdigit():
                                        surrounding_possible.append(z)
                        while coord in surrounding_possible:
                            surrounding_possible.remove(coord)

                        if dis:
                            print(record, "record, square, times it appeared in possible combos")
                            print(surrounding_possible, "surrounding possible")
                            print(possible_combos_fin, "possible combo final")
                            print(states, "states")

                        # trouble child section
                        # check if in all instances if the amount of mines around the neighbor is constant
                        for l in set(surrounding_possible):
                            if not self.b.grid_value(l).isdigit():
                                continue
                            all_num = []
                            for n in possible_combos_fin:
                                number = 0
                                for z in n:
                                    if l in self.b.is_neighbor(z):
                                        number += 1
                                all_num.append(number)

                            check = True
                            for n in range(len(all_num)-1):
                                if all_num[n] != all_num[n+1]:
                                    check = False
                                    continue
                            # print(check, l)
                            # if all combos lead to same number of mines around the square
                            if not check:
                                continue
                            surround_neighbor_states = {"flag": [], "unknown": []}
                            for n in self.b.is_neighbor(l):
                                if self.b.grid_value(n) in "?▩=":
                                    surround_neighbor_states["unknown"].append(n)
                                elif self.b.grid_value(n) == "F":
                                    surround_neighbor_states["flag"].append(n)
                            remain = int(self.b.grid_value(l)) - all_num[0]
                            if remain != 0:
                                continue
                            for n in self.b.is_neighbor(l):
                                if n not in states["unknown"] and n not in states["flag"]:
                                    self.discover(n, step)

                        # sees what squares are all connectes to all possible combos and see if it fills the similar squares
                        deep = []
                        surrounding_possible = {y: 0 for x in states["unknown"] for y in self.b.is_neighbor(x) if self.b.grid_value(y).isdigit()}
                        for l in states["unknown"]:
                            for n in self.b.is_neighbor(l):
                                if self.b.grid_value(n).isdigit():
                                    surrounding_possible[n] += 1
                        for l in surrounding_possible:
                            if surrounding_possible[l] == len(states["unknown"]):
                                deep.append(l)

                        # print(deep, "possible fully connected squares")
                        for l in set(deep):
                            theory_stat = {"unknown": [], "flag": []}
                            for n in self.b.is_neighbor(l):
                                if self.b.grid_value(n) == "F":
                                    theory_stat["flag"].append(n)
                                if self.b.grid_value(n) in "?▩=" and n not in states["unknown"]:
                                    theory_stat["unknown"].append(n)
                            # print(theory_stat, "theory_stat")
                            if int(self.b.grid_value(l)) - len(theory_stat["flag"]) == amount - len(states["flag"]):
                                for n in theory_stat["unknown"]:
                                    self.discover(n, step)

                            if int(self.b.grid_value(l)) == len(theory_stat["flag"]) + len(theory_stat["unknown"]) + amount - len(states["flag"]):
                                for n in theory_stat["unknown"]:
                                    self.flag(n)

            if prev_grid == self.b.grid:
                cleared_list = []
                tally += 1
            else:
                tally = 0

            if step and tally > through:
                return self.b.grid, self.backgrid.grid, False
            if tally > through:
                return self.b.grid, self.backgrid.grid, False
                # print(input("hey, come and troubleshoot"))
                pass
            # prev_grid = tuple([list(x) for x in list(self.b.grid)])
            prev_grid = list(self.b.grid)

        else:
            return self.b.grid, self.backgrid.grid, True

    def realize_step(self):
        for guess in self.sudo_open:
            self.b.change_grid([guess], self.backgrid.grid_value(guess))
        self.sudo_open.clear()

    def step_by_step(self):
        temp_grid = [x.copy() for x in self.b.grid.copy()]
        vis, *_ = self.ai(20, False)
        self.b.grid = temp_grid
        self.b.display()
        print(input("next"))
        while self.b.grid != vis:
            self.ai(0, True, True)
            self.b.display()
            print("displayed")
            print(input("next"))
            self.realize_step()
