#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import json
import logging
import random

w = [1405, -193, 201, 271, 154, -618, -121, -202, -2621, -4403]
#w = [808.2, -28.7, 9.3, 35.6, 84.4, -256.3, -22.7, -53.6, -1731.1, -3331.5]

def Evaluate(g, player, myself):
    """
    "player" refers to the person whose side we are going to evaluate this game state
    "myself" represents our side
    """
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
    
    score += (tmp_board[0][2] + tmp_board[0][5] + tmp_board[2][0] + tmp_board[2][7] 
            + tmp_board[5][0] + tmp_board[5][7] + tmp_board[7][2] + tmp_board[7][5]) * w[3]
    
    score += (tmp_board[0][3] + tmp_board[0][4] + tmp_board[3][0] + tmp_board[3][7]
            + tmp_board[4][0] + tmp_board[4][7] + tmp_board[7][3] + tmp_board[7][4]) * w[4]
    
    score += (tmp_board[1][1] + tmp_board[1][6] + tmp_board[6][1] + tmp_board[6][6]) * w[5]
    
    score += (tmp_board[1][2] + tmp_board[1][5] + tmp_board[2][1] + tmp_board[2][6]
            + tmp_board[5][1] + tmp_board[5][6] + tmp_board[6][2] + tmp_board[6][5]) * w[6]
    
    score += (tmp_board[1][3] + tmp_board[1][4] + tmp_board[3][1] + tmp_board[3][6]
            + tmp_board[4][1] + tmp_board[4][6] + tmp_board[6][3] + tmp_board[6][4]) * w[7]
    
    score += (tmp_board[2][2] + tmp_board[2][5] + tmp_board[5][2] + tmp_board[5][5]) * w[8]
    
    score += (tmp_board[2][3] + tmp_board[2][4] + tmp_board[3][2] + tmp_board[3][5] 
            + tmp_board[4][2] + tmp_board[4][5] + tmp_board[5][3] + tmp_board[5][4]) * w[9]

    numOfPieces = 0 
    for row in g._board["Pieces"]:
        for piece in row:
            if piece != 0:
                numOfPieces += 1

    if player == 2:
        score *= -1

    if myself == player:
        if numOfPieces > 50:
            return score
        else:
            print "score = ", score, " numOfPieces * 400 = ", numOfPieces * 400
            return score + numOfPieces * 400
        #return score
    else:
        return score

def MiniMax(g, depth, myself):
    """
    This function calculates the best move based on the evaluation of the player who is now in the turn
    receives game state, depth and our side
    returns the best move
    """
    if depth == 0:
        return g
    valid_moves = g.ValidMoves()
    if len(valid_moves) == 0:
        return g

    origin_g = copy.deepcopy(g)
    if g._board["Next"] == myself:
        maximum = -99999999
        for move in valid_moves:
            gnext = g.NextBoardPosition(move)
            value = Evaluate(MiniMax(gnext, depth - 1, myself), 3 - myself, myself)
            if value > maximum:
                maximum = value
                gmax = gnext
            g = copy.deepcopy(origin_g)
            return gmax

    if g._board["Next"] != myself:
        minimum = 99999999
        for move in valid_moves:
            gnext = g.NextBoardPosition(move)
            value = Evaluate(MiniMax(gnext, depth - 1, myself), myself, myself)
            if value < minimum:
                minimum = value
                gmin = gnext
            g = copy.deepcopy(origin_g)
            return gmin


##original
#def MiniMax(g, depth, player):
#    if depth == 0:
#        return Evaluate(g, player)
#    valid_moves = g.ValidMoves()
#    if len(valid_moves) == 0:
#        return Evaluate(g, player)
#
#    origin_g = copy.deepcopy(g)
#    if g._board["Next"] == player:
#        #print "my turn"
#        maximum = -99999999
#        for move in valid_moves:
#            gnext = g.NextBoardPosition(move)
#            value = MiniMax(gnext, depth - 1, player)
#            if (value > maximum):
#                maximum = value
#            g = copy.deepcopy(origin_g)
#        return maximum
#
#    if g._board["Next"] != player:
#        minimum = 99999999
#        for move in valid_moves:
#            gnext = g.NextBoardPosition(move)
#            value = MiniMax(gnext, depth - 1, player)
#            if (value < minimum):
#                minimum = value
#            g = copy.deepcopy(origin_g)
#        return minimum

def PickBestMove(g, valid_moves): ##the player who gets the turn is decided by the game
    player = g._board["Next"]
    origin_board = copy.deepcopy(g._board["Pieces"])
    best_score = -99999999
    best_move = {"Where":[1, 1] , "As":player}
    for move in valid_moves:
        #print move, " score = ", Evaluate(g)
        #print PrettyPrint(g._board["Pieces"])
        gnext = g.NextBoardPosition(move)
        value = Evaluate(MiniMax(gnext, 2, player), player, player)
        if value > best_score:
            best_score = value
            best_move = move
            print "best_move:", best_move
        g._board["Pieces"] = copy.deepcopy(origin_board)
    return best_move
