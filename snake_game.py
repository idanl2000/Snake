from typing import Optional
from game_display import GameDisplay
from snake import *
import math

UP = "Up"
DOWN = "Down"
LEFT = "Left"
RIGHT = "Right"


class SnakeGame:
    """
    Represents the Snake game, managing the game state, snake movements,
    interactions with walls and apples, and rendering the board.
    """

    def __init__(self, length, hight, wall_list: list, apple_list: list, is_debug) -> None:
        """
        Initializes the Snake game.

        Args:
            length (int): Width of the game board.
            hight (int): Height of the game board.
            wall_list (list): List of walls to be placed on the board.
            apple_list (list): List of apples to be placed on the board.
            is_debug (bool): Flag indicating whether to start the game in debug mode.
        """
        if is_debug:
            self.__snake = Snake(-1, -1)
        else:
            self.__snake = Snake(length // 2, hight // 2)
        self.__length = length
        self.__hight = hight
        self.__wall_list = wall_list
        self.__apple_list = apple_list
        self.__active_wall_list = []
        self.__active_apple_list = []
        self.__key_clicked = None
        self.__move_wall = False
        self.__score = 0

    def add_objects(self):
        """
        Adds walls and apples to the game board.
        """
        self.add_wall()
        self.add_apple()

    def get_wall_list(self):
        """
        Returns the list of walls for possible modification.

        Returns:
            list: The wall list.
        """
        return self.__wall_list

    def get_apple_list(self):
        """
        Returns the list of apples for possible modification.

        Returns:
            list: The apple list.
        """
        return self.__apple_list

    def read_key(self, key_clicked: Optional[str]) -> None:
        """
        Reads the key input for snake movement.

        Args:
            key_clicked (str): The direction key pressed by the user.
        """
        self.__key_clicked = key_clicked

    def update_objects(self) -> None:
        """
        Updates all objects on the game board in a single turn.
        This includes moving the snake, moving walls, checking interactions,
        and adding new walls and apples.
        """
        # Move the objects
        self.move_snake()
        self.move_wall()
        # Check interactions
        self.snake_eat()
        self.wall_eat_snake()
        self.wall_eat_apple()
        # Add new objects to the board
        self.add_wall()
        self.wall_out()
        self.add_apple()

    def wall_eat_snake(self):
        """
        Checks if any wall intersects with the snake, causing the snake to die
        or be cut if it touches a wall's edge.
        """
        for wall in self.__active_wall_list:
            if self.__snake.get_x_y() in wall.get_wall_body():
                self.__snake.kill()
            elif wall.get_wall_edge() in self.__snake.get_snake_body():
                self.__snake.cut(wall.get_wall_edge())

    def snake_eat(self):
        """
        Checks if the snake eats an apple and increases the score.
        """
        for index, apple in enumerate(self.__active_apple_list):
            if self.__snake.get_x_y() == apple.get_location():
                self.__score += int(math.sqrt(self.__snake.get_length()))
                self.__snake.eat()
                self.__apple_list.append(self.__active_apple_list.pop(index))

    def wall_eat_apple(self):
        """
        Checks if any wall intersects with an apple, causing the apple to be eaten by the wall.
        """
        for wall in self.__active_wall_list:
            loc = wall.get_wall_edge()
            for index, apple in enumerate(self.__active_apple_list):
                if loc == apple.get_location():
                    self.__apple_list.append(self.__active_apple_list.pop(index))

    def move_wall(self):
        """
        Moves all walls on the board by one step.
        """
        if self.__move_wall:
            for index, wall in enumerate(self.__active_wall_list):
                wall.move_wall()
            self.__move_wall = False
        else:
            self.__move_wall = True

    def wall_out(self):
        """
        Checks if any walls are out of the board's bounds and moves them back to the wall list.
        """
        for index, wall in enumerate(self.__active_wall_list):
            if wall.is_wall_out(self.__length, self.__hight):
                self.__wall_list.append(self.__active_wall_list.pop(index))

    def move_snake(self):
        """
        Moves the snake in the specified direction based on the key input.
        """
        snake_x, snake_y = self.__snake.get_x_y()
        if (self.__key_clicked == LEFT) and (snake_x > 0):
            self.__snake.set_direction(LEFT)
            if not self.__snake.move():
                self.__snake.kill()
        elif (self.__key_clicked == RIGHT) and (snake_x < self.__length - 1):
            self.__snake.set_direction(RIGHT)
            if not self.__snake.move():
                self.__snake.kill()
        elif (self.__key_clicked == UP) and (snake_y < self.__hight - 1):
            self.__snake.set_direction(UP)
            if not self.__snake.move():
                self.__snake.kill()
        elif (self.__key_clicked == DOWN) and (snake_y > 0):
            self.__snake.set_direction(DOWN)
            if not self.__snake.move():
                self.__snake.kill()
        elif (0 < snake_x) and (snake_x < self.__length - 1) and (0 < snake_y) and (snake_y < self.__hight - 1):
            if not self.__snake.move():
                self.__snake.kill()
        elif snake_x == 0 or snake_y == 0 or snake_x == self.__length - 1 or snake_y == self.__hight - 1:
            self.move_snake_edge(snake_x, snake_y)

    def move_snake_edge(self, snake_x, snake_y):
        """
        Handles the snake's movement when it is on the edge of the board.
        """
        if self.__key_clicked:
            self.__snake.set_direction(self.__key_clicked)
        if snake_x == 0 and self.__snake.get_direction() == LEFT:
            self.__snake.kill()
        elif snake_x == self.__length - 1 and self.__snake.get_direction() == RIGHT:
            self.__snake.kill()
        elif snake_y == 0 and self.__snake.get_direction() == DOWN:
            self.__snake.kill()
        elif snake_y == self.__hight - 1 and self.__snake.get_direction() == UP:
            self.__snake.kill()
        else:
            self.__snake.move()

    def add_wall(self):
        """
        Adds a wall to the active wall list if a wall is available and the location is valid.
        """
        add = True
        if self.__wall_list:
            for loc in self.__wall_list[0].get_wall_body():
                if not self.valid_loc(loc):
                    add = False
            if add:
                self.__active_wall_list.append(self.__wall_list.pop(0))

    def add_apple(self):
        """
        Adds an apple to the active apple list if an apple is available and the location is valid.
        """
        if self.__apple_list:
            if self.valid_loc(self.__apple_list[0].get_location()):
                self.__active_apple_list.append(self.__apple_list.pop(0))

    def valid_loc(self, loc):
        """
        Checks if a given location is valid for placing an object (wall or apple).

        Args:
            loc (tuple): The location to check (x, y).

        Returns:
            bool: True if the location is valid, False otherwise.
        """
        x, y = loc
        # Check if the location is within board bounds
        if 0 > x or x >= self.__length or y < 0 or y >= self.__hight:
            return False
        # Check if the location is on the snake body
        if loc not in self.__snake.get_snake_body():
            for wall in self.__active_wall_list:
                # Check if the location is on a wall
                if loc in wall.get_wall_body():
                    return False
            for apple in self.__active_apple_list:
                # Check if the location is on an apple
                if loc in apple.get_location():
                    return False
            return True
        else:
            return False

    def draw_board(self, gd: GameDisplay) -> None:
        """
        Draws all the objects (snake, walls, apples) on the board using the GameDisplay object.

        Args:
            gd (GameDisplay): The game display object to render the board.
        """
        # Draw all apples
        for apple in self.__active_apple_list:
            apple.draw_apple(gd)
        # Draw the snake
        self.__snake.draw(gd)
        # Draw all walls
        for wall in self.__active_wall_list:
            for cell in wall.get_wall_body():
                x, y = cell
                if 0 <= x < self.__length and 0 <= y < self.__hight:
                    wall.draw_cell(cell, gd)
        gd.show_score(self.__score)

    def rest_game(self) -> None:
        """
        Resets the game, including the snake's position, the walls, apples, and score.
        """
        for i in range(len(self.__active_apple_list)):
            self.__apple_list.append(self.__active_apple_list[i])
        self.__active_apple_list = []
        for i in range(len(self.__active_wall_list)):
            self.__wall_list.append(self.__active_wall_list[i])
        self.__active_wall_list = []
        self.__snake.save(self.__length // 2, self.__hight // 2)
        self.__key_clicked = None
        self.__move_wall = False
        self.__score = 0

    def is_over(self) -> bool:
        """
        Checks if the game is over (when the snake dies or other game-ending conditions are met).

        Returns:
            bool: True if the game is over, False otherwise.
        """
        if not (self.__snake.get_alive() or self.__apple_list or \
                 self.__active_apple_list or self.__wall_list or self.__active_wall_list):
            return True
        elif self.__snake.get_length() == 0:
            return True
        elif (not self.__snake.get_alive()) and self.__snake.get_length() > 0:
            return True

        return False
