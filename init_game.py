import pygame
from pygame.locals import *
import sys
import itertools

def init_game(board, screen, player_no, flag=False):

    screen.fill((0,205,0))   # 画面を緑色で塗りつぶす

    for i in range(9):
        #タテ線
        pygame.draw.line(screen, (0,0,0), (60+60*i,60), (60+60*i,540))
        #ヨコ線
        pygame.draw.line(screen, (0,0,0), (60,60+60*i), (540,60+60*i))

    #黒点
    pygame.draw.circle(screen, (0,0,0), (180,180), 4, 0)
    pygame.draw.circle(screen, (0,0,0), (420,180), 4, 0)
    pygame.draw.circle(screen, (0,0,0), (180,420), 4, 0)
    pygame.draw.circle(screen, (0,0,0), (420,420), 4, 0)

    #得点の黒石、白石
    pygame.draw.circle(screen, (0,0,0), (90,570), 15, 0)
    pygame.draw.circle(screen, (255,255,255), (210,570), 15, 0)

    if flag:
        return

    #最初に置く石
    board[4][4] = 1
    board[4][5] = 2
    board[5][4] = 2
    board[5][5] = 1

    #番兵
    for i in range(10):
        #ヨコ
        board[0][i] = board[9][i] = -1
        #タテ
        board[i][0] = board[i][9] = -1
