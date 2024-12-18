import pygame, time
pygame.init()
if __name__ == "__main__":
    #name of decorator

    def timer(func):
        # the actual function to return
        def timer_actual(*params):
            t1 = time.time()
            func(*params)
            difference = time.time()-t1
            print(difference, "time taken")
        return timer_actual


    class Test:
        @timer
        def __call__(self, *args):
            print(sum(args))
    test = Test()


    test(2, 3, 2)

    from multidispatch import multifunction
    dict()
    import inspect
    join = multifunction.new("join")
    # print(dict(join))
    print()
    @join.overload((int, complex), (int, complex))
    def join(x, y):
        return x + y


    print()


    @join.overload(float,  float)
    def join(x, y):
        print(x, y)
        return None
    print()
    # print(dict(join))
    # print(join)
    print("calling function")
    print(join(3, 4))

    hello = multifunction.new("hello")
    @hello.overload(int)
    def hello(number):
        print(number)

    @hello.overload((tuple, list, dict))
    def hello(number):
        for x in number:
            print(x)
    hello([2])


class UnimplementedError(ReferenceError):
    def __init__(self):
        super().__init__("Method not implemented")


class Grid:

    def __contains__(self, item) -> bool:
        if isinstance(item, str):
            if item in self.grid_ids:
                if self.grid_ids[item]:
                    return True
        elif isinstance(item, tuple):
            if item[0] < self.x and item[1] < self.y:
                return True
        else:
            return False

    def __len__(self):
        return self.x * self.y

    def __str__(self):
        grid = ""
        for x in self.grid[::-1]:
            grid += " ".join(x)
            grid += "\n"
        return grid

    def __hash__(self):
        raise UnimplementedError
        return hash((self.x, self.y, tuple([tuple(x) for x in self.grid])))

    def __repr__(self):
        """see inside"""
        self.info()
        information = [
            f"From {self.__module__} file, Type: {type(self).__name__}, id: {hex(id(self))}",
            str(self),
            "\n".join([f"{x} : {self.grid_ids[x]}" for x in self.grid_ids])]
        print(information[0])
        print(information[1])
        print("Grid")
        print(information[2])
        print("info")
        return "\n".join(information)

    def __eq__(self, other):
        return self.grid == other.grid

    def __ne__(self, other):
        return self.grid != other.grid

    def __add__(self, other):
        if self.x != other.x:
            raise TypeError("Grids of different heights cannot be added together")
        self.x *= 2
        for x in range(self.y):
            self.grid[x] += other.grid[x]
        return self

    def __neg__(self):
        self.grid = self.grid[::-1]
        self.info()
        return

    def __dict__(self):
        product = {}
        coord = tuple()
        for x in range(self.x):
            for y in range(self.y):
                coord = tuple([x+1, y+1])
                product[coord] = self[coord]
        return product

    def copy(self):
        self1 = object.__new__(type(self))
        self1.grid = [[x for x in y] for y in self.grid]
        self1.x, self1.y = int(self.x), int(self.y)
        self1.info()
        return self1

    def __init__(self, x: int, y: int, startup="_"):
        self.x, self.y = x, y
        self.grid = [[startup for x in range(x)] for _ in range(y)]
        self.grid_ids = {startup: [(x + 1, y + 1) for x in range(self.x) for y in range(self.y)]}

    def convert_strlis(self, x: int, y, list1: str, char_lis, ignore: list = []):
        """
        converts a long string of characters into a grid form (resets grid)
        :param ignore: what charaters to ignore in a list
        :param x: width
        :param y: height
        :param list1: the map as a string
        :param char_lis: diffent characters within the map wished to be located
        :return: nothing
        """
        self.x, self.y = x, y
        count = 0
        maplist = []

        if "\n" in ignore:
            ignore.remove("\n")
        else:
            ignore.append("\n")
        for x in list1:
            if x in ignore:
                continue
            if (len(maplist) - 1) < (count // self.x):
                maplist.append([])
            if len(maplist) > y:
                break
            maplist[count // self.x].append(x)
            if x not in self.grid_ids:
                self.grid_ids[x] = []
            self.grid_ids[x].append((count % self.x + 1, self.y - (count // self.x)))
            count += 1
        else:
            if count < self.x * self.y:
                self.grid_ids[" "] = []
                while count // self.x < self.y:
                    maplist.append([])
                    enter = (count // self.x) + 1
                    while count < self.x * enter:
                        maplist[count // self.x].append(" ")
                        self.grid_ids[" "].append((count % self.x + 1, self.y - (count // self.x)))
                        count += 1
        chars = {x: self.grid_ids[x] for x in char_lis}
        self.grid = maplist[::-1]
        return [chars[x] for x in chars]

    @staticmethod
    def coords() -> tuple:
        """
        takes user input and transforms into usable input
        :return:
        """
        while True:
            try:
                a = input("what square: (x, y)").split(",")
                if a[0].isdigit() and a[1].isdigit():
                    return (int(a[0]), int(a[1]))
            except:
                pass

    @staticmethod
    def coord_adjust(coord, x: int = 0, y: int = 0, **_):
        """
        shifts the x axis or y axis given the amount to adjust
        :param coord: the coord that will be adjisted
        :param x: the amount x should be shifted
        :param y: the amount y axis will be shifted
        :param _: buffer
        :return: the adjusted coords/result
        """
        return coord[0] + x, coord[1] + y

    def pos_get(self) -> list:
        def get_key(key_name: str) -> bool:
            """
            list of manually selected coordinates
            :param key_name: name of key
            :return: True if the key is pressed
            """

            for _ in pygame.event.get():
                pass
            keyinput = pygame.key.get_pressed()
            mykey = getattr(pygame, "K_{}".format(key_name))
            if keyinput[mykey]:
                return True

        coord = (1, 1)
        poss = {}
        self.display()
        while not get_key("ESCAPE"):
            time.sleep(0.4)
            if get_key("UP"):
                if coord[1] < self.y:
                    coord = (coord[0], coord[1] + 1)
                    self.blip("#", coord)

            elif get_key("DOWN"):
                if coord[1] > 1:
                    coord = (coord[0], coord[1] - 1)
                    self.blip("#", coord)

            elif get_key("RIGHT"):
                if coord[0] < self.x:
                    coord = (coord[0] + 1, coord[1])
                    self.blip("#", coord)

            elif get_key("LEFT"):
                if coord[0] > 1:
                    coord = (coord[0] - 1, coord[1])
                    self.blip("#", coord)

            elif get_key("RETURN"):
                if self.grid_value(coord) != "X":

                    poss[coord] = self.grid_value(coord)
                    self.change_grid([coord], "X")
                    self.display()
                else:
                    self.change_grid([coord], poss[coord])
                    poss.pop(coord)
                    self.display()
        for l in poss:
            self.change_grid([l], poss[l])
        return [x for x in poss]

    def display(self, separators=" "):
        try:
            for x in self.grid[::-1]:
                row = x[0]
                for y in x[1:]:
                    row += separators + str(y)
                print(row)
            print()
        except IndexError:
            print("Actual grid size don't match provides size")

    def blip(self, change_to="0", *spots):
        store = {}
        for spot in spots:
            store[spot] = self.grid_value(spot)
            self.change_grid([spot], change_to, blip=True)
        self.display()
        for spot in spots:
            self.change_grid([spot], store[spot], blip=True)

    @staticmethod
    def multi_display(grids: list, separators: str = " ") -> None:
        for x in range(len(grids[0])):
            row = ""
            for y in grids:
                row += str(separators).join(y[len(y) - x - 1]) + " | "
            print(row)
        print()

    def is_neighbor(self, coords: tuple):
        try:
            in_list = []
            for w in range(3):
                for z in range(3):
                    if 0 < coords[1] + w - 1 < self.y + 1 and 0 < coords[0] + z - 1 < self.x + 1:
                        in_list.append((coords[0] + z - 1, coords[1] + w - 1))
            in_list.remove(coords)
            return in_list
        except ValueError:
            return []

    def direct_neighbor(self, coords: tuple):
        try:
            in_list = []
            for x in [(coords[0] - 1, coords[1]), (coords[0] + 1, coords[1]), (coords[0], coords[1] - 1),
                      (coords[0], coords[1] + 1)]:
                # print(x[::-1])
                if 0 < x[1] < self.y + 1 and 0 < x[0] < self.x + 1:
                    # print(x[::-1], "is in")
                    in_list.append(x)
            return in_list
        except ValueError:
            return []

    def __setitem__(self, keys: list, value: str):
        """
        coordinate to grid interaction
        changes the value of coordinates inside keys to value
        :param keys: coordinats that will be changed
        :param value: the value the keys will be changed to
        :return:
        """
        if value not in self.grid_ids:
            self.grid_ids[value] = []
        if isinstance(keys, tuple):
            self.grid_ids[value].append(keys)
            self.grid[keys[1] - 1][keys[0] - 1] = value
        elif isinstance(keys, list):
            self.grid_ids[value] += keys
            for coord in keys:
                self.grid[coord[1] - 1][coord[0] - 1] = value

    def change_grid(self, change: list, change_to: str, blip: bool = False):
        """
        coordinate to grid interaction
        changes the value of the coords in the grid to change_to
        :param change: the coordinates that will be changed
        :param change_to: the value the coord changes to
        :param blip: help eleiviate memory use
        :return:
        """
        if change_to not in self.grid_ids and not blip:
            self.grid_ids[change_to] = []
        for x in change:
            self.grid[x[1] - 1][x[0] - 1] = change_to
            if not blip:
                for y in self.grid_ids:
                    if x in self.grid_ids[y]:
                        self.grid_ids[y].remove(x)
                self.grid_ids[change_to].append(x)

    def replace_all(self, **change_to):
        for x in change_to:
            print("replace", self.grid_ids[x], change_to[x])
            self.change_grid(list(self.grid_ids[x]), change_to[x])

    @staticmethod
    def block_create(corner1: tuple, corner2: tuple):
        corner1, corner2 = (min(corner1[0], corner2[0]), min(corner1[1], corner2[1])), (
            max(corner1[0], corner2[0]), max(corner1[1], corner2[1]))
        return [(y, x) for x in range(corner1[1], corner2[1] + 1) for y in range(corner1[0], corner2[0] + 1)]

    def __getitem__(self, item: tuple):
        return self.grid[item[1]-1][item[0]-1]

    def grid_value(self, coordinate: tuple):
        if coordinate[0] > self.x and coordinate[1] > self.y:
            raise IndexError("Both numbers are too big")
        elif coordinate[0] > self.x:
            raise IndexError("The first number is too big")
        elif coordinate[1] > self.y:
            raise IndexError("The second number is too big")
        return self.grid[coordinate[1] - 1][coordinate[0] - 1]

    def info(self, *spec_char) -> dict:
        """
        returns all locations of characters in the form of dictionary
        :param spec_char: the characters the program chould output, returns all loctions of all characters if nothing is inputted
        :return:
        """
        self.grid_ids = {}
        locations = {}
        for x in range(self.x):
            for y in range(self.y):
                value = self.grid_value((x + 1, y + 1))
                if value not in self.grid_ids:
                    self.grid_ids[value] = []
                if not spec_char:
                    if value not in locations:
                        locations[value] = []
                    locations[value].append((x + 1, y + 1))
                    self.grid_ids[value].append((x + 1, y + 1))
                else:
                    if value in spec_char:
                        if value not in locations:
                            locations[value] = []
                        locations[value].append((x + 1, y + 1))
                        self.grid_ids[value].append((x + 1, y + 1))
        return locations


class InfiniGrid(Grid):

    def foucus(self, coord: tuple, x_start=0, x_end=0, y_start=0, y_end=0) -> tuple:
        """
        foucuses the coord back on the board
        :param coord: coord that will be foucused
        :return: the foucused coord
        """
        x_start -= 1
        y_start -=1
        if x_end == 0:
            x_end = self.x - x_start
        else:
            x_end -= x_start
            # x_end += 1

        if y_end == 0:
            y_end = self.y - x_start
        else:
            y_end -= y_start
            # y_end += 1
        # 1 2 3 4 5 6 7 8
        #   2 3 4 5 6
        # x_start, x_end =  = 2, 8
        # x_start = 2, x_end = 6
        return (coord[0] + x_end - 1 - x_start) % x_end + 1 + x_start, (coord[1] + y_end - 1- y_start) % y_end + 1 + y_start

    def coord_adjust(self, coord, x: int = 0, y: int = 0, **_) -> tuple:
        """
        shifts the x axis or y axis given the amount to adjust
        :param coord: the coord that will be adjisted
        :param x: the amount x should be shifted
        :param y: the amount y axis will be shifted
        :param _: buffer
        :return: the adjusted coords/result
        """
        return (coord[0] + x + self.x-1) % self.x + 1, (coord[1] + y + self.y - 1) % self.x + 1

    def pos_get(self) -> dict:

        def get_key(key_name: str) -> bool:
            """
            list of manually selected coordinates
            :param key_name: name of key
            :return: True if the key is pressed
            """

            for _ in pygame.event.get():
                pass
            keyinput = pygame.key.get_pressed()
            mykey = getattr(pygame, "K_{}".format(key_name))
            if keyinput[mykey]:
                return True

        coord = (1, 1)
        poss = {}
        self.display()
        while not get_key("ESCAPE"):
            time.sleep(0.4)
            if get_key("UP"):
                coord = (coord[0], coord[1] + 1)
                self.blip("#", coord)

            elif get_key("DOWN"):
                coord = self.foucus((coord[0], coord[1] - 1))
                self.blip("#", coord)

            elif get_key("RIGHT"):
                coord = self.foucus((coord[0] + 1, coord[1]))
                self.blip("#", coord)

            elif get_key("LEFT"):
                coord = self.foucus((coord[0] - 1, coord[1]))
                self.blip("#", coord)

            elif get_key("RETURN"):
                if self.grid_value(coord) != "X":

                    poss[coord] = self.grid_value(coord)
                    self.change_grid([coord], "X")
                    self.display()
                else:
                    self.change_grid([coord], poss[coord])
                    poss.pop(coord)
                    self.display()
        for l in poss:
            self.change_grid([l], poss[l])
        return poss

    def is_neighbor(self, coords: tuple):
        try:
            in_list = []
            for w in range(3):
                for z in range(3):
                    in_list.append(self.foucus((coords[0] + w - 1, coords[1] + z - 1)))
            in_list.remove(coords)
            return in_list
        except ValueError:
            return []

    def direct_neighbor(self, coords: tuple):
        try:
            in_list = []
            for x in [(coords[0] - 1, coords[1]), (coords[0] + 1, coords[1]), (coords[0], coords[1] - 1),
                      (coords[0], coords[1] + 1)]:
                in_list.append(self.foucus(x))
            return in_list
        except ValueError:
            return []

    def change_grid(self, change: list, change_to: str, blip: bool = False):
        if change_to not in self.grid_ids and not blip:
            self.grid_ids[change_to] = []
        for x in change:
            x = self.foucus(x)
            self.grid[x[1] - 1][x[0] - 1] = change_to
            if not blip:
                for y in self.grid_ids:
                    if x in self.grid_ids[y]:
                        self.grid_ids[y].remove(x)
                self.grid_ids[change_to].append(x)


