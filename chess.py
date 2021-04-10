import copy


class Board:
    BLACK = 0
    WHITE = 1
    TURN = 1
    LOG = []

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

    def __str__(self):
        s = '  +---+---+---+---+---+---+---+---+ \n'
        for y in range(len(self.board)):
            s += str(8 - y) + ' | '
            for x in range(len(self.board[y])):
                if self.board[y][x] is None:
                    s += '  | '
                else:
                    s += str(self.board[y][x]) + ' | '
            s += '\n  +---+---+---+---+---+---+---+---+ \n'
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
                        if self.TURN == piece.color and piece.name == "Pawn":
                            print(f"moving {piece} to {notation}")
                            origin = [x, y]
                            if TAKES:
                                destination = [self.col(notation[2]), 8 - int(notation[-1])]
                            else:
                                destination = [x, 8 - int(notation[-1])]

        elif notation[0] == 'K':
            # King move
            pass
        elif notation[0] == 'Q':
            # Queen move
            pass
        elif notation[0] == 'R':
            # Rook move
            destination = [self.col(notation[-2]), 8 - int(notation[-1])]
            # there's definitely a better way to find this rook...
            for y in range(len(self.board)):
                for x in range(len(self.board[y])):
                    if self.board[y][x] is not None:
                        piece = copy.deepcopy(self.board[y][x])
                        if self.TURN == piece.color and piece.name == "Rook":
                            print(f"{piece} is at {x}, {y}")
                            if x == destination[0] or y == destination[1]:
                                if origin == []:
                                    origin = [x, y]
                                else:
                                    if len(notation) < 4:
                                        print("Please use the row/column to clarify which rook to move.")
                                        origin = []
                                    elif isinstance(notation[1], str):
                                        if x == self.col(notation[1]): 
                                            origin = [x, y]
                                    elif y == 8 - int(notation[1]):
                                        origin = [x, y]
        elif notation[0] == 'B':
            # Bishop move
            pass
        elif notation[0] == 'N':
            # Knight move
            destination = [self.col(notation[-2]), 8 - int(notation[-1])]
            # there's definitely a better way to find this knight...
            for y in range(len(self.board)):
                for x in range(len(self.board[y])):
                    piece = copy.deepcopy(self.board[y][x])
                    if piece is not None:
                        if self.TURN == piece.color and piece.name == "Knight":
                            print(f"{piece} is at {x}, {y}")
                            if abs(y - destination[1]) == 2 and abs(x - destination[0]) == 1 or abs(x - destination[0]) == 2 and abs(y- destination[1]) == 1:
                                origin = [x, y]
                                print(origin)

        if origin == [] or destination == [] or origin == destination:
            print("Sorry, that move appears to be invalid.")
            return None

        if TAKES and self.board[origin[1]][origin[0]].color == self.board[destination[1]][destination[0]].color:
            print("You're not allowed to take your own piece.")
            return None

        if move_now:
            self.move((origin, destination))

        self.LOG.append(notation)
        
        return (origin, destination)

    def move(self, move):
        origin = move[0]
        destination = move[1]
        print(origin)
        print(destination)
        piece = copy.deepcopy(self.board[origin[1]][origin[0]])
        if piece.verify_move(self.board, move):
            self.board[origin[1]][origin[0]] = None
            self.board[destination[1]][destination[0]] = piece
            self.end_turn()
            return True
        else:
            self.invalid_move(move)
        return False

    def end_turn(self):
        if self.TURN:
            self.TURN = 0
        else:
            self.TURN = 1

    def invalid_move(self, move):
        print("This move is not valid, please enter a valid move.")
        return True

    def log(self):
        s = ""
        for i in range(len(self.LOG)):
            if i % 2 == 0:
                s += f"{i // 2 + 1}. {self.LOG[i]}    {self.LOG[i+1]}"
        print(s)
        return s


class Piece:
    def __init__(self, color):
        self.color = color

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
        print(f"Attempting vertical move from {begin} to {end}.")
        for i in range(begin + 1, end):
            if board[i][move[0][0]] is not None:
                return False
        return True

    def check_diagonal(self, board, move):
        return True



class King(Piece):
    name = "King"
    pt_val = None

    def __str__(self):
        if self.color > 0:
            return 'K'
        else:
            return 'k'

    def verify_move(self, move):
        return True


class Queen(Piece):
    name = "Queen"
    pt_val = 9

    def __str__(self):
        if self.color > 0:
            return 'Q'
        else:
            return 'q'

    def verify_move(self, move):
        return True


class Rook(Piece):
    name = "Rook"
    pt_val = 5

    def __str__(self):
        if self.color > 0:
            return 'R'
        else:
            return 'r'

    def verify_move(self, board, move):
        origin = move[0]
        destination = move[1]

        if origin[0] == destination[0] and self.check_vertical(board, move):
            return True
        elif origin[1] == destination[1] and self.check_horizontal(board, move):
            return True
        return False

class Bishop(Piece):
    name = "Bishop"
    pt_val = 3

    def __str__(self):
        if self.color > 0:
            return 'B'
        else:
            return 'b'

    def verify_move(self, move):
        return True


class Knight(Piece):
    name = "Knight"
    pt_val = 3

    def __str__(self):
        if self.color > 0:
            return 'N'
        else:
            return 'n'

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

    def __str__(self):
        if self.color > 0:
            return 'P'
        else:
            return 'p'

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
