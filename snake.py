COLOR_BLACK = "black"
SNAKE_START_LENGTH = 3
UP = "Up"
DOWN = "Down"
LEFT = "Left"
RIGHT = "Right"

from game_display import GameDisplay

class Snake:
    """
    Represents a Snake object in the game, managing its movement, state, and interactions.
    """

    def __init__(self, x, y):
        """
        Initializes the Snake with a starting position and length.

        Args:
            x (int): The x-coordinate of the snake's head.
            y (int): The y-coordinate of the snake's head.
        """
        self._x = x
        self._y = y

        # Set snake length using debug function to validate
        def debug(x):
            if x < 0:
                return 0
            else:
                return SNAKE_START_LENGTH
        self._length = debug(x)
        self._color = COLOR_BLACK
        self._snake_body = [(x, y - i) for i in range(self._length)]
        self._direction = UP
        self._alive = False if x < 0 else True
        self._food = 0

    def get_alive(self):
        """Returns whether the snake is alive."""
        return self._alive

    def get_direction(self):
        """Returns the current direction of the snake."""
        return self._direction

    def get_x_y(self):
        """Returns the coordinates of the snake's head."""
        return self._x, self._y

    def get_length(self):
        """Returns the length of the snake."""
        return self._length

    def eat(self):
        """Increases the snake's food counter (represents eating an apple)."""
        self._food += 3

    def get_snake_body(self):
        """Returns a list of tuples representing the coordinates of the snake's body."""
        return self._snake_body

    def opist_diretion(self):
        """Returns the opposite direction of the snake's current direction."""
        if self._direction == UP:
            return DOWN
        elif self._direction == DOWN:
            return UP
        elif self._direction == RIGHT:
            return LEFT
        elif self._direction == LEFT:
            return RIGHT

    def set_direction(self, direction):
        """
        Sets the direction of the snake, ensuring it cannot go in the opposite direction.

        Args:
            direction (str): The new direction the snake should move in (UP, DOWN, LEFT, RIGHT).
        """
        if not direction == self.opist_diretion():
            self._direction = direction

    def _move_eat(self):
        """
        Handles the snake's movement when it eats food (apple). The snake grows and the food counter decreases.
        If the snake eats itself, it dies.
        """
        if self._food:
            if (self._x, self._y) != self._snake_body[-1]:
                self._food -= 1
                self._length += 1
                self._snake_body.insert(0, (self._x, self._y))
                return True
            else:
                self.kill()
                return False
        else:
            self._snake_body.pop()
            self._snake_body.insert(0, (self._x, self._y))
            return True

    def move(self) -> bool:
        """
        Moves the snake one step in its current direction. If it collides with its own body, it dies.

        Returns:
            bool: True if the move was successful, False if the snake died (e.g., collided with its body).
        """
        if self._direction == UP:
            self._y += 1
        elif self._direction == DOWN:
            self._y -= 1
        elif self._direction == RIGHT:
            self._x += 1
        elif self._direction == LEFT:
            self._x -= 1

        if not (self._x, self._y) in self._snake_body[:-1]:
            return self._move_eat()
        else:
            self.kill()
            return False

    def cut(self, loc):
        """
        Cuts the snake's body at the given location.

        Args:
            loc (tuple): The location where the snake's body should be cut.
        """
        for index, snake_loc in enumerate(self._snake_body):
            if loc == snake_loc:
                if index == 1:
                    self.kill()
                self._length = index
                self._snake_body = self._snake_body[:index]

    def draw(self, gd: GameDisplay):
        """
        Draws the snake on the game board.

        Args:
            gd (GameDisplay): The game display object that handles rendering.
        """
        for x, y in self._snake_body:
            gd.draw_cell(x, y, self._color)

    def kill(self):
        """Kills the snake, making it unable to move or grow."""
        if self._length:
            self._alive = False
            self._snake_body.pop(0)

    def save(self, x, y):
        """
        Resets the snake's state for a new game.

        Args:
            x (int): The starting x-coordinate of the snake's head.
            y (int): The starting y-coordinate of the snake's head.
        """
        if self._length:
            self._x = x
            self._y = y
            self._length = SNAKE_START_LENGTH
            self._snake_body = [(x, y - i) for i in range(self._length)]
            self._direction = UP
            self._alive = True
            self._food = 0
