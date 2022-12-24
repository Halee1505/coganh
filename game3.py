ROW = 5
COL = 5


class Game:
    def __init__(self, board, newBoard, player):
        self.board = board
        self.newBoard = newBoard
        self.player = player
        self.moveList = []
        self.moveList.append((board, newBoard, player))

    def getNeighbor(self, x, y):
        neighborList = [
            (x-1, y), (x+1, y), (x, y-1), (x, y+1),
            (x-1, y-1), (x+1, y+1), (x-1, y+1), (x+1, y-1)
        ] if (x+y) % 2 == 0 else [
            (x, y-1), (x, y+1), (x-1, y), (x+1, y)
        ]
        res = []
        for neighbor in neighborList:
            if neighbor[0][0] < 0 or neighbor[0][0] >= COL or \
                    neighbor[0][1] < 0 or neighbor[0][1] >= ROW or \
                    neighbor[1][0] < 0 or neighbor[1][0] >= COL or \
                    neighbor[1][1] < 0 or neighbor[1][1] >= ROW:
                continue
            res.append(neighbor)
        return res

    def getValidMove(self, move):
        x, y = move
        getNeighbor = self.getNeighbor(x, y)
        validMoveList = []
        for neighbor in getNeighbor:
            if self.board[neighbor[0]][neighbor[1]] == 0:
                validMoveList.append(neighbor)
        return validMoveList
