#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 13:36:45 2023

@author: carolin
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def main():   
    year = "2011"
    month = "01"
    sample_size = 164102 
    seed = 42
    
    l_delta = [100, 400]
    l_k = [10, 25, 50, 100]
    n_users = 370
    
    transformed_date = True
    norm_il = False

    path = "anonymized_data/"
    headers = ["address", "year", "week", "weekday", "time" ] #["address", "week", "weekday", "time" ] #
    if(not transformed_date):
        headers = ["address", "date", "time" ]
      
    h_l = []
    # initialize all possible header columns
    for h in headers:
        h_l.append(("min_il_" + h))
        h_l.append(("il_" + h)) 
        h_l.append(("max_il_" + h))
    
    df_il = pd.DataFrame( columns = (["k", "delta", "n_users", "consumption diversity"] + h_l))
    
    """
    load data of CASTLE anonymization
    """
    for delta in l_delta:
        for k in l_k:
            
            header_str = ''.join(headers)   
            
            input_file = "anonymization_" + str(n_users) + "users"  + "_PID" + str(n_users) + "_" + year + "-" + month\
                                + "_delta" + str(delta) + "_k" + str(k) + "_sample" + str(sample_size)\
                                + "_headers-" + header_str + "_seed" + str(seed) + ".csv"
            if(transformed_date):
                input_file = "transformed_date_" + input_file
                
            if(norm_il):
                input_file = "normIL_localRange/normIL_" + input_file
            
            input_file = "ANALYZED_CLUSTERS" + input_file # this file has the information loss per cluster
            df = pd.read_csv((path + input_file), index_col = 0, sep = ",")
            # add all data to list
            dl = []
            dl.append(k)
            dl.append(delta)
            dl.append(n_users)
            dl.append(np.mean(df["consumption diversity"]))
            for h in headers:
                # average information loss over all clusters per attribute
                dl.append(np.min(df[("il_" + h)]))
                dl.append(np.mean(df[("il_" + h)])) 
                dl.append(np.max(df[("il_" + h)]))
            # append to general dataframe   
            df_il.loc[len(df_il.index)] = dl
     
    """
    load data of ARX anonymization (baseline)
    """
    for k in [10, 25, 50, 100]:
        #input_file = "ARXgroundtruth_transformed_data_anonymization_370users_2011-01_k10_sample149184_headers-addressyearweekdaytime.csv"
        input_file = "ANALYZED_CLUSTERS" + "ARX_anonymization_370users_2011-01_k" + str(k) +"_sample164102_headers-" + header_str + ".csv"
        df = pd.read_csv((path + input_file), index_col = 0, sep = ",")
        dl = []
        dl.append(k)
        dl.append("ARX")
        dl.append(n_users)
        dl.append(np.mean(df["consumption diversity"]))
        for h in headers:
            # average information loss over all clusters per attribute
            dl.append(np.min(df[("il_" + h)]))
            dl.append(np.mean(df[("il_" + h)])) 
            dl.append(np.max(df[("il_" + h)]))
           
        df_il.loc[len(df_il.index)] = dl
        
    """
    plot data
    """
    color_pal = sns.color_palette("colorblind", 5)
    sns.set_theme(style = "white", palette = "colorblind")#, font_scale = 9)
    sns.set_context(rc={"font.size": 30, "axes.titlesize": 'medium', 'axes.labelsize': 'medium', 
                        'xtick.labelsize': 'medium', 'ytick.labelsize': 'medium',
                        "legend.fontsize": 'medium', 'legend.title_fontsize': 'medium',
                        'lines.markersize': 9.0, 'lines.linewidth': 3.8,})


    plt.figure(figsize=(15,7.5))
    g = sns.lineplot(data = df_il, x = "k", y = "il_address", hue = "delta", style = "delta", 
                     markers = True, palette = "colorblind")
    g.set(xlabel = "k", ylabel = "Information loss - Address")
    sns.despine( )
    #plt.show()
    plt.savefig(("./plots/InfoLoss_address.pdf"), bbox_inches = "tight")
    plt.close() 
    
    plt.figure(figsize=(15,7.5))
    g = sns.lineplot(data = df_il, x = "k", y = "il_week", hue = "delta", style = "delta", 
                     markers = True, palette = "colorblind")
    g.set(xlabel = "k", ylabel = "Information loss - Week")#, title = "Average Information loss [week]")
    sns.despine( )
    #plt.show()
    plt.savefig(("./plots/InfoLoss_week.pdf"), bbox_inches = "tight")
    plt.close() 
    
    plt.figure(figsize=(15,7.5))
    g = sns.lineplot(data = df_il, x = "k", y = "il_weekday", hue = "delta", style = "delta", 
                     markers = True, palette = "colorblind")
    g.set(xlabel = "k", ylabel = "Information Loss - Weekday")
    sns.despine( )
    #plt.show()
    plt.savefig(("./plots/InfoLoss_weekday.pdf"), bbox_inches = "tight")
    plt.close() 
    
    plt.figure(figsize=(15,7.5))
    g = sns.lineplot(data = df_il, x = "k", y = "il_time", hue = "delta", style = "delta", 
                     markers = True, palette = "colorblind")
    g.set(xlabel = "k", ylabel = "Information loss - Time")
    sns.despine( )
    #plt.show()
    plt.savefig(("./plots/InfoLoss_time.pdf"), bbox_inches = "tight")
    plt.close() 
               
if __name__ == "__main__":
    main()
