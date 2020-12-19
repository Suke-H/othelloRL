import sys
import random
import numpy as np

from check import check

#ランダムに石を置くだけのAI
def randomAI(board, stalement):

    hand = random.choice(stalement)
    stones, board = check(board, hand[0], hand[1], 2)

    return hand, board

#ランダムに石を置くだけのAI

class random_agent:

    # def __init__(self, enable_actions):
    #     self.enable_actions = enable_actions
    #     self.n_actions = len(self.enable_actions)

    def select_action(self, state, legal_hands):

        return random.choice(legal_hands)