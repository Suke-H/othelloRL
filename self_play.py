import pygame
from pygame.locals import *
import sys
import numpy as np
import torch

from draw import draw_board, indicate_legal_hands, board_down, board_up, init_game
from player import random_agent, DQNAgent
from othello_env import othello_env

env = othello_env()

SCREEN_SIZE = (600, 600)  # 画面サイズ

# #10*10マス(1マス外枠)
# big_board = np.array([[0 for i in range(10)] for j in range(10)])
#8*8マス
board = np.array([[0 for i in range(8)] for j in range(8)])

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

# 環境
env = othello_env()
# エージェント
# agent = random_agent()
agent = DQNAgent()

# モデル読み込み
agent.model.load_state_dict(torch.load('data/model_96.pth', map_location=torch.device('cpu')))

env.reset()
state_t_1, reward_t, terminal = env.observe()
legal_hands = env.legal_hands[0]

# board描画
draw_board(state_t_1, screen, 1, stop)
indicate_legal_hands(state_t_1, screen, legal_hands)

pygame.display.update()  # 画面を更新

player_no = 1

# ゲームループ
while True:

    # イベント処理
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

        # 左クリックで石おく
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:

            # 終了
            if terminal:
                stop = True
                # 終了表示
                draw_board(state_t_1, screen, 1, stop)
                # 画面を更新
                pygame.display.update()  

            # 状態を更新
            state_t = state_t_1

            print(state_t)
            print(legal_hands)

            # pass
            if len(legal_hands) == 0:
                # 合法手を相手に変える
                legal_hands = env.legal_hands[2-player_no]
                # pass表示
                draw_board(state_t, screen, player_no, stop, True)
                # 画面を更新
                pygame.display.update()  
                continue

            # エージェントが行動を決定
            action_t = agent.select_action(state_t, legal_hands)
            # 環境に行動を反映
            env.step(action_t, player_no)

            # 環境を観察
            state_t_1, reward_t, terminal = env.observe()

            # 合法手を相手に変える
            legal_hands = env.legal_hands[2-player_no]

            # board描画
            draw_board(state_t_1, screen, player_no, stop)
            indicate_legal_hands(state_t_1, screen, legal_hands)
            # 画面を更新
            pygame.display.update()

            # player_noを変更
            player_no = 3 - player_no
