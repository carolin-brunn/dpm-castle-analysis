#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 09:52:28 2023

@author: carolin
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

year = "2011"
month = "01"
sample_size = 164102
l_delta = [100, 400]
l_k = [10, 25, 50, 100]
n_users = 370
headers = ["address", "year", "week", "weekday", "time" ]
transformed_date = True
path = "anonymized_data/"

delta_df = pd.DataFrame()
for delta in l_delta:
    merged_df = pd.DataFrame()
    for k in l_k:
        header_str = ''.join(headers)   
        
        input_file = "anonymization_" + str(n_users) + "users"  + "_PID" + str(n_users) + "_" + year + "-" + month\
                            + "_delta" + str(delta) + "_k" + str(k) + "_sample" + str(sample_size)\
                            + "_headers-" + header_str + "_seed" + str(42) + ".csv"
        if(transformed_date):
            input_file = "transformed_date_" + input_file
        
        input_file = "ANALYZED_CLUSTERS" + input_file # this file has the information loss per cluster
        df = pd.read_csv((path + input_file), index_col = 0, sep = ",")

        df["k"] = k
        merged_df = pd.concat([merged_df, df])
    merged_df["delta"] = delta
    delta_df = pd.concat([delta_df, merged_df])

    
"""
load data of ARX anonymization
"""
headers = ["address", "year", "week", "weekday", "time" ]
header_str = ''.join(headers)   
merged_df = pd.DataFrame()
for k in l_k:

    input_file = "ARX_anonymization_370users_2011-01_k" + str(k) +"_sample164102_headers-" + header_str + ".csv"

    input_file = "ANALYZED_CLUSTERS" + input_file # this file has the analyzed attributes for each cluster
    df = pd.read_csv((path + input_file), index_col = 0, sep = ",")

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


g = sns.relplot(data = delta_df, x = "PID diversity", y = "consumption_range", hue = "k", 
                style = "k", col_wrap = 3, palette = "colorblind", col = "delta", aspect = 2)

g.fig.subplots_adjust(top=0.95)
titles = ["CASTLE, delta = 100", "CASTLE, delta = 400", "ARX"]
for ax, title in zip(g.axes.flatten(),titles):
    ax.set_title(title)
ax_label = g.facet_axis(0, 0)
ax_label.set_ylabel("Consumption range")
g.set(xlabel = "PID diversity")
#plt.show()
plt.savefig(("./plots/consRange_PIDDiv_3.pdf"), bbox_inches = "tight")
plt.close() 
