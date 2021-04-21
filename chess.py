import copy
from colorama import Fore, Back, init

class Board:
    BLACK = 0
    WHITE = 1
    turn = 1
    LOG = []
    init(autoreset=True)
    verbose = False

    def __init__(self):
        self.board = [
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None]]

    def set_standard(self):
        self.board = [
        [Rook(0), Knight(0), Bishop(0), Queen(0), King(0), Bishop(0), Knight(0), Rook(0)],
        [Pawn(0), Pawn(0), Pawn(0), Pawn(0), Pawn(0), Pawn(0), Pawn(0), Pawn(0)],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [Pawn(1), Pawn(1), Pawn(1), Pawn(1), Pawn(1), Pawn(1), Pawn(1), Pawn(1)],
        [Rook(1), Knight(1), Bishop(1), Queen(1), King(1), Bishop(1), Knight(1), Rook(1)]]

    def set_verbose(self):
        self.verbose = True
        for y in range(len(self.board)):
            for item in self.board[y]:
                if item is not None:
                    item.verbose = True

    def __str__(self):
        greybg = '\033[47m'
        blackbg = '\033[00m'
        s = '  +---+---+---+---+---+---+---+---+ \n'
        for y in range(len(self.board)):
            s += str(8 - y) + ' |'
            if y % 2 == 0:
                s += greybg
            s += ' ' 

            for x in range(len(self.board[y])):
                if (x + y) % 2 == 0:
                    s += greybg
                    if self.board[y][x] is None:
                        s += '  ' + blackbg + '| '
                    else:
                        s += str(self.board[y][x]) + greybg +' ' + blackbg + '| '
                else:
                    if self.board[y][x] is None:
                        if x < 7:
                            s += '  |' + greybg + ' '
                        else: 
                            s += '  | '
                    else:
                        s += str(self.board[y][x]) + ' |'
                        if x < 7:
                            s += greybg + ' '
                        else: 
                            s += ' '
                s += blackbg
            s += '\n ' + blackbg + ' +---+---+---+---+---+---+---+---+ \n'
        s += '    a   b   c   d   e   f   g   h'
        return s

    def col(self, cha):
        return ord(cha) - 97

    def parse(self, notation, move_now = False):
        """
        Translates traditional chess notation to a 'current space, new space' format.

        Parameters: 
            notation (string): Traditional chess notation for a move. Kb2 or e5, for example.

        Returns: 
            move (tuple): Returns two pairs in a tuple signifying the origination of the piece and it's destination.
        """
        origin = []
        destination = []
        TAKES = 0
        if notation[1] == 'x':
            TAKES = 1

        if 0 <= ord(notation[0]) - 97 < 26:
            # lower case character leading, pawn move

            # there's definitely a better way to find this pawn...
            for y in range(len(self.board)):
                for x in range(len(self.board[y])):
                    piece = copy.deepcopy(self.board[y][x])
                    if self.col(notation[0]) == x and piece is not None:
                        if self.turn == piece.color and piece.name == "Pawn":
                            print(f"moving {piece} to {notation}")
                            origin = [x, y]
                            if TAKES and len(notation) == 4:
                                destination = [self.col(notation[2]), 8 - int(notation[-1])]
                            elif len(notation) == 2:
                                destination = [x, 8 - int(notation[-1])]
                            elif len(notation) == 3:
                                print("It looks like you meant to capture. Please use 'x' to indicate capturing.")
                                print("For example, 'exd4' indicates e pawn capturing on d4.")
                                destination = []
                            else:
                                destination = []

        elif notation[0] == 'K':
            # King move
            destination = [self.col(notation[-2]), 8 - int(notation[-1])]

            for y in range(len(self.board)):
                for x in range(len(self.board[y])):
                    piece = self.board[y][x]
                    if piece is not None:
                        if self.turn == piece.color and piece.name == "King":
                            origin = [x, y]
                            
        elif notation[0] == 'Q':
            # Queen move
            destination = [self.col(notation[-2]), 8 - int(notation[-1])]

            for y in range(len(self.board)):
                for x in range(len(self.board[y])):
                    piece = self.board[y][x]
                    if piece is not None:
                        if self.turn == piece.color and piece.name == "Queen":
                            origin = [x, y]
            # DEBUG
            #print(f"Moving Queen from {origin} to {destination}")


        elif notation[0] == 'R':
            # Rook move
            destination = [self.col(notation[-2]), 8 - int(notation[-1])]
            # look in each of the 4 directions and find possible matching rooks
            directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
            rooks = []
            for direction in directions:
                loc = [destination[0] + direction[0], destination[1] + direction[1]]
                # keep looking in that direction until finding a piece, if it's the right color rook, store it
                while 0 <= loc[0] <= 7 and 0 <= loc[1] <= 7:
                    piece = self.board[loc[1]][loc[0]]
                    if piece is not None:
                        if piece.name == "Rook" and piece.color == self.turn:
                            rooks.append([loc[0], loc[1]])
                        break
                    loc[0] += direction[0]
                    loc[1] += direction[1]

            # we didn't find any rooks, there must be a mistake
            if len(rooks) == 0:
                origin = []

            # move the rook we found!
            elif len(rooks) == 1:
                origin = rooks[0]

            # we found more than one rook, check the notation for which should move
            elif len(rooks) > 1:
                if len(notation) < 4:
                    print("Please use the row/column to clarify which rook to move.")
                    origin = []
                else:
                    try:
                        y_val = 8 - int(notation[1])
                        for rook in rooks:
                            if rook[1] == y_val:
                                origin = rook
                    except ValueError:
                        x_val = self.col(notation[1])
                        for rook in rooks:
                            if rook[0] == x_val:
                                origin = rook

        elif notation[0] == 'B':
            # Bishop move
            destination = [self.col(notation[-2]), 8 - int(notation[-1])]
            # look in each of the 4 directions and find possible matching rooks
            directions = [[1, 1], [-1, 1], [-1, -1], [1, -1]]
            bishop = None
            for direction in directions:
                loc = [destination[0] + direction[0], destination[1] + direction[1]]
                # keep looking in that direction until finding a piece, if it's the right color bishop, store it
                while 0 <= loc[0] <= 7 and 0 <= loc[1] <= 7:
                    piece = self.board[loc[1]][loc[0]]
                    if piece is not None:
                        if piece.name == "Bishop" and piece.color == self.turn:
                            bishop = [loc[0], loc[1]]
                        break
                    loc[0] += direction[0]
                    loc[1] += direction[1]

            # we didn't find any bishops, there must be a mistake
            if bishop is None:
                origin = []
                
            # move the bishop we found!
            else:
                origin = bishop

        elif notation[0] == 'N':
            # Knight move
            destination = [self.col(notation[-2]), 8 - int(notation[-1])]
            # there's definitely a better way to find this knight...
            for y in range(len(self.board)):
                for x in range(len(self.board[y])):
                    piece = copy.deepcopy(self.board[y][x])
                    if piece is not None:
                        if self.turn == piece.color and piece.name == "Knight":
                            print(f"{piece} is at {x}, {y}")
                            if abs(y - destination[1]) == 2 and abs(x - destination[0]) == 1 or abs(x - destination[0]) == 2 and abs(y- destination[1]) == 1:
                                origin = [x, y]
                                print(origin)

        if origin == [] or destination == [] or origin == destination:
            print("Sorry, that move appears to be invalid.")
            return None

        if self.board[destination[1]][destination[0]] is not None:
            if self.board[origin[1]][origin[0]].color == self.board[destination[1]][destination[0]].color:
                print("You're not allowed to take your own piece.")
                return None

        if self.board[destination[1]][destination[0]] is not None and not TAKES:
            print("When taking a piece, please use an 'x' after the piece you're moving. For example: 'Rxe8'.")
            notation = notation[0] + 'x' + notation[1:]

        if move_now:
            self.move((origin, destination), notation)

        return (origin, destination)

    def move(self, move, notation):
        origin = move[0]
        destination = move[1]
        print(origin)
        print(destination)
        piece = copy.deepcopy(self.board[origin[1]][origin[0]])
        backup = copy.deepcopy(self.board[destination[1]][destination[0]])
        if piece.verify_move(self.board, move):
            self.board[origin[1]][origin[0]] = None
            self.board[destination[1]][destination[0]] = piece

            # Check if player moving remained in check
            if self.check_check(self.turn):
                print(self.LOG[-1][-1])
                if self.LOG[-1][-1] == '+':
                    print("You are in check, you must move out of check.")
                    # The most recent move did not relieve check, belay
                    self.board[origin[1]][origin[0]] = piece
                    self.board[destination[1]][destination[0]] = backup
                    self.invalid_move(move)
                    return False
            
            # Check if opponent was placed in check
            if self.check_check(abs(self.turn - 1)):
                print("Check!")
                notation += '+'
                # TODO: Check for checkmate
                
            self.LOG.append(notation)
            self.end_turn()
            return True
        else:
            self.invalid_move(move)
        return False

    def end_turn(self):
        if self.turn:
            self.turn = 0
        else:
            self.turn = 1

    def invalid_move(self, move):
        print("This move is not valid, please enter a valid move.")
        return True

    def check_check(self, color):
        # Find the enemy King on the board
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] is not None:
                    piece = self.board[y][x]
                    if piece.color == color and piece.name == "King":
                        # Check for check by running verify move on stationary king
                        if self.verbose:
                            print(f"Checking {'Black' if self.turn else 'White'} king at {[x, y]} for checks.")
                        # Return opposite of verify move (move verify `True` = no check, verify `False` = check)
                        return not piece.verify_move(self.board, [[x, y], [x, y]])

    def log(self):
        s = ""
        for i in range(len(self.LOG)):
            if i % 2 == 0 and i + 1 < len(self.LOG):
                s += f"{i // 2 + 1}. {self.LOG[i]}    {self.LOG[i+1]} \n"
        if not self.turn:
            s += f"{i // 2 + 1}. {self.LOG[i]} \n"
        return s


