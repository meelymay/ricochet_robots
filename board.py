# raw_input('')
import random
import sys

ROBOTS = ['A', 'B', 'C', 'D', 'E', 'F']
LETTERS = {
    'red': 'a',
    'blue': 'b',
    'cyan': 'c',
    'yellow': 'd',
    'green': 'e',
    'purple': 'f'
}
COLORS = {
    'a': 'red',
    'b': 'blue',
    'c': 'cyan',
    'd': 'yellow',
    'e': 'green',
    'f': 'purple'
}
WALL_DENSITY = 1/15.

class Square:
    def __init__(self, x, y, hor_wall=0, vert_wall=0):
        # booleans to indicate if there is a wall in that direction
        self.x = x
        self.y = y
        self.hor_wall = hor_wall
        self.vert_wall = vert_wall
        self.robot = None
        self.target = None

    def set_robot(self, robot):
        self.robot = robot

    def set_target(self, target):
        self.target = target

    def empty(self):
        self.robot = None

    def copy(self, board):
        # print "square copy"
        square = Square(self.x, self.y, self.hor_wall, self.vert_wall)
        if self.robot:
            # print "set robot"
            square.set_robot(self.robot.copy(board))
        # print "set target",self.target
        square.set_target(self.target)
        return square


    def __str__(self):
        if self.robot is not None:
            return self.robot.__str__()
        if self.target:
            return self.target.__str__().lower()
        return '*'

class Robot:
    def __init__(self, name, x, y, color, board):
        self.name = name
        self.color = color
        self.x = x
        self.y = y
        self.board = board

    def copy(self, board):
        # print "robot copy",self.color, self.x, self.y, board.board[self.x][self.y]
        return Robot(self.name, self.x, self.y, self.color, board)

    def move(self, hor, vert):
        if abs(hor+vert) != 1 or abs(hor) not in [0,1] or abs(vert) not in [0,1]:
            raise Exception("can only move one direction at a time")
        while self.can_move(hor, vert):
            self.x += hor
            self.y += vert
        return self.square()

    def square(self):
        return self.board.board[self.x][self.y]

    def can_move(self, hor, vert):
        # border
        if self.x+hor < 0 or self.x+hor >= self.board.size or self.y+vert < 0 or self.y+vert >= self.board.size:
            return False
        # walled in current square
        if abs(hor) == 1 and hor == self.square().hor_wall:
            return False
        if abs(vert) == 1 and vert == self.square().vert_wall:
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
        return self.name

class AI:
    def __init__(self, game):
        self.game = game
        self.moves = self.get_moves()

    def get_moves(self):
        moves = []
        for robot in ROBOTS:
            for hor in (-1, 0, 1):
                for vert in (-1, 0, 1):
                    if abs(hor+vert) == 1:
                        moves.append((robot, hor, vert))
        return moves

    def find_path(self):
        paths = [[(self.game.copy(), None)]]

        count = 1
        while True:
            # count += 1
            # take a path off the queue
            first_path = paths[0]
            paths.remove(first_path)
            # get the current game state in that path
            game = first_path[-1][0]
            if count % 100 == 0:
                print "Searching...",count
                game.show_board()
            # try all moves from that state
            for move in self.moves:
                new_game = game.copy()
                new_path = first_path+[(new_game, move)]
                (robot, hor, vert) = move
                square = new_game.move_robot(robot, hor, vert)
                if new_game.moves == 0:
                    return new_path
                paths.append(new_path)

