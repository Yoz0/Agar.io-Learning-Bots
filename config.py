"""
file: config.py
This file holds configuration options,
it also holds the initialisation of global variables
This file has to be imported in other modules 
"""

import tkinter as tk

# CONFIGURATION OPTIONS ############################################################
WIDTH = 60      # in square
HEIGHT = 60     # in square
SQUARE_SIZE = 10
NBR_GEMS = 100
NBR_BOT = 30
FPS = 20
MAX_STRENGTH = 30
NB_SELECT_BOT = 5

# GLOBAL VARIABLES #################################################################
root = tk.Tk()
canvas = tk.Canvas(root, width=WIDTH*SQUARE_SIZE, height=HEIGHT*SQUARE_SIZE, background='white')
canvas.pack(side="top")