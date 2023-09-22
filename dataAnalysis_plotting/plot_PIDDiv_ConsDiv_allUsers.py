#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 13:14:21 2023

@author: carolin
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

year = "2014"
month = "11"
sample_size = 164102
l_delta = [100, 400]
l_k = [10, 25, 50, 100]
n_users = 370
headers = ["address", "week", "weekday", "time" ] #["address", "year", "week", "weekday", "time" ]
header_str = ''.join(headers)   
epsilon = 0.2

transformed_date = True
woHigh = False

data_path = "../anonymized_data/"
plot_path = "../plots/"

color_pal = sns.color_palette("colorblind", 5)

"""
load data of CASTLE anonymization
"""
delta_df = pd.DataFrame()
for delta in l_delta:
    merged_df = pd.DataFrame()
    for k in l_k:
        
        input_file = "anonymization_" + str(n_users) + "users"  + "_PID" + str(n_users) + "_" + year + "-" + month\
                            + "_delta" + str(delta) + "_k" + str(k) + "_sample" + str(sample_size)\
                            + "_headers-" + header_str + "_seed" + str(42) + ".csv"
        if(transformed_date):
            input_file = "transformed_date_" + input_file
        
        if(woHigh):
            input_file = "wo_high_" + input_file
            
        input_file = "ANALYZED_CLUSTERS_prox" + str(int(epsilon*100)) + "_" + input_file # this file has the information loss per cluster
        
        df = pd.read_csv((data_path + input_file), index_col = 0, sep = ",")
        df = df.loc[df["tuple_count"] < 500]
        df["k"] = k
        merged_df = pd.concat([merged_df, df])
        
    merged_df["delta"] = delta
    delta_df = pd.concat([delta_df, merged_df])
    
    
"""
load data of ARX anonymization
"""

merged_df = pd.DataFrame()
for k in l_k:

    input_file = "ARX_anonymization_370users_" + year + '-' + month + "_k" + str(k) +"_headers-" + header_str + ".csv"
    if(woHigh):
        input_file = "wo_high_" + input_file
    input_file = "ANALYZED_CLUSTERS_prox" + str(int(epsilon*100)) + "_" + input_file
    
    
        
    df = pd.read_csv((data_path + input_file), index_col = 0, sep = ",")
    df = df.loc[df["tuple_count"] < 500]
    df["k"] = k
    merged_df = pd.concat([merged_df, df])
merged_df["delta"] = "ARX"
delta_df = pd.concat([delta_df, merged_df])
    

"""
plot data
"""
color_pal = sns.color_palette("colorblind", 5)
sns.set_theme(style = "white", palette = "colorblind")#, font_scale = 9)
sns.set_context(rc={"font.size": 30, "axes.titlesize": 'medium', 'axes.labelsize': 'medium', 
                    'xtick.labelsize': 'medium', 'ytick.labelsize': 'medium',
                    "legend.fontsize": 'medium', 'legend.title_fontsize': 'medium',
                    'lines.markersize': 9.0, 'lines.linewidth': 2.8,})

g = sns.relplot(data = delta_df, x = "PID diversity", y = "consumption diversity", hue = "k", style = "k", 
                col_wrap = 3, palette = "colorblind", col = "delta")
g.fig.subplots_adjust(top=0.95)
g.set(xlabel = "PID diversity")
titles = ["CASTLE, delta = 100", "CASTLE, delta = 400", "ARX"]
i = 0
for ax, title in zip(g.axes.flatten(),titles):
    ax.set_title(title)
    ax.set_ylabel('')
ax_label = g.facet_axis(0, 0)
ax_label.set_ylabel("Consumption diversity")
g.set(xlabel = "PID diversity")
#plt.show()
plot_file = "ConsDiv_PIDDiv" + year + "-" + month +".pdf"
if(woHigh):
    plot_file = "wo_high_" + plot_file
plt.savefig((plot_path + plot_file), bbox_inches = "tight")
plt.close() 

 