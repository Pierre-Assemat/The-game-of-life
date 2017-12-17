#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The life game

2 rules:
- Each living block which have 2 or 3 living block around stay alive
- Each dead block which have exactly 3 living block around become alive

"""

from random import randint
import pygame
import math
import numpy as np

APP_TITLE = "The game life"
SCREEN_SIZE = [1080, 720]
RECT = True
LENGTH = 100
VITESSE = 0.6  # N = VITESSE * 10
PROBABILITY = 0.3
_oldBoard = np.zeros((LENGTH, LENGTH), int)
# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def createInitBoard(init=None):
    board = _oldBoard.copy()
    if init:
        for block in init:
            board[block[0]][block[1]] = 1
    else:
        for yIdx in range(LENGTH):
            for xIdx in range(LENGTH):
                x = randint(0, 100)
                if x < PROBABILITY * 100:
                    board[yIdx][xIdx] = 1
    return board


def countLivingBlocAround(board, X, Y):
    if board[Y][X]:
        cpt = -1  # The bloc (x, y) doesn't count
    else:
        cpt = 0
    for h in range(-1, 2):
        if not Y:
            if h == -1:
                continue
        elif Y == LENGTH - 1:
            if h == 1:
                continue
        y = Y + h
        for j in range(-1, 2):
            if not X:
                if j == -1:
                    continue
            elif X == LENGTH - 1:
                if j == 1:
                    continue
            x = X + j
            if board[y][x]:
                cpt += 1
    return cpt


def update(board):
    for yIdx in range(LENGTH):
        for xIdx in range(LENGTH):
            living_blocs = countLivingBlocAround(board, xIdx, yIdx)
            if board[yIdx][xIdx]:
                if living_blocs == 2 or living_blocs == 3:
                    continue
                board[yIdx][xIdx] = 0
            else:
                if living_blocs == 3:
                    board[yIdx][xIdx] = 1
    return board


def screenFit():
    r = SCREEN_SIZE[1]/LENGTH
    origin = (SCREEN_SIZE[0] / 2 - SCREEN_SIZE[1] / 2, 0)
    pixel_size = math.floor(r)
    return {
        'origin': origin,
        'pixel_size': pixel_size
    }


def displayBoard(board, screen, params):
    origin = params['origin']
    pixel_size = params['pixel_size']

    for y in range(LENGTH):
        for x in range(LENGTH):
            if board[y][x]:
                if RECT:
                    # [posX, posY, width, height]
                    posX = x * pixel_size + origin[0]
                    posY = y * pixel_size + origin[1]
                    pygame.draw.rect(screen, BLACK, [posX, posY, pixel_size, pixel_size])
                else:
                    pass
                    # Draw a circle
                    # pygame.draw.circle(screen, BLACK, [60, 250], 40)
    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()


def display(board):
    global _oldBoard
    # Initialize the game engine
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(APP_TITLE)

    done = False
    first = True
    # Loop until the user clicks the close button.
    clock = pygame.time.Clock()
    params = screenFit()
    cpt = 0

    while not done:
        cpt += 1
        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(VITESSE*10)

        # Exit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        # Clear the screen and set the screen background
        screen.fill(WHITE)
        if first:
            first = False
        else:
            _oldBoard = board.copy()
            board = update(board)

        displayBoard(board, screen, params)
        if np.array_equal(board, _oldBoard):
            done = True
    # Be IDLE friendly
    pygame.quit()
    return cpt


if __name__ == '__main__':
    initBoard = [(0, 0), (1, 1), (5, 6), (7, 8), (5, 6), (4, 6), (5, 5), (6, 6),
                 (23, 20), (24, 20), (24, 21), (23, 19), (5, 23), (23, 26), (43, 24), (2, 24),
                 (30, 30), (31, 31), (35, 36), (37, 38), (35, 36), (34, 36), (35, 32), (34, 43),
                 (30, 40), (31, 41), (35, 46), (37, 48), (35, 46), (34, 46), (35, 45), (36, 46)]
    board = createInitBoard(init=initBoard)
    # Display
    print(display(board))