#!/usr/bin/env python
# -*- coding: utf-8 -*-
from main import Game
from main import Pos
from main import SetPos
from main import PrettyPrint
from main import PrettyMove
#from evaluate import Evaluate
from evaluate import MiniMax
from evaluate import PickBestMove

import copy
import json
import logging
import random

w = [100, 0, 0, 0, 0, 0, 0, 0]

def Evaluate(g, myself): ##player: represents for whom this board is worth this point
    tmp_board = copy.deepcopy(g._board["Pieces"])
    for r in range(0, 8):
        for c in range(0, 8):
            if tmp_board[r][c] == 2:
                tmp_board[r][c] = -1
    #print(PrettyPrint(tmp_board))

    score = 0
    for row in tmp_board:
        for piece in row:
            score += piece * w[0]

    score += (tmp_board[0][0] + tmp_board[0][7] + tmp_board[7][0] + tmp_board[7][7]) * w[1]
    score += (tmp_board[0][1] + tmp_board[0][6] + tmp_board[1][0] + tmp_board[1][7] 
            + tmp_board[6][0] + tmp_board[6][7] + tmp_board[7][1] + tmp_board[7][6]) * w[2]
    score += (tmp_board[0][2] + tmp_board[0][5] + tmp_board[2][0] + tmp_board[2][7]
            + tmp_board[5][0] + tmp_board[5][7] + tmp_board[7][2] + tmp_board[7][5]) * w[3]
    score += (tmp_board[
    score += (tmp_board[3][3] + tmp_board[3][4] + tmp_board[4][3] + tmp_board[4][4]) * w[2]
    score += (tmp_board[

    numOfPieces = 0 
    for row in g._board["Pieces"]:
        for piece in row:
            if piece != 0:
                numOfPieces += 1

    if myself == 1:
        if numOfPieces > 50:
            return score
        else:
            return score * 0.2 + numOfPieces * 80
    else:
        return -1 * score


def SA():
