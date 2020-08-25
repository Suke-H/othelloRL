import numpy as np

def train_dqn(env, agent, n_epochs):

    win = 0

    for e in range(n_epochs):
        # reset
        frame = 0
        loss = 0.0
        Q_max = 0.0
        env.reset()
        state_t_1, reward_t, terminal = env.observe()

        while not terminal:
            state_t = state_t_1

            # stateをDQNに入力してactionを決め、envに実行
            action_t = agent.select_action(state_t, agent.exploration)
            env.execute_action(action_t)

            # envを観察(次状態、報酬、終了状態を出力)
            state_t_1, reward_t, terminal = env.observe()

            # 経験を蓄積
            agent.store_experience(state_t, action_t, reward_t, state_t_1, terminal)

            # experience replay
            agent.experience_replay()

            # for log
            frame += 1
            loss += agent.current_loss
            Q_max += np.max(agent.Q_values(state_t))
            if reward_t == 1:
                win += 1

        if e % 100 == 0:
            print("EPOCH: {:03d}/{:03d} | WIN: {:03d} | LOSS: {:.4f} | Q_MAX: {:.4f}".format(
                e, n_epochs - 1, win, loss / frame, Q_max / frame))
