# code AI chơi cờ gánh bằng minimax
import copy
import math
from draw import draw
import random
import time
ROW = 5
COL = 5
# RED = -1
# BLUE = 1
INIT_BOARD = [[1, 1, 1, 1, 1],
              [1, 0, 0, 0, 1],
              [1, 0, 0, 0, -1],
              [-1, 0, 0, 0, -1],
              [-1, -1, -1, -1, -1]]

weight = [[1, 1, 3, 1, 1],
          [1, 7, 4, 7, 1],
          [3, 4, 8, 4, 3],
          [1, 7, 4, 7, 1],
          [1, 1, 3, 1, 1]]


class Game:
    def __init__(self, board, newBoard, player):
        self.board = board
        self.newBoard = newBoard
        self.player = player  # player turn to move next

    def gameOver(self):
        count = 0
        for i in range(ROW):
            for j in range(COL):
                count += self.newBoard[i][j]
        if count == 16 or count == -16:
            return True
        return False

    def evaluate(self):
        count_me = 0
        count_player = 0
        for i, row in enumerate(self.board):
            for j, pos in enumerate(row):
                if pos == 1:
                    count_me = count_me + \
                        weight[i][j] + len(self.getValidMove((i, j)))
                elif pos == -1:
                    count_player = count_player + \
                        weight[i][j] + len(self.getValidMove((i, j)))
        return count_me - count_player

    def oldEvaluate(self):
        count_me = 0
        count_player = 0
    #     for i, row in enumerate(self.board):
    #         for j, pos in enumerate(row):
    #             if pos == 1:
    #                 count_me += weight[i][j]
    #             elif pos == -1:
    #                 count_player += weight[i][j]
    #     return count_me - count_player
        for i in range(ROW):
            for j in range(COL):
                if self.newBoard[i][j] == 1:
                    count_me += len(self.getValidMove((i, j)))
                elif self.newBoard[i][j] == -1:
                    count_player += len(self.getValidMove((i, j)))
        return count_me - count_player

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
        if biVayList == None:
            return
        for pos in biVayList:
            self.newBoard[pos[0]][pos[1]] = -self.player

    def Ganh(self):
        start, end = self.getMove()
        x, y = end
        coupleNeighborList = self.getCoupleNeighbor(x, y)
        for coupleNeighbor in coupleNeighborList:
            if self.newBoard[coupleNeighbor[0][0]][coupleNeighbor[0][1]] == self.player and \
                    self.newBoard[coupleNeighbor[1][0]][coupleNeighbor[1][1]] == self.player:
                self.newBoard[coupleNeighbor[0][0]
                              ][coupleNeighbor[0][1]] = -self.player
                self.newBoard[coupleNeighbor[1][0]
                              ][coupleNeighbor[1][1]] = -self.player
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
        if self.board == None:
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
                    newGameList.append(newGame)
        else:
            mo = self.Mo()
            if mo is not None:
                posMove, posGanh = mo
                newBoard = copy.deepcopy(self.newBoard)
                newBoard[posMove[0][0]][posMove[0][1]] = 0
                newBoard[posMove[1][0]][posMove[1][1]] = self.player
                newBoard[posGanh[0][0]][posGanh[0][1]] = self.player
                newBoard[posGanh[1][0]][posGanh[1][1]] = self.player
                newGame = Game(self.newBoard, newBoard, self.player * -1)
                newGame.Vay()
                newGameList.append(newGame)
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
                        newGame = Game(self.newBoard, newBoard,
                                       self.player * -1)
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


def updateGame(board, start, end, player):
    newBoard = copy.deepcopy(board)
    newBoard[start[0]][start[1]] = 0
    newBoard[end[0]][end[1]] = player
    return newBoard


