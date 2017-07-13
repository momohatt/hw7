#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import json
import logging
import random

w = [770.3, 4.2, -21.8, 64.0, -221.6, -4.0, 20.4, 22.0]

def Evaluate(g, myself): ##player: represents for whom this board is worth this point
    tmp_board = copy.deepcopy(g._board["Pieces"])
    for r in range(0, 8):
        for c in range(0, 8):
            if tmp_board[r][c] == 2:
                tmp_board[r][c] = -1
    #print(PrettyPrint(tmp_board))

    score = 0
    #for row in tmp_board:
    #    for piece in row:
    #        score += piece * w[0]

    score += (tmp_board[0][0] + tmp_board[0][7] + tmp_board[7][0] + tmp_board[7][7]) * w[0]
    score += (tmp_board[3][3] + tmp_board[3][4] + tmp_board[4][3] + tmp_board[4][4]) * w[1]
    score += (tmp_board[0][1] + tmp_board[0][6] + tmp_board[1][0] + tmp_board[1][7] 
            + tmp_board[6][0] + tmp_board[6][7] + tmp_board[7][1] + tmp_board[7][6]) * w[2]
    score += (tmp_board[0][2] + tmp_board[0][3] + tmp_board[0][4] + tmp_board[0][5]
            + tmp_board[2][0] + tmp_board[2][7] + tmp_board[3][0] + tmp_board[3][7]
            + tmp_board[4][0] + tmp_board[4][7] + tmp_board[5][0] + tmp_board[5][7] 
            + tmp_board[7][2] + tmp_board[7][3] + tmp_board[7][4] + tmp_board[7][5]) * w[3]
    score += (tmp_board[1][1] + tmp_board[1][6] + tmp_board[6][1] + tmp_board[6][6]) * w[4]
    score += (tmp_board[1][2] + tmp_board[1][3] + tmp_board[1][4] + tmp_board[1][5] 
            + tmp_board[2][1] + tmp_board[2][6] + tmp_board[3][1] + tmp_board[3][6]
            + tmp_board[4][1] + tmp_board[4][6] + tmp_board[5][1] + tmp_board[5][6] 
            + tmp_board[6][2] + tmp_board[6][3] + tmp_board[6][4] + tmp_board[6][5]) * w[5]
    score += (tmp_board[2][2] + tmp_board[2][5] + tmp_board[5][2] + tmp_board[5][5]) * w[6]
    score += (tmp_board[2][3] + tmp_board[2][4] + tmp_board[3][2] + tmp_board[3][5] 
            + tmp_board[4][2] + tmp_board[4][5] + tmp_board[5][3] + tmp_board[5][4]) * w[7]

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
        if numOfPieces > 50:
            return -0.2 * score + numOfPieces * 80
        else:
            return -1 * score


def MiniMax(g, depth, myself): ##myself: represents for whom we are to forsee the future
    if depth == 0:
        return Evaluate(g, myself)
    valid_moves = g.ValidMoves()
    if len(valid_moves) == 0:
        return Evaluate(g, myself)

    print "next : ", g._board["Next"]
    print valid_moves
    #print PrettyPrint(g._board["Pieces"])
    origin_g = copy.deepcopy(g)
    if g._board["Next"] == myself:
        print "my turn"
        maximum = -999999
        for move in valid_moves:
            gnext = g.NextBoardPosition(move)
            #print PrettyPrint(gnext._board["Pieces"])
            print "next : ", gnext._board["Next"]
            value = MiniMax(gnext, depth - 1, myself)
            if (value > maximum):
                maximum = value
            print "depth : ", depth, " maximum : ", maximum," when ", move
            g = copy.deepcopy(origin_g)
        print "depth : ", depth , " true maximum : ", maximum
        return maximum

    if g._board["Next"] != myself:
        print "opponent's turn"
        minimum = 999999
        for move in valid_moves:
            gnext = g.NextBoardPosition(move)
            #print PrettyPrint(gnext._board["Pieces"])
            print "next : " , gnext._board["Next"]
            value = MiniMax(gnext, depth - 1, myself)
            if (value < minimum):
                minimum = value
            print "depth : ", depth, " minimum : ", minimum, " when ", move
            g = copy.deepcopy(origin_g)
        print "depth: ", depth, " true minimum : ", minimum
        return minimum


def PickBestMove(g, valid_moves): ##the player who gets the turn is decided by the game
    player = g._board["Next"]
    origin_board = copy.deepcopy(g._board["Pieces"])
    best_score = -999999
    best_move = {"Where":[1, 1] , "As":player}
    for move in valid_moves:
        #print move, " score = ", Evaluate(g)
        #print PrettyPrint(g._board["Pieces"])
        gnext = g.NextBoardPosition(move)
        if MiniMax(gnext, 2, player) > best_score:
            best_score = MiniMax(gnext, 2, player)
            best_move = move
            print "best_move:", best_move
        g._board["Pieces"] = copy.deepcopy(origin_board)
    return best_move
