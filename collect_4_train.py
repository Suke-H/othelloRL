import numpy as np

from othello_env import othello_env
from collect_4_env import collect_4_env
from player import random_agent 

def train(env, agent, n_epochs):
    """
    players(AI)だけでゲーム
    """

    for epoch in range(n_epochs):

        env.reset()
        state_t_1, reward_t, terminal = env.observe()
        # legal_hands = env.legal_hands[0]
        legal_hands = env.legal_hands

        while not terminal:

            for player_no in [1,2]:

                # 状態を更新
                state_t = state_t_1

                print(state_t)
                print(legal_hands)

                # pass
                if len(legal_hands) == 0:
                    # 合法手を相手に変える
                    # legal_hands = env.legal_hands[2-player_no]
                    env.make_legal_hands()
                    legal_hands = env.legal_hands
                    continue

                # player 1が勝った時用
                if terminal:
                    print("player 1 win")
                    continue

                # エージェントが行動を決定
                action_t = agent.select_action(state_t, legal_hands)

                print(action_t)
                a = input()

                # 環境に行動を反映
                env.step(action_t, player_no)

                # 環境を観察
                state_t_1, reward_t, terminal = env.observe()

                # 合法手を相手に変える
                env.make_legal_hands()
                legal_hands = env.legal_hands


if __name__ == "__main__":

    # 環境
    # env = othello_env()
    env = collect_4_env()

    # エージェント
    agent = random_agent()

    self_play(env, agent, 3)