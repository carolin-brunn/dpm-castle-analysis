#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 15:16:07 2023

@author: carolin
"""


import pandas as pd
import random
import numpy as np

def main():
    """
    input:
        datasets with measurements from different clients, 1 dataset per client
    procedure:
        load data for specifed number of clients
        merge them randomly, but based on time point of measuremnet to create a single dataset that emulates a distributed data stream
    output:
        1 dataset containing data of all specified clients
    """
    data_path = "../consumption_data/"
    merged_cons_data = pd.DataFrame() #columns=["consumption", "pid", "address", "postal", "date", "time"])
    
    n_users = 370 # define number of users that shall be included in merged dataset, complete = 370 users

    for x in range(1, (n_users + 1) ):
        str_x = "%03d" % x
        filename = "singleUsers/consumption_user_MT_" + str_x + ".csv"
        
        df = pd.read_csv((data_path + filename), sep = ",", index_col = False)
        
        # merge client data with other clients
        merged_cons_data = pd.concat([merged_cons_data, df], ignore_index=True, axis = 0)

    # in case that a sample shall be extracted, change frac = ...
    shuffled = merged_cons_data.sample(frac = 1) #merged_cons_data.apply(np.random.permutation, axis=1)
    
    # sort shuffled data based on measurement time points
    #   simulate distributed datastream
    #   data of the same time point but from different clients shall arrive in random order order but still "simultaneously"
    sorted_shuffled = shuffled.sort_values(by=["date", "time"]).reset_index(drop=True)
        
    # save merged file for further processing
    sorted_shuffled.to_csv((data_path + "merged_orig_consumption_" + str(n_users) + "_users.csv"), sep = ",", index = False)
    

if __name__ == "__main__":
    main()