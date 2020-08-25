import argparse
import os
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from glob import glob

from catch_ball import CatchBall
from dqn_agent import DQNAgent
from train import train_dqn

# 以後アニメーションに関する関数
def init():
    img.set_array(state_t_1)
    plt.axis("off")
    return img,

def animate(step):
    global win, lose
    global state_t_1, reward_t, terminal

    if terminal:
        env.reset()

        # ログ
        if reward_t == 1:
            win += 1
        elif reward_t == -1:
            lose += 1

        print("WIN: {:03d}/{:03d} ({:.1f}%)".format(win, win + lose, 100 * win / (win + lose)))

    else:
        state_t = state_t_1

        # execute action in environment
        action_t = agent.select_action(state_t, 0.0)
        env.execute_action(action_t)

    # observe environment
    state_t_1, reward_t, terminal = env.observe()

    # animate
    img.set_array(state_t_1)
    plt.axis("off")
    return img,

if __name__ == "__main__":

    # environmetとagentを決定
    env = CatchBall()
    agent = DQNAgent(env.enable_actions, env.name)
    train_dqn(env, agent, n_epochs=1000)

    # ログ用
    win, lose = 0, 0

    # アニメーション
    state_t_1, reward_t, terminal = env.observe()

    fig = plt.figure(figsize=(env.screen_n_rows / 2, env.screen_n_cols / 2))
    fig.canvas.set_window_title("{}-{}".format(env.name, agent.name))
    img = plt.imshow(state_t_1, interpolation="none", cmap="gray")
    
    # 100フレームのアニメーションをGIF形式で保存
    ani = animation.FuncAnimation(fig, animate, init_func=init, interval=(1000 / env.frame_rate), blit=True, frames=100)
    ani.save("data/test.gif", writer = 'imagemagick')
