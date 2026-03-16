from settings import INIT_POSITION

class Notation:
    def __init__(self, FEN_notation: str = INIT_POSITION) -> None:
        self.FEN = FEN_notation

    '''def __str__(self) -> str:
        return str(self.FEN)'''

    def as_position_array(self) -> list[str]:
        "Returns the position as an array of strings(chars)"
        position: list[str] = []
        for c in self.FEN:
            if c.isdigit():
                position += ['' for _ in range(int(c))]
            elif c != '/':
                position.append(c)
        return(position)
    
    '''def as_FEN(self) -> str:
        "Returns the FEN notation of the current positon"
        notation = ''
        for i, piece in enumerate(self.position):
            if (i)%8 == 0:
                notation += '/'
            if piece == '':
                if notation[-1].isdigit():
                    notation = notation[:-1] + str(int(notation[-1]) + 1)
                else:
                    notation += '1'
            else:
                notation += piece
        return notation[1:]'''


'''def from_FEN_notation(FEN_notation: str) -> Notation:
   return Notation(FEN_notation = FEN_notation)

def from_move_sequence(move_sequence: str) -> Notation:
    return Notation()'''