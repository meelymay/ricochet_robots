# raw_input('')
import random
import sys

ROBOTS = ['A', 'B', 'C', 'D', 'E', 'F']
WALL_DENSITY = 2/25.

class Square:
    def __init__(self, hor_wall=0, vert_wall=0):
        # booleans to indicate if there is a wall in that direction
        self.hor_wall = hor_wall
        self.vert_wall = vert_wall
        self.robot = None

    def set_robot(self, robot):
        self.robot = robot

    def empty(self):
        self.robot = None

    def __str__(self):
        return '*' if self.robot is None else self.robot.__str__()

class Robot:
    def __init__(self, color, x, y, board):
        self.color = color
        self.x = x
        self.y = y
        self.board = board

    def move(self, hor, vert):
        if abs(hor+vert) != 1 or abs(hor) not in [0,1] or abs(vert) not in [0,1]:
            raise Exception("can only move one direction at a time")
        while self.can_move(hor, vert):
            self.x += hor
            self.y += vert

    def can_move(self, hor, vert):
        # border
        if self.x+hor < 0 or self.x+hor >= self.board.size or self.y+vert < 0 or self.y+vert >= self.board.size:
            return False
        # walled in current square
        if abs(hor) == 1 and hor == self.board.board[self.x][self.y].hor_wall:
            return False
        if abs(vert) == 1 and vert == self.board.board[self.x][self.y].vert_wall:
            return False
        # walled in next square
        if abs(hor) == 1 and hor == -self.board.board[self.x+hor][self.y].hor_wall:
            return False
        if abs(vert) == 1 and vert == -self.board.board[self.x][self.y+vert].vert_wall:
            return False
        # robot
        if self.board.board[self.x+hor][self.y+vert].robot is not None:
            return False
        return True

    def __str__(self):
        return self.color

class Board:
    def __init__(self, size):
        self.size = size
        self.board = self.init_squares()
        self.robots = {}
        self.place_robots()

    def init_squares(self):
        board = [[Square() for s in range(self.size)] for s in range(self.size)]
        for row in board:
            for i in range(len(row)):
                if random.random() < WALL_DENSITY:
                    angle = random.randint(0,3)
                    if angle == 0:
                        row[i] = Square(hor_wall=-1, vert_wall=-1)
                    elif angle == 1:
                        row[i] = Square(hor_wall=1, vert_wall=-1)
                    elif angle == 2:
                        row[i] = Square(hor_wall=1, vert_wall=1)
                    elif angle == 3:
                        row[i] = Square(hor_wall=-1, vert_wall=1)
        return board

    def place_robots(self):
        for robot in ROBOTS:
            (x,y) = (random.randint(0,self.size-1),random.randint(0,self.size-1))
            while self.board[x][y].robot is not None:
                (x,y) = (random.randint(0,self.size-1),random.randint(0,self.size-1))
            robot_obj = Robot(robot, x, y, self)
            self.board[x][y].set_robot(robot_obj)
            self.robots[robot] = robot_obj

    def move_robot(self, robot_color, hor, vert):
        robot = self.robots[robot_color]
        self.board[robot.x][robot.y].empty()
        robot.move(hor, vert)
        self.board[robot.x][robot.y].set_robot(robot)

    def show_board(self):
        s = [[' ' for i in range(self.size*2+1)] for j in range(self.size*2+1)]

        # borders
        for i in range(len(s)):
            s[i][0] = '|'
            s[0][i] = '-'
            s[i][-1] = '|'
            s[-1][i] = '-'

        # inner walls
        for i in range(self.size):
            for j in range(self.size):
                (x,y) = (i*2+1, j*2+1)
                square = self.board[i][j]
                if square.hor_wall == -1:
                    for offset in range(-1,2):
                        s[x-1][y+offset] = '-' if s[x-1][y+offset] == ' ' else s[x-1][y+offset]
                if square.hor_wall == 1:
                    for offset in range(-1,2):
                        s[x+1][y+offset] = '-' if s[x+1][y+offset] == ' ' else s[x+1][y+offset]
                if square.vert_wall == -1:
                    for offset in range(-1,2):
                        s[x+offset][y-1] = '|' if s[x+offset][y-1] == ' ' else s[x+offset][y-1]
                if square.vert_wall == 1:
                    for offset in range(-1,2):
                        s[x+offset][y+1] = '|' if s[x+offset][y+1] == ' ' else s[x+offset][y+1]
                s[x][y] = self.board[i][j]
        for i in range(len(s)):
            for j in range(len(s)):
                print s[i][j],
            print

if __name__ == "__main__":
    size = int(sys.argv[1])
    game = Board(size)
    game.show_board()

    input = None
    while input != "EXIT":
        input = raw_input('Which robot should move? Which way? ')
        robot, hor, vert = input.split()
        hor = int(hor)
        vert = int(vert)
        game.move_robot(robot, hor, vert)
        game.show_board()


