from Grids import Grid, InfiniGrid
import pygame, random, os
pygame.init()


class Snake:
    # split off the functions of the snake
    def __init__(self, x, y, speed: float = 1, snake_start_len: int = 5, apple_sprite="A", snake_body_sprite="s",
                 background_sprite=" ", safe: bool=False):
        self.apple_sprite, self.snake_sprite, self.background_sprite = apple_sprite, snake_body_sprite, background_sprite

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

        if x < 10 or y < 10:
            print("suggested board too small")
            return

        self.x, self.y = x, y

        if not safe:
            self.board = Grid(x, y, background_sprite)
        else:
            self.board = InfiniGrid(x, y, background_sprite)

        self.boarder = [(x, y) for x in range(self.x + 1) for y in range(self.y + 1) if
                        x == self.x or x == 1 or y == self.y or y == 1]
        self.board[self.boarder] = "#"

        center = (int(x/2), int(y/2))
        self.snake = [Grid.coord_adjust(center, x=x) for x in range(snake_start_len)]



        # apple spawn
        self.spawn_apple()

        tick_per_block = int(2000/speed)  # iterations per tile/square
        # average 110000 iterations per second
        # game loop
        tick = 0
        direction = "W"
        self.direction = str(direction)
        direction_actual = {
            "N": {"y": 1},
            "E": {"x": 1},
            "S": {"y": -1},
            "W": {"x": -1}
        }
        while True:
            if get_key("LEFT") and self.direction != "E":
                direction = "W"
            elif get_key("UP") and self.direction != "S":
                direction = "N"
            elif get_key("RIGHT") and self.direction != "W":
                direction = "E"
            elif get_key("DOWN") and self.direction != "N":
                direction = "S"
            elif get_key("ESCAPE"):
                break

            # check for player input, change direction in response
            tick += 1
            if tick % tick_per_block == tick_per_block - 1:
                print("\n"*30)
                print(len(self.snake) - snake_start_len, ": score")
                self.board.display()
            if tick % tick_per_block == 0:
                self.direction = str(direction)

                # destroys snake
                self.board[self.snake] = background_sprite

                # coord of the block in front of the head

                block_ahead = Grid.coord_adjust(self.snake[0], **direction_actual[direction])
                if safe:
                    block_ahead = self.board.foucus(block_ahead, x_start=2, x_end=self.board.x-1, y_start=2,
                                                    y_end=self.board.y-1)
                print(self.board[block_ahead])
                # if the snake hits a apple
                if self.board[block_ahead] == apple_sprite:
                    self.board[block_ahead] = background_sprite

                    self.snake.insert(0, block_ahead)
                    self.spawn_apple()
                # if the snake head hits the wall or itself
                elif not safe and (self.board[block_ahead] == "#" or block_ahead in self.snake):
                    print("Game over")
                    break
                elif safe and len(self.snake) > len(self.board)/2:
                    print("you've had enough, stop")
                    break

                # if nothing happens
                else:

                    self.snake.insert(0, block_ahead)
                    self.snake.pop()

                # recreate snake
                self.board[self.snake] = snake_body_sprite
                for x in self.snake:
                    appearance = self.snake.count(x)
                    self.board[x] = appearance % 10

                # snake head sprite
                if [y for x in self.board.is_neighbor(self.snake[0])
                        for y in self.board.is_neighbor(x) if safe and self.board[self.board.foucus(y)] == apple_sprite]:
                    self.board[self.snake[0]] = "O"
                else:
                    self.board[self.snake[0]] = "H"

    def spawn_apple(self):
        random_coord = (random.randrange(1, self.x), random.randrange(1, self.y))
        while self.board[random_coord] != self.background_sprite or random_coord in self.snake:
            random_coord = (random.randrange(1, self.x), random.randrange(1, self.y))
        self.board[random_coord] = self.apple_sprite


if __name__ == "__main__":
    n = Snake(x=24, y=21, speed=1, snake_start_len=5, safe=True)