class Board:
    def __init__(self, size, blank=False):
        self.size = size
        self.board = self.init_squares()
        self.robots = {}
        if not blank:
            self.place_robots()
            self.place_target()
        self.moves = 0

    def copy(self):
        board = Board(self.size, blank=True)
        board.board = [[sq.copy(board) for sq in row] for row in self.board]
        board.robots = dict(reduce(lambda x, y: x+y, [[(col.robot.name, col.robot) for col in row if col.robot is not None] for row in board.board]))
        board.moves = self.moves
        return board

    def empty_square(self):
        (x,y) = (random.randint(0,self.size-1),random.randint(0,self.size-1))
        while self.board[x][y].robot is not None:
            (x,y) = (random.randint(0,self.size-1),random.randint(0,self.size-1))
        return (x,y)

    def place_target(self):
        (x,y) = self.empty_square()
        self.board[x][y].set_target(random.choice(ROBOTS))

    def init_squares(self):
        board = [[Square(x, y) for x in range(self.size)] for y in range(self.size)]
        for k, row in enumerate(board):
            for i in range(len(row)):
                if random.random() < WALL_DENSITY:
                    angle = random.randint(0,3)
                    if angle == 0:
                        row[i] = Square(i, k, hor_wall=-1, vert_wall=-1)
                    elif angle == 1:
                        row[i] = Square(i, k, hor_wall=1, vert_wall=-1)
                    elif angle == 2:
                        row[i] = Square(i, k, hor_wall=1, vert_wall=1)
                    elif angle == 3:
                        row[i] = Square(i, k, hor_wall=-1, vert_wall=1)
        return board

    def place_robots(self):
        for robot in ROBOTS:
            (x,y) = self.empty_square()
            robot_obj = Robot(robot, x, y, COLORS[robot.lower()], self)
            self.board[x][y].set_robot(robot_obj)
            self.robots[robot] = robot_obj

    def target_hit(self, square=None):
        if not square:
            square = filter(lambda x: x.target is not None, reduce(lambda x, y: x + y, self.board))
        return square.target == square.robot.color

    def move_robot(self, robot_name, hor, vert):
        robot = self.robots[robot_name]
        if hor not in [-1, 0, 1] or vert not in [-1, 0, 1] or abs(hor + vert) != 1:
            return None
        self.board[robot.x][robot.y].empty()
        square = robot.move(hor, vert)
        self.board[robot.x][robot.y].set_robot(robot)
        self.moves += 1
        if self.target_hit(square):
            square.set_target(None)
            self.place_target()
            print '\n\n-----------------\nCongrats! You hit the target in %s moves!\n-----------------' % self.moves
            self.moves = 0
        return square

    def board_view(self):
        view = []
        for y, row in enumerate(self.board):
            for x, square in enumerate(row):
                obj = {}
                obj['x'] = x
                obj['y'] = y
                obj['hor'] = square.hor_wall
                obj['vert'] = square.vert_wall
                obj['robot'] = square.robot.color if square.robot else None
                view.append(obj)
        return view

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

def parse_input(raw_text):
    usage = "Requires three inputs: [ROBOT] [VERTICAL: {1, 0, 1}] [HORIZONTAL: {-1, 0, 1}]"
    if raw_text == "AI":
        return ("AI", None, None)
    if raw_text == "EXIT":
        return ("EXIT", None, None)
    text = raw_text.split()
    if len(text) != 3:
        print usage
        return None
    try:
        vert = int(text[1])
        hor = int(text[2])
        if hor not in [-1, 0, 1] or vert not in [-1, 0, 1] or abs(hor + vert) != 1:
            print usage
            return None
    except:
        print usage
        return None
    return (text[0], int(text[1]), int(text[2]))

def get_input():
    triplet = None
    while triplet == None:
        triplet = parse_input(raw_input('Which robot should move? Which way? '))
    return triplet

if __name__ == "__main__":
    size = int(sys.argv[1])
    game = Board(size)
    game.show_board()

    # ai_moves = AI(game).find_path()

    input = None
    while input != "EXIT":
        robot, hor, vert = get_input()
        if robot == "EXIT":
            break
        if robot == "AI":
            for move in ai_moves:
                print move[1]
                move[0].show_board()
                print len(ai_moves),"moves"
        game.move_robot(robot, hor, vert)
        game.show_board()


