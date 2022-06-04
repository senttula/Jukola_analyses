
import pandas as pd
import numpy as np


def mistake_per_hour(temp_df):
    temp_df['mistake_per_hour'] = temp_df['mistake_seconds'] / temp_df['control_time'] * 3600
    return temp_df


def process_df(temp_df, years):
    # categorical dtype saves memory
    temp_df = temp_df.astype({
        'team_name': 'category',
        'name': 'category',
        'control_id': 'category'
    })


    temp_df = remove_last_control(temp_df)

    temp_df = add_clock(temp_df, years)

    temp_df = add_control_numbers(temp_df)

    temp_df = add_leg_placement(temp_df)

    temp_df = add_topteam_control_baseline(temp_df)

    temp_df = filter_buggy_emits(temp_df)

    temp_df = add_control_placement(temp_df)

    temp_df = add_control_baseline(temp_df)

    temp_df = add_person_controls_baseline(temp_df)

    temp_df = add_mistake_seconds(temp_df)
    return temp_df

def remove_last_control(temp_df):
    """
    This notebook is meant to filter and add baselines for normal controls, removing last control makes sense
    """
    number_of_controls_before = temp_df[['control_id']].drop_duplicates().shape[0]
    control_ids_to_remove = temp_df.sort_values(['year', 'leg_number', 'control_number'])\
        .groupby(['year', 'leg_number']).tail(1)[['control_id']].drop_duplicates()

    control_ids_to_remove['to_remove'] = 1

    temp_df = temp_df.merge(control_ids_to_remove, on=['control_id'], how='left')

    temp_df = temp_df[temp_df['to_remove'].isna()].drop(columns='to_remove')

    number_of_controls_after = temp_df[['control_id']].drop_duplicates().shape[0]

    print('removed last controls, control count: '+ str(number_of_controls_before) + ' -> '
          + str(number_of_controls_after))

    return temp_df


def add_control_numbers(temp_df):
    """
    adds the total number of controls in course
    adds the control number from the finish
    legs might have different number of controls depending on forking, taking the max
    """
    n_controls = temp_df.groupby(['year', 'leg_number'])['control_number'].max()

    temp_df = temp_df.merge(n_controls.rename("n_controls"), on=['year', 'leg_number'])

    temp_df['control_number_inverse'] = temp_df['control_number'] - temp_df['n_controls']

    return temp_df


def add_leg_placement(return_df):
    temp_df = return_df[['year', 'team_number', 'leg_number', 'leg_time']].drop_duplicates()
    temp_df['leg_time'] = temp_df['leg_time'].replace(-1, 99999)
    temp_df["leg_placement"] = temp_df.groupby(['year', "leg_number"])["leg_time"].rank("dense").astype('int32')
    return_df = return_df.merge(temp_df, on=['year', 'team_number', 'leg_number', 'leg_time'])
    return return_df


def add_topteam_control_baseline(temp_df):
    """
    As first baseline for control times we take the best times from top teams
    This is used to filter out everyone that has buggy emit clock

    top 5 times from top 30 teams
    """
    topteam_control_times = temp_df[temp_df["team_placement"].between(1, 30)] \
        .sort_values(['control_id', 'control_time']) \
        .groupby(['control_id']).head(5) \
        .groupby(['control_id'])['control_time'].mean()

    temp_df = temp_df.join(topteam_control_times, on='control_id', rsuffix='_topteam')
    temp_df['control_time_topteam_percent'] = temp_df['control_time'] / temp_df['control_time_topteam']

    return temp_df


def filter_buggy_emits(temp_df):
    """
    best control_times can be around 0.9 of the control_time_topteam and can be achieved by anyone
    but achieving multiple these time or having times half the control_time_topteam is sign of emit clock failure
    """

    people_to_remove = temp_df[temp_df["control_time_topteam_percent"] <= 0.9] \
        .groupby(['year', 'team_number', 'leg_number']) \
        .agg(control_min=('control_time_topteam_percent', 'min'),
             control_count=('control_time_topteam_percent', 'count'),
             control_mean=('control_time_topteam_percent', 'mean'),
             team_placement=('team_placement', 'first'),
             leg_placement=('leg_placement', 'first')) \
        .reset_index().dropna()

    # some tolerance for top runners and teams
    people_to_remove = people_to_remove[
        ~((people_to_remove['leg_placement'] < 100) & (people_to_remove['control_min'] > 0.8)) &
        ~((people_to_remove['team_placement'].between(1, 100)) & (people_to_remove['leg_placement'] < 200) &
          (people_to_remove['control_min'] > 0.8)) &
        ~((people_to_remove['control_count'] == 1) & (people_to_remove['leg_placement'] < 200) &
          (people_to_remove['control_min'] > 0.85))
        ]

    people_to_remove = people_to_remove[['year', 'team_number', 'leg_number']]

    # also remove ones with missing or very high control times
    people_to_remove = pd.concat([people_to_remove,
                                  temp_df[(temp_df["control_time"] > 3600 * 10) | (temp_df["control_time"].isna())]
                                  [['year', 'team_number', 'leg_number']].drop_duplicates()])

    people_to_remove['to_remove'] = 1
    temp_df = temp_df.merge(people_to_remove, on=['year', 'team_number', 'leg_number'], how='left')
    temp_df = temp_df[temp_df['to_remove'].isna()].drop(columns='to_remove')

    return temp_df


