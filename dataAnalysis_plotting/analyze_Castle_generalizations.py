#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 14:16:27 2023

@author: carolin
"""

import pandas as pd
import numpy as np
import matplotlib
import seaborn as sns

#################################
#################################
#################################

def calc_info_loss(uni_df, headers):
    """
    calculcate information loss for every cluster
        based on generalized loss metric introduced by Iyengar 2002
    """
    for h in headers:
        min_idx = "min" + h
        max_idx = "max" + h
        
        col_name = "il_" + h
        
        # max range for this attribute over all possible values
        big_l = min(uni_df[min_idx])
        big_u = max(uni_df[max_idx])
        total_dif = big_u - big_l
        
        # calculate information loss for each unique cluster in df
        if(total_dif > 0):
            uni_df[col_name] =  (uni_df[max_idx] - uni_df[min_idx]) / total_dif
        else:
            uni_df[col_name] = 0 
    
#################################

def calc_qi_range(uni_df, headers):
    """
    calculate the cluster size for all generalized attributes
    """
        
    for h in headers:
        min_idx = "min" + h
        max_idx = "max" + h
        size = (uni_df[max_idx] - uni_df[min_idx])
        uni_df[(h + "_range")] = size
        
#################################

def evaluate_proximity(orig_df, uni_df, epsilon):
    """
    evaluate the proximity of SA of tuples to each other based on (epsilon, m)-anonymity (Li 2008)
        calculate proximity for each tuple and save average of all tuples in 1 cluster as its proximity ratio
        meaning that this ratio/percentage of tuples were closer than epsilon to each other
    """

    uni_df["proximity_ratio"] = 0.0
    
    uni_labels = uni_df["cluster_label"].unique()
    
    # for every cluster:
    for l in uni_labels:
        # create list to save proximity number of each tuple
        proximity_ratio = []
        
        cluster_cons = orig_df.loc[orig_df["cluster_label"] == l, "consumption"]
        sorted_cons = cluster_cons.sort_values(axis = 0, ascending = True)
        sorted_cons.reset_index(drop = True, inplace = True)
        total_no_tuples = len(sorted_cons)

        # for every tuple: 
        for i in range(total_no_tuples):
            t = sorted_cons[i]

            # extract number of tuples in relative neighbourhood (epsilon indicates proximity range)
            no_neighbour_tuples = 0
            no_neighbour_tuples = len(sorted_cons[ (sorted_cons >= (t*(1-epsilon))) & (sorted_cons <= (t*(1+epsilon))) & (sorted_cons.index != i) ])
             
            # divide by total number of members in tuple
            t_neighbour_ratio = 0
            t_neighbour_ratio = no_neighbour_tuples / total_no_tuples
               
            # save in list
            proximity_ratio.append(t_neighbour_ratio)
            
        # calculate average over all proximity ranges of tuples in cluster
        # this is the average ratio of tuples within proximity range of each other in the cluster
        c_neighbour_ratio = 0
        c_neighbour_ratio = np.mean(proximity_ratio)
        uni_df.at[l, "proximity_ratio"] = c_neighbour_ratio
  
#################################

def evaluate_proximity_wo_zero(orig_df, uni_df):
    """
    evaluate the proximity of SA of tuples to each other based on (epsilon, m)-anonymity (Li 2008)
        calculate proximity for each tuple and save average of all tuples in 1 cluster as its proximity ratio
        meaning that this ratio/percentage of tuples were closer than epsilon to each other
    """     
    uni_df["proximity_ratio_wo_zero"] = 0.0
    
    uni_labels = uni_df["cluster_label"].unique()
    
    # for every cluster:
    for l in uni_labels:
        # create list to save proximity number of each tuple
        proximity_ratio = [0]
       
        cluster_cons = orig_df.loc[orig_df["cluster_label"] == l, "consumption"]
        sorted_cons = cluster_cons[cluster_cons != 0]
        sorted_cons = sorted_cons.sort_values(axis = 0, ascending = True)
        sorted_cons.reset_index(drop = True, inplace = True)
        total_no_tuples = len(sorted_cons)

        # for every tuple: 
        for i in range(total_no_tuples):
            t = sorted_cons[i]

            # extract number of tuples in relative neighbourhood (epsilon indicates proximity range)
            no_neighbour_tuples = 0
            no_neighbour_tuples = len(sorted_cons[ (sorted_cons >= (t*(1-0.1))) & (sorted_cons <= (t*(1+0.1))) & (sorted_cons.index != i) ])
            
            # divide by total number of members in tuple
            t_neighbour_ratio = 0
            t_neighbour_ratio = no_neighbour_tuples / total_no_tuples
               
            # save in list
            proximity_ratio.append(t_neighbour_ratio)       
            
        # calculate average over all proximity ranges of tuples in cluster
        # this is the average ratio of tuples within proximity range of each other in the cluster
        if (len(proximity_ratio) > 1):
            c_neighbour_ratio = np.mean(proximity_ratio)
            uni_df.at[l, "proximity_ratio_wo_zero"] = c_neighbour_ratio
        else:
            uni_df.at[l, "proximity_ratio_wo_zero"] = 3

#################################

def calc_sensitive_difference(orig_df, uni_df):
    """
    calculate the range of the senstive attribute (= electricity consumption) for each cluster
    """
    uni_df["consumption_difference"] = 0.0
    uni_df["consumption_difference_wo_zero"] = 0.0
    uni_labels = uni_df["cluster_label"].unique()
    
    for l in uni_labels:
        cluster_cons = orig_df.loc[orig_df["cluster_label"] == l, "consumption"] # extract column with consumption values within cluster
        
        cluster_cons = cluster_cons.sort_values()
        diff_cons = np.mean(cluster_cons.diff())
        uni_df.at[l, "consumption_difference"] = diff_cons
        
        cons_wo_zero = 0
        cons_wo_zero = [x for x in cluster_cons if x != 0.0]
        cons_wo_zero = pd.Series(cons_wo_zero, dtype = 'float64')
        diff_wo_zero = np.mean(cons_wo_zero.diff() if (len(cons_wo_zero) > 1) else 0)
        uni_df.at[l, "consumption_difference_wo_zero"] = diff_wo_zero
        
#################################

def calc_sensitive_range(orig_df, uni_df):
    """
    calculate the range of the senstive attribute (= electricity consumption) for each cluster
    """
    uni_df["consumption_range"] = 0.0
    uni_labels = uni_df["cluster_label"].unique()
    
    for l in uni_labels:
        min_cons = min(orig_df.loc[orig_df["cluster_label"] == l, "consumption"])
        max_cons = max(orig_df.loc[orig_df["cluster_label"] == l, "consumption"])
        cons_range = max_cons - min_cons
        
        uni_df.at[l, "consumption_range"] = cons_range
        
#################################

def calc_diversity(orig_df, uni_df):
    """
    calculate the diversity of the senstive attribute (= electricity consumption) for each cluster
    """
    uni_df["consumption diversity"] = 0
    uni_df["PID diversity"] = 0
    
    uni_labels = uni_df["cluster_label"].unique()
    
    for l in uni_labels:
        cons_div = len(set(orig_df.loc[orig_df["cluster_label"] == l, "consumption"]))
        uni_df.at[l, "consumption diversity"] = cons_div
        
        pid_div = len(set(orig_df.loc[orig_df["cluster_label"] == l, "orig_pid"]))
        uni_df.at[l, "PID diversity"] = pid_div
        
#################################

def label_cluster_id(orig_df, uni_df, minmaxheaders):
    """
    add unique cluster labels to big df with all generalizations
        e.g. to analyze occurrence over time
    """
    # merge df with unique and all clusters to have cluster labels for all clusters
    #   merge is done on the minmaxheaders, so the generalized attributes 
    #   whose unique value combinations are the identifier of unique clusters
    merged_df = pd.merge(orig_df, uni_df, on=minmaxheaders, how='inner')
    return merged_df

#################################

def get_unique_cluster(df, minmaxheaders):
    """
    extract unique clusters based on unique value combinations of generalized attributes
        and get cluster size based on contained tuples
    """
    print("unique clusters\n")
    uni_df = df.groupby(minmaxheaders).size().reset_index().rename(columns={0:'tuple_count'})
    uni_df["cluster_label"] = range(0, len(uni_df))
    
    return uni_df

#################################
#################################

def process_anonymized_df(input_file, headers):
    '''
    call all functions that are needed for processing the anonymized data
    '''
    path = "../anonymized_data/"
    print("Now loading: " + path  + input_file)
    # anonymized data file
    df = pd.read_csv((path + input_file),  sep = ",")

    minmaxheaders = []
    for h in headers:
        minmaxheaders.append("min" + h)
        minmaxheaders.append("max" + h)
    
    # dataframe to save results of cluster analysis
    # extract unique clusters
    unique_cluster_df = get_unique_cluster(df, minmaxheaders)
    print(unique_cluster_df.head())
    
    # add cluster labels to big data set for further processing
    df = label_cluster_id(df, unique_cluster_df, minmaxheaders)
    
    # calculate the diversity of clusters
    calc_diversity(df, unique_cluster_df)
    
    # label original anonymized data set
    output_file = "labeledCl_" + input_file  
    #output_file = "wo_high_" + output_file
    df.to_csv((path + output_file), sep = ",")
    
    # calculate the range of the sensitive attribute for all clusters inspired by Zhang 2007
    calc_sensitive_range(df, unique_cluster_df)
    
    # calculate the avergae difference between neighbouring sensitive attribute values for each cluster
    calc_sensitive_difference(df, unique_cluster_df)
    
    # evaluate the proximity of neighbouring sensitive attribute values for each cluster inspired by J. Li 2008
    epsilon = 0.2
    evaluate_proximity(df, unique_cluster_df, epsilon)
    #evaluate_proximity_wo_zero(df, unique_cluster_df)
    del(df)
    
    """calculate further information for each cluster"""
    # calculate range for each QI attribute per cluster
    calc_qi_range(unique_cluster_df, headers)
    
    # calculate the information loss for each QI attribute per cluster 
    calc_info_loss(unique_cluster_df, headers)
    
    output_file = "ANALYZED_CLUSTERS_prox" + str(int(epsilon*100)) + "_" + input_file
    #output_file = "wo_high_" + output_file
    unique_cluster_df.to_csv((path + output_file), sep = ",")


#################################
#################################

def main():

    year = "2014"
    month = "11"
    sample_size = 164102 
    seed = 42
    
    l_delta = [100, 200, 400] 
    l_k = [10, 25, 50, 100]
    n_users = 370
    
    transformed_date = True
    woHigh = False # optionally: possible to analyze simulation in which large consumers were excluded

    for delta in l_delta:
        if(delta == 0):
            str_delta = "complete" # optionally: possible to analyze simulation in which delta was set to complete sample size, TODO: simulation did not scale!!!
        else:
            str_delta = str(delta)
        for k in l_k:

            headers =  ["address", "week", "weekday", "time" ] # QI attributes
            if(not transformed_date):
                headers = ["address", "date", "time" ]
 
            header_str = ''.join(headers)   
            
            input_file = "anonymization_" + str(n_users) + "users"  + "_PID" + str(n_users) + "_" + year + "-" + month\
                                + "_delta" + str_delta + "_k" + str(k) + "_sample" + str(sample_size)\
                                + "_headers-" + header_str + "_seed" + str(seed) + ".csv"
            if(transformed_date):
                input_file = "transformed_date_" + input_file
            
            if(woHigh):
                input_file = "wo_high_" + input_file

            process_anonymized_df(input_file, headers)          
                    

if __name__ == "__main__":
    main()