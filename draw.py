import pygame
import sys
import time
WIDTH = 600
MARGIN = 50
ROWS = 5
COLS = 5
ROWWIDTH = WIDTH // (ROWS - 1)
RADIUS = 20
OUTLINE = 4
FPS = 60

# ===== Set up display to visualize pathfinding =====
WIN = pygame.display.set_mode((WIDTH + MARGIN * 2, WIDTH + MARGIN * 2))
pygame.display.set_caption("Co ganh")


#  ================== Setting color  =====================
ORANGE = (255, 165, 0)          #
TURQUOISE = (64, 224, 208)      #
WHITE = (255, 255, 255)         #
BLACK = (0, 0, 0)               #
RED = (255, 0, 0)               # Red piece
PURPLE = (128, 0, 128)          #
GREEN = (0, 255, 0)             #
GREY = (128, 128, 128)          # Gridline color
YELLOW = (255, 255, 0)          # Legal move
BLUE = (0, 0, 255)            # Blue piece


def drawGridLine(self):
    # draw vertical and horizontal line
    for i in range(ROWS):
        pygame.draw.line(WIN, GREY, (0 + MARGIN, i * ROWWIDTH +
                         MARGIN), (WIDTH + MARGIN, i * ROWWIDTH + MARGIN))
    for i in range(ROWS):
        pygame.draw.line(WIN, GREY, (i * ROWWIDTH + MARGIN,
                         0 + MARGIN), (i * ROWWIDTH + MARGIN, WIDTH + MARGIN))
    # draw diagonal
    pygame.draw.line(WIN, GREY, (MARGIN, MARGIN),
                     (MARGIN + ROWWIDTH * 2, MARGIN + ROWWIDTH * 2))
    pygame.draw.line(WIN, GREY, (MARGIN + ROWWIDTH * 2, MARGIN),
                     (MARGIN + ROWWIDTH * 4, MARGIN + ROWWIDTH * 2))
    pygame.draw.line(WIN, GREY, (MARGIN, MARGIN + ROWWIDTH * 2),
                     (MARGIN + ROWWIDTH * 2, MARGIN))
    pygame.draw.line(WIN, GREY, (MARGIN + ROWWIDTH * 2, MARGIN +
                     ROWWIDTH * 2), (MARGIN + ROWWIDTH * 4, MARGIN))

    pygame.draw.line(WIN, GREY, (MARGIN, MARGIN + ROWWIDTH * 2),
                     (MARGIN + ROWWIDTH * 2, MARGIN + ROWWIDTH * 4))
    pygame.draw.line(WIN, GREY, (MARGIN + ROWWIDTH * 2, MARGIN +
                     ROWWIDTH * 2), (MARGIN + ROWWIDTH * 4, MARGIN + ROWWIDTH * 4))
    pygame.draw.line(WIN, GREY, (MARGIN, MARGIN + ROWWIDTH * 4),
                     (MARGIN + ROWWIDTH * 2, MARGIN + ROWWIDTH * 2))
    pygame.draw.line(WIN, GREY, (MARGIN + ROWWIDTH * 2, MARGIN +
                     ROWWIDTH * 4), (MARGIN + ROWWIDTH * 4, MARGIN + ROWWIDTH * 2))


def drawPlayer(x, y, player):
    x = x * ROWWIDTH + MARGIN
    y = y * ROWWIDTH + MARGIN
    if player == 1:
        pygame.draw.circle(WIN, PURPLE, (x, y), RADIUS + OUTLINE)
        pygame.draw.circle(WIN, BLUE, (x, y), RADIUS)
    else:
        pygame.draw.circle(WIN, GREY, (x, y), RADIUS + OUTLINE)
        pygame.draw.circle(WIN, RED, (x, y), RADIUS)


clock = pygame.time.Clock()


def getRowColFromMouse(pos):
    x, y = pos
    row = (y - MARGIN // 2) // ROWWIDTH
    col = (x - MARGIN // 2) // ROWWIDTH
    return row, col


def draw(board):
    WIN.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    drawGridLine(WIN)
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j] == 1:
                drawPlayer(i, j, 1)
            elif board[i][j] == -1:
                drawPlayer(i, j, -1)

    pygame.display.update()
    time.sleep(0.2)