def minimax(game, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or game.gameOver():
        return game.evaluate(), None

    if maximizingPlayer:
        maxEval = -math.inf
        newGameList = game.getNewGameList()
        if newGameList == []:
            return -math.inf, game

        curNewGame = newGameList[0]
        for newGame in newGameList:
            curNewGame = newGame
            eval, nextGame = minimax(newGame, depth - 1, alpha, beta, False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval, curNewGame
    else:
        minEval = math.inf
        newGameList = game.getNewGameList()
        if newGameList == []:
            return math.inf, game
        curNewGame = newGameList[0]
        for newGame in newGameList:
            curNewGame = newGame
            eval, nextGame = minimax(newGame, depth - 1, alpha, beta, True)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval, curNewGame


def oldMinimax(game, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or game.gameOver():
        return game.oldEvaluate(), None

    if maximizingPlayer:
        maxEval = -math.inf
        newGameList = game.getNewGameList()
        if newGameList == []:
            return -math.inf, game

        curNewGame = newGameList[0]
        for newGame in newGameList:
            curNewGame = newGame
            eval, nextGame = minimax(newGame, depth - 1, alpha, beta, False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval, curNewGame
    else:
        minEval = math.inf
        newGameList = game.getNewGameList()
        if newGameList == []:
            return math.inf, game
        curNewGame = newGameList[0]
        for newGame in newGameList:
            curNewGame = newGame
            eval, nextGame = minimax(newGame, depth - 1, alpha, beta, True)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval, curNewGame


def goToNextState(game):
    minimaxValue, newGame = minimax(game, 4, -math.inf, math.inf, True)
    if minimaxValue == -math.inf or minimaxValue == math.inf or newGame is None:
        return None
    return newGame


def move(prev_board, board, player, remain_time_x, remain_time_o):
    game = Game(prev_board, board, player)
    nextState = goToNextState(game)
    if nextState is None:
        return None
    return nextState


def oldGoToNextState(game):
    minimaxValue, newGame = oldMinimax(game, 4, -math.inf, math.inf, False)
    if minimaxValue == -math.inf or minimaxValue == math.inf or newGame is None:
        return None
    return newGame


def oldMove(prev_board, board, player, remain_time_x, remain_time_o):
    game = Game(prev_board, board, player)
    nextState = oldGoToNextState(game)
    if nextState is None:
        return None
    return nextState


def randomMove(prev_board, board, player, remain_time_x, remain_time_o):
    game = Game(prev_board, board, player)
    newGameList = game.getNewGameList()
    if newGameList == []:
        return None
    return random.choice(newGameList)


def checkWin(board):
    countX = 0
    countO = 0
    for i in range(ROW):
        for j in range(COL):
            if board[i][j] == 1:
                countO += 1
            elif board[i][j] == -1:
                countX += 1
    if countX >= countO:
        return -1
    else:
        return 1


def main():
    prev_board = None
    board = INIT_BOARD
    player = -1
    remain_time_x = 0
    remain_time_o = 0
    step_count = 100
    draw(board)
    while True:
        nextState = move(prev_board, board, player,
                         remain_time_x, remain_time_o)

        if nextState is None:
            print("player", -player, "win")
            break
        prev_board = nextState.board
        board = nextState.newBoard

        draw(board)
        step_count -= 1
        if step_count == 0:
            print("100 step, Win player", checkWin(board))

            break
        randomNextState = oldMove(
            prev_board, board, -player, remain_time_x, remain_time_o)
        if randomNextState is None:
            print("player", player, "win")
            break
        prev_board = randomNextState.board
        board = randomNextState.newBoard
        draw(board)
        step_count -= 1
        if step_count == 0:
            print("100 step, Win player", checkWin(board))

            break
        # player *= -1


def test():
    prev_board = [
        [1, 1,  1, 1, 1],
        [1, 0, 0, 0, 1],
        [1,  0, 0, 0, -1],
        [-1, 0, 0, 0, -1],
        [-1, -1, -1, -1, -1]
    ]
    board = [
        [1, 1,  1, 1, 1],
        [1, 1, 0, 0,  1],
        [0, 0,  0, 0, -1],
        [-1, 0, 0,  0, -1],
        [-1, -1, -1, -1, -1]]
    player = -1

    game = Game(prev_board, board, player)
    nextGame = game.getNewGameList()
    for game in nextGame:
        print("+++++++++++++++++++++++++++++++++++++++")
        printBoard(game.board)
        draw(game.board)
        printBoard(game.newBoard)
        print(game.getMove())
        draw(game.newBoard)
        print(game.evaluate())
        print("+++++++++++++++++++++++++++++++++++++++")


# test()
main()
