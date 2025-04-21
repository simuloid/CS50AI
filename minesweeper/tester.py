#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 15:56:11 2025

@author: srowe
"""

from minesweeper import *

print('============== (2,0) = 0')
ai = MinesweeperAI(3,3)
ai.add_knowledge((2,0), 0)
print(ai.knowledge)
print('safe:', ai.safes)
print('mines:', ai.mines)

print('============== (2,2) = 3')
ai = MinesweeperAI(3,3)
ai.add_knowledge((2,2), 3)
print(ai.knowledge)
print('safe:', ai.safes)
print('mines:', ai.mines)

print('============== (0,0) = 1')
ai = MinesweeperAI(3,3)
ai.add_knowledge((0,0), 1)
print(ai.knowledge)
print('safe:', ai.safes)
print('mines:', ai.mines)

print('============== AND (0,2) = 1')
ai.add_knowledge((0,2), 1)
print(ai.knowledge)
print('safe:', ai.safes)
print('mines:', ai.mines)

print('============== AND (0,1) = 1')
ai.add_knowledge((0,1), 1)
print(ai.knowledge)
print('safe:', ai.safes)
print('mines:', ai.mines)

print('============== AND (2,1) = 2')
ai.add_knowledge((2,1), 2)
print(ai.knowledge)
print('safe:', ai.safes)
print('mines:', ai.mines)
