import pygame
from pygame.locals import *
import sys
import numpy as np

from draw import draw_board
from check import indicate_stalement, make_stalemate, check
from init_game import init_game
from player import randomAI

SCREEN_SIZE = (600, 600)  # 画面サイズ

#9*9マス(1マス外枠)
board = np.array([[0 for i in range(10)] for j in range(10)])

# Pygameを初期化
pygame.init()
# SCREEN_SIZEの画面を作成
screen = pygame.display.set_mode(SCREEN_SIZE)
# タイトルバーの文字列をセット
pygame.display.set_caption("Othello Game")

#初期設定
init_game(board, screen, 1)

#ゲーム終了時にTrueにする
stop = False

# ゲームループ
while True:

    #board描画
    draw_board(board, screen, 1, stop)
    indicate_stalement(board, screen)

    pygame.display.update()  # 画面を更新

    # イベント処理
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

        if stop:
            break

        #自分がpass
        elif not make_stalemate(board, 1):

            #player1のpass表示
            draw_board(board, screen, 1, stop, True)

            if not make_stalemate(board, 2):
                stop = True
                draw_board(board, screen, 1, stop)

                break

            else:
                print(randomAI(board, make_stalemate(board, 2)))

        #クリックで石おく→COMが石おくまでをここで行う
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:

            ###自分のターン###

            x, y = event.pos

            #マスの場所
            mas_x = x // 60
            mas_y = y // 60

            print(1, mas_x, mas_y)

            #枠外を押していたらbreak
            if mas_x <= 0 or mas_x >= 9 or mas_y <= 0 or mas_y >= 9:
                break

            #合法手じゃなかったらbreak
            if [mas_x, mas_y] not in make_stalemate(board, 1):
                break

            #それ以外ならboardを動かす
            print(1, [mas_x, mas_y])
            stones, board = check(board, mas_x, mas_y, 1)
            print(board[1:9, 1:9])

            #board描画
            draw_board(board, screen, 2, stop)
            pygame.display.update()  # 画面を更新


            #待ち時間
            print(pygame.time.delay(2000))

            ###相手のターン###

            #pass
            if not make_stalemate(board, 2):
                #player2のpass表示
                draw_board(board, screen, 2, stop, True)
                break

            hand, board = randomAI(board, make_stalemate(board, 2))
            print(2, hand)
            print(board[1:9, 1:9])