def add_control_baseline(temp_df):
    """
    next baseline for control times can be added from all runners as the bugged ones are filtered out
    """
    control_times = temp_df \
        .sort_values(['control_id', 'control_time']) \
        .groupby(['control_id']).head(5) \
        .groupby(['control_id'])['control_time'].mean()

    temp_df = temp_df.join(control_times, on='control_id', rsuffix='_baseline')
    temp_df['control_time_baseline_percent'] = temp_df['control_time'] / temp_df['control_time_baseline']

    df_confirming_baseline = temp_df[['control_id', 'control_time_topteam', 'control_time_baseline']].drop_duplicates()
    df_confirming_baseline['baseline_difference'] = df_confirming_baseline['control_time_topteam'] / \
                                                    df_confirming_baseline['control_time_baseline']

    print('\nconfirm that the baseline difference doesnt differ highly, should be little over one')
    print(df_confirming_baseline['baseline_difference'].describe().to_string(), '\n')

    temp_df = temp_df.drop(columns=['control_time_topteam', 'control_time_topteam_percent'])

    return temp_df


def add_control_placement(return_df):
    temp_df = return_df[['control_id', 'control_time']].drop_duplicates()
    temp_df['control_time'] = temp_df['control_time'].replace(-1, 99999)
    temp_df["control_placement"] = temp_df.groupby(['control_id'])["control_time"].rank("dense").astype('int32')
    return_df = return_df.merge(temp_df, on=['control_id', 'control_time'])
    return return_df


def add_person_controls_baseline(temp_df):
    person_placement = temp_df.groupby(['year', 'team_number', 'leg_number'])[['control_placement']].median()

    person_placement["bias"] = np.clip((person_placement['control_placement'] - 1) * 0.05, 0, 10)

    temp_df = temp_df.merge(person_placement.drop(columns=['control_placement']), on=['year', 'team_number', 'leg_number'])


    temp_df['approximated_control_time_percent'] = (temp_df['control_time'] - temp_df["bias"]) / temp_df['control_time_baseline']

    percentage_median = temp_df.groupby(['year', 'team_number', 'leg_number'])[['approximated_control_time_percent']].median()

    temp_df = temp_df.drop(columns=['approximated_control_time_percent'])

    temp_df = temp_df.merge(percentage_median, on=['year', 'team_number', 'leg_number'])

    temp_df['approximated_control_time'] = temp_df['control_time_baseline'] * \
                                           temp_df['approximated_control_time_percent'] + \
                                           temp_df['bias']

    return temp_df


def add_mistake_seconds(temp_df):
    temp_df['mistake_seconds'] = temp_df['control_time'] - temp_df['approximated_control_time']

    temp_df['mistake_seconds'] = np.clip(temp_df['mistake_seconds'], 0, None)

    return temp_df


def add_clock(temp_df, years):
    # adds team cumulative timestamp for each control
    # leg start is added instead of summing all control times to reduce rounding effect

    df_leg_times = pd.concat((pd.read_csv('processed_data/legs_' + str(year) + '.csv').assign(year=year)
                              for year in years))

    legtimes_cumsum_df = df_leg_times.sort_values(['year', 'team_number'])
    legtimes_cumsum_df['leg_start_clock'] = legtimes_cumsum_df.groupby(['team_number', 'year'])['leg_time'].cumsum()

    legtimes_cumsum_df['leg_start_clock'] = legtimes_cumsum_df['leg_start_clock'].shift(1)
    legtimes_cumsum_df.loc[legtimes_cumsum_df['leg_number'] == 1, 'leg_start_clock'] = 0


    controltimes_cumsum_df = temp_df[['team_number', 'year', 'leg_number', 'control_number', 'control_time']].drop_duplicates()\
        .sort_values(['team_number', 'year', 'leg_number', 'control_number'])

    controltimes_cumsum_df['control_start_clock'] = controltimes_cumsum_df.groupby(['team_number', 'year', 'leg_number'])['control_time'].cumsum()

    #start from 0
    controltimes_cumsum_df['control_start_clock'] = controltimes_cumsum_df['control_start_clock'].shift(1)
    controltimes_cumsum_df.loc[controltimes_cumsum_df['control_number'] == 1, 'control_start_clock'] = 0

    controltimes_cumsum_df = controltimes_cumsum_df.merge(legtimes_cumsum_df, on=['team_number', 'year', 'leg_number'])
    controltimes_cumsum_df['control_start_clock'] = controltimes_cumsum_df['control_start_clock'] + controltimes_cumsum_df['leg_start_clock']

    controltimes_cumsum_df = controltimes_cumsum_df[['team_number', 'year', 'leg_number', 'control_number', 'control_start_clock']]

    temp_df = temp_df.merge(controltimes_cumsum_df, on=['team_number', 'year', 'leg_number', 'control_number'])

    return temp_df

