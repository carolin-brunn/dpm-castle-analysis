import numpy as np
import pandas as pd
import csv

import app

from castle import CASTLE, Parameters
from visualisations import display_visualisation
import datetime as dt

def handler(value: pd.Series):
    #print("RECIEVED VALUE: \n{}".format(value))
    return

def create_csvfile(output_file, headers, n_users):
    col_names = ["consumption", "year"]
    
    if(n_users == 1):
        col_names.append("address")
    
    for h in headers:
        col_names.append("min"+h)
        col_names.append("max"+h)
     
    col_names.append("orig_pid")
    
    if(n_users == 1):
        col_names.append("orig_address")
        
    for h in headers:
        col_names.append("orig_"+h)
        if(h == "address"):
            col_names.append("orig_year")
        
    col_names.extend(["delta", "k", "beta", "tau", "mu", "l", "dp", "tkc", "norm_il"])
    
    with open(output_file, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(col_names)


def main():
    args = app.parse_args()
    print("args: {}".format(args))

    seed = 42 # NEW same seed for all simulations #args.seed if args.seed else np.random.randint(1e6)
    np.random.seed(seed)
    print("USING RANDOM SEED: {}".format(seed))
    print("START: ", dt.datetime.now())
    
    n_users = args.n_users #370 # 370
    user_id = args.user_id #210
    year = args.year #"2011"
    month = args.month #"01"
    transformed_date = True
    
    path = "../consumption_data/"
    filename = "transformed_date_2011-01-eletricity_consumption_week_sample_164102.csv"
        
    if(transformed_date):
        # sort_keys = ["address", "year", "week", "weekday", "time"] # needed if sample is extracted randomly and needs to be sorted
        
        ### Eletricity consumption ###
        headers = ["address", "week", "weekday", "time"] #["time", "weekday", "week", "address"]  #["address", "year", "week", "weekday", "time"]
        if(n_users == 1):
            filename = "PID_" + str(user_id) + "_" + filename
            path = "../consumption_data/singleUser/"
            headers = [ "week", "weekday", "time"] # !!! Address cannot be used as generalized attribute
        
        sensitive_attr = "consumption"
        
        # specify dtype off columns (Warning otherwise) because consumption is of type object
        frame = pd.read_csv(( path + filename), index_col = False, dtype={0:'object',1:'int64',2:'int64', 3:'int64', 4:'int64', 5:'int64', 6:'int64'})
        
    
    ### PID is needed for further processing -> add if missing 
    if( "pid" not in frame.columns):
        frame["pid"] = np.arange(0, len(frame.iloc[0:,1]), 1)
    
        
    if(n_users == 1):
        frame["pid"] = frame.index # reset inex to enable algorithm looking for ks-ano 

    
    """NEW: artificial test frame to raise split_l exception"""
    #frame = frame[frame["pid"].isin([1, 2, 3, 4, 5])]
    #frame = frame.reset_index(drop = True)
    
    # use whole file if sample_size is set to zero or indicated sample_size larger than file size
    if((args.sample_size > 0) & (args.sample_size < len(frame))):
        #frame = frame.sample(args.sample_size).sort_values(by=sort_keys).reset_index(drop=True) # RANDOM SAMPLE
        frame = frame.iloc[:args.sample_size] # ORDERED SAMPLE

    params = Parameters(args)
    
    # create CASTLE instance
    stream = CASTLE(handler, headers, sensitive_attr, params)
    
    # delta == 0 indicates ground truth simulation -> look at whole dataset at once
    if(stream.delta == 0):
        stream.delta = len(frame)
        str_delta = "complete"
    else:
        str_delta = str(stream.delta)

    header_str = ''.join(headers)
    sample_size = args.sample_size #164102 #len(frame) # args.sample_size TODO: rather use specified size even if frame is smaller in case of a lot of varying frame sizes
    
    output_file = "anonymization_" + str(n_users) + "users"  + "_PID" + str(n_users) + "_" + year + "-" + month\
                        + "_delta" + str_delta + "_k" + str(stream.k) + "_sample" + str(sample_size)\
                        + "_headers-" + header_str + "_seed" + str(seed) + ".csv"
                        
    if(n_users == 1):
        output_file = "anonymization_" + str(n_users) + "users_" + "_PID" + str(user_id) + "_" + year + "-" + month\
                            + "_delta" + str_delta + "_k" + str(stream.k) + "_sample" + str(sample_size)\
                            + "_headers-" + header_str + "_seed" + str(seed) + ".csv"  
                            
    if(transformed_date):
        output_file = "transformed_date_" + output_file
        
    if(stream.norm_il):
        output_file = "normIL_" + output_file
    
    # define and prepare file to store generalized tuples in
    ### for GROUND TRUTH: filename ###
    #output_file = "anonymized_" + filename
    
    path = "../anonymized_data/"
    create_csvfile(( path + output_file), headers, n_users)
    stream.gentuple_file = ( path + output_file)

    ### START simulation ###
    for (_, row) in frame.iterrows():
        stream.insert(row)
     
    ### NEW ###
    # every row is inserted to clusters in the previous step, 
    # however, delay_constraint is only called when global_tuples is larger than delta
    # hence, to publish the last tupes, we call delay_constraint procedure again
    while( len(stream.global_tuples) > 0):
        stream.delay_constraint(stream.global_tuples[0])
        stream.update_tau()
    
    print("END: ", dt.datetime.now())
    
    if args.display:
        display_visualisation(stream)

if __name__ == "__main__":
    main()
