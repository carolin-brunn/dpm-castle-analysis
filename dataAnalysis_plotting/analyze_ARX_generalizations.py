#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 15:30:43 2023

@author: carolin
"""

import pandas as pd
import numpy as np
import matplotlib
import seaborn as sns

#################################

def calc_info_loss(uni_df, gen_headers):
    """
        calculcate information loss for every cluster
            based on generalized loss metric
    """
    # generalized loss metric
    # only generalized attributes are realevant, the others have info_loss zero
        
    for h in gen_headers:
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

def calc_cluster_range(uni_df, gen_headers):
    """
        calculate the cluster range for all generalized attributes
    """
    for h in gen_headers:
        min_idx = "min" + h
        max_idx = "max" + h
        rng = (uni_df[max_idx] - uni_df[min_idx])
        uni_df[(h + "_range")] = rng

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
        cons_range = float(max_cons - min_cons)
        
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
        diversity = len(set(orig_df.loc[orig_df["cluster_label"] == l, "consumption"]))
        uni_df.at[l, "consumption diversity"] = diversity
        
        pid_div = len(set(orig_df.loc[orig_df["cluster_label"] == l, "pid"]))
        uni_df.at[l, "PID diversity"] = pid_div
        
#################################    

def label_cluster_id(orig_df, uni_df, cl_headers):
    """
        add unique cluster labels to big df with all generalizations
            e.g. to analyze occurrence over time
    """
    # merge df with unique and all clusters to have cluster labels for all clusters
    #   merge is done on the minmaxheaders, so the generalized attributes 
    #   whose unique value combinations are the identifier of unique clusters
    merged_df = pd.merge(orig_df, uni_df, on=cl_headers, how='inner')
    return merged_df

#################################

def get_unique_cluster(df, cl_headers):
    """
        extract unique clusters based on unique value combinations of generalized attributes
    """
    print("unique clusters\n")
    uni_df = df.groupby(cl_headers).size().reset_index().rename(columns={0:'tuple_count'})
    uni_df["cluster_label"] = range(0, len(uni_df))
    
    return uni_df

#################################

def split_columns(df, headers):
    """
        split columns into columns with min and max limit
    """
    for h in headers:
        if( '[' in df[h].to_string()):
            df[h] = df[h].str.replace('[', '', regex = False)
            df[["min"+h, "max"+h]] = df[h].str.split(", ", expand = True).astype(int)
        else:
            # if attribute was not generalized during ano process, meaning that no intervals were formed
            #   => just use the same value for min and max
            df["min"+h] = df[h]
            df["max"+h] = df[h]
        df = df.drop([h], axis = 1)
    return df

#################################
#################################

def process_anonymized_df(input_file, headers): 
    '''
        call all functions that are needed for processing the anonymized data
    '''
    path = "../anonymized_data/"
    print("Now loading: " + input_file)
    df = pd.read_csv((path + input_file), index_col = False, sep = ",")
    
    # split columns that were generalized and contain intervals at the moment        
    df = split_columns(df, headers)
    
    # needed for all headers that were indicated as QI during anonymization
    # needed to add the remaining headers: anonymization ran on these as well but nothing was grouped => however, still needed fot cluster identification
    cl_headers = []
    for h in headers:
        cl_headers.append("min"+h)
        cl_headers.append("max"+h)
        
    # find unique QI combinations to identify clusters
    unique_cluster_df = get_unique_cluster(df, cl_headers)
    print(unique_cluster_df.head())
    
    # add cluster labels to original data set for further processing
    df = label_cluster_id(df, unique_cluster_df, cl_headers)
    
    # calculate diversity of sensitive attribute
    calc_diversity(df, unique_cluster_df)
    
    # save original data file with cluster labels
    output_file = "labeledCl_" + input_file  
    df.to_csv((path + output_file), sep = ",")
    
    # calculate the range of the sensitive attribute for all clusters inspired by Zhang 2007
    calc_sensitive_range(df, unique_cluster_df)
    
    # calculate the avergae difference between neighbouring sensitive attribute values for each cluster
    calc_sensitive_difference(df, unique_cluster_df)
    
    # evaluate the proximity of neighbouring sensitive attribute values for each cluster inspired by J. Li 2008
    epsilon = 0.2
    evaluate_proximity(df, unique_cluster_df, epsilon)
    #evaluate_proximity_wo_zero(df, unique_cluster_df) # proximity without zero values
    del(df)
    
    """calculate further information for each cluster"""
    calc_cluster_range(unique_cluster_df, headers)
    calc_info_loss(unique_cluster_df, headers)

    output_file = "ANALYZED_CLUSTERS_prox" + str(int(epsilon*100)) + "_" + input_file
    unique_cluster_df.to_csv((path + output_file), sep = ",")

#################################
#################################
def main():
    year = "2014"
    month = "11"
    sample_size = 164102
    l_k = [10, 25, 50, 100]
    header_str = ["address", "week", "weekday", "time" ] 
    header_str = ''.join(header_str)
    
    woHigh = False # optionally: possible to analyze simulation in which large consumers were excluded
    
    for k in l_k:
        input_file = "ARX_anonymization_370users_" + year + '-' + month + "_k" + str(k) +"_headers-" + header_str + ".csv"
        headers = ["address", "year", "week", "weekday", "time" ] # QI attributes
        if(woHigh):
            input_file = "wo_high_" + input_file
            
        process_anonymized_df(input_file, headers)     
                    
                        

if __name__ == "__main__":
    main()