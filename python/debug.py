#!/usr/bin/env python
# -*- coding: utf-8 -*-

from main import Game
from main import Pos
from main import SetPos
from main import Evaluate
from main import MiniMax
from main import PickBestMove
from main import PrettyPrint
from main import PrettyMove

import copy
import json
import logging
import random

w = [100, 610.2, -112.3, -194.9]

def main():
    f = open('./input.json', 'r')
    g = Game(f.read())
    gtmp = Game(f.read())
    #print g._board
    f.close()
    pickMove(g)
    #test(gtmp)

def pickMove(g):
    valid_moves = g.ValidMoves()
    if len(valid_moves) == 0:
        print "PASS"
    else:
        move = PickBestMove(g, valid_moves)
        print "NEXT MOVE : ", PrettyMove(move)

#def test(g):
#    move1 = {"Where": [4, 3], "As": 1}
#    print "------test start------"
#    if g.NextBoardPosition(move1):
#        gnext = g.NextBoardPosition(move1)
#        print PrettyPrint(gnext._board["Pieces"])
#    print "------test finish-----"

if __name__ == '__main__':
    main()
