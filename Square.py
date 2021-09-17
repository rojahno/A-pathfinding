import pygame

# colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
THISTLE = (221, 160, 221)


class Square:
    def __init__(self, row, col, width, total_rows):
        # Fields for visuals
        self.col = col  # The column position
        self.row = row  # The row position
        self.x = col * width
        self.y = row * width
        self.color = WHITE  # Sets the default color to white
        self.width = width
        self.total_rows = total_rows

        # Fields for algorithm
        self.parent = None  # The parent with the lowest f value
        self.neighbors = []  # An array of the neighbors.
        self.g_value = 0  # The g-value of the square.
        self.f_value = 0  # The f-value of the square.
        self.h_value = 0  # THe h-value of the square.
        self.cost = 1  # The cost of the square. Default is 1

    def set_color(self, color):
        """
        Sets the color of the square
        :param color: The color
        """
        self.color = color

    def set_parent(self, parent):
        """
        Sets the parent of the square
        :param parent: The parent
        """
        self.parent = parent

    def get_parent(self):
        """
        Returns the parent of the square.
        :return: The parent
        """
        return self.parent

    def draw(self, window):
        """
        Draws the square
        :param window: The pygame window
        """
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def get_pos(self):
        """
        Returns the position of the Square.
        :return: An array of the location of the square.
        """
        return [self.row, self.col]

    def is_wall(self):
        """
        Checks if the square is a part of the wall
        :return: True if it is part of the wall
        """
        return self.color == RED

    def make_wall(self):
        """
        Creates the wall of the map
        """
        self.color = RED

    def make_path(self):
        """
        Creates the path when the shortest path is found.
        """
        self.color = THISTLE

    def update_neighbors(self, grid):
        """
        Updates the neighbor of this square.
        :param grid: The grid
        """
        self.neighbors = [] # Initialized the list

        down_neighbor: Square = grid[self.row + 1][self.col]
        up_neighbor: Square = grid[self.row - 1][self.col]
        right_neighbor: Square = grid[self.row][self.col + 1]
        left_neighbor: Square = grid[self.row][self.col - 1]

        if self.row < self.total_rows - 1 and not down_neighbor.is_wall():  # Down
            self.neighbors.append(down_neighbor)

        if self.row > 0 and not up_neighbor.is_wall():  # UP
            self.neighbors.append(up_neighbor)

        if self.col < self.total_rows - 1 and not right_neighbor.is_wall():  # RIGHT
            self.neighbors.append(right_neighbor)

        if self.col > 0 and not left_neighbor.is_wall():  # LEFT
            self.neighbors.append(left_neighbor)

    def __lt__(self, other):
        """
        Defines the behaviour of the less-than operator
        :param other:
        :return:
        """
        return False
