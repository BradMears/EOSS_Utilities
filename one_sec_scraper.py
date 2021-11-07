#!/usr/bin/env python3
'''Reads the contents of an Edge of Space Sciences one second telemetry
file and extracts data we will use for analysis.'''

from sys import argv
from os import listdir
import pandas as pd

def find_launch_time(df, alt_col):
    '''Returns the index of the approximate launch time based on altitude.'''

    # Figure out the altitude of the ground
    # The altitude jumps around a bit on the ground but an average of the first 
    # five minutes should be pretty close. It might be sitting on a table or in
    # the back of somebody's truck during this time but that won't throw if off 
    # too much.
    avg_alt_on_ground = one_sec[alt_col][0:300].mean()
    
    # Find the first moment when the altitude is significantly higher than ground level.
    # How high is significant? There might be a clever way to determine that but for
    # now we'll use an arbitrary magic number.
    how_high_is_high = 50
    try:
        idx = df.index[df[alt_col] > (avg_alt_on_ground + how_high_is_high)][0]
        return idx
    except:
        return None

#
# main
#
if __name__ == '__main__':
    # We'll examine every xlsx file. Some will be in the wrong format 
    # but we can ignore those.
    for file in listdir("."):
        if file.endswith(".xlsx"):
            print(f'Processing {file}')
            one_sec = pd.read_excel(file, index_col=0)

            # Note about file format:
            # The column names in the telemetry file are inconsistent from flight to flight. 
            # All we can do is look for a key substring in every column name and assume that 
            # if that substring is present, then that column is one of interest. 

            # Process all the 'altitude' columns 
            altitude_found = False
            for col in one_sec.columns:
                if 'alt' in col.lower():  # This is probably an altitude column
                    try:
                        launch_time = find_launch_time(one_sec, col)
                        max_alt = round(one_sec[col].max())
                        ndx = one_sec[col].idxmax()
                        print(f'Max {col} = {max_alt:,} at time {ndx}', end='')
                        if launch_time:
                            print(f'\tLaunch happened at approximately {launch_time}', end='')
                        print()
                        altitude_found = True
                    except:
                        pass

            # Process all the 'temperature' columns 
            temperature_found = False
            for col in one_sec.columns:
                if 'temp' in col.lower():  # This is probably a temperature column
                    try:
                        launch_temp = round(one_sec[col][launch_time])
                        print(f'{col} at launch = {launch_temp}')
                        temperature_found = True
                    except:
                        pass

            # If we couldn't find a key value, then print out all the column names.
            #  Maybe there will be one that we can use. If so, a code change will
            # be needed.
            if not altitude_found or not temperature_found:
                print("\t Couldn't find key data. Maybe one of these columns instead?")
                print('\t', one_sec.columns)
                print

            print()
