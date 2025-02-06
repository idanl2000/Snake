
COLOR_GREEN = "green"
class Apple:

    def __init__(self,x,y):
        self.__color = COLOR_GREEN
        self.__x = x
        self.__y = y

    def draw_apple(self, gd) -> None:
        """draw the apple on a given screen"""
        gd.draw_cell(self.__x, self.__y, COLOR_GREEN)

    def change_cord(self,x,y):
        """changes the loc of the apple"""
        self.__x = x
        self.__y = y

    def get_location(self):
        """get apple location"""
        return self.__x,self.__y

