# Brandon Shellenberger
# 4/03/2024

# import all packages
from shiny import reactive, render
from shiny.express import input, ui
from shinyswatch import theme
from shinywidgets import render_plotly
import plotly.express as px
import pandas as pd
from faicons import icon_svg
import mlbstatsapi


ui.page_opts(title="Kansas City Royals Season", fillable=True)

with ui.sidebar(open='open'):
    
    ui.h2("Select a range of seasons")
    
    ui.input_slider(
        'year', 
        'Seasons',
        min=00,
        max=24,
        value=[18, 24],
    )
    
    
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
def get_stats():
    """This retrieves statistics from 'mlbstatsapi.MLB' 
    and stores it in dataframes for seasonal hitting and pitching."""
    
    # makes a list of the seasons
    year = list(input.year())
    year_range = []
    for i in year:
        year_range.append(int('20' + str(i)))
    
    mlb = mlbstatsapi.Mlb()

    team_id = mlb.get_team_id('Kansas City Royals')[0]
    stats = ['season']
    groups = ['pitching', 'hitting']
    seasonal_hitting_stats = {}
    seasonal_pitching_stats = {}
    for year in range(year_range[0], year_range[1] + 1):
        params = {'season': year}

        seasonal_hitting_stats[year] = {}
        seasonal_pitching_stats[year] = {}

        # Grabs stats for the team for a certain season (stats), type (groups), and parameters (params)
        stats_dict= mlb.get_team_stats(team_id, stats=stats, groups=groups, **params)
        hitting_stats = stats_dict['hitting']['season']
        pitching_stats = stats_dict['pitching']['season']
        
        # Splits stats from a dictiononary into a dataframe
        for split in hitting_stats.splits:
            for k, v in split.stat.__dict__.items():
                seasonal_hitting_stats[year][k] = v
        
        for split in pitching_stats.splits:
            for k, v in split.stat.__dict__.items():
                seasonal_pitching_stats[year][k] = v

    seasonal_hitting_stats_df = pd.DataFrame(seasonal_hitting_stats).T
    seasonal_pitching_stats_df = pd.DataFrame(seasonal_pitching_stats).T
    
    return seasonal_hitting_stats_df, seasonal_pitching_stats_df


