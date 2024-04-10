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
import mlbstatsapi

# Define variables
    # time interval

ui.page_opts(title="Kansas City Royals Season Comparison", fillable=True)

with ui.sidebar(open='open'):
    
    ui.h2("Select a range of seasons")
    
    ui.input_slider(
        'seasons', 
        'Seasons',
        min=2000,
        max=2024,
        value=[2020, 2024]
    )
    
    # check boxes for different types of hits
    
    ui.hr()
    ui.a(
        'MLB Stats API',
        href='https://github.com/zero-sum-seattle/python-mlb-statsapi',
        target='_blank'
    )
    
    ui.a(
        'GitHub',
        href='https://github.com/Bshell13/cintel-06-custom',
        target='_blank'
    )


@reactive.calc
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



with ui.layout_columns():
    with ui.value_box(
        showcase=icon_svg("baseball-bat-ball"),
        theme = ("info")
    ):
        "Current Season"
        
        @render.text
        def display_hits():
            hitting_stats_dict = hitting_stats()
            return f"Total Hits: {hitting_stats_dict['hits']}"
        
        @render.text
        def display_doubles():
            hitting_stats_dict = hitting_stats()
            return f"Doubles: {hitting_stats_dict['doubles']}"
        
        @render.text
        def display_triples():
            hitting_stats_dict = hitting_stats()
            return f"Triples: {hitting_stats_dict['triples']}"
        
        

