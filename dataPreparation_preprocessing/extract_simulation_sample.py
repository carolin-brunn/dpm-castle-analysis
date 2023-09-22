#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 16:13:30 2023

@author: carolin
"""

import pandas as pd

def main():
    """
        input:
            1 dataset containing data of all clients per month (in our simulations: with adapted date format)
        procedure:
            randomly extract specified fraction of the whole dataset
            like this 1) the dataset becomes smaller 2) clients do not "send" measurements for each timestamp, which is more realistic
        output:
            1 dataset containing specified fraction
    """
    n_users = 370 # define number of users that shall be included in merged dataset, complete = 370 users
    year = "2014"
    month = "11"
    week = [46, 47]
    transformed_date = True
    sample_size = 0.33
    sort_keys = ["year", "week", "weekday", "time"] # sort extracted sample based on measurement time points (simulate distributed datastream: data of the same time point but from different clients shall arrive in random order order but still "simultaneously")
    
    data_path = "../consumption_data/monthlyConsumption/"
    input_file = year + "-" + month + "-eletricity_consumption.csv"
    if(transformed_date):
        input_file = "transformed_date_" + input_file
    
    df = pd.read_csv((data_path + input_file), sep = ",", index_col = False)
    print(df.head())
    
    df_sample = df[(df["week"].isin( week))]
    df_sample = df_sample.sample(frac = sample_size).sort_values(by=sort_keys).reset_index(drop=True)
    
    output_file = year + "-" + month + "-eletricity_consumption_sample_" + str(len(df_sample)) + ".csv"
    if(transformed_date):
        output_file = "transformed_date_" + output_file
    # save simulation sample in more general location
    df_sample.to_csv(("../consumption_data/" + output_file), sep = ',', index = False)

    ### optional: delete specified clients with very high consumption
    highconsumers = [196, 270, 362, 370]
    df_wo_high = df_sample[~(df_sample["pid"].isin( highconsumers ))]
    output_file = "wo_high_" + output_file
    df_wo_high.to_csv(("../consumption_data/" + output_file), sep = ',', index = False)


if __name__ == "__main__":
    main()
