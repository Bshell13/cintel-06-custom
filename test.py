from shiny import reactive, render
from shiny.express import input, ui
from shinyswatch import theme
from shinywidgets import render_plotly
from collections import deque
import plotly.express as px
import pandas as pd
from scipy import stats
from faicons import icon_svg
import mlbstatsapi


def hitting_stats():
    mlb = mlbstatsapi.Mlb()

    team_id = mlb.get_team_id('Kansas City Royals')[0]
    stats = ['season']
    groups = ['hitting']

    stats_dict= mlb.get_team_stats(team_id, stats=stats, groups=groups)
    hitting_stats = stats_dict['hitting']['season']

    hitting_stats_dict = {}

    for split in hitting_stats.splits:
        for k, v in split.stat.__dict__.items():
            hitting_stats_dict[k] = v

    return hitting_stats_dict


def pitching_stats():
    mlb = mlbstatsapi.Mlb()

    team_id = mlb.get_team_id('Kansas City Royals')[0]
    stats = ['season']
    groups = ['pitching']

    stats_dict= mlb.get_team_stats(team_id, stats=stats, groups=groups)
    pitching_stats = stats_dict['pitching']['season']

    pitching_stats_dict = {}

    for split in pitching_stats.splits:
        for k, v in split.stat.__dict__.items():
            pitching_stats_dict[k] = v

    return pitching_stats_dict

def getting_seasons():
    mlb = mlbstatsapi.Mlb()
    
    seasons = mlb.get_game_box_score(game_id = 534196)
    

hit_stats = hitting_stats()
pitch_stats = pitching_stats()
season_stats = getting_seasons()
print(hit_stats)