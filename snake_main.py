import argparse
import game_utils
from snake_game import SnakeGame
from game_display import GameDisplay
from wall import Wall
from apple import Apple

def make_apple():
    """
    Create and return a random apple using game utilities.
    """
    x, y = game_utils.get_random_apple_data()
    return Apple(x, y)

def make_apple_list(num):
    """
    Generate a list of apples of the given size.

    :param num: Number of apples to create.
    :return: List of Apple objects.
    """
    return [make_apple() for _ in range(num)]


def change_apple_list(apple_list):
    """
    Change the position of the first apple in the given list.
    :param apple_list: List of Apple objects.
    """
    if apple_list:
        apple = apple_list[0]
        x, y = game_utils.get_random_apple_data()
        apple.change_cord(x, y)

def change_apple_list_all(apple_list):
    """
    Change the position of all apples in the given list.

    :param apple_list: List of Apple objects.
    """
    for apple in apple_list:
        x, y = game_utils.get_random_apple_data()
        apple.change_cord(x, y)

def make_wall():
    """
    Create and return a random wall using game utilities.
    """
    x, y, direction = game_utils.get_random_wall_data()
    return Wall(x, y, direction)

def make_wall_list(num):
    """
    Generate a list of walls of the given size.

    :param num: Number of walls to create.
    :return: List of Wall objects.
    """
    return [make_wall() for _ in range(num)]

def change_wall_list(wall_list):
    """
    Change the position of the first wall in the given list.

    :param wall_list: List of Wall objects.
    """
    if wall_list:
        wall = wall_list[0]
        x, y, direction = game_utils.get_random_wall_data()
        wall.change_wall(x, y, direction)

def change_wall_list_all(wall_list):
    """
    Change the position of all walls in the given list.

    :param wall_list: List of Wall objects.
    """
    for wall in wall_list:
        x, y, direction = game_utils.get_random_wall_data()
        wall.change_wall(x, y, direction)

def run_game(game, gd: GameDisplay, wall_list, apple_list):
    """
    The main game loop for a single round.

    :param game: The SnakeGame instance.
    :param gd: The GameDisplay instance.
    :param wall_list: List of Wall objects.
    :param apple_list: List of Apple objects.
    """
    # DRAW BOARD
    game.add_objects()
    game.draw_board(gd)
    #the main loop of one turn in the game
    while not game.is_over():
        # CHECK KEY CLICKS
        key_clicked = gd.get_key_clicked()
        game.read_key(key_clicked)
        # UPDATE OBJECTS
        game.update_objects()
        # DRAW BOARD
        game.draw_board(gd)
        # get anew apple and wall to put on the bord if we have any
        change_apple_list(apple_list)
        change_wall_list(wall_list)
        gd.end_round()

def main_loop(gd: GameDisplay, args: argparse.Namespace) -> None:
    """
       The main loop for the game.

       :param gd: The GameDisplay instance.
       :param args: Command-line arguments containing game settings.
       """
    #geting the input from the user
    bord_width = args.width
    bord_height = args.height
    num_of_apples = args.apples
    is_debug = args.debug
    num_of_walls = args.walls
    num_of_rounds = args.rounds
    #bilding a random list of apple and wall for the game
    wall_list = make_wall_list(num_of_walls)
    apple_list = make_apple_list(num_of_apples)
    # INIT OBJECTS
    game = SnakeGame(bord_width, bord_height, wall_list, apple_list, is_debug)
    gd.show_score(0)
    #ckeck if the user wants to play forever :)
    if num_of_rounds < 0:
        while True:
            run_game(game, gd, wall_list, apple_list)
            game.rest_game()
            change_wall_list(wall_list)
            change_apple_list(apple_list)
    else:
        while num_of_rounds >= 0:
            run_game(game, gd, wall_list, apple_list)
            num_of_rounds -= 1
            game.rest_game()
            change_wall_list(wall_list)
            change_apple_list(apple_list)




if __name__ == "__main__":
    print("You should run:\n"
          "> python game_display.py")