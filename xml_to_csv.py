from io import StringIO

import xml.etree.cElementTree as et
import pandas as pd

import numpy as np

xml_files_path = r"data/"
csv_path = r"processed_data/"

"""
parses the xml files (results_j2000_ju.xml) and saves as csv

saves the leg times separately as it is possible to have legit time with no control times
and to get the exact course
"""


"""
xml format

team
    teamid
    teamname
    teamnro
    result
    tsecs
    placement
    leg
        legnro
        nm
        crs
        emit
        control
            cn
            cc
            ct
            cd
"""

"""
cn: the control number on that leg
cc: destination control code 
cd: control time
"""


years = list(range(2000, 2022))
years.remove(2020)

def xml_read(path):
    return et.parse(path)

def read_df(path):

    try:
        df = xml_read(path)

    except:
        # & char produces errors
        raw_text = " ".join(open(path).readlines())
        raw_text = raw_text.replace("&", "and")

        df = xml_read(StringIO(raw_text))

    return df


def time_parser(x):
    try:
        if x == None:
            return None
        splitted = x.split(':')
        total_seconds = -1
        if len(splitted) == 1:
            total_seconds = int(splitted[0])
        elif len(splitted) == 2:
            total_seconds = int(splitted[0]) * 60 + int(splitted[1])
        elif len(splitted) == 3:
            total_seconds = int(splitted[0]) * 60 * 60 + int(splitted[1]) * 60 + int(splitted[2])
    except ValueError:
        total_seconds = np.nan
    return total_seconds

for year in years:

    # legtimes are saved separately because if emit fails, no control times found but legtime is
    LEG_teamnro_list = []
    LEG_legnro_list = []
    LEG_leg_tsecs_list = []
    LEG_crs = []  # also adding the course forking

    teamname_list = []
    teamnro_list = []
    placement_list = []
    tsecs_list = []
    legnro_list = []
    leg_tsecs_list = []
    nm_list = []
    cn_list = []
    cc_list = []
    ct_list = []
    cd_list = []

    tree=read_df(xml_files_path+r'results_j'+str(year)+'_ju.xml')
    root=tree.getroot()

    for team in root.iter('team'):
        root1 = et.Element('root')
        root1 = team
        teamname = root1.find("teamname").text
        teamnro = root1.find("teamid").text

        placement = root1.find("placement")
        if placement == None:
            placement = -1
        else:
            placement = placement.text

        tsecs = root1.find("tsecs")
        if tsecs == None:
            tsecs = -1
        else:
            tsecs = tsecs.text

        #print(teamname)
        #if teamname =='Delta':
        #    break
        for leg in root1.iter('leg'):
            root2 = et.Element('root')
            root2 = leg
            legnro = root2.find("legnro").text

            leg_fork = root2.find("crs").text

            nm = root2.find("nm").text

            leg_tsecs = root2.find("tsecs")
            if leg_tsecs == None:
                leg_tsecs = -1
            else:
                leg_tsecs = leg_tsecs.text

            LEG_teamnro_list.append(teamnro)
            LEG_legnro_list.append(legnro)
            LEG_leg_tsecs_list.append(leg_tsecs)
            LEG_crs.append(leg_fork)


            for control in root2.iter('control'):
                cn = control.find("cn").text
                cc = control.find("cc").text
                ct = control.find("ct").text
                cd = control.find("cd").text

                teamname_list.append(teamname)
                teamnro_list.append(teamnro)
                placement_list.append(placement)
                tsecs_list.append(tsecs)
                legnro_list.append(legnro)
                leg_tsecs_list.append(leg_tsecs)
                nm_list.append(nm)
                cn_list.append(cn)
                cc_list.append(cc)
                ct_list.append(ct)
                cd_list.append(cd)


    ###########################################################
    # leg times first
    df = pd.DataFrame({
        'team_number': LEG_teamnro_list,
        'leg_number': LEG_legnro_list,
        'leg_time': LEG_leg_tsecs_list,
        'leg_fork': LEG_crs
    })

    df = df.astype({
        'team_number': 'int32',
        'leg_number': 'int32',
        'leg_time': 'int32'
    })

    df.to_csv(csv_path+'legs_'+str(year)+'.csv', index=False)
    ###########################################################


    df = pd.DataFrame({
        'team_name': teamname_list,
        'team_number': teamnro_list,
        'team_placement': placement_list,
        'team_time': tsecs_list,
        'leg_number': legnro_list,
        'leg_time': leg_tsecs_list,
        'name': nm_list,
        'control_number': cn_list,
        'control_end': cc_list,
        'control_time': cd_list
    })

    df['control_start'] = df['control_end'].shift(1)

    # add zero as leg start
    df.loc[df['control_number'] == '1', 'control_start'] = '0'

    # add 1 to differentiate relay start
    df.loc[(df['control_number'] == '1') & df['leg_number'] == '1', 'control_start'] = '1'

    df['control_id'] = str(year) + '-' + df['control_start'] + '-' + df['control_end']

    df = df.astype({
        'team_placement': 'int32',
        'team_time': 'int32',
        'leg_number': 'int32',
        'leg_time': 'int32',
        'control_end': 'int32',
        'control_number': 'int32',
        'control_start': 'int32'
    })

    df['control_time'] = df['control_time'].apply(time_parser)


    # add the control type
    """
    forking?
    0 from common to common
    1 from fork to common
    2 from common to fork
    3 from fork to fork
    """

    max_runners = df.groupby(['leg_number', 'control_end'])[['team_name']].count().max().iloc[0]

    temp_df = df.groupby(['leg_number', 'control_end'])[['team_name']].count().reset_index()
    temp_df['common_control'] = temp_df['team_name'] > max_runners * 0.75
    temp_df = temp_df.drop(columns='team_name')

    df = df.merge(temp_df, on=['leg_number', 'control_end'], how='left')

    temp_df = temp_df.rename(columns={'common_control': 'common_control_previous', 'control_end': 'control_start'})

    df = df.merge(temp_df, on=['leg_number', 'control_start'], how='left')
    df.loc[df['control_number'] == 1, 'common_control_previous'] = True

    df = df.fillna(value={"common_control_previous": True})
    df['control_type'] = 3

    df.loc[df['common_control'] & df['common_control_previous'], 'control_type'] = 0
    df.loc[df['common_control'] & (~df['common_control_previous']), 'control_type'] = 1
    df.loc[(~df['common_control']) & df['common_control_previous'], 'control_type'] = 2


    df = df.drop(columns='control_end')
    df = df.drop(columns='control_start')
    df = df.drop(columns='common_control')
    df = df.drop(columns='common_control_previous')
    df.to_csv(csv_path+str(year)+'.csv', index=False)

    print(df.head().to_string())










