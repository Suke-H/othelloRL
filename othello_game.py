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
agent.model.load_state_dict(torch.load('data/model_15984.pth', map_location=torch.device('cpu')))

env.reset()
state_t_1, reward_t, terminal = env.observe()
legal_hands = env.legal_hands[0]
player_no = 1

# passしたらTrueにし、passでなかったらFalseに戻す
# Trueの時に再びpassが起きたらゲーム終了
pass_flag = False

# board描画
draw_board(state_t_1, screen, 1, stop)
indicate_legal_hands(state_t_1, screen, legal_hands)

pygame.display.update()  # 画面を更新

# ゲームループ
while True:

    # イベント処理
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

        # 左クリックで石おく
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            # 状態を更新
            state_t = state_t_1

            # print(state_t)

            # 終了
            if terminal:
                stop = True
                # 終了表示
                draw_board(state_t, screen, 1, stop)
                # 画面を更新
                pygame.display.update()  
                break

            # pass
            if len(legal_hands) == 0:
                # passフラグが立ってたらゲーム終了
                if pass_flag:
                    terminal = stop = True
                    # 終了表示
                    draw_board(state_t, screen, 1, stop)
                    # 画面を更新
                    pygame.display.update()
                    break

                else:
                    # passフラグを立てる
                    pass_flag = True
                    # 合法手を相手に変える
                    env.make_legal_hands(3-player_no)
                    legal_hands = env.legal_hands[2-player_no]
                    # pass表示
                    draw_board(state_t, screen, player_no, stop, True)
                    # 画面を更新
                    pygame.display.update()
                    # player_noを変更
                    player_no = 3 - player_no

            else:
                # クリックした場所
                x, y = event.pos
                # マスの場所
                mas_x = x // 60
                mas_y = y // 60

                # 枠外を押していたらbreak
                if mas_x <= 0 or mas_x >= 9 or mas_y <= 0 or mas_y >= 9:
                    break

                # 合法手じゃなかったらbreak
                action_t = int((mas_x-1) + (mas_y-1)*8)
                if action_t not in legal_hands:
                    break

                # デバッグ用
                # action_t = agent.select_action(state_t, legal_hands)
            
                pass_flag = False
                # 環境に行動を反映
                env.step(action_t, player_no)

                # 環境を観察
                state_t_1, reward_t, terminal = env.observe()

                # 合法手を相手に変える
                env.make_legal_hands(3-player_no)
                legal_hands = env.legal_hands[2-player_no]

                # player_noを変更
                player_no = 3 - player_no

                # board描画
                draw_board(state_t_1, screen, player_no, stop)
                indicate_legal_hands(state_t_1, screen, legal_hands)
                # 画面を更新
                pygame.display.update()
                
            ### player 2 ###    
                
            # 状態を更新
            state_t = state_t_1

            # 遅延
            pygame.time.delay(1000)

            # print(state_t)

            # 終了
            if terminal:
                stop = True
                # 終了表示
                draw_board(state_t, screen, 1, stop)
                # 画面を更新
                pygame.display.update()  
                break

            # pass
            if len(legal_hands) == 0:

                # passフラグが立ってたらゲーム終了
                if pass_flag:
                    terminal = stop = True
                    # 終了表示
                    draw_board(state_t, screen, 1, stop)
                    # 画面を更新
                    pygame.display.update()
                    break

                else:
                    # passフラグを立てる
                    pass_flag = True
                    # 合法手を相手に変える
                    env.make_legal_hands(3-player_no)
                    legal_hands = env.legal_hands[2-player_no]
                    # pass表示
                    draw_board(state_t, screen, player_no, stop, True)
                    # 画面を更新
                    pygame.display.update()

                    # 遅延
                    pygame.time.delay(1000)
                    # player_noを変更
                    player_no = 3 - player_no
                    # player1のTURN用の画面表示
                    draw_board(state_t, screen, player_no, stop)
                    indicate_legal_hands(state_t, screen, legal_hands)
                    # 画面を更新
                    pygame.display.update()
                    break

            pass_flag = False
            # エージェントが行動を決定
            action_t = agent.select_action(state_t, legal_hands)
            # 環境に行動を反映
            env.step(action_t, player_no)

            # 環境を観察
            state_t_1, reward_t, terminal = env.observe()

            # 合法手を相手に変える
            env.make_legal_hands(3-player_no)
            legal_hands = env.legal_hands[2-player_no]

            # player_noを変更
            player_no = 3 - player_no  

            # board描画
            draw_board(state_t_1, screen, player_no, stop)
            indicate_legal_hands(state_t_1, screen, legal_hands)
            # 画面を更新
            pygame.display.update()
            