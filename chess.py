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

        if ord(notation[0]) - 97 < 26:
            # lower case character leading, pawn move
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
            pass
        elif notation[0] == 'B':
            # Bishop move
            pass
        elif notation[0] == 'N':
            # Knight move
            pass

        if move_now:
            self.move((origin, destination))

        self.LOG.append(notation)
        
        return (origin, destination)

    def move(self, move):
        origin = move[0]
        destination = move[1]
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
    pass

class King(Piece):
    name = "King"
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return 'K'

    def verify_move(self, move):
        return True
    
class Queen(Piece):
    name = "Queen"
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return 'Q'

    def verify_move(self, move):
        return True
    
class Rook(Piece):
    name = "Rook"
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return 'R'

    def verify_move(self, move):
        return True
    
class Bishop(Piece):
    name = "Bishop"
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return 'B'

    def verify_move(self, move):
        return True
    
class Knight(Piece):
    name = "Knight"
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return 'N'

    def verify_move(self, move):
        return True
    
class Pawn(Piece):
    name = "Pawn"
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return 'p'

    def verify_move(self, board, move):
        origin = move[0]
        destination = move[1]
        direction = 1
        if not self.color:
            direction = -1
        print(f"Attempting to move pawn from {origin} to {destination} in direction {direction}.")
        
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
