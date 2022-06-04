
import pandas as pd
from utils import process_df, mistake_per_hour

import lxml
from io import StringIO

import numpy as np

from plotly.subplots import make_subplots
import plotly.graph_objects as go

import plotly.express as px

from sklearn.linear_model import LinearRegression

years = list(range(2020, 2022))
years = list(range(2000, 2022))
years.remove(2020)

df = pd.concat((pd.read_csv('processed_data/'+str(year)+'.csv').assign(year=year)
                for year in years))

df = process_df(df, years)

print(df.describe().to_string())
print(df.info())


# we don't really care about the slow ones
# taking only people who are top n in leg times or team placement is in top n
n = 70
filtered_df = df[(df["leg_placement"].between(1, n)) |
                 (df["team_placement"].between(1, n))]



asd = df[(df["team_placement"].between(1, n))][['year', 'team_number', 'leg_number', 'leg_placement', 'team_placement']]\
    .drop_duplicates()

for i in range(1, 8):
    asdasd = asd[asd['leg_number'] == i]
    my_rho = np.corrcoef(asdasd['leg_placement'], asdasd['team_placement'])[0, 1]

    print(i, my_rho)


#asd = filtered_df.groupby(['control_id'])[['mistake_seconds', 'control_time']].mean()
#asdasd = filtered_df.groupby(['control_id'])[['control_time_baseline', 'control_time']].first()
#fig = px.scatter(x=asdasd['control_time_baseline'], y=asd['mistake_seconds'])
#fig.show()

mistake_per_leg = filtered_df.groupby(['leg_number'])[['mistake_seconds', 'control_time']].mean()
mistake_per_leg = mistake_per_hour(mistake_per_leg)
print(mistake_per_leg)


mistake_per_control_number = filtered_df[filtered_df['control_number'] <= 16]\
                                .groupby(['control_number'])[['mistake_seconds', 'control_time']].mean()
mistake_per_control_number = mistake_per_hour(mistake_per_control_number)
print(mistake_per_control_number)


mistake_per_control_number = filtered_df[filtered_df['control_number_inverse'] >= -5]\
                                .groupby(['control_number_inverse'])[['mistake_seconds', 'control_time']].mean()
mistake_per_control_number = mistake_per_hour(mistake_per_control_number)
print(mistake_per_control_number)


mistake_per_leg = filtered_df.groupby(['year'])[['mistake_seconds', 'control_time']].mean()
mistake_per_leg = mistake_per_hour(mistake_per_leg)
print(mistake_per_leg)

"""
control_type
0 from common to common
1 from fork to common
2 from common to fork
3 from fork to fork
"""

mistake_per_fork_type = filtered_df.groupby(['control_type'])[['mistake_seconds', 'control_time']].mean()
mistake_per_fork_type = mistake_per_hour(mistake_per_fork_type)
print(mistake_per_fork_type)


top_performances = filtered_df.groupby(['year', 'team_number', 'leg_number']).agg(
    {'name': 'first', 'leg_placement': 'first', 'mistake_seconds': 'sum'})
print(top_performances.sort_values('mistake_seconds').head(50).to_string())


#asd = filtered_df.groupby(['control_time_baseline'])[['control_time_baseline', 'mistake_seconds']].mean()
#fig = px.scatter(x=asd['control_time_baseline'], y=asd['mistake_seconds'])
#fig.show()


mistake_per_team_placement = filtered_df[filtered_df['team_placement'].between(1, n)]
mistake_per_team_placement = mistake_per_team_placement.groupby(['team_placement'])\
        [['team_placement', 'mistake_seconds', 'control_time']].mean()

mistake_per_team_placement = mistake_per_hour(mistake_per_team_placement)

fig = px.scatter(x=mistake_per_team_placement['team_placement'], y=mistake_per_team_placement['mistake_per_hour'])
fig.write_html("mistake_per_team_placement.html")


