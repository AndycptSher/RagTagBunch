import time, inspect, random


#stuff
#def hey():
#     # print(inspect.getmembers(inspect.currentframe()))
#     print(str(inspect.currentframe()).split(", ")[3][5:-1])
# hey()
# quit()

# pyautogui.click(120, 440)
n = tuple([tuple([1, 2]), 3])
print(type(n))
test = {n: 1}
print(test)
n = ((1, 3), 4)
test[n] = 2
print(test)



def quick_route(gra: dict, start: str, end: str) -> [list, int]:

    # quick exits
    if start == end:
        print([start], 0)
        return [start, end], 0

    if start not in gra:
        print("start not found")
        return ["nowhere"], 0

    if end not in gra:
        print("end not found")
        return ["nowhere"], 0

    # reformatting
    graph = {}
    for x in gra:
        if type(gra[x]) in [list, set, tuple]:
            graph[x] = {}
            for y in gra[x]:
                if y not in gra:
                    continue
                graph[x][y] = 1
        if type(gra[x]) == dict:
            graph[x] = dict(gra[x])
            for y in gra[x]:
                if y not in gra:
                    graph[x].pop(y)

    # waiting list
    waiting = [start]

    # route
    wandered_to = {start: []}

    # how far it is from start
    location_distance = {start: 0}

    # run until every node is explored
    while waiting:
        # removes from waiting list, and adds to focused variable
        location: str = waiting.pop(0)

        # finishes when node is reached
        if location == end:
            return [start] + wandered_to[location], location_distance[location]

        # goes through all connected nodes
        for x in graph[location]:

            # simplification
            distance_from_last: int = graph[location][x]

            # add to the list to be explored
            if x not in waiting and x not in location_distance:

                # optimiser/ sorter for the waiting list
                for y, z in enumerate(waiting):
                    # inserts the path into the correct order
                    if location_distance[z] > location_distance[location]+distance_from_last:
                        waiting.insert(y, x)
                        break
                else:
                    waiting.append(x)
                wandered_to[x]: list = wandered_to[location] + [x]
                location_distance[x]: int = location_distance[location] + distance_from_last
    else:
        print("Destination not found")
        return ["nowhere"], 0


def grid_quick_route(cls, blocked: list, start: tuple, end: tuple, block_look: str = "#", visited: str = ".", tick: int = 0.25) -> None:
    # change the underlying display
    cls.change_grid(blocked, block_look)

    # the value of the square: distance from start, distance from end, total distance
    # could be wrapped up in a class
    visit_distance: dict = {(z + 1, w + 1): [] for w in range(len(cls.grid)) for z in range(len(cls.grid[0]))}

    # the parent square
    paths = {start: ()}

    # where it has been to
    solidified = []

    # quick exits
    if start == end:
        print([start], 0)
        return

    if start not in visit_distance:
        print("start not found")
        return

    if end not in visit_distance:
        print("end not found")
        return

    if end in blocked:
        print("the end is obstructed")
        return

    # waiting list
    waiting_list = [start]

    from math import sqrt

    # a cleaner version of a distance value between two points
    def difference_in_distance(one: tuple, two: tuple):
        one, two = (min(one[0], two[0]), min(one[1], two[1])), (max(one[0], two[0]), max(one[1], two[1]))
        pair = two[0]-one[0], two[1]-one[1]
        return (abs(pair[0]-pair[1]), min(pair))

    # specislised adding method
    def percise_adding(one: tuple, two: tuple):
        return (one[0] + two[0], one[1] + two[1])

    # returns the value
    def value(one: tuple):
        return one[0] + one[1]*sqrt(2)

    # initialise
    visit_distance[start] = [(0, 0), difference_in_distance(start, end),
                             difference_in_distance(start, end)]

    # loop until the waiting list is empty
    while waiting_list:
        time.sleep(tick)

        # loads on the first square on the waiting list
        current = waiting_list.pop(0)

        # if what its looking at is the end, wrap it up
        if current == end:
            break

        # adds the square looked at to the where it has been to list
        solidified.append(current)

        # display change
        cls.change_grid([current], visited)

        # shows which square is beeing looked at
        cls.blip("0", current)

        # looks through what's beside the square
        for x in cls.is_neighbor(current):
            if x in solidified or x in blocked:
                continue

            # if it's not already been to or a wall, look into it
            # how far away it is from the end and the start
            cost = [percise_adding(difference_in_distance(x, current), visit_distance[current][0]),
                    difference_in_distance(x, end),
                    percise_adding(percise_adding(difference_in_distance(x, end), difference_in_distance(x, current)), visit_distance[current][0])]
            # if the neighbor is already in the waiting list and it has a shorter path, go the the next neighbor
            # if not, delete all previous records
            if x in waiting_list:
                if value(visit_distance[x][2]) > value(cost[2]) or value(visit_distance[x][0]) > value(cost[0]):
                    waiting_list.remove(x)
                    paths.pop(x)
                else:
                    continue
            # inserts the square into the correct slot in the waiting list
            for y, z in enumerate(waiting_list):
                try:
                    if value(visit_distance[z][2]) >= value(cost[2]):
                        waiting_list.insert(y, x)
                        visit_distance[x] = cost
                        paths[x] = current
                        break
                except TypeError:
                    waiting_list.insert(y, x)
                    visit_distance[x] = cost
                    paths[x] = current
                    break
            else:
                waiting_list.append(x)
                visit_distance[x] = cost
                paths[x] = current

    path = [""]
    thing = end
    # goes through every parent square starting from end and changes the board accordingly
    while path[0] != start:
        path.insert(0, thing)
        thing = paths[thing]

    path.pop()
    cls.change_grid(path, "O")
    cls.display(" ")
    print("looked through", len(solidified), "squares and the path is", value(visit_distance[end][2]), "squares")



