"""
file: config.py
This file holds configuration options,
it also holds the initialisation of global variables
This file has to be imported in other modules 
"""

import tkinter as tk

# CONFIGURATION OPTIONS RELATED TO GAME_V1
# DISPLAY OPTIONS
WIDTH = 60      # in square
HEIGHT = 60     # in square
MARGE = 2       # affects the way gems are displayed

# GAME OPTIONS
NBR_GEMS = 200              # number of gems to set on the board for every generation
NBR_BOT = 30                # number of bots per generation
DEFAULT_SPEED = 30                    # speed of time factor
MAX_STRENGTH = 30           # maximum strength of a bot
NB_SELECT_BOT = 5
NB_TURN_GENERATION = 90     # number of turns to pass after a new generation is created
                            # (used when auto_gen is ON)
                            
SQUARE_SIZE = 10

LIST_SIZES = [4]
NBR_INPUT = 8
NO_MURDER = 0
