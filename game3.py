# code AI chơi cờ gánh bằng minimax
import copy
ROW = 5
COL = 5
INIT_BOARD = [[1, 1, 1, 1, 1],
              [1, 0, 0, 0, 1],
              [1, 0, 0, 0, -1],
              [-1, 0, 0, 0, -1],
              [-1, -1, -1, -1, -1]]


class Game:
    def __init__(self, board, newBoard, player):
        self.board = board
        self.newBoard = newBoard
        self.player = player  # player turn to move next

    def getMove(self):
        for i in range(ROW):
            for j in range(COL):
                if self.board[i][j] != 0 and self.newBoard[i][j] == 0:
                    start = (i, j)
                if self.board[i][j] == 0 and self.newBoard[i][j] != 0:
                    end = (i, j)
        return start, end

    def getNeighbor(self, x, y):
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

    def getCoupleNeighbor(self, x, y):
        coupleNeighborList = [
            ((x-1, y), (x+1, y)), ((x, y-1), (x, y+1)),
            ((x-1, y-1), (x+1, y+1)), ((x-1, y+1), (x+1, y-1))
        ] if (x+y) % 2 == 0 else [
            ((x, y-1), (x, y+1)), ((x-1, y), (x+1, y))
        ]
        res = []
        for coupleNeighbor in coupleNeighborList:
            if coupleNeighbor[0][0] < 0 or coupleNeighbor[0][0] >= COL or \
                    coupleNeighbor[0][1] < 0 or coupleNeighbor[0][1] >= ROW or \
                    coupleNeighbor[1][0] < 0 or coupleNeighbor[1][0] >= COL or \
                    coupleNeighbor[1][1] < 0 or coupleNeighbor[1][1] >= ROW:
                continue
            res.append(coupleNeighbor)
        return res

    def getValidMove(self, move):
        x, y = move
        getNeighbor = self.getNeighbor(x, y)
        validMoveList = []
        for neighbor in getNeighbor:
            if self.newBoard[neighbor[0]][neighbor[1]] == 0:
                validMoveList.append(neighbor)
        return validMoveList

    def getPlayerPosition(self, player):
        res = []
        for i in range(ROW):
            for j in range(COL):
                if self.newBoard[i][j] == player:
                    res.append((i, j))
        return res

    def posNotMove(self, pos):
        x, y = pos
        neighborList = self.getNeighbor(x, y)
        for neighbor in neighborList:
            if self.newBoard[neighbor[0]][neighbor[1]] == 0:
                return False
        return True

    def checkVay(self, notMoveList):
        checklist = notMoveList
        while True:
            temp = []
            for position in checklist:
                neighborList = self.getNeighbor(position[0], position[1])
                neighborList = [
                    neighbor for neighbor in neighborList
                    if self.newBoard[neighbor[0]][neighbor[1]] == self.player]
                for neighbor in neighborList:
                    if neighbor not in checklist:
                        temp.append(position)
            if temp == []:
                break
            if(len(temp) == len(checklist)):
                return None
            checklist = [pos for pos in checklist if pos not in temp]
        return checklist

    def Vay(self):
        playerPosition = self.getPlayerPosition(self.player)
        notMoveList = []
        for position in playerPosition:
            if self.posNotMove(position):
                notMoveList.append(position)
        biVayList = self.checkVay(notMoveList)
        for pos in biVayList:
            self.newBoard[pos[0]][pos[1]] = -self.player

    def Ganh(self):
        start, end = self.getMove()
        x, y = end
        coupleNeighborList = self.getCoupleNeighbor(x, y)
        for coupleNeighbor in coupleNeighborList:
            if self.newBoard[coupleNeighbor[0][0]][coupleNeighbor[0][1]] == -self.player and \
                    self.newBoard[coupleNeighbor[1][0]][coupleNeighbor[1][1]] == -self.player:
                self.newBoard[coupleNeighbor[0][0]
                              ][coupleNeighbor[0][1]] = self.player
                self.newBoard[coupleNeighbor[1][0]
                              ][coupleNeighbor[1][1]] = self.player
                return

    def checkMo(self, pos):
        x, y = pos
        coupleNeighborList = self.getCoupleNeighbor(x, y)
        posGanh = None
        for coupleNeighbor in coupleNeighborList:
            if self.newBoard[coupleNeighbor[0][0]][coupleNeighbor[0][1]] == -self.player and \
                    self.newBoard[coupleNeighbor[1][0]][coupleNeighbor[1][1]] == -self.player:
                posGanh = coupleNeighbor

        neighborList = self.getNeighbor(x, y)
        posMove = None
        for neighbor in neighborList:
            if self.newBoard[neighbor[0]][neighbor[1]] == self.player:
                posMove = (neighbor, pos)

        if posGanh is not None and posMove is not None:
            return posMove, posGanh
        return None

    def Mo(self):
        start, end = self.getMove()
        validMoveList = self.getValidMove(end)
        for validMove in validMoveList:
            mo = self.checkMo(validMove)
            if mo is not None:
                return mo
        return None

    def updateGame(self, start, end):
        self.board = self.newBoard
        self.board[start[0]][start[1]] = 0
        self.newBoard[end[0]][end[1]] = self.player
        self.player *= -1

    def getNewGameList(self):
        newGameList = []
        mo = self.Mo()
        if mo is not None:
            posMove, posGanh = mo
            newBoard = copy.deepcopy(self.newBoard)
            newBoard[posMove[0][0]][posMove[0][1]] = 0
            newBoard[posMove[1][0]][posMove[1][1]] = self.player
            newBoard[posGanh[0][0]][posGanh[0][1]] = self.player
            newBoard[posGanh[1][0]][posGanh[1][1]] = self.player
            newGameList.append(Game(self.newBoard, newBoard, self.player * -1))
        else:
            playerPosition = self.getPlayerPosition(self.player)
            for position in playerPosition:
                validMoveList = self.getValidMove(position)
                for validMove in validMoveList:
                    start = position
                    end = validMove
                    newBoard = copy.deepcopy(self.newBoard)
                    newBoard[start[0]][start[1]] = 0
                    newBoard[end[0]][end[1]] = self.player
                    newGame = Game(self.newBoard, newBoard, self.player * -1)
                    newGame.Ganh()
                    newGame.Vay()
                    newGameList.append(newGame)
        return newGameList