import inspect
def jankey_copy():

    print("hi")
    print(str(inspect.currentframe()).split(", ")[3][5:-1])
    return
    # This class represents a node
    class Node:
        # Initialize the class
        def __init__(self, position: (), parent: ()):
            self.position = position
            self.parent = parent
            self.g = 0  # Distance to start node
            self.h = 0  # Distance to goal node
            self.f = 0  # Total cost

        # Compare nodes
        def __eq__(self, other):
            return self.position == other.position

        # Sort nodes
        def __lt__(self, other):
            return self.f < other.f

        # Print node
        def __repr__(self):
            return ('({0},{1})'.format(self.position, self.f))


    # Draw a grid
    def draw_grid(map, width, height, spacing=2, **kwargs):
        for y in range(height):
            for x in range(width):
                print('%%-%ds' % spacing % draw_tile(map, (x, y), **kwargs), end='')
            print()


    # Draw a tile
    def draw_tile(map, position, **kwargs):
        # Get the map value
        value = map.get(position)
        # Check if we should print the path
        if 'path' in kwargs and position in kwargs['path']: value = '+'
        # Check if we should print start point
        if 'start' in kwargs and position == kwargs['start']: value = '@'
        # Check if we should print the goal point
        if 'goal' in kwargs and position == kwargs['goal']: value = '$'
        # Return a tile value
        return value


    # A* search
    def astar_search(map, start, end):
        # Create lists for open nodes and closed nodes

        open = []
        closed = []

        # Create a start node and an goal node
        start_node = Node(start, None)
        goal_node = Node(end, None)
        # Add the start node
        open.append(start_node)

        # Loop until the open list is empty
        while len(open) > 0:
            # Sort the open list to get the node with the lowest cost first
            open.sort()
            # Get the node with the lowest cost
            current_node = open.pop(0)
            # Add the current node to the closed list
            closed.append(current_node)

            # Check if we have reached the goal, return the path
            if current_node == goal_node:
                path = []
                while current_node != start_node:
                    path.append(current_node.position)
                    current_node = current_node.parent
                # path.append(start)
                # Return reversed path
                return path[::-1]
            # Unzip the current node position
            (x, y) = current_node.position
            # Get neighbors
            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            # Loop neighbors
            for next in neighbors:
                # Get value from map
                map_value = map.get(next)
                # Check if the node is a wall
                if (map_value == '#'):
                    continue
                # Create a neighbor node
                neighbor = Node(next, current_node)
                # Check if the neighbor is in the closed list
                if (neighbor in closed):
                    continue
                # Generate heuristics (Manhattan distance)
                neighbor.g = abs(neighbor.position[0] - start_node.position[0]) + abs(
                    neighbor.position[1] - start_node.position[1])
                neighbor.h = abs(neighbor.position[0] - goal_node.position[0]) + abs(
                    neighbor.position[1] - goal_node.position[1])
                neighbor.f = neighbor.g + neighbor.h
                # Check if neighbor is in open list and if it has a lower f value
                if (add_to_open(open, neighbor) == True):
                    # Everything is green, add neighbor to open list
                    open.append(neighbor)
        # Return None, no path is found
        return None


    # Check if a neighbor should be added to open list
    def add_to_open(open, neighbor):
        for node in open:
            if (neighbor == node and neighbor.f >= node.f):
                return False
        return True

    # The main entry point for this module
    def main():
        # Get a map (grid)
        map = {}
        chars = ['c']
        start = None
        end = None
        width = 0
        height = 0
        # Open a file
        fp = ["#################################################################################",
    "#.#...#....$....#...................#...#.........#.......#.............#.......#",
    "#.#.#.#.###.###.#########.#########.#.#####.#####.#####.#.#.#######.###.#.#####.#",
    "#...#.....#...#.#.........#.#.....#.#...#...#...#.......#.#.#.......#.#.#.#...#.#",
    "#############.#.#.#########.#.###.#.###.#.###.#.#.#######.###.#######.#.#.#.#.#.#",
    "#...........#.#...#.#.....#...#...#...#.#.#.#.#...#...#.......#.......#.#.#.#.#.#",
    "#.#########.#.#####.#.#.#.#.###.#####.#.#.#.#.#####.#.#########.###.###.###.#.#.#",
    "#.#.........#...#...#.#.#.#...#.....#.#.#.#...#.#...#.......#.....#.#...#...#...#",
    "#.#########.#.#.###.#.#.#####.###.#.#.#.#.#.###.#.#########.#####.#.#.###.#####.#",
    "#.#.......#.#.#...#...#.#.....#.#.#.#...#.#.....#.#.....#.#...#...#.......#...#.#",
    "#.#.#####.#.#.###.#####.#.#####.#.#.###.#.#######.###.#.#.###.#.###########.#.#.#",
    "#...#...#.#.#...#.....#.#.......#.#.#...#.....#...#...#.....#.#.#...#...#...#...#",
    "#####.#.#.#.#########.#.#######.#.###.#######.#.###.#########.###.#.#.#.#.#######",
    "#.....#...#.#.........#.......#.#...#.#.#.....#.#.....#.......#...#.#.#.#.#.....#",
    "#.#########.#.#########.###.###.###.#.#.#.###.#.#.###.#.#######.###.#.###.#.###.#",
    "#...#.#.....#...#.....#.#.#...#.#.#.....#...#.#.#...#.#...#...#...#.#.#...#...#.#",
    "###.#.#.#####.#.#.#.###.#.###.#.#.#####.###.###.#####.###.#.#.#.###.#.#.#####.#.#",
    "#...#...#.....#.#.#.#...#...#.....#...#.#...#...........#.#.#...#...#.......#.#.#",
    "#.###.#########.#.#.#.###.#.#####.#.#.###.###.###########.#.#####.#########.###.#",
    "#.#.............#.#.......#.#...#.#.#...#.#...#.#.......#.......#.#...#.....#...#",
    "#.#.#############.#########.#.#.###.###.#.#.###.#.#####.#.#######.#.#.#.#####.#.#",
    "#.#.#...........#.#.#.#.....#.#.....#...#.#.....#...#.#.#.#.#...#.#.#.#.#.....#.#",
    "#.###.#########.#.#.#.#######.#######.###.#####.###.#.#.#.#.###.#.#.#.#.#####.#.#",
    "#.....#...#.....#...#.........#.....#...#.....#...#...#.#.....#.#...#.#.#.....#.#",
    "#.#####.#.#.#######.###########.#######.#.#######.###.#.###.###.#####.#.#.#####.#",
    "#.....#.#.#...#...#.#.......#.........#.#...#.......#.#.#...#...#.....#.#.#...#.#",
    "#######.#.###.#.###.#.#####.#.#####.###.#.#.#.#######.#.#####.###.#####.#.###.#.#",
    "#.......#.#...#.....#.#...#.#...#.#.....#.#.#.#.#.....#...#...#...#.....#...#.#.#",
    "#.#######.#.#.#####.#.###.#.###.#.#######.#.#.#.#.#######.#.###.#.###.#####.#.#.#",
    "#.#.#.....#.#.#...#.#...#.#...#...#.#...#.#...#.#.....#.#...#...#...#.......#...#",
    "#.#.#.#####.#.#.#.#####.#.###.###.#.#.#.#.#####.#####.#.#####.#####.#########.###",
    "#.#...#.....#.#.#.#...#...#.#.#...#...#.#.#...#.....#...#.#...#...#.....#...#.#.#",
    "#.###.###.#.###.#.#.#.###.#.#.#.#######.#.#.#.#####.###.#.#.###.#.#####.###.#.#.#",
    "#...#...#.#.#...#.#.#...#.#.#.#.#.......#...#.........#.#...#...#.#...#...#.#...#",
    "#.#.###.#.#.#.###.#.###.#.#.#.#.###.###.###########.###.#.###.###.###.###.#.###.#",
    "#.#...#.#.#.#...#...#...#.#.#.#.....#...#...#.....#.#...#.....#.....#.#...#...#.#",
    "#.###.#.#.#####.#####.#.#.#.#.#######.###.#.#####.#.#.#############.#.#.###.#.#.#",
    "#...#.#...#...#.....#.#.#.#.#.#...#...#.#.#.......#.#.#...#...#...#...#.#.#.#...#",
    "###.#.#####.#.#####.#.###.#.#.#.#.#.###.#.#########.#.#.#.#.#.#.#.#####.#.#.#####",
    "#...#.......#.......#.......#...#.......@...........#...#...#...#.......#.......#",
    "#################################################################################"]

        # map is a dictionary with all coordinates as a key and
        # every coordinate has a corresponding value from the list
        # start and end is also found here

        # creator of code is complete idiot
        # following is an infinite loop that goes nowhere

        # Loop until there is no more lines
        for _ in range(len(chars)):
            # Get chars in a line
            chars = fp
            # Calculate the width
            width = len(chars) if width == 0 else width
            # Add chars to map
            for x in range(len(chars)):
                map[(x, height)] = chars[x]
                if (chars[x] == '@'):
                    start = (x, height)
                elif (chars[x] == '$'):
                    end = (x, height)

            # Increase the height of the map
            height += 1
        print("hi")
        print(map)

        quit()

        # Find the closest path from start(@) to end($)
        path = astar_search(map, start, end)
        print()
        print(path)
        print()
        draw_grid(map, width, height, spacing=1, path=path, start=start, goal=end)
        print()
        print('Steps to goal: {0}'.format(len(path)))
        print()
    print("hi")
    main()
    # Tell python to run main method
    if __name__ == "__main__":
        main()