class Piece:
    B_COLOR = Fore.RED
    W_COLOR = Fore.WHITE
    name = ''

    def __init__(self, color):
        self.color = color
        self.verbose = False

    def check_horizontal(self, board, move):
        begin = min(move[0][0], move[1][0])
        end = max(move[0][0], move[1][0])
        for i in range(begin + 1, end):
            if board[move[0][1]][i] is not None:
                return False
        return True

    def check_vertical(self, board, move):
        begin = min(move[0][1], move[1][1])
        end = max(move[0][1], move[1][1])
        if self.verbose:
            print(f"Attempting vertical move from {begin} to {end}.")
        for i in range(begin + 1, end):
            if board[i][move[0][0]] is not None:
                return False
        return True

    def check_diagonal(self, board, move):
        if move[0][0] - move[1][0] > 0:
            dx = -1
        else:
            dx = 1
        if move[0][1] - move[1][1] > 0:
            dy = -1
        else:
            dy = 1
        location = [move[0][0] + dx, move[0][1] + dy]
        while location != move[1]:
            if board[location[1]][location[0]] is not None:
                return False
            location[0] += dx
            location[1] += dy
        return True

    def check_directions(self, board, move, directions, fears, distance = 8):
        destination = move[1]
        for direction in directions:
            position = [destination[0] + direction[0], destination[1] + direction[1]]
            travel = 1
            while 0 <= position[0] <= 7 and 0 <= position[1] <= 7 and travel <= distance:
                if (self.verbose):
                    print(f"Checking {position} for {fears}.")
                if board[position[1]][position[0]] is not None:
                    encounter = board[position[1]][position[0]]
                    if self.verbose:
                        print(f"Found {'White' if encounter.color else 'Black'} {encounter.name}")
                    if encounter.color != self.color and encounter.name in fears:
                        if self.verbose:
                            print("Threat.")
                        return False
                    # Found a piece that wasn't a threat
                    else:
                        if self.verbose:
                            print("Not a threat.")
                        break
                position[0] += direction[0]
                position[1] += direction[1]
                travel += 1
        return True

    def printB(self, text):
        # red
        return "\033[91m" + text + "\033[00m"

    def printW(self, text):
        # cyan
        return "\033[96m" + text + "\033[00m"

    def __str__(self):
        if self.name == "Knight":
            return self.printW('N') if self.color else self.printB('n')

        return self.printW(self.name[0]) if self.color else self.printB(self.name[0].lower())


