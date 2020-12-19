import numpy as np

from othello_env import othello_env
from player import random_agent 

def self_play(env, agent, n_epochs):
    """
    players(AI)だけでゲーム
    """

    env.reset()
    state_t_1, reward_t, terminal = env.observe()
    legal_hands = env.legal_hands[0]

    for epoch in range(n_epochs):

        while not terminal:

            for player_no in [1,2]:
                # 状態を更新
                state_t = state_t_1

                print(state_t)
                print(legal_hands)

                # pass
                if len(legal_hands) == 0:
                    # 合法手を相手に変える
                    legal_hands = env.legal_hands[2-player_no]
                    continue

                # エージェントが行動を決定
                action_t = agent.select_action(state_t, legal_hands)
                # 環境に行動を反映
                env.step(action_t, player_no)

                # 環境を観察
                state_t_1, reward_t, terminal = env.observe()

                # 合法手を相手に変える
                legal_hands = env.legal_hands[2-player_no]

                a = input()

    print(state_t_1)

if __name__ == "__main__":

    # 環境
    env = othello_env()
    # エージェント
    agent = random_agent()

    self_play(env, agent, 1)

