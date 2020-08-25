import sys
import random
import numpy as np

from check import check

#ランダムに石を置くだけのAI
def randomAI(board, stalement):

    hand = random.choice(stalement)
    stones, board = check(board, hand[0], hand[1], 2)

    return hand, board