class King(Piece):
    name = "King"
    pt_val = None

    def verify_move(self, board, move):
        origin = move[0]
        destination = move[1]

        # Check that move is only one space away
        if abs(origin[0] - destination[0]) > 1 or abs(origin[1] - destination[1]) > 1:
            if self.verbose:
                print("Kings can't move more than one space.")
            return False

        # Check for Knights
        for spot in [[-2, -1], [-2, 1], [2, -1], [2, 1], [-1, -2], [-1, 2], [1, -2], [1, 2]]:
            try:
                location = [destination[1] + spot[1], destination[0] + spot[0]]
                if all(x > 0 for x in location):
                    encounter = board[location[1]][location[0]]
                    if encounter.name == "Knight" and encounter.color != self.color:
                        if self.verbose:
                            print(f"Enemy knight at {[destination[1] + spot[1], destination[0] + spot[0]]}threatens this space. You cannot move into check.")
                        return False
            except (IndexError, AttributeError):
                pass

        # Check diagonals for Bishops and Queens of the opposite color
        directions = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        fears = ["Bishop", "Queen"]
        if not self.check_directions(board, move, directions, fears):
            if self.verbose:
                print("An enemy bishop or queen occupies this diagonal. You cannot move into check.")
            return False

        # Check horizontal/vertical directions for Rooks and Queens of the opposite color
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        fears = ["Rook", "Queen"]
        if not self.check_directions(board, move, directions, fears):
            if self.verbose:
                print("An enemy rook or queen occupies this rank/file. You cannot move into check.")
            return False

        # Check for opposing pawns in the relevant spaces
        # Black king fears pawns at [1, 1] and [-1, 1] of destination
        # White king fears pawns at [1, -1] and [-1, -1]
        if self.color:
            if not self.check_directions(board, move, [[1, -1], [-1, -1]], ["Pawn"], 1):
                if self.verbose:
                    print("An enemy pawn threatens that space. You cannot move into check.")
                return False

        else:
            if not self.check_directions(board, move, [[1, 1], [-1, 1]], ["Pawn"], 1):
                if self.verbose:
                    print("An enemy pawn threatens that space. You cannot move into check.")
                return False

        # Check for presence of enemy King in any direction
        directions = [[1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1], [0, -1]]
        fears = ["King"]
        distance = 1
        if not self.check_directions(board, move, directions, fears, distance):
            if self.verbose:
                print("An enemy king threatens that space. You cannot move into check.")
                return False

        return True


