import pygame
from pygame.locals import *
import numpy as np
import sys
import copy
import itertools

#合法手に赤丸を描画
def indicate_stalement(board, screen):

    stalement = make_stalemate(board, 1)

    for st in stalement:
        put_x = 30 + st[0] * 60
        put_y = 30 + st[1] * 60
        pygame.draw.circle(screen, (255,0,0), (put_x,put_y), 20, 1)

#合法手生成
def make_stalemate(board, player_no):

    stalement = []

    for x, y in itertools.product(range(1, 9), range(1, 9)):
        #print(x, y)
        stones, _ = check(board, x, y, player_no)

        if stones > 0:
            stalement.append([x, y])
            #print(board[1:9, 1:9])

    return stalement

#問題点：doneをFalseにしているのにboardが書き変わる
#今はmake_stalemate(board)において、tmpしているので問題ない
def check(board, mas_x, mas_y, player_no):

    #dir, put, pwdは[x, y]の順に入っている
    #boardの(x,y)成分はboard[y][x]なので注意
    #boardは変更可能な引数なので、tmpboardにコピーする

    tmpboard = copy.deepcopy(board)

    #上、左上、左、左下、下、右下、右、右上
    directions = np.array([[0, -1], [-1, -1], [-1, 0], [-1, 1], \
                            [0, 1], [1, 1], [1, 0], [1, -1]])
    #put:置く場所、pwd:現在位置
    put = np.array([mas_x, mas_y])
    pwd = np.array([mas_x, mas_y])
    #各dirで返せる石
    stones_num = 0

    #pwdに石があれば終わり
    if tmpboard[put[1]][put[0]] != 0:
        return 0, tmpboard

    # 8方向ごとに走査
    for i, direct in enumerate(directions):

        #初期化
        stone_count = 0
        pwd = np.array([mas_x, mas_y])
        #pwd = put[:]

        #一歩進んで
        pwd += direct

        #相手の石じゃなくなるまでdirへ移動し続ける
        while tmpboard[pwd[1]][pwd[0]] == 3 - player_no:
            pwd += direct
            stone_count += 1


        #移動した間に相手の石を通っていて、いまいる場所が自分の石なら
        if stone_count > 0 and tmpboard[pwd[1]][pwd[0]] == player_no:

            #返せる石の数をstones_numに代入
            stones_num += stone_count

            #doneがFalseなら石を裏返さない
            #if not done:
                #continue

            #一歩もどって
            pwd -= direct
            #pwd = putになるまで石を返す
            while not all(pwd == put):
                tmpboard[pwd[1]][pwd[0]] = player_no
                pwd -= direct


    #1個でも返していたらputの位置に石を置いておく
    if stones_num > 0:
        tmpboard[put[1]][put[0]] = player_no

    return stones_num, tmpboard
