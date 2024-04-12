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

ui.page_opts(title="Kansas City Royals Season", fillable=True)

with ui.sidebar(open='open'):
    
    ui.h2("Select a range of seasons")
    
    ui.input_slider(
        'seasons', 
        'Seasons',
        min=00,
        max=24,
        value=[20, 24]
    )
    
    # check boxes for different types of hits
    
    ui.hr()
    ui.a(
        'Python MLB Stats API',
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

@reactive.calc
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

# @reactive.calc
# def getting_seasons():
#     mlb = mlbstatsapi.Mlb()
    
#     seasons = mlb.get_seasons(sport_id=1)
    

# Value boxes of stats for hitting, pitching, and base running seperatly
with ui.layout_columns():
    with ui.value_box(
        showcase=icon_svg("baseball-bat-ball"),
        theme = ("info")
    ):
        "Hitting"
        @render.text
        def display_avg():
            hitting_stats_dict = hitting_stats()
            return f"Batting AVG: {hitting_stats_dict['avg']}"
        
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
        
        @render.text
        def display_homeruns():
            hitting_stats_dict = hitting_stats()
            return f"Home Runs: {hitting_stats_dict['homeruns']}"

        
    with ui.value_box(
        showcase=icon_svg("baseball"),
        theme = ("info")
    ):
        "Pitching"
        @render.text
        def display_era():
            pitching_stats_dict = pitching_stats()
            return f"ERA: {pitching_stats_dict['era']}"
        
        @render.text
        def display_number_of_pitches():
            pitching_stats_dict = pitching_stats()
            return f"Total Pitches: {pitching_stats_dict['numberofpitches']}"
        
        @render.text
        def display_batters_faced():
            pitching_stats_dict = pitching_stats()
            return f"Total Batters Faced: {pitching_stats_dict['battersfaced']}"
        
        @render.text
        def display_strikeouts():
            pitching_stats_dict = pitching_stats()
            return f"Total Strikeouts: {pitching_stats_dict['strikeouts']}"
        
        @render.text
        def display_shutouts():
            pitching_stats_dict = pitching_stats()
            return f"Total Shutouts: {pitching_stats_dict['shutouts']}"
        

    with ui.value_box(
        showcase=icon_svg("person-running"),
        theme = ("info")
    ):
        
        "Base Running"
        @render.text
        def display_total_runs():
            hitting_stats_dict = hitting_stats()
            return f"Total Runs: {hitting_stats_dict['runs']}"
        
        @render.text
        def display_rbi():
            hitting_stats_dict = hitting_stats()
            return f"RBI: {hitting_stats_dict['rbi']}"
        
        @render.text
        def display_stolen_base_percentage():
            hitting_stats_dict = hitting_stats()
            return f"Stolen Base Percentage: {hitting_stats_dict['stolenbasepercentage']}"
        
        @render.text
        def display_obp():
            hitting_stats_dict = hitting_stats()
            return f"On-Base Percentage: {hitting_stats_dict['obp']}"
        
        @render.text
        def display_left_on_base():
            hitting_stats_dict = hitting_stats()
            return f"Runners Left on Base: {hitting_stats_dict['leftonbase']}"

with ui.navset_pill(id='tab'):
    with ui.nav_panel("Win-Loss"):
        @render_plotly
        def win_loss_line_graph():
            plotly_win_loss = px.line(
                ui.h2("graphs")
            )