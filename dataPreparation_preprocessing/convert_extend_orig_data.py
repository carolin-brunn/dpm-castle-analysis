#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 18:17:06 2022

@author: carolin
"""

import pandas as pd
import numpy as np
import datetime as dt
import random

def main():
    """
        input: 
            1 dataset with 370 columns taken from UCI Machine Learning Repository (https://doi.org/10.24432/C58C86)
            columns: consumption data, 1 column per client 
            rows: timestamp and measurements
        procedure:
            prepare and format raw data file for anonymization simulation
            transform timestmap format
            convert file format, such that each row is 1 measurement
            add artificial addresses for each user
        output: 
            1 file per user
            colummns: consumption, PID, address, date, time
            rows: each row represents 1 measurement 
        afterwards the files for individuals can be mergeed based on requirements for further simmulation
    """

    df = pd.read_csv("../consumption_data/LD2011_2014.txt", sep = ";")
    #print(df.shape)
    
    time_df = pd.DataFrame()
    
    # strings are datetime strings (date_time_str)
    timestamp_series = df.iloc[:, 0] # take only a sample: [:10, 0]
    timelist = []
    daylist = []
    
    # convert strings in time column to timestamps (datetime format) with date and time
    for timestr in timestamp_series:
        timestamp = dt.datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S')
        d = timestamp.date()
        daylist.append(d)
        
        t = timestamp.time()
        timelist.append(t)
        
    time_df["date"] = daylist
    time_df["time"] = timelist

    
    my_seed = random.seed()
    random.seed(a=my_seed)
    for x in df.columns[1:]: # or take only a subsample of clients: e.g., [1:20]
        user_df = pd.DataFrame()
        user_time_df = pd.DataFrame()
        
        # extract column from data frame that contains wlwctrical consumption of the particular user
        user_consumption = df[x]
        # convert consumption string format to uniform float format
        float_consumption = pd.Series([float(c.replace(',','.')) if ',' in str(c) else float(c) for c in user_consumption])
        user_df["consumption"] = float_consumption 
        
        n_entries = len(user_df["consumption"])
        
        # add pid to df: needed for CASTLE algorithm
        user_id = int(x[-3::])
        user_df["pid"] = [user_id] * n_entries

        # use street and house number as a combined number
        #   it could be enough to delete the house number and just keep the street
        #   but im not sure about prioritizing generalizing attributes in CASTLE so instead I use it similar to postal
        #   when building ranges the house no should be cut first like this
        street = random.randint(1000, 1110) # 110 streets in Moabit
        houseno = random.randint(10, 80)    # assume at most 70 houses per street on average
        
        # add randomly generated postal code
        postal = random.randint(10551, 10559) # Postleitzahlen von Moabit
        address = postal * 1000000 + street*100 + houseno 
        
        user_df["address"] = [address] * n_entries
        
        # add timestamp to dataset
        user_time_df = pd.concat([user_df, time_df], axis=1)
        
        # save dataset per user for further processing
        user_time_df.to_csv(("../consumption_data/singleUsers/consumption_user_" + x + ".csv"), sep = ",", index = False)
        


if __name__ == "__main__":
    main()