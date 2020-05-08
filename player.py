import sys
import random
import numpy as np

from check import check

#テスト用の自動プレーヤー
def testPlayer(board, stalement):
    hand = random.choice(stalement)
    stones, board = check(board, hand[0], hand[1], 1)

    return hand, board

#ランダムに石を置くだけのAI
def randomAI(board, stalement):

    hand = random.choice(stalement)
    stones, board = check(board, hand[0], hand[1], 2)

    return hand, board
