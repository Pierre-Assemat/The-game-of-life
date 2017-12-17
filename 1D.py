#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The life game

2 rules:
- Each living block which have 2 or 3 living block around stay alive
- Each dead block which have exactly 3 living block around become alive

"""

from random import randint
import matplotlib.pyplot as plt

print("Start")
################
#  VERSION 1D
################
"""
Rules: 
- (a) Each living block without living block around die,
- (b) Each living block with 2 living block around die
- (c) Each dead block which have 1 living block around live
"""

def createInit(init, N):
    return [
        1 if idx in init else 0
        for idx in range(0, N)
    ]

def createTab(N):
    return [
        randint(0, 1) for idx in range(0, N)
    ]


def isValid(N, tab=None):
        if tab:
            return len(tab) <= N
        return False

def update(last_turn):
    Tab = last_turn.copy()
    for idx in range(0, len(Tab)):
        front_block = None
        behind_block = None
        if idx != len(Tab) - 1:
            front_block = Tab[idx + 1]
        if idx:
            behind_block = Tab[idx - 1]
        if Tab[idx]:
            # Rule (a) and (b)
            if front_block is None:
                if not behind_block:
                    Tab[idx] = 0
            elif behind_block is None:
                if not front_block:
                    Tab[idx] = 0
            elif front_block == behind_block:
                Tab[idx] = 0
        else:
            # Rule (c)
            if front_block is None:
                if behind_block:
                    Tab[idx] = 1
            elif behind_block is None:
                if front_block:
                    Tab[idx] = 1
            elif front_block != behind_block:
                    Tab[idx] = 1
    return Tab


def diff(first, second):
    d = {}
    for k, v in second.items():
        if v and first[k]:
            d[k] = 0
        elif not v and not first[k]:
            d[k] = 0
        else:
            d[k] = 1
    return d


def display(game=None, xMax=50, yMax=50):
    if game:
        for tps in game:
            for idx in range(0, len(game[tps])):
                block = game[tps][idx]
                if block:
                    plt.plot(idx, tps, marker='x', markersize=2, color="blue")
    plt.grid(True)
    plt.axis([0, xMax, 0, yMax])
    plt.xlabel('Game evolution')
    plt.show()
        

if __name__ == '__main__':
    game = {}
    tryNum = 80
    N = 80
    # Init
    initSet = [45, 46]
    if isValid(N, initSet):
        tab = createInit(initSet, N)
    else:
        tab = createTab(N)
    game[0] = tab
    print(game[0])
    # Evolution
    for idx in range(1, tryNum + 1):
        tab2 = update(game[idx - 1])
        game[idx] = tab2
        print(game[idx])
    # Display life graph
    display(game=game, xMax=len(tab), yMax=tryNum)
