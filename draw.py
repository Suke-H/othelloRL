import pygame
from pygame.locals import *
import sys

import itertools

from init_game import init_game

#合法手に赤丸を描画
def indicate_stalement(big_board, screen):

    stalement = make_stalemate(big_board, 1)

    for st in stalement:
        put_x = 30 + st[0] * 60
        put_y = 30 + st[1] * 60
        pygame.draw.circle(screen, (255,0,0), (put_x,put_y), 20, 1)

def put_stone(big_board, mas_x, mas_y, player, screen):

    #石を置く座標
    put_x = 30 + mas_x * 60
    put_y = 30 + mas_y * 60

    # player1は黒石
    if player == 1:
        pygame.draw.circle(screen, (0,0,0), (put_x,put_y), 20, 0)

    # player2は白石
    else:
        pygame.draw.circle(screen, (255,255,255), (put_x,put_y), 20, 0)

def draw_board(big_board, screen, player_no, stop, pass_flag=False):
    #一度塗りつぶす
    init_game(big_board, screen, player_no, True)

    #boardを見て石を置き直す
    for x, y in itertools.product(range(1, 9), range(1, 9)):
        if big_board[y][x] != 0:
            put_stone(big_board, x, y, big_board[y][x], screen)

    #石の個数をカウント
    player1_score = player2_score = 0
    for x, y in itertools.product(range(1, 9), range(1, 9)):
        if big_board[y][x] == 1:
            player1_score += 1

        elif big_board[y][x] == 2:
            player2_score += 1

    #スコア表示
    sysfont = pygame.font.SysFont(None, 40)
    player1_score_text = sysfont.render(str(player1_score), True, (0,0,0))
    player2_score_text = sysfont.render(str(player2_score), True, (255,255,255))
    screen.blit(player1_score_text, (135,558))
    screen.blit(player2_score_text, (255,558))
    #pygame.draw.circle(screen, (0,0,0), (135,558), 3, 0)
    #pygame.draw.circle(screen, (0,0,0), (255,558), 3, 0)
    #pygame.draw.line(screen, (0,0,0), (0,570), (540,570))

    #ゲーム終了したら、どちらが勝ちかを表示
    if stop:
        if player1_score == player2_score:
            turn_text = sysfont.render("DRAW", True, (0,0,0))

        elif player1_score > player2_score:
            turn_text = sysfont.render("PLAYER1 WIN!", True, (0,0,0))

        else:
            turn_text = sysfont.render("PLAYER2 WIN!", True, (255,255,255))

    else:
        #PASS表示
        if pass_flag:
            if player_no == 1:
                turn_text = sysfont.render("PLAYER1 PASS!", True, (0,0,0))

            else:
                turn_text = sysfont.render("PLAYER2 PASS!", True, (0,0,0))

        #どっちのターンか表示
        else:
            if player_no == 1:
                turn_text = sysfont.render("PLAYER1 TURN", True, (0,0,0))

            else:
                turn_text = sysfont.render("PLAYER2 TURN", True, (255,255,255))

    #設定したテキスト表示
    screen.blit(turn_text, (345, 558))

def board_up(board):
    tmp_board = np.zeros((10,10))
    tmp_board[1:9, 1:9] = board

    return tmp_board

def board_down(big_board):
    return big_board[1:9, 1:9]