# Value boxes of stats for hitting, pitching, and base running seperatly
with ui.layout_columns():
    with ui.value_box(
        showcase=icon_svg("baseball-bat-ball"),
        theme = ("info")
    ):
        ui.h2("Hitting")
        @render.text
        def display_avg():
            seasonal_hitting_stats, seasonal_pitching_stats = get_stats()
            return f"Batting AVG: {seasonal_hitting_stats['avg'][2024]}"
        
        @render.text
        def display_hits():
            seasonal_hitting_stats, seasonal_pitching_stats = get_stats()
            return f"Total Hits: {seasonal_hitting_stats['hits'][2024]}"
        
        @render.text
        def display_doubles():
            seasonal_hitting_stats, seasonal_pitching_stats = get_stats()
            return f"Doubles: {seasonal_hitting_stats['doubles'][2024]}"
        
        @render.text
        def display_triples():
            seasonal_hitting_stats, seasonal_pitching_stats = get_stats()
            return f"Triples: {seasonal_hitting_stats['triples'][2024]}"
        
        @render.text
        def display_homeruns():
            seasonal_hitting_stats, seasonal_pitching_stats = get_stats()
            return f"Home Runs: {seasonal_hitting_stats['homeruns'][2024]}"

        
    with ui.value_box(
        showcase=icon_svg("baseball"),
        theme = ("info")
    ):
        ui.h2("Pitching")
        @render.text
        def display_era():
            seasonal_hitting_stats, seasonal_pitching_stats = get_stats()
            return f"ERA: {seasonal_pitching_stats['era'][2024]}"
        
        @render.text
        def display_number_of_pitches():
            seasonal_hitting_stats, seasonal_pitching_stats = get_stats()
            return f"Total Pitches: {seasonal_pitching_stats['numberofpitches'][2024]}"
        
        @render.text
        def display_batters_faced():
            seasonal_hitting_stats, seasonal_pitching_stats = get_stats()
            return f"Total Batters Faced: {seasonal_pitching_stats['battersfaced'][2024]}"
        
        @render.text
        def display_strikeouts():
            seasonal_hitting_stats, seasonal_pitching_stats = get_stats()
            return f"Total Strikeouts: {seasonal_pitching_stats['strikeouts'][2024]}"
        
        @render.text
        def display_shutouts():
            seasonal_hitting_stats, seasonal_pitching_stats = get_stats()
            return f"Total Shutouts: {seasonal_pitching_stats['shutouts'][2024]}"
        

    with ui.value_box(
        showcase=icon_svg("person-running"),
        theme = ("info")
    ):
        
        ui.h2("Base Running")
        @render.text
        def display_total_runs():
            seasonal_hitting_stats, seasonal_pitching_stats = get_stats()
            return f"Total Runs: {seasonal_hitting_stats['runs'][2024]}"
        
        @render.text
        def display_rbi():
            seasonal_hitting_stats, seasonal_pitching_stats = get_stats()
            return f"RBI: {seasonal_hitting_stats['rbi'][2024]}"
        
        @render.text
        def display_stolen_base_percentage():
            seasonal_hitting_stats, seasonal_pitching_stats = get_stats()
            return f"Stolen Base Percentage: {seasonal_hitting_stats['stolenbasepercentage'][2024]}"
        
        @render.text
        def display_obp():
            seasonal_hitting_stats, seasonal_pitching_stats = get_stats()
            return f"On-Base Percentage: {seasonal_hitting_stats['obp'][2024]}"
        
        @render.text
        def display_left_on_base():
            seasonal_hitting_stats, seasonal_pitching_stats = get_stats()
            return f"Runners Left on Base: {seasonal_hitting_stats['leftonbase'][2024]}"

with ui.navset_card_tab(id='tab'):
    with ui.nav_panel("Win-Loss"):
        @render_plotly
        def win_loss_line_graph():
            seasonal_hitting_stats, seasonal_pitching_stats = get_stats()
            
            plotly_win_loss = px.line(
                seasonal_pitching_stats,
                y=seasonal_pitching_stats['wins'] / (seasonal_pitching_stats['wins'] + seasonal_pitching_stats['losses']),
            )
            plotly_win_loss.update_layout(
                xaxis_title="Season",
                yaxis_title='Win-Loss %'
            )
            return plotly_win_loss
        
    with ui.nav_panel('Batting AVG'):
        @render_plotly
        def batting_avg():
            seasonal_hitting_stats, seasonal_pitching_stats = get_stats()
            
            plotly_batting_avg = px.line(
                seasonal_hitting_stats,
                y=seasonal_hitting_stats['avg'],
            )
            plotly_batting_avg.update_layout(
                xaxis_title="Season",
                yaxis_title='Batting AVG %'
            )
            return plotly_batting_avg
        
    with ui.nav_panel('ERA'):
        @render_plotly
        def era():
            seasonal_hitting_stats, seasonal_pitching_stats = get_stats()
            
            plotly_era = px.line(
                seasonal_pitching_stats,
                y=seasonal_pitching_stats['era'],
            )
            plotly_era.update_layout(
                xaxis_title="Season",
                yaxis_title='ERA'
            )
            return plotly_era
        
    with ui.nav_panel('Total Runs'):
        @render_plotly
        def total_runs():
            seasonal_hitting_stats, seasonal_pitching_stats = get_stats()
            
            plotly_total_runs = px.line(
                seasonal_hitting_stats,
                y=seasonal_hitting_stats['runs'],
            )
            plotly_total_runs.update_layout(
                xaxis_title="Season",
                yaxis_title='Total Runs'
            )
            return plotly_total_runs