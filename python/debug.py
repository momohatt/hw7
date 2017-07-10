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

def pickMove(g):
    valid_moves = g.ValidMoves()
    if len(valid_moves) == 0:
        print "PASS"
    else:
        move = PickBestMove(g, valid_moves)
        print PrettyMove(move)

def main():
    f = open('./input.json', 'r')
    g = Game(f.read())
    print g._board
    f.close()
    pickMove(g)


if __name__ == '__main__':
    main()
