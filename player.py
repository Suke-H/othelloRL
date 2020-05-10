import sys
import random
import numpy as np

from check import check

#ランダムに石を置くだけのAI
def randomAI(board, stalement, player_no):

    hand = random.choice(stalement)
    _, board = check(board, hand[0], hand[1], player_no)

    return hand, board


