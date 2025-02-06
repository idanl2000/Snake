COLOR_BLUE = "blue"
WALL_LENGTH = 3
UP = "Up"
DOWN = "Down"
LEFT = "Left"
RIGHT = "Right"


class Wall:

    def __init__(self, x, y, direction):
        self._x = x
        self._y = y
        self._length = WALL_LENGTH
        self._color = COLOR_BLUE
        self._direction = direction
        self._wall_body = self.get_wall_body()

    def get_wall_body(self) -> list:
        """return the body of the wall"""
        if self._direction == UP or self._direction == DOWN:
            return [(self._x, self._y - 1), (self._x, self._y), (self._x, self._y + 1)]
        else:
            return [(self._x - 1, self._y), (self._x, self._y), (self._x + 1, self._y)]

    def get_wall_edge(self):
        """return the edge of the wall"""
        if self._direction == UP or self._direction == RIGHT:
            return  self._wall_body[2]
        else:
            return self._wall_body[0]

    def move_wall(self):
        """move the wall one stap in hid direction"""
        if self._direction == UP:
            self._y += 1
            self._wall_body = self.get_wall_body()
        elif self._direction == DOWN:
            self._y -= 1
            self._wall_body = self.get_wall_body()
        elif self._direction == RIGHT:
            self._x += 1
            self._wall_body = self.get_wall_body()
        elif self._direction == LEFT:
            self._x -= 1
            self._wall_body = self.get_wall_body()



    def change_wall(self, x, y, direction):
        """change the loc and direction of a given wall"""
        self._x = x
        self._y = y
        self._direction = direction
        self._wall_body = self.get_wall_body()


    def draw_cell(self, loc, gd):
        """draw a given cell if it is in the wall"""
        if loc in self.get_wall_body():
            x, y = loc
            gd.draw_cell(x, y, self._color)


    def is_wall_out(self, len_x, len_y):
        """check if the wall is after agiven length or higth"""
        for cell in self._wall_body:
            x, y = cell
            if self._direction == UP:
                if y < len_y:
                    return False
            elif self._direction == DOWN:
                if y >= 0:
                    return False
            elif self._direction == RIGHT:
                if x < len_x:
                    return False
            elif self._direction == LEFT:
                if x >= 0:
                    return False
        return True



