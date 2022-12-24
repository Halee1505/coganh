
import math
import copy
# (x,y)
# with x >= 0 and y >= 0 and x < COL and y < ROW
# x+y %2 == 0 => can move 8 directions
# x+y %2 == 1 => can move 4 directions
COL = 5
ROW = 5
weight = [[1, 1, 3, 1, 1],
          [1, 7, 4, 7, 1],
          [3, 4, 8, 4, 3],
          [1, 7, 4, 7, 1],
          [1, 1, 3, 1, 1]]

INITBOARD = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, -1],
    [-1, 0, 0, 0, -1],
    [-1, -1, -1, -1, -1]
]


class Game:
    def __init__(self, prev_board, board, player):
        self.prev_board = prev_board
        self.board = board
        self.player = player

    def getMove(self):
        for i in range(ROW):
            for j in range(COL):
                if self.prev_board[i][j] != 0 and self.board[i][j] == 0:
                    start = (i, j)
                if self.prev_board[i][j] == 0 and self.board[i][j] != 0:
                    end = (i, j)
        return start, end

    def gameOver(self):
        count = 0
        for i in range(ROW):
            for j in range(COL):
                count += 1
        if count == 16 or count == -16:
            return True
        else:
            return False

    def evaluate(self):
        count_me = 0
        count_player = 0
        for i, row in enumerate(self.board):
            for j, pos in enumerate(row):
                if pos == 1:
                    count_me += weight[i][j]
                elif pos == -1:
                    count_player += weight[i][j]
        return count_me - count_player

    def getNode(self, player):
        node = []
        for i in range(ROW):
            for j in range(COL):
                if self.board[i][j] == player:
                    node.append((i, j))
        return node

    def canMove(self, x, y):
        neighborList = self.asymmetricalNeighbors(x, y)
        canMove = []
        for neighbor in neighborList:
            if self.board[neighbor[0]][neighbor[1]] == 0:
                canMove.append(neighbor)
        return canMove

    def ganhMove(self, start, end, player):
        x, y = end
        burdenedNodeList = self.getNeighbor(x, y)
        for burdenedNode in burdenedNodeList:
            if self.board[burdenedNode[0][0]][burdenedNode[0][1]] == -player and \
                    self.board[burdenedNode[1][0]][burdenedNode[1][1]] == -player:
                self.board[burdenedNode[0][0]][burdenedNode[0][1]] = player
                self.board[burdenedNode[1][0]][burdenedNode[1][1]] = player

    def asymmetricalNeighbors(self, x, y):
        neighborList = [
            (x-1, y), (x+1, y), (x, y-1), (x, y+1),
            (x-1, y-1), (x+1, y+1), (x-1, y+1), (x+1, y-1)
        ] if (x+y) % 2 == 0 else [
            (x, y-1), (x, y+1), (x-1, y), (x+1, y)
        ]
        res = []
        for neighbor in neighborList:
            if neighbor[0] < 0 or neighbor[0] >= COL or \
                    neighbor[1] < 0 or neighbor[1] >= ROW:
                continue
            res.append(neighbor)
        return res

    def getNeighbor(self, x, y):
        neighborList = [
            ((x-1, y), (x+1, y)), ((x, y-1), (x, y+1)
                                   ), ((x-1, y-1), (x+1, y+1)), ((x-1, y+1), (x+1, y-1))
        ] if (x+y) % 2 == 0 else [
            ((x, y-1), (x, y+1)), ((x-1, y), (x+1, y))
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

    def isCarry(self, x, y, player):
        neighborList = self.getNeighbor(x, y)
        asymmetricalNeighbors = self.asymmetricalNeighbors(x, y)
        goFrom = None
        burdened = None

        for asymmetricalNeighbor in asymmetricalNeighbors:
            if self.board[asymmetricalNeighbor[0]][asymmetricalNeighbor[1]] == -player:
                goFrom = asymmetricalNeighbor
                break
        for neighbor in neighborList:
            if self.board[neighbor[0][0]][neighbor[0][1]] == player and \
                    self.board[neighbor[1][0]][neighbor[1][1]] == player:
                burdened = neighbor
        if goFrom is not None and burdened is not None:

            return goFrom, burdened
        else:

            return None

    def carryUpdate(self, goFrom, goTo, burdened, player):
        self.updateBoard(goFrom, goTo, player)
        self.board[burdened[0][0]][burdened[0][1]] = -player
        self.board[burdened[1][0]][burdened[1][1]] = -player

    def openMove(self, start, end,  player):
        x, y = end
        tempNeighbor = self.asymmetricalNeighbors(x, y)
        carryNodeList = []
        for neighbor in tempNeighbor:
            if self.board[neighbor[0]][neighbor[1]] == 0:
                carryNodeList.append(neighbor)
        for carryNode in carryNodeList:
            isCarry = self.isCarry(carryNode[0], carryNode[1], player)
            if isCarry is not None:
                return (carryNode[0], carryNode[1]), isCarry
        return None

    def updateBoard(self, start, end, player):
        x, y = end
        self.board[x][y] = -player
        self.board[start[0]][start[1]] = 0

    def genNewGame(self, start, end, player):
        newBoard = copy.deepcopy(self.board)
        newBoard[end[0]][end[1]] = player
        newBoard[start[0]][start[1]] = 0
        return Game(self.board, newBoard, player)

    def getNextGameList(self, player):
        playerNode = self.getNode(player)
        newGameList = []
        for node in playerNode:
            canMove = self.canMove(node[0], node[1])
            for move in canMove:
                newGame = self.genNewGame(node, move, player)
                newGameList.append(newGame)
        return newGameList


def printBoard(board):
    for i in range(ROW):
        for j in range(COL):
            if board[i][j] == 0:
                print(" 0", end=' ')
            elif board[i][j] == 1:
                print(" 1", end=' ')
            elif board[i][j] == -1:
                print("-1", end=' ')
        print()
    print("=====================================")


def minimax(game, depth, alpha, beta, maximize, player):
    if depth == 0 or game.gameOver():
        return game.evaluate(), game
    if maximize:
        maxEval = -math.inf
        maxGame = None
        for nextBoard in game.getNextGameList(player):
            eval, game = minimax(nextBoard, depth-1,
                                 alpha, beta, False, -player)
            if eval > maxEval:
                maxEval = eval
                maxGame = game
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval, maxGame
    else:
        minEval = math.inf
        minGame = None
        for nextBoard in game.getNextGameList(-player):
            eval, game = minimax(nextBoard, depth-1,
                                 alpha, beta, True, -player)
            if eval < minEval:
                minEval = eval
                minGame = game
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval, minGame


def move(prev_board, board, player, remain_time_x, remain_time_o):
    game = Game(prev_board, board, player)
    if prev_board != None:
        start, end = game.getMove()
        if game.openMove(start, end, player) is not None:
            goTo, carry = game.openMove(start, end, player)
            goFrom, burdened = carry
            game.carryUpdate(goFrom, goTo, burdened, player)

    nextGame = minimax(game, 3, -math.inf, math.inf, True, player)[1]

    return nextGame


def main():
    # prev_board = [[0, 0, 1, 0, 1],
    #               [-1, -1, 0, 0, 1],
    #               [-1, -1, 1, 0, 0],
    #               [-1, -1, 1, 1, 1],
    #               [-1, 1, 0, 0, 1]
    #               ]
    # board = [[0, 0, 1, 0, 1],
    #          [-1, -1, 0, 0, 1],
    #          [-1, -1, 1, 0, 0],
    #          [-1, -1, 0, 1, 1],
    #          [-1, 1, 1, 0, 1]
    #          ]
    prev_board = None
    board = INITBOARD

    player = 1
    while True:
        nextGame = move(prev_board, board, player, 0, 0)
        print("player: ", player)
        printBoard(nextGame.board)
        if nextGame.gameOver():
            break
        prev_board = nextGame.prev_board
        board = nextGame.board
        player = -player


main()