# jankey_copy()
# quit()
# jankey_copy()


from Grids import Grid, InfiniGrid


def Game_of_Life(x_di, y_di):
    m = Grid(x_di, y_di, " ")
    n = Grid(x_di, x_di, " ")
    m[[(random.randrange(1, x_di), random.randrange(1, y_di)) for _ in range(int(x_di*y_di/2))]] = "+"
    print(m, sep="")
    for _ in range(1000):
        for l in m.__dict__():
            # m.blip("+", x)
            neighbors = len([x for x in m.is_neighbor(l) if m.grid_value(x) == "+"])
            print(neighbors)
            # time.sleep(2)
            if m[l] != "+" and neighbors == 3:
                n[l] = "+"
            if m[l] != "+":
                continue
            if neighbors in [2, 3]:
                n[l] = "+"
            else:
                n[l] = " "

        print(n)
        m = n.copy()
        n = Grid(x_di, y_di, " ")
        print(m)
        time.sleep(2)


#Game_of_Life(30, 20)
#quit()
from Minesweeper import Minesweeper


"""
n = Minesweeper(25, 25, 110)
n.startupcheck()
n.step_by_step()
Grid.multi_display([n.b.grid, n.a.grid])

quit()
"""

grid = \
    ["""
0 0 X X X 0 X X X 0 0 0 X 0 0 0 0 X 0 0 0 0 0 X
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 X 0 0 0 0 X 0 X X
0 0 0 0 0 X 0 0 0 X 0 0 X 0 0 0 0 X 0 0 0 0 0 0
0 0 0 0 0 0 0 X X 0 0 0 0 0 0 0 X 0 0 0 0 0 0 0
X 0 0 X X 0 0 X 0 0 0 0 0 0 0 X X 0 0 0 0 0 0 0
0 0 0 0 0 X 0 0 0 X 0 0 0 0 0 0 0 0 0 0 0 0 0 0
X 0 X 0 0 0 0 0 0 0 X 0 0 0 0 0 0 0 0 0 0 0 0 0
X 0 0 0 0 0 0 0 X 0 0 X 0 0 0 X 0 0 0 0 X 0 0 0
X 0 X 0 X 0 0 0 0 0 0 0 0 0 0 X 0 0 0 0 X 0 0 0
0 0 0 X 0 0 0 0 X 0 0 0 0 0 0 0 0 X X 0 0 X 0 0
0 0 0 0 X X 0 0 0 X 0 0 0 0 0 0 X 0 0 0 0 0 0 0
0 X 0 0 X X 0 0 X 0 X 0 0 0 0 X 0 0 0 X 0 0 0 0
0 0 0 X 0 0 0 0 0 X X 0 0 0 0 0 X 0 0 0 0 0 0 0
X X 0 0 0 0 0 X 0 0 0 0 0 X X 0 0 X 0 0 X 0 0 X
0 X 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 X 0 0 0 0 0
0 0 X 0 0 0 X 0 0 0 X 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 X 0 0 0 0 X 0 0 0 0 0 0 0 0 X 0 0 0 X 0 0 0
0 0 0 X 0 0 0 0 0 0 X 0 0 0 0 0 0 X X 0 X 0 X 0
0 0 0 0 X X 0 0 0 X 0 0 X 0 0 0 0 X 0 0 X 0 0 0
X X 0 X 0 0 0 0 0 X 0 0 0 0 0 0 0 0 0 X 0 0 0 0
""",
"""
00000XX0000X00X000000X00
0000000XX0X0000000X00X0X
X00X000000X000000000X000
0000X0000X000000X000000X
X000X000XXX0X000000X000X
X0X0000000000X000000X000
XX0000X0000X000X00000000
X000000X00000000X00XXX00
0X00000000X0000X000X000X
00000X0XX00000X0X0000X00
0X00X000000000000X000000
0000000XX0000000X00000XX
000000000X000X00000000XX
00X0X0X000X00000XX0X000X
00000000000000000000X000
00X000000000X00XX00X0000
00X0X0000000X000X00X0XX0
000000000000000XX0000000
XXX00XX000000000000000XX
000000000000X00X000XX000
""",
"""
00X0000000X0X00000XX0000
000000X00X0000X000X00000
00X00000X00000XXXX000X00
000000X0000X0X0X00X0X0X0
0000000X000000X000000000
XXX000X0000XX0000XX000XX
00X0000000X0000000000000
0X00X000X0000000X000000X
XX00000000000X0X000X0000
0000XX00X000000X0X00XX00
00000X00X00000000X0000X0
0X0000000X00000X0000X000
000X0X000000000X000000X0
X0X0000X0XX000X00X000000
0000000X000000000XX00000
X000X0X0000XX000000X0XX0
X000X00000000000X0000000
X0000XX00XX00000000000X0
000000000X000000000X0000
X00000000X0000X000000X00
""",
"""
0000X00X00000X0X0000X000
X0000000X000XX000000000X
0000XX00000X00X000000000
00XX00000XXX000XX000XX00
00X000000XXXX0000000X000
00XXX00X000000000000X000
000X000000X0X00000000000
000000000X0000XX000X0000
0X000000X0000000000000X0
000X00X0X000000X0X000000
0000X0X00000000000000XX0
X00X0X00000000000X00000X
000000X0000000000000X0X0
X000000000X000000000X0X0
XX0000XX0X000X000X0X0X00
0X0X000X0XX0000XX000X0X0
00X000X000X0000000X00000
000000000000X00000000000
00X0X000000X00X0X0X00000
000000X0X00X00000X00X000
""",
"""
0X00000000000000000X00X0
000000X00X0XXX000X0X00X0
00000X0000X000X00000X000
0X0X000000X0000X0XX0XXX0
00000X0000000000X0000000
000X0000X00X000X0X0X00XX
000X000XX000X00X000X0XXX
X000X0XX0X00000000X00000
0X0000X00000X0000X000000
0000000XX0000X000000X000
0X0000X000000000000000X0
X00000X00000000000000X00
0X0000000X00X000X0000000
00000000000000000X0X0X00
0000X0000XX000000X0X0000
0000000X0XXX00X000000X00
X000000000000X000000X000
0X00X0000X0X00X000XX0XX0
0000000X0000000000X00000
00000XX00000000000000XX0
""",
"""
0000XXX0XXXXXX0X00000000
00000000XX0000000000X0XX
000000000XX0X0X0X000X000
000000XX0000000000000000
XX0X000XXX0X00X00000000X
00000000X000X000X0X0X000
X000000000X0X000XX000000
00X0000X000X0XX0000XX000
0000X000000000X00X000000
0X000X0000000000000X000X
00000000000000XX00000000
000000X0XX0000X000000X00
00000X0000000XX0000000XX
0000X00X0000000000X000X0
000X000000XX00000X000000
00000XXXX0X0000000X00X00
000X0000000000000X00000X
000X0000000XX00000000X00
000XX0000000XX00X0X00000
0X00000X000000000000000X
""",
"""
999999X999999X999999X9X9
00XX0X0X00X0000000000X00
00000000X0000X00X000000X
00X0X000X00X000X000X0X00
00000X0000X00X0X00000X00
000X000000000000X0XX0000
000X000000XX000X00X000X0
00000X0X0X000000X0X00000
0000X0X0000000X0X00000XX
X0X00000XX000X000X0X0XX0
000X0X0000000000000000X0
00000000000000XXXX000000
00X00X000X000XX0X0000X00
00X000000000X000000000X0
00000000000000000X00000X
00000000X000000000000000
00000X00X0X0XX00000000X0
0X0000X00000X00X0X0X000X
0000000X0000X0X000000000
00X0000X000000XXX0X00X00
""",
"""
000X0000X000000X00X00000
000X00000000000000000000
0X000X000X00000X00X00X00
X000X000000000000000000X
0X000000X00XX0000X000000
00000000X00000000000XXX0
00000X0X000000XX0X000X00
0000000X000X00000000000X
0000000000000X00000000XX
000XXX00000000X0X000000X
000XXX0X000000000X000000
X0XX0000XX0000000X000X00
000X000XX00000X0X000000X
X000000000000000000X0X00
0X0X0X0000XXX00000000000
XX00000000X000000X00XXXX
X00X0XX0000XX0X000000X00
000000X0X0XX00X0000X00X0
X000000000000X0000000000
0X00XXX0X00000X000000000
""",
"""
000000X0X0X00000X00X0000
00XX000X00000000000X0000
X0X0X0X000XX00XXX0000X00
0000XXX00X000000X00X00X0
00X0X00X000000X000000000
X0000X000X0X00X0X000X000
0000X0000000000X000X0000
0000000000000000000000X0
0X000XX0000000000X0X000X
0000X000X0000000000000X0
00X0XX0000000X0X0XX00000
0000X0X00000X00000000000
000X00000X000X0000000XX0
0000000XX0000000000000X0
X000X0X00X00XXX000X000X0
00000000X0000X0000X00000
X000X000000000X00000XX00
000X00000X00000000000000
X0X0X00000000XX0XXXX0000
""",
"""
000X00X000000X000X0X00X0
0000000000X00000000000X0
00X000000X00000X000X00X0
0X0X0X00X000XX0000000000
000X00000X0X00X00X0000X0
0X00000000000000X000000X
0X0X0000X000000X0X000X00
0000000000000X0000X0X0X0
X000000000000X00XX000000
X0000000000000000X000000
000000000000X00X0X00X0X0
00XXX0X0000X00000XX00X00
0000X0X0X0XX000000X00X00
X000X0000000000000000X00
0000XXXXX00000XX0000X000
000X0X0000000000X0000000
0X00X00000XX000X0X000XXX
000000000X0X000X00000000
00X000X00000000000000X0X
00X0X000X0X0X00000000000
""",
"""
0000000000XX00000X000X00
00000000000X0X00XX00X000
X00XXX000X000X0000X00X00
0X000000000000000000XX00
000X0000000XX0X0000X0000
000000000X00000XX0000000
0X000X0000000X0X000X0000
00000X000000000X000XX000
000X000000000000XX000000
00000X000X000000000000XX
00000X000000000XX0X0X000
00X00XX0XX0000X000000000
X00000XXX00000000XX0X000
00000X0000X0000000X0000X
X00XX00XXX00000000X00000
0X00000X0000000000000X00
0000X0000XXX000000000000
XX0X0X00000XXX00X0000000
0000X000000X00XX0000X000
000X00X0X0000X0000000XX0
""",
"""
0X0X000X0000X0000X000000
00000XX0000X0000000XXXX0
XX0000000XX000X0000X00X0
0X000000X0XXXX0X000X00X0
0000000000000000XX000X00
00000000X000X00000000X00
0000000000X000X000X0X000
000X0000X00X00X00X000000
X000000XX00X0X00000X0000
000X000XX000000X00000000
00000000XX00000000X00X00
X000X00X0000000X0000XX00
0000X00000000X000X0XX000
00000XX000X0000XX0000000
00000000XX000X000XX00000
000X00000000X00XX0000000
0000000000000XX00000XX00
X000000X0000000X00X0X000
00X000X00000000000000000
00000X00000X0X00000XX0X0
""",
"""
0XX00X0X0000000000000000
00000000000X00000XX00000
00XX000X0XXX000000X00000
000X00000X0X00X0X00X0000
0X000000X0000000X0X00000
0X000000X000X0000X0000XX
000X0000X000000000000000
000X0X0000X00000XXX00X00
00000X00X0000X0000X0000X
0X0000X00X00000000X0000X
000000X0X0000000XX0X0000
000000000000000XX00X0X0X
X0XX0X00000000X0000X0000
00000X000XX0X0X000X0000X
0000000000000000X00X0000
0X0X000X00X000X00X000X00
0000X000000X0X00X00000XX
00000X00X0000000000000XX
000000XX00000X0XX0000X00
X00000000000000X00000000
""",
"""
X0000000X00X00X00X000000
0000X0XXX000000XXX00XX00
00X000X000000000000X0000
0000000XX0X00X0000000000
0000000X0X0000000X0X0000
0X000000X0X000X0000000X0
00000X000X00000000X00XX0
0000000000X0000000000X0X
0XX00X0X00000000XXX0000X
0XX0000XXX00000XX0000000
X00X00000X0000X0XX000000
0000X000000000000000X000
00XX000000XX0XX00X000000
0X0000X0X0X000000000000X
0X000000X000X000X00XX000
X000000X0000000000000000
00000000000X00000X00XX00
00X000000000XX0000000000
XXX00000000000000X0X0XX0
""",
"""
000X00XX0XX0XX00X0000000
00000000XX0X00X00000000X
000X0X0000XX000000000000
0000XX0000000000X0000XXX
000X0X000XX0000X0000000X
000X0X00X0000000000X0000
000X0000X00XX0000XX00000
9999999999X999X99X99XX99
000X0X000000000000000X0X
X0X0XX000000000000XX0000
X00000000X0000XX00000000
0X0000000X0X00X000X00000
000X0XXXXX0000000X000X0X
00000000X00X0XX00X00000X
00000000000X000X000XX000
000X000X000X0000X00X0X0X
0000000000000000X0000X00
000X00000000000000X0000X
0000000000X0000000000000
""",
"""
0X0000X000000X0XX00000X0
0000000000000000X0000X00
000000000000X0000X000000
XX0X00000000X00X00X00000
0XX000X0000X0000000X00XX
X000X000000XX0000000X0X0
000XXX000000000000000000
X000000XX000X0000X000000
0XX0000000000000X0000X0X
000XX00000X000000X0XXX0X
000X000000000X00000X0000
000X0X000000000000000X0X
X00000X00000000XX0000000
00X00X000000XX0000000000
00000000X00X000000X00000
00000X00000000X0X00X00X0
0000X0000XX0000000X00000
X0X00X0000XX0X0000X000X0
X0X000X00X00000X00X00000
000X0XX000X00X000X00X0X0
""",
"""
0X0000X0X00X00000XX00X00
XX000X00000000000X000000
X0X000X000XX000000X00X00
X0000X0XX0000X00000X000X
000000X0X0000X0000000000
000X000000XX00000X00X0X0
X0X000000000000000XX00X0
000X0000X000000000000X00
0XX0X000000000X000X00000
000X00XX000000X00000X000
00000000000000000X00X000
0X000XX000X000000000X000
000000X0000X0000X000X0X0
000000X0000000X0000X0000
X000000000X000000X0000XX
X00000000XX0000000X000X0
0X0X0000000000000X000000
X00X000000XX000000X0X00X
000XXX00X000000XX000000X
000X0000000X0XX00000000X
""",
"""
00X000000XX0000X00X00000
0000X000XX00000000000X0X
X0000000X0000X00X000000X
000000XX0000000000X0000X
00000XX0X000XXX00XX00X00
0000000000000X0X0000X000
00000X000000000X000X0X00
0X00X0X00X0XX0000X00XX00
0000000000X00000000000X0
000000000000000000000XXX
0XX000X00000000000000X00
0000X0000X0000XX0000000X
X0X0000000000X0X0X000000
X0000X0X0000XXX00000000X
X0000000000000000X000000
0X00X0X00X0X00000X000000
X000X00X000X0000000000XX
0X00000X0000X0000X00000X
000000X0000000XXX000X000
0000X000000XX000000X0X00
""",
"""
000000000X000000000X0X00
X0X00000X00X00000X000000
0000000X00000000X000000X
X0X000000X000000XX0X00X0
0X0000X00X000XX000000XX0
000000XX0000000X00000XXX
0X000000000000000X0000X0
XXXX0XX000000000000X0000
00000000XXX000X000XXX00X
X000X00000000000X0000000
0000XX000000000000000000
0X0X00X000000000000000X0
00000XX0000X00X0000X0000
0X0X00X0000X000000000000
0X000000000XXX00X00000X0
000000X000X0X0000X00X000
00000000X00000XX00000XX0
X0000000X0X00X00X000X000
00000X000X0000X0000X0X00
XX00000X000000X000000X00
"""
     ]