class Queen(Piece):
    name = "Queen"
    pt_val = 9

    def verify_move(self, board, move):

        if move[0][0] != move[1][0] and move[0][1] != move[1][1]:
            return self.check_diagonal(board, move)

        elif move[0][0] == move[1][0]:
            return self.check_horizontal(board, move)

        elif move[0][1] == move[1][1]: 
            return self.check_vertical(board, move)

        return False


class Rook(Piece):
    name = "Rook"
    pt_val = 5

    def verify_move(self, board, move):
        origin = move[0]
        destination = move[1]

        if origin[0] == destination[0]:
            return self.check_vertical(board, move)
        elif origin[1] == destination[1]:
            return self.check_horizontal(board, move)

        return False

class Bishop(Piece):
    name = "Bishop"
    pt_val = 3

    def verify_move(self, board, move):
        return self.check_diagonal(board, move)


class Knight(Piece):
    name = "Knight"
    pt_val = 3

    def verify_move(self, board, move):
        origin = move[0]
        destination = move[1]

        if abs(origin[1] - destination[1]) == 2 and abs(origin[0] - destination[0]) == 1:
            return True
        elif abs(origin[0] - destination[0]) == 2 and abs(origin[1] - destination[1]) == 1:
            return True

        return False
    
class Pawn(Piece):
    name = "Pawn"
    pt_vl = 1

    def verify_move(self, board, move):
        origin = move[0]
        destination = move[1]
        direction = 1
        if not self.color:
            direction = -1
        
        # Forward one space (player dependent), unless blocked
        if origin[0] == destination[0] and (origin[1] - destination[1]) * direction == 1 and board[destination[1]][destination[0]] is None:
            return True
        
        # Forward two spaces (player dependent), unless blocked, and only if on starting row
        elif origin[0] == destination[0] and ((origin[1] - destination[1]) * direction) == 2 and board[destination[1]][destination[0]] is None:
            if (direction == 1 and origin[1] == 6) or (direction == -1 and origin[1] == 1):
                return True

        # diagonally forward one space (player dependent), only if taking
        elif abs(destination[0] - origin[0]) == 1 and (origin[1] - destination[1]) * direction == 1 and board[destination[1]][destination[0]] is not None:
            return True

        return False
