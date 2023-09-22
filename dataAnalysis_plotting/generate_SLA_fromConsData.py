#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 09:04:06 2023

@author: carolin
"""

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

sample = False

if(sample):
    df = pd.read_csv("../consumption_data/transformed_date_2014-11-eletricity_consumption_sample_164102.csv")  #load whole dataset of November - 
else:
    df = pd.read_csv("../consumption_data/monthlyConsumption/transformed_date_2014-11-eletricity_consumption.csv") #"_sample_164102.csv")  #load whole dataset of November - 

l_threshold = [4000, 9000]

for threshold in l_threshold:
    
    df_high = df.loc[df["consumption"] > threshold] 		# get users with extremly high consumption 
    print("These are users with high consumption above "+str(threshold)+": ", df_high["pid"].unique()	) # returns 196, 279, 362, 370
             
    ### get data for remaining users for complete November                           
    df_low = df.loc[df["consumption"] < threshold]	
    # default behavior in seaborn is to aggregate the multiple measurements at each x value by plotting the mean and the 95% confidence interval around the mean
    # alternative: standard deviation -> set errorbar = "sd"
    g = sns.lineplot(data = df_low, x = "time", y = "consumption")			# shows a SLA
    #g = sns.relplot(data = dfu9000, x = "time", y = "consumption", kind = "line")	
    g.set(xlabel = "Time point", ylabel = "consumption [(k)W]", title = "Consumption of all small users in November")
    #plt.show()
    if(sample):
        plt.savefig(("../plots/consNov2014_below_" + str(threshold) + "_SLA_sample_164102.pdf"), bbox_inches = "tight")
    else:
        plt.savefig(("../plots/consNov2014_below_" + str(threshold) + "_SLA.pdf"), bbox_inches = "tight")
    plt.close()
    
    ### data for a whole week
    week = 46
    df_low_week = df_low.loc[( (df_low["week"] == week) ) ]					
    g = sns.lineplot(data = df_low_week, x = "time", y = "consumption")
    #g = sns.relplot(data = dfu9000w46, x = "time", y = "consumption", kind = "line")
    g.set(xlabel = "Time point", ylabel = "consumption [(k)W]", title = "Consumption of all small users for 1 week in November")
    #plt.show()
    if(sample):
        plt.savefig(("../plots/consNov2014_below_" + str(threshold) + "_week_" + str(week) + "_SLA_sample_164102.pdf"), bbox_inches = "tight")
    else:
        plt.savefig(("../plots/consNov2014_below_" + str(threshold) + "_week_" + str(week) + "_SLA.pdf"), bbox_inches = "tight")
    plt.close()
    
    ### data for one weekday
    day = 3
    df_low_day = df_low.loc[( (df_low["week"] == week) & (df_low["weekday"] == day) ) ]		# data for a Wednesday in November
    g = sns.lineplot(data = df_low_day, x = "time", y = "consumption")			# already shows some kind of SLA
    g.set(xlabel = "Time point", ylabel = "consumption [(k)W]", title = "Consumption of all small users for 1 day in November")
    if(sample):
        plt.savefig(("../plots/consNov2014_below_" + str(threshold) + "_week_" + str(week) + "_day_" + str(day) + "_SLA_sample_164102.pdf"), bbox_inches = "tight")
    else:
        plt.savefig(("../plots/consNov2014_below_" + str(threshold) + "_week_" + str(week) + "_day_" + str(day) + "_SLA.pdf"), bbox_inches = "tight")
    #plt.show()
    plt.close()