m = Grid(1, 1)
# grid 8 is unsolvable
# grid 11 has interesting text show up
mines, = m.convert_strlis(24, 20, grid[14], "X", ignore=[" "])
m.display()
info = m.info()
print(*[(x, info[x]) for x in info])
n = Minesweeper(24, 20, 99, True, mines)
n.startupcheck()
front, back , result = n.ai(100, True)
n.b.display()
Grid.multi_display([front, back])
if result:
    print("solved")
else:
    print("unsolved")
#quit()


#quit()
def multi_display(grids: list, separators: str = " ") -> None:
    for x in range(len(grids[0])):
        row = ""
        for y in grids:
            row += str(separators).join(y[len(y)-x-1]) + " | "
        print(row)


trouble_list = []
for l in range(2):
    n = Minesweeper(24, 20, 99)
    n.startupcheck()
    vis, back, res = n.ai(18, False)
    trouble_list.append((vis, back, res))
    print("\n" * l)
    print(l)

m = Grid(1, 1)
print(len(trouble_list), "len of trouble list")
print("display")
m.multi_display([x[0] for x in trouble_list])
print("backend")
m.multi_display([x[1] for x in trouble_list])
print()
"""
for n, l in enumerate(trouble_list):
    m.grid = list(l[0])
    m.display()
    print(F"({n}/{len(trouble_list)})")
    inp = input("next")
    while inp != "":
        if inp == "re":
            minesweeper_ai(24, 20, 99,False, True, True, l[2], l[1])
        elif inp == "back":
            m.grid = list(l[1])
            m.display()
        inp = input("next?")
"""
n = 0
while n < len(trouble_list):
    m.grid = list(trouble_list[n][0])
    m.display()
    if trouble_list[n][2]:
        print("solved")
    else:
        print("unsolved")
    print(f"({n+1}/{len(trouble_list)})")
    inp = " "
    while inp != "next":
        if "skip" in inp:
            n = len(trouble_list)
            break
        if "re" in inp:
            o = Minesweeper(24, 20, 99, True, [], trouble_list[n][2], trouble_list[n][1])
            o.startupcheck()
            vis, *_ = o.ai(15)
            m.grid = vis
            m.display()
        elif inp == "ans":
            m.grid = list(trouble_list[n][1])
            m.display()
        elif "fr" in inp:
            m.grid = list(trouble_list[n][0])
            m.display()
        elif inp == "both":
            m.multi_display(trouble_list[n][:2])
        elif inp == "back":
            n -= 1
        inp = input("next? (redo, front, ans, both, next, back)")
    n += 1





