import numpy as np
import itertools
import copy

class othello_env:
    def __init__(self):
        """
        board: 8*8
        空 -> 0
        player1の石 -> 1
        player2の石 -> 2

        winner: 勝者
        ゲーム中, 引き分け -> 0, 
        player1 -> 1, 
        player2 -> 2, 

        """
        # ボード(2次元配列)
        self.board = np.zeros((8, 8), dtype=int)
        self.board[3, 3] = 1
        self.board[4, 4] = 1
        self.board[3, 4] = 2
        self.board[4, 3] = 2

        # 合法手(player1, 2の合法手)
        self.legal_hands = [0, 0]
        self.make_legal_hands(1)
        self.make_legal_hands(2)

        self.winner = 0
        self.reward = 0
        self.terminal = False

    def reset(self):
        """
        ゲームリセット
        """
        # ボード
        self.board = np.zeros((8, 8), dtype=int)
        self.board[3, 3] = 1
        self.board[4, 4] = 1
        self.board[3, 4] = 2
        self.board[4, 3] = 2

        # 合法手(player1, 2の合法手)
        self.legal_hands = [0, 0]
        self.make_legal_hands(1)
        self.make_legal_hands(2)

        self.winner = 0
        self.reward = 0
        self.terminal = False

    def make_legal_hands(self, player_no):
        """
        合法手生成
        player_no: 1 or 2
        """
        hands = []

        # 1マスずつチェック
        for action in range(64):

            # 合法手だったら追加
            if self.is_regal_hand(action, player_no):
                hands.append(action)

        self.legal_hands[player_no-1] = np.array(hands)

    def is_regal_hand(self, action, player_no):
        """
        行動が合法手かチェック

        """
        # actionをx, yに変換
        x, y = int(action % 8)+1, int(action // 8)+1

        # 返せる石の数
        stones_num = 0

        # 走査のために外枠1マス追加
        tmpboard = np.zeros((10,10), dtype=int)
        tmpboard[1:9, 1:9] = self.board

        # directions: 上、左上、左、左下、下、右下、右、右上
        directions = np.array([[0, -1], [-1, -1], [-1, 0], [-1, 1], \
                                [0, 1], [1, 1], [1, 0], [1, -1]])
        # put:置く場所、pwd:現在位置
        put = np.array([x, y])
        pwd = np.array([x, y])

        # pwdに石があれば終わり
        if tmpboard[put[1]][put[0]] != 0:
            return False

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

            # 移動した間に相手の石を通っていて、いまいる場所が自分の石なら合法手である
            if stone_count > 0 and tmpboard[pwd[1]][pwd[0]] == player_no:
                return True

        return False

    def update_board(self, action, player_no):
        """
        行動（[x, y]にplayer_noの石を置く）をボードに反映

        """
        # actionをx, yに変換
        x, y = int(action % 8)+1, int(action // 8)+1

        # 返せる石の数
        stones_num = 0

        # 走査のために外枠1マス追加
        tmpboard = np.zeros((10,10), dtype=int)
        tmpboard[1:9, 1:9] = self.board

        # directions: 上、左上、左、左下、下、右下、右、右上
        directions = np.array([[0, -1], [-1, -1], [-1, 0], [-1, 1], \
                                [0, 1], [1, 1], [1, 0], [1, -1]])
        # put:置く場所、pwd:現在位置
        put = np.array([x, y])
        pwd = np.array([x, y])

        # pwdに石があれば終わり
        if tmpboard[put[1]][put[0]] != 0:
            return

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

        # ボードを反映
        self.board = tmpboard[1:9, 1:9]
            
    def check_terminate(self, player_no):
        """
        終了判定をする
        ・self.winnerに代入
        ・ゲーム中 -> 0, 終了 -> 1

        """
        
        # 盤が埋まってたら勝者を決める
        empty_num = np.count_nonzero(self.board == 0)
        
        if empty_num != 0:
            return
        
        # 終了状態をTrueに
        self.terminal = True

        # 石の個数をカウント
        player1_score = np.count_nonzero(self.board == 1)
        player2_score = np.count_nonzero(self.board == 2)

        # player1の勝ち
        if player1_score > player2_score:
            self.winner = 1

        # player2の勝ち
        elif player1_score < player2_score:
            self.winner = 2

        # 引き分けは処理なし

        # 勝利でreward 1
        if self.winner == player_no:
            self.reward = 1

        # 敗北でreward -1 (player_noが1なら2、2なら1)
        elif self.winner == 3 - player_no:
            self.reward = -1

        # 引き分けは処理なし

    def step(self, action, player_no):
        """
        <入力>
        action(行動、0~63)
        player_no(1か2)

        <出力>
        次状態、報酬、ゲーム終了フラグ

        """

        # 行動をボードに反映
        self.update_board(action, player_no)

        # 相手の合法手生成
        self.make_legal_hands(3-player_no)

        # 終了状態確認
        self.check_terminate(player_no)

    def observe(self):
        """
        環境を観察
        """
        return self.board, self.reward, self.terminal

