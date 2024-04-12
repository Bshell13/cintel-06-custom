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
import seaborn as sns
import matplotlib.pyplot as plt
    

def get_stats():
    mlb = mlbstatsapi.Mlb()

    year = (23, 24)
    year_range = []
    for i in year:
        year_range.append(int('20' + str(i)))

    team_id = mlb.get_team_id('Kansas City Royals')[0]
    stats = ['season']
    groups = ['pitching', 'hitting']
    seasonal_hitting_stats = {}
    seasonal_pitching_stats = {}
    for year in range(year_range[0], year_range[1] + 1):
        params = {'season': year}

        seasonal_hitting_stats[year] = {}
        seasonal_pitching_stats[year] = {}

        stats_dict= mlb.get_team_stats(team_id, stats=stats, groups=groups, **params)
        hitting_stats = stats_dict['hitting']['season']
        pitching_stats = stats_dict['pitching']['season']
        
        for split in hitting_stats.splits:
            for k, v in split.stat.__dict__.items():
                seasonal_hitting_stats[year][k] = v
        
        for split in pitching_stats.splits:
            for k, v in split.stat.__dict__.items():
                seasonal_pitching_stats[year][k] = v
    
    return seasonal_hitting_stats, seasonal_pitching_stats


seasonal_hitting_stats, seasonal_pitching_stats = get_stats()
seasonal_hitting_stats_df = pd.DataFrame(seasonal_hitting_stats).T
seasonal_pitching_stats_df = pd.DataFrame(seasonal_pitching_stats)

print(seasonal_pitching_stats_df)


# sns.lineplot(
#     seasonal_hitting_stats_df,
#     x='rbi',
#     y='homeruns'
# )

# plt.show()