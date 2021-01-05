import numpy as np
import torch

from othello_env import othello_env
from player import random_agent, DQNAgent


def train(env, agent, n_epochs):
    """
    players(AI)だけでゲーム
    """

    win = 0

    for epoch in range(n_epochs):

        # reset
        frame = 0
        loss = 0.0
        Q_max = 0.0
        env.reset()

        # passしたらTrueにし、passでなかったらFalseに戻す
        # Trueの時に再びpassが起きたらゲーム終了
        pass_flag = False

        state_t_1, reward_t, terminal = env.observe()
        legal_hands = env.legal_hands[0]

        while not terminal:
            
            for player_no in [1,2]:
                # 状態を更新
                state_t = state_t_1

                # print(state_t)
                # print(legal_hands)

                # passの時
                if len(legal_hands) == 0:

                    # passフラグが立ってたらゲーム終了
                    if pass_flag:
                        terminal = True
                        print("パスで終了")
                        break

                    else:
                        # 合法手を相手に変える
                        env.make_legal_hands(3-player_no)
                        legal_hands = env.legal_hands[2-player_no]
                        # passフラグを立てる
                        pass_flag = True
                        print("pass")
                        continue

                pass_flag = False

                # エージェントが行動を決定
                action_t = agent.select_action(state_t, legal_hands)
                # 環境に行動を反映
                env.step(action_t, player_no)

                # 環境を観察
                state_t_1, reward_t, terminal = env.observe()

                # 合法手を相手に変える
                legal_hands = env.legal_hands[2-player_no]

                # 経験を蓄積
                agent.store_experience(state_t, action_t, reward_t, state_t_1, terminal)

                # for log
                frame += 1
                loss += agent.current_loss
                Q_max += np.max(agent.Q_values(state_t))
                if reward_t == 1:
                    win += 1

        print("epoch: {}".format(epoch))

        if epoch % 16 == 0 and epoch != 0:
            # experience replay
            agent.experience_replay()
            # 保存
            torch.save(agent.model.state_dict(), 'data/model_'+str(epoch)+'.pth')
            # log
            print("EPOCH: {:05d}/{:05d} | WIN: {:03d} | LOSS: {:.4f} | Q_MAX: {:.4f}".format(
                    epoch, n_epochs, win, loss / frame, Q_max / frame))

if __name__ == "__main__":

    # 環境
    env = othello_env()
    # エージェント
    # agent = random_agent()
    agent = DQNAgent()

    train(env, agent, 17)
