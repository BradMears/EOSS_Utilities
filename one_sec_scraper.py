#!/usr/bin/env python3
'''Reads the contents of an Edge of Space Sciences one second telemetry
file and extracts data we will use for analysis.'''

import pandas as pd
from sys import argv, exit
import os


# Column names from the telemetry file. Hopefully these stay the same
# from flight to flight.
gps_alt_names = ['GPS_altitude','GPS altitude']
alt_col = None # Real name to use for GPS altitude. Gets set later

ext_temperature_names = ['Baro Temp F','Baro_Temp_F','Ext_Temp F']
ext_temperature_col = None  # Real name to use for temperature. Gets set later

int_temperature_names = ['Int_Temp F','Int_Temp_F','Int Temp F']
int_temperature_col = None  # Real name to use for temperature. Gets set later

def find_actual_column_name(df, candidate_names):
    '''The names of some columns of interest are inconsistent between files. Try the
    variations we know about.'''
    for name in candidate_names:
        if name in df.columns:
            return name
    return None


def find_launch_time(df):
    '''Returns the index of the approximate launch time based on GPS altitude.'''
    global alt_col
    
    # The altitude jumps around a bit on the ground but an average of the first 
    # five minutes should be pretty close. It might be sitting on a table or in
    # the back of somebody's truck during this time but that won't throw if off 
    # too much.
    avg_alt_on_ground = one_sec[alt_col][0:300].mean()
    
    # Find the first moment when the altitude is significantly higher than ground level.
    # How high is significant? There might be a clever way to determine that but for
    # now we'll use an arbitrary magic number.
    how_high_is_high = 50
    idx = df.index[df[alt_col] > (avg_alt_on_ground + how_high_is_high)][0]
    return idx

if __name__ == '__main__':
    for file in os.listdir("."):
        # We'll examine every xlsx file. Some will be in the wrong format 
        # but we can ignore those.
        if file.endswith(".xlsx"):
            print(f'Processing {file}')
            one_sec = pd.read_excel(file, index_col=0)

            # Step #1 is to figure out the names our columns of interest 
            alt_col = find_actual_column_name(one_sec, gps_alt_names)
            if alt_col == None:
                print(f'Unable to find the GPS altitude column')

            ext_temperature_col = find_actual_column_name(one_sec, ext_temperature_names)
            if alt_col == None:
                print(f'Unable to find the external temperature column')

            int_temperature_col = find_actual_column_name(one_sec, int_temperature_names)
            if int_temperature_col == None:
                print(f'Unable to find the internal temperature column')

            if alt_col == None or alt_col == None or int_temperature_col == None:
                print('One or more columns not found. Maybe one of these instead?')
                print(one_sec.columns)
                print

            # Step #2 is to pull the data we want from each of those columns
            if alt_col:
                print(f'Max altitude = {one_sec[alt_col].max()} at time {one_sec[alt_col].idxmax()}')
                launch_time = find_launch_time(one_sec)
                print(f'Launch happened at approximately {launch_time}')

            if ext_temperature_col:
                launch_temp = one_sec[ext_temperature_col][launch_time]
                print(f'Ext temperature at launch = {launch_temp} ({ext_temperature_col})')

            if int_temperature_col:
                launch_temp = one_sec[int_temperature_col][launch_time]
                print(f'Int temperature at launch = {launch_temp} ({int_temperature_col})')

            print()


"""
def find_gps_alt_name(df):
    '''The name of the altitude column is inconsistent between files. Try the
    variations we know about.'''
    global gps_alt_names
    for name in gps_alt_names:
        if name in df.columns:
            return name
    print('No GPS altitude column found')
    print(df.columns)
    return None

def find_ext_temperature_name(df):
    '''The name of the temperature column is inconsistent between files. Try the
    variations we know about.'''
    global ext_temperature_names
    for name in ext_temperature_names:
        if name in df.columns:
            return name
    print('No ext_temperature column found')
    return None

def find_int_temperature_name(df):
    '''The name of the temperature column is inconsistent between files. Try the
    variations we know about.'''
    global int_temperature_names
    for name in int_temperature_names:
        if name in df.columns:
            return name
    print('No int_temperature column found')
    return None
"""
