import pygame
from Square import Square
from queue import PriorityQueue

from Map import Map_Obj

# This project is inspired by: https://www.youtube.com/watch?v=JtiK0DOeI4A&t=200s for the visuals
# and https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2. for the A* algorithm.

WIDTH = 564
HEIGHT = 468

# Initializing surface
WIN = pygame.display.set_mode((HEIGHT, WIDTH))

# Sets the title of the window
pygame.display.set_caption("A* Path Finding Algorithm")

# colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
GREY = (200, 200, 200)
LINE_GREY = (128, 128, 128)
DARK_GREY = (100, 100, 100)
PINK = (255, 130, 185)

# Sets the background color
WIN.fill(WHITE)

# Selects the map
CURRENT_MAP = 1


def set_map_to(map_nr: int):
    global CURRENT_MAP
    CURRENT_MAP = map_nr


def get_map_array():
    """
    Fetches the map array from the map object
    :return: The array of the map
    """
    maps = Map_Obj(CURRENT_MAP).get_maps()
    array_map = maps[0]
    return array_map


def get_map_rows():
    """
    Returns the length of the rows of the 2D-array
    :return: The rows of the array
    """
    return len(get_map_array())


def get_map_columns():
    """
    Returns the length of the columns of the 2D-array
    :return: The columns of the array
    """
    return len(get_map_array()[0])


def get_start_position():
    """
    Fetches the start position from the map object.
    :return: The start position
    """
    return Map_Obj(CURRENT_MAP).get_start_pos()


def get_end_position():
    """
    Fetches the end position from the map object.
    :return: The end position
    """
    return Map_Obj(CURRENT_MAP).get_end_goal_pos()


def set_original_color(grid):
    """
    Sets the squares back to their original color.
    :param grid: The grid
    :return:
    """
    for array in grid:
        for square in array:
            if square.color == GREEN:
                if square.cost == 1:
                    square.set_color(WHITE)
                elif square.cost == 2:
                    square.set_color(GREY)
                elif square.cost == 3:
                    square.set_color(DARK_GREY)
                elif square.cost == 4:
                    square.set_color(BLACK)


