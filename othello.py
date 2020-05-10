import pygame
from pygame.locals import *
import sys
import numpy as np

from draw import draw_board
from check import indicate_stalement, make_stalemate, check
from init_game import init_game
from player import randomAI

# Pygameを初期化
pygame.init()
# 画面サイズ
SCREEN_SIZE = (600, 600)  
# SCREEN_SIZEの画面を作成
screen = pygame.display.set_mode(SCREEN_SIZE)
# タイトルバーの文字列をセット
pygame.display.set_caption("Othello Game")

# 10*10マス(1マス外枠)
board = np.zeros((10, 10))
# 初期設定
init_game(board, screen, 1)
# ゲーム終了時にTrueにする
stop = False
# player1が人かAIか選択
# player1 = "human"
player1 = randomAI
# player2はAIから選択
player2 = randomAI

# ゲームループ
while True:

    hands1 = make_stalemate(board, 1)

    # board描画
    draw_board(board, screen, 1, stop)
    indicate_stalement(board, screen, hands1)

    # 画面を更新
    pygame.display.update()

    # イベント処理
    for event in pygame.event.get():

        # QUIT
        if event.type == QUIT:
            sys.exit()

        # stopがTrueだとQUIT以外イベント処理しない
        if stop:
            break

        # player1が人じゃなかったらこっち
        if player1 is not "human":

            ### player1のターン ###

            # 考え中
            pygame.time.delay(1000)

            # player1がpass
            if not hands1:
                
                # player1のpass表示
                draw_board(board, screen, 1, stop, True)
                
                # player2もpassしたらゲーム終了の描画 -> ゲーム終了
                if not make_stalemate(board, 2):
                    stop = True
                    draw_board(board, screen, 1, stop)
                    break

            # AIの一手
            hand, board = player1(board, hands1, 1)
            print(1, hand)
            #print(board[1:9, 1:9])

            # board描画
            draw_board(board, screen, 1, stop)
            pygame.display.update()  # 画面を更新

            ### player2のターン ###

            # 考え中
            pygame.time.delay(1000)

            hands2 = make_stalemate(board, 2)

            # player2がpass
            if not hands2:

                # player2のpass表示
                draw_board(board, screen, 2, stop, True)
                break

            # AIの一手
            hand, board = player2(board, hands2, 2)
            print(2, hand)
            #print(board[1:9, 1:9])
            break

        # player1がpass
        elif hands1:

            # player1のpass表示
            draw_board(board, screen, 1, stop, pass_flag=True)

            # player2もpassしたらゲーム終了の描画 -> ゲーム終了
            if not make_stalemate(board, 2):
                stop = True
                draw_board(board, screen, 1, stop)
                break

            #else:
                #print(player2(board, make_stalemate(board, 2)))

        ### 以降イベント処理 ######################################################

        # 左クリックで石おく -> COMが石おくまでをここで行う
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:

            ###自分のターン###

            # クリックした場所
            pos_x, pos_y = event.pos

            # マスの場所
            mas_x = pos_x // 60
            mas_y = pos_y // 60

            print(1, mas_x, mas_y)

            # 枠外を押していたらbreak
            if mas_x <= 0 or mas_x >= 9 or mas_y <= 0 or mas_y >= 9:
                break

            # 合法手じゃなかったらbreak
            if [mas_x, mas_y] not in hands1:
                break

            # それ以外ならboardを動かす
            print(1, [mas_x, mas_y])
            stones_num, board = check(board, mas_x, mas_y, 1)
            #print(board[1:9, 1:9])

            # board描画
            draw_board(board, screen, 2, stop)
            pygame.display.update()  # 画面を更新

            ###相手のターン###

            # 考え中
            pygame.time.delay(1000)

            hands2 = make_stalemate(board, 2)

            # player2がpass
            if not hands2:

                # player2のpass表示
                draw_board(board, screen, 2, stop, True)
                break

            # AIの一手
            hand, board = player2(board, hands2, 2)
            print(2, hand)
            #print(board[1:9, 1:9])
