import numpy as np
import copy

class collect_4_env:
    def __init__(self):
        """
        board: 6*7
        空 -> 0
        player1の石 -> 1
        player2の石 -> 2

        winner: 勝者
        ゲーム中, 引き分け -> 0, 
        player1 -> 1, 
        player2 -> 2, 

        """
        self.reset()

    def reset(self):
        """
        ゲームリセット
        """
        # ボード
        self.board = np.zeros((6, 7), dtype=int)

        # 合法手生成(0~6埋まってるか確認)
        self.make_legal_hands()

        self.winner = 0
        self.reward = 0
        self.terminal = False

    def make_legal_hands(self):
        """
        合法手生成(0~6埋まってるか確認)
        """

        # 一度ボードの石を全て1に
        tmpboard = np.where(self.board != 0, 1, 0)

        # 全部埋まっている列があるか確認
        check = np.sum(tmpboard, axis=0)

        # 埋まっていない列を列挙
        self.legal_hands = np.where(check < 6)[0]

    def update_board(self, action, player_no):
        """
        行動（0~6のどれか1つの列にplayer_noの石を落とす）をボードに反映
        """
        # 石を落とした時の行番号
        for i in reversed(range(6)):
            if self.board[i, action] == 0:
                row = i
                break

        # ボードを反映
        self.board[row, action] = player_no

    def check_collect_4(self, board):

        # 4*4のマスを左上から走査(4*4フィルタの畳み込みの要領)
        for i in reversed(range(3)):
            for j in range(4):
                # 4*4マスを抽出
                check_board = board[i:i+4, j:j+4]

                # 何もなかったら終わり
                if np.sum(check_board) == 0:
                    continue

                # タテ
                check = np.sum(check_board, axis=0)
                if np.count_nonzero(check == 4) != 0:
                    return True

                # ヨコ
                check = np.sum(check_board, axis=1)
                if np.count_nonzero(check == 4) != 0:
                    return True

                # ナナメ
                check_1 = np.trace(check_board)
                check_2 = np.trace(np.fliplr(check_board))
                if check_1 == 4 or check_2 == 4:
                    return True

        return False
            
    def check_terminate(self, player_no):
        """
        終了判定をする
        ・self.winnerに代入
        ・ゲーム中 -> 0, 終了 -> 1

        """
        # 石が全て埋まっていたら終了状態をTrueに
        tmpboard = np.where(self.board != 0, 1, 0)
        if np.sum(tmpboard) == 42:
            self.terminal = True

        # player1,2それぞれの石のみ存在するボードに分ける
        player_1_board = np.where(self.board==1, 1, 0)
        player_2_board = np.where(self.board==2, 1, 0)

        # 4つそろっている箇所があるかチェック
        flag_1 = self.check_collect_4(player_1_board)

        if not flag_1:
            flag_2 = self.check_collect_4(player_2_board)
        else:
            flag_2 = False

        print(flag_1, flag_2)

        # player1の勝ち
        if flag_1:
            self.winner = 1
            self.terminal = True

        # player2の勝ち
        elif flag_2:
            self.winner = 2
            self.terminal = True

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
        self.make_legal_hands()

        # 終了状態確認
        self.check_terminate(player_no)

    def observe(self):
        """
        環境を観察
        """
        return self.board, self.reward, self.terminal
