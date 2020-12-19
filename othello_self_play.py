import pygame
from pygame.locals import *
import sys
import numpy as np

from draw import draw_board, indicate_stalement, board_down, board_up
from check import indicate_stalement, make_stalemate, check
from init_game import init_game
from player import randomAI, random_agent
from othello_env import othello_env

env = othello_env()

SCREEN_SIZE = (600, 600)  # 画面サイズ

#10*10マス(1マス外枠)
big_board = np.array([[0 for i in range(10)] for j in range(10)])

# Pygameを初期化
pygame.init()
# SCREEN_SIZEの画面を作成
screen = pygame.display.set_mode(SCREEN_SIZE)
# タイトルバーの文字列をセット
pygame.display.set_caption("Othello Game")

#初期設定
init_game(big_board, screen, 1)

#ゲーム終了時にTrueにする
stop = False

# ゲームループ
while True:

    # board描画
    draw_board(big_board, screen, 1, stop)
    indicate_stalement(big_board, screen)

    pygame.display.update()  # 画面を更新

    # イベント処理
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

        if stop:
            break

        ###プレイヤー1のターン###

        # プレイヤー1がpassするとき
        elif not make_stalemate(big_board, 1):

            # プレイヤー1のpass表示
            draw_board(big_board, screen, 1, stop, True)

            # プレイヤー2もpassするとき
            if not make_stalemate(big_board, 2):

                # 終了
                stop = True
                draw_board(big_board, screen, 1, stop)

                break

        # プレイヤー1の行動
        hand = random_agent(board_down(big_board), make_stalemate(big_board, 1))
        action = int(hand[0] + hand[1]*8)
        print(action)

        # 行動をboardに反映させる
        board, reward, terminate = env.step(action, 1)
        big_board = np.copy(board)

        # board描画
        draw_board(big_board, screen, 2, stop)
        # 画面を更新
        pygame.display.update()  

        #待ち時間
        print(pygame.time.delay(2000))

        ###プレイヤー2のターン###

        # pass
        if not make_stalemate(big_board, 2):
            # player2のpass表示
            draw_board(big_board, screen, 2, stop, True)
            break

        # プレイヤー2の行動
        hand = random_agent(big_board, make_stalemate(board, 2))
        action = int(hand[0] + hand[1]*8)
        print(action)

        # 行動をboardに反映させる
        board, reward, terminate = env.step(action, 1)
        big_board = np.copy(board)

        #待ち時間
        print(pygame.time.delay(2000))