def winner_candidates(temp_df):
    temp_df = temp_df[temp_df['team_time'] != -1]
    temp_df = temp_df.groupby(['year', 'team_number'])\
        .agg({'team_time' : 'first',  'mistake_seconds': 'sum'})

    temp_df = temp_df.merge(temp_df.groupby('year').agg({'team_time' : 'first'}),
                            on=['year'], how='inner', suffixes=('', '_min'))

    temp_df['time_behind_first_team'] = temp_df['team_time'] - temp_df['team_time_min']
    temp_df['time_behind_without_mistakes'] = temp_df['time_behind_first_team'] - temp_df['mistake_seconds']

    #no one never has zero mistakes, calcuting with 2min mistake as optimal
    amount_of_winner_candidates = temp_df[
        (temp_df['time_behind_without_mistakes'] < -120) |
        (temp_df['time_behind_first_team'] == 0)
            ].groupby('year')['team_time'].count()

    print(amount_of_winner_candidates.to_string())



winner_candidates(df)


#top performances

# mistake / optimal time

# ero kärkeen juoksua vai virhettä
# group running per leg and team placement

def alone(temp_df: pd.DataFrame):
    """
    if at start and end of controls the clock is the same for 2 runners, they are counted as running in group whole time

    if clock same at start but not end, counted as running in group some time correlated to control time

    computationally expensive, filtering slow ones
    """
    tolerance = 8  # seconds

    df_filtered = temp_df[
        (temp_df["team_placement"].between(1, 50))
        ]
    df_others = temp_df[
        (temp_df["leg_placement"].between(1, 300))
        ][['year', 'team_number', 'control_id', 'leg_number', 'control_start_clock', 'control_time', 'name']]

    df_to_filter = df_filtered.merge(df_others, on=['control_id', 'leg_number'], how='inner', suffixes=('', '_other'))


    df_to_filter = df_to_filter[df_to_filter['year'] == df_to_filter['year_other']]
    df_to_filter = df_to_filter[df_to_filter['team_number'] != df_to_filter['team_number_other']]

    df_to_filter['clock_difference'] = df_to_filter['control_start_clock'] - df_to_filter['control_start_clock_other']

    df_to_filter = df_to_filter[np.abs(df_to_filter['clock_difference']) <= tolerance]


    df_to_filter['control_time_difference'] = df_to_filter['control_time'] - df_to_filter['control_time_other']

    df_to_filter['next_control_clock_difference'] = \
        np.abs(df_to_filter['clock_difference'] + df_to_filter['control_time_difference'])

    mask = df_to_filter['next_control_clock_difference'] < tolerance

    df_to_filter.loc[ mask, 'time_as_group'] = df_to_filter['control_time']

    df_to_filter.loc[~mask, 'time_as_group'] = \
        df_to_filter['control_time'] * (tolerance) / df_to_filter['next_control_clock_difference']


    #print(df_to_filter.sort_values('control_start_clock_other').tail(6)[['control_number', 'team_name', 'team_name_other']].to_string())

    df_to_filter = df_to_filter[['team_number', 'year', 'leg_number', 'control_number', 'time_as_group']]\
        .groupby(['team_number', 'year', 'leg_number', 'control_number']).max().reset_index()

    df_filtered = df_filtered.merge(df_to_filter[['team_number', 'year', 'leg_number', 'control_number', 'time_as_group']],
            on=['team_number', 'year', 'leg_number', 'control_number'], how='left')
    df_filtered['time_as_group'] = df_filtered['time_as_group'].fillna(0)



    asd = df_filtered[['control_type', 'time_as_group', 'control_time']].groupby('control_type').sum()
    print(asd['time_as_group'] / asd['control_time'])

    asd = df_filtered[['leg_number', 'time_as_group', 'control_time']].groupby('leg_number').sum()
    print(asd['time_as_group'] / asd['control_time'])



alone(df)
