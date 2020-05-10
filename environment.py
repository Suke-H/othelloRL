import numpy as np
import itertools
import copy

from check import make_stalemate

class environment:
    def __init__(self):
        """
        board: 1*64の1次元配列
        空 -> 0
        黒石 -> 1
        白石 -> -1

        winner: 勝者
        ゲーム中 -> 0, 
        player1 -> 1, 
        player2 -> 2, 
        引き分け -> 3

        """
        self.board = np.zeros((8, 8))
        self.board[3, 3] = 1
        self.board[4, 4] = 1
        self.board[3, 4] = -1
        self.board[4, 3] = -1

        self.winner = 0

    def reset(self):
        """
        ゲームリセット
        """
        self.board = np.zeros((8, 8))
        self.board[3, 3] = 1
        self.board[4, 4] = 1
        self.board[3, 4] = -1
        self.board[4, 3] = -1

        self.winner = 0

    def make_hands(self, player_no):
        """
        合法手生成
        """
        stalement = []

        for x, y in itertools.product(range(8), range(8)):
            stones = self.check_hand(x, y, player_no)

            if stones > 0:
                stalement.append([x, y])

        return stalement

    def check_hand(self, x, y, player_no):
        """
        [x, y]にplayer_noの石を置いたとき、何個の石を返せるか(=stones_num)を出力

        ※コード中のdirect, put, pwdは[x, y]の順に入っているが、
          boardの(x,y)成分はboard[y][x]なので注意

        """
        # 返せる石の数
        stones_num = 0

        # tmpboard = board[:, :]
        tmpboard = copy.deepcopy(self.board)

        # directions: 上、左上、左、左下、下、右下、右、右上
        directions = np.array([[0, -1], [-1, -1], [-1, 0], [-1, 1], \
                                [0, 1], [1, 1], [1, 0], [1, -1]])
        # put:置く場所、pwd:現在位置
        put = np.array([x, y])
        pwd = np.array([x, y])

        # pwdに石があれば終わり
        if tmpboard[put[1]][put[0]] != 0:
            return 0, tmpboard

        # 8方向ごとに走査
        for direct in directions:

            # 初期化
            stone_count = 0
            pwd = np.array([x, y])

            # 一歩進んで
            pwd += direct
            # 相手の石じゃなくなるまでdirへ移動し続ける
            while tmpboard[pwd[1]][pwd[0]] == 3 - player_no:
                pwd += direct
                stone_count += 1

            # 移動した間に相手の石を通っていて、いまいる場所が自分の石なら
            if stone_count > 0 and tmpboard[pwd[1]][pwd[0]] == player_no:

                # 返せる石の数をstones_numに代入
                stones_num += stone_count

                # 一歩もどって
                pwd -= direct
                # pwd = putになるまで石を返す
                while not all(pwd == put):
                    tmpboard[pwd[1]][pwd[0]] = player_no
                    pwd -= direct

        # 1個でも返していたらputの位置に石を置いておく
        if stones_num > 0:
            tmpboard[put[1]][put[0]] = player_no

        return stones_num, tmpboard

    def get_nextboard(self, x, y):
        self.board

    def get_reward(self, action, player_no):
        """
        報酬を返す。board更新も行う

        ゲーム中 -> 0
        勝利 -> 1
        敗北 -> -1
        石の置きミス -> -1

        """
        # ゲーム中
        if self.winner == 0:

            # action(1次元配列)をx, yに変換
            x, y = action % 8, action / 8

            # 石を何個返せる手かチェック
            num, tmpboard = self.check_hand(x, y, player_no)

            # 石を返せなかったら(置きミス)報酬-1
            if num == 0:
                return -1

            # 石を返せたらboard上書きして報酬0
            self.board = tmpboard[:, :]
            return 0
            
        # 勝利で報酬1
        elif self.winner == player_no:
            return 1

        # 敗北で報酬-1
        else:
            return -1

    def check_terminate(self):
        """
        終了判定をする
        ・self.winnerに代入
        ・ゲーム中 -> 0, 終了 -> 1

        """
        # ゲーム中だったとき
        if self.winner == 0:

            # 盤が埋まってたら勝者を決める
            empty_num = len(np.where(self.board == 0)[0])
            if empty_num == 0:
            
                # 石の個数をカウント
                player1_score = player2_score = 0
                for x, y in itertools.product(range(8), range(8)):
                    if self.board[y][x] == 1:
                        player1_score += 1

                    elif self.board[y][x] == -1:
                        player2_score += 1

                # player1の勝ち
                if player1_score > player2_score:
                    self.winner = 1
                # player2の勝ち
                elif player1_score < player2_score:
                    self.winner = 2
                # 引き分け
                else:
                    self.winner = 3

                # 終了したなら1を返す
                return 1

            # ゲーム中なら0を返す
            else:
                return 0

        # 終了したなら1を返す
        else:
            return 1

    def step(self, action, player_no):
        """
        <入力>
        行動(action: 石を置く)

        <出力>
        次状態(next_state: 置いた後の盤｡1次元配列にする)
        報酬(reward: get_rewardにより返す)
        ーム終了フラグ(done: check_terminateにより返す)

        """
        # 報酬を得る、board更新も行う
        reward = self.get_reward(action, player_no)

        # 終了判定
        done = self.check_terminate()

        return self.board.reshape(64), reward, done