#quit()
fp = """#################################################################################
    #.#...#....$....#...................#...#.........#.......#.............#.......#
    #.#.#.#.###.###.#########.#########.#.#####.#####.#####.#.#.#######.###.#.#####.#
    #...#.....#...#.#.........#.#.....#.#...#...#...#.......#.#.#.......#.#.#.#...#.#
    #############.#.#.#########.#.###.#.###.#.###.#.#.#######.###.#######.#.#.#.#.#.#
    #...........#.#...#.#.....#...#...#...#.#.#.#.#...#...#.......#.......#.#.#.#.#.#
    #.#########.#.#####.#.#.#.#.###.#####.#.#.#.#.#####.#.#########.###.###.###.#.#.#
    #.#.........#...#...#.#.#.#...#.....#.#.#.#...#.#...#.......#.....#.#...#...#...#
    #.#########.#.#.###.#.#.#####.###.#.#.#.#.#.###.#.#########.#####.#.#.###.#####.#
    #.#.......#.#.#...#...#.#.....#.#.#.#...#.#.....#.#.....#.#...#...#.......#...#.#
    #.#.#####.#.#.###.#####.#.#####.#.#.###.#.#######.###.#.#.###.#.###########.#.#.#
    #...#...#.#.#...#.....#.#.......#.#.#...#.....#...#...#.....#.#.#...#...#...#...#
    #####.#.#.#.#########.#.#######.#.###.#######.#.###.#########.###.#.#.#.#.#######
    #.....#...#.#.........#.......#.#...#.#.#.....#.#.....#.......#...#.#.#.#.#.....#
    #.#########.#.#########.###.###.###.#.#.#.###.#.#.###.#.#######.###.#.###.#.###.#
    #...#.#.....#...#.....#.#.#...#.#.#.....#...#.#.#...#.#...#...#...#.#.#...#...#.#
    ###.#.#.#####.#.#.#.###.#.###.#.#.#####.###.###.#####.###.#.#.#.###.#.#.#####.#.#
    #...#...#.....#.#.#.#...#...#.....#...#.#...#...........#.#.#...#...#.......#.#.#
    #.###.#########.#.#.#.###.#.#####.#.#.###.###.###########.#.#####.#########.###.#
    #.#.............#.#.......#.#...#.#.#...#.#...#.#.......#.......#.#...#.....#...#
    #.#.#############.#########.#.#.###.###.#.#.###.#.#####.#.#######.#.#.#.#####.#.#
    #.#.#...........#.#.#.#.....#.#.....#...#.#.....#...#.#.#.#.#...#.#.#.#.#.....#.#
    #.###.#########.#.#.#.#######.#######.###.#####.###.#.#.#.#.###.#.#.#.#.#####.#.#
    #.....#...#.....#...#.........#.....#...#.....#...#...#.#.....#.#...#.#.#.....#.#
    #.#####.#.#.#######.###########.#######.#.#######.###.#.###.###.#####.#.#.#####.#
    #.....#.#.#...#...#.#.......#.........#.#...#.......#.#.#...#...#.....#.#.#...#.#
    #######.#.###.#.###.#.#####.#.#####.###.#.#.#.#######.#.#####.###.#####.#.###.#.#
    #.......#.#...#.....#.#...#.#...#.#.....#.#.#.#.#.....#...#...#...#.....#...#.#.#
    #.#######.#.#.#####.#.###.#.###.#.#######.#.#.#.#.#######.#.###.#.###.#####.#.#.#
    #.#.#.....#.#.#...#.#...#.#...#...#.#...#.#...#.#.....#.#...#...#...#.......#...#
    #.#.#.#####.#.#.#.#####.#.###.###.#.#.#.#.#####.#####.#.#####.#####.#########.###
    #.#...#.....#.#.#.#...#...#.#.#...#...#.#.#...#.....#...#.#...#...#.....#...#.#.#
    #.###.###.#.###.#.#.#.###.#.#.#.#######.#.#.#.#####.###.#.#.###.#.#####.###.#.#.#
    #...#...#.#.#...#.#.#...#.#.#.#.#.......#...#.........#.#...#...#.#...#...#.#...#
    #.#.###.#.#.#.###.#.###.#.#.#.#.###.###.###########.###.#.###.###.###.###.#.###.#
    #.#...#.#.#.#...#...#...#.#.#.#.....#...#...#.....#.#...#.....#.....#.#...#...#.#
    #.###.#.#.#####.#####.#.#.#.#.#######.###.#.#####.#.#.#############.#.#.###.#.#.#
    #...#.#...#...#.....#.#.#.#.#.#...#...#.#.#.......#.#.#...#...#...#...#.#.#.#...#
    ###.#.#####.#.#####.#.###.#.#.#.#.#.###.#.#########.#.#.#.#.#.#.#.#####.#.#.#####
    #...#.......#.......#.......#...#.......@...........#...#...#...#.......#.......#
    #################################################################################"""

d = Grid(1, 1)
block, start, end = d.convert_strlis(81,41,fp,[ "#", "@", "$"] ,ignore=[" "])
start, = start
end, = end
print(d.grid, "hey")
time.sleep(2)
d.change_grid(block, "#")
#grid_quick_route(d, block, start, end)

#c.change_grid([(4, 3), (5, 3), (5, 2)], "+")

c = Grid(41, 24, " ")
print(c.grid)
grid_quick_route(c, c.block_create(
    (4, 20), (24, 20))+c.block_create(
    (7, 18), (7, 8))+c.block_create(
    (10, 13), (29, 13))+c.block_create(
    (16, 5), (27, 5))+c.block_create(
    (19, 22), (40, 22))+c.block_create(
    (32, 8), (32, 18)), (15, 2), (19, 23), "#", ".", 0.5)

graph = {'a': ['b'],
       'b': {'a', 'c'},
       'c': {'f': 2, 'd': 2},
       'd': ('f', 'e'),
       'e': 'f',
       "f": {"d"}
        }
a, b = quick_route(graph, "a", "e")
print("from \"" + "\" to \"".join(a) + "\" in", b, "steps")
if __name__ == '__main__':
    pass