def printBoard(board):
    for i in range(ROW):
        for j in range(COL):
            if board[i][j] == 1:
                print(' 1', end=' ')
            elif board[i][j] == -1:
                print('-1', end=' ')
            else:
                print(' 0', end=' ')
        print()

    print("========================")


def goToNextState(game):
    newGameList = game.getNewGameList()
    if newGameList == []:
        return None
    return newGameList


def move(prev_board, board, player, remain_time_x, remain_time_o):
    game = Game(prev_board, board, player)
    newGameList = goToNextState(game)
    if newGameList is None:
        print('None')
        return None
    for newGame in newGameList:
        printBoard(newGame.newBoard)

    return newGameList


def main():
    # player = -1
    # prev_board = [
    #     [-1, 0, 1, 0, 1],
    #     [0, -1, 0, 0, 1],
    #     [1, 1, -1, 0, 0],
    #     [-1, -1, 1, 1, 1],
    #     [-1, 0, 0, -1, -1]
    # ]
    # board = [
    #     [0, 0, 1, 0, 1],
    #     [-1, -1, 0, 0, 1],
    #     [1, 1, -1, 0, 0],
    #     [-1, -1, 1, 1, 1],
    #     [-1, 0, 0, -1, -1]
    # ]

    # player = 1
    # prev_board = [
    #     [0, 0, 1, 0, 1],
    #     [-1, -1, 0, 0, 1],
    #     [-1, -1, 1, 0, 0],
    #     [-1, -1, -1, 1, 1],
    #     [-1, 1, 0, 0, 1]
    # ]
    # board = [
    #     [0, 0, 1, 0, 1],
    #     [-1, -1, 0, 0, 1],
    #     [-1, -1, 1, 0, 0],
    #     [-1, -1, 0, 1, 1],
    #     [-1, 1, -1, 0, 1]
    # ]

    # thế cờ mở
    player = -1
    prev_board = [
        [0, 0, 1, 0, 1],
        [-1, -1, 0, 0, 1],
        [-1, -1, 1, 0, 0],
        [-1, -1, 1, 1, 1],
        [-1, 1, 0, 0, 1]
    ]
    board = [
        [0, 0, 1, 0, 1],
        [-1, -1, 0, 0, 1],
        [-1, -1, 1, 0, 0],
        [-1, -1, 0, 1, 1],
        [-1, 1, 1, 0, 1]
    ]

    game = Game(prev_board, board, player)
    printBoard(game.newBoard)
    move(prev_board, board, player, 0, 0)


main()
