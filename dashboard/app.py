# Brandon Shellenberger
# 4/03/2024

# import all packages
from shiny import reactive, render
from shiny.express import input, ui
from shinyswatch import theme
from shinywidgets import render_plotly
from collections import deque
import plotly.express as px
import pandas as pd
from scipy import stats
from faicons import icon_svg
import statsapi

# Define variables
    # time interval

# test = statsapi.league_leaders('homeruns', season=2019, playerPool='rookies', limit=5)
# test = test.split('\n')
# print(test.dtype)

# Wins and Losses for KC Royals
standings = pd.DataFrame(statsapi.standings_data(103)[202]['teams'])
team = standings[standings['name'].isin(['Kansas City Royals'])]
wins = team['w']
loses = team['l']
print(wins, loses)