def make_grid(rows: int, width: int, map_array: []):
    """
    Creates the grid in the pygame window.
    :param rows: Amount of rows in the window.
    :param width: The width of the pygame window.
    :param map_array: The 2D-array of the map.
    :return: The grid object.
    """
    grid = []
    gap = (width // rows)
    for i in range(rows):
        grid.append([])
        map_list = map_array[i]
        for j in range(len(map_list)):
            list_value = map_list[j]
            if list_value == 1:
                square = Square(i, j, gap, rows)
            elif list_value == -1:
                square = Square(i, j, gap, rows)
                square.make_wall()
            elif list_value == 2:
                square = Square(i, j, gap, rows)
                square.set_color(GREY)
            elif list_value == 3:
                square = Square(i, j, gap, rows)
                square.set_color(DARK_GREY)
            elif list_value == 4:
                square = Square(i, j, gap, rows)
                square.set_color(BLACK)
            square.cost = list_value
            grid[i].append(square)

    # Sets the color of the start position
    start_pos = get_start_position()
    start_square: Square = grid[start_pos[0]][start_pos[1]]
    start_square.set_color(PINK)

    # Sets the color of the goal position
    end_position = get_end_position()
    end_square: Square = grid[end_position[0]][end_position[1]]
    end_square.set_color(ORANGE)

    return grid


def draw_grid(win, rows, columns, width):
    """
    Draws the grid in the pygame window.
    :param columns: The amount of columns
    :param win: The pygame window
    :param rows: The amount of rows
    :param width: The width of the pygame window
    """
    gap = (width // rows)
    for i in range(rows):
        pygame.draw.line(win, LINE_GREY, (0, i * gap), (width, i * gap))
        for j in range(columns):
            pygame.draw.line(win, LINE_GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, columns, width):
    """
    Creates a grid pattern.
    :param win: The pygame window.
    :param grid: The grid generated in "make_grid".
    :param rows: The amount of rows
    :param columns: The amount of columns.
    :param width: The width of the pygame window
    """

    # Draws the lines in the pygame window.
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, columns, width)
    pygame.display.update()


def calculate_h_value(p1, p2):
    """
    Calculates the h-value in the a* algorithm.
    :param p1: The first position
    :param p2: The second position
    :return: The absolute value of the distance between the first position and the second.
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def backtrack(path, draw):
    """
    Backtracks the path found in the algorithm and creates the path in the Pygame window.
    :param path: A list with the shortest path.
    :param draw: The draw function to update the screen.
    """
    for current in path:
        current.make_path()
        draw()


def check_if_in_open(node: Square, open_list: PriorityQueue):
    """
    Checks if the node is in the open_list
    :param node: The square we want to check
    :param open_list: The priority queue with the open nodes
    :return: True if the node is in the open_list.
    """
    for square in open_list.queue:
        if node.col == square[1].col and node.row == square[1].row:
            return True
    return False


def algorithm(draw, grid):
    """
    The a* algorithm.
    :param draw: The draw function to update the pygame window.
    :param grid: The grid created in make_grid
    :return: The shortest path if found, or an empty array if no path was found.
    """
    # The list with the open nodes.
    # Uses a priority queue to retrieve the nodes with the lowest f value.
    open_list: [Square] = PriorityQueue()

    # The list with the closed nodes
    closed_list = []

    # The start square
    start = get_start_position()
    start_square: Square = grid[start[0]][start[1]]

    # The end square
    end = get_end_position()
    end_square: Square = grid[end[0]][end[1]]

    # Puts the start square in the open list.
    open_list.put((start_square.f_value, start_square))

    while not open_list.empty():
        # The list is sorted by the lowest f value. The get removes the square from the Priority Queue.
        current_square: Square = open_list.get()[1]

        # Adds the current square to the closed list.
        closed_list.append(current_square)

        # If the current square equals the goal square,
        # we save the path and creates the path in the pygame
        if current_square == end_square:
            path = []
            current = current_square
            while current is not None:
                path.append(current)
                current = current.parent
            return path[::-1]  # Return reversed path

        else:
            current_square.update_neighbors(grid)  # Updates the neighbors of the current square
            neighbors = current_square.neighbors
            for square in neighbors:
                if square not in closed_list:
                    # Update the g, h, and f values
                    square.g_value = current_square.g_value + square.cost
                    square.h_value = calculate_h_value(square.get_pos(), end_square.get_pos())
                    square.f_value = square.g_value + square.h_value

                    # If the square is not in the open list, we add it and change the color of it in the pygame window.
                    if not check_if_in_open(square, open_list):
                        if square is not start_square and square is not end_square:
                            square.set_color(GREEN)

                        square.set_parent(current_square)  # Sets the parent of the square. This enables backtracking.

                        open_list.put((square.f_value, square))
            draw()
    return []


def main():
    rows = get_map_rows()  # Gets the amount of rows
    columns = get_map_columns()  # Gets the amount of columns
    map_array = get_map_array()  # Gets the 2D array of the map
    grid = make_grid(rows, WIDTH, map_array)  # Creates the grid
    run = True
    while run:
        draw(WIN, grid, rows, columns, WIDTH)

        # Handles the events in pygame
        for event in pygame.event.get():

            # Shuts down the application pygame is quit
            if event.type == pygame.QUIT:
                run = False

            # Closes the window if escape is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

                # Runs the algorithm when space is pressed
                if event.key == pygame.K_SPACE:
                    grid = make_grid(rows, WIDTH, map_array)  # Clears the grid if the code ran before.
                    path = algorithm(lambda: draw(WIN, grid, rows, columns, WIDTH),
                                     grid)  # returns the path from algorithm
                    # set_original_color(grid)
                    backtrack(path, lambda: draw(WIN, grid, rows, columns, WIDTH))  # Draws the path

                if event.key == pygame.K_1:
                    set_map_to(1)
                    map_array = get_map_array()  # Gets the 2D array of the map
                    grid = make_grid(rows, WIDTH, map_array)  # Clears the grid if the code ran before.

                if event.key == pygame.K_2:
                    set_map_to(2)
                    map_array = get_map_array()  # Gets the 2D array of the map
                    grid = make_grid(rows, WIDTH, map_array)  # Clears the grid if the code ran before.

                if event.key == pygame.K_3:
                    set_map_to(3)
                    map_array = get_map_array()  # Gets the 2D array of the map
                    grid = make_grid(rows, WIDTH, map_array)  # Clears the grid if the code ran before.

                if event.key == pygame.K_4:
                    set_map_to(4)
                    map_array = get_map_array()  # Gets the 2D array of the map
                    grid = make_grid(rows, WIDTH, map_array)  # Clears the grid if the code ran before.

    pygame.quit()


if __name__ == "__main__":
    main()
