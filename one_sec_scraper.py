#!/usr/bin/env python3
'''Reads the contents of an Edge of Space Sciences one second telemetry
file and extracts data we will use for analysis.'''

import pandas as pd
from sys import argv, exit

# Column names from the telemetry file. Hopefully these stay the same
# from flight to flight.
alt_col = 'GPS_altitude'
temperature_col = 'Baro Temp F'


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
    try:
        one_sec_file = argv[1]
    except BaseException as e:
        print(e)
        print(f'Usage: {argv[0]} filename')
        exit(1)

    one_sec = pd.read_excel(one_sec_file, index_col=0)

    print(f'Max altitude = {one_sec[alt_col].max()} at time {one_sec[alt_col].idxmax()}')

    launch_time = find_launch_time(one_sec)
    print(f'Launch happened at approximately {launch_time}')
    try:
        launch_temp = one_sec[launch_time][temperature_col]
        print(f'Temperature at launch = {launch_temp}')
    except:
        print('No temperature data found')
        # We could use the Internal Temperature as a fallback but I'm not sure how
        # close that is to the external temperature. That's something to look into.
