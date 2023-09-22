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

"""
create a csv file to save published clusters for later analysis
TODO: headers and order of columns have to be adapted manually if simulation structure/results change
"""
def create_csvfile(output_file, headers, n_users):
    # non-modified data
    col_names = ["consumption", "year"]
    
    if(n_users == 1):
        col_names.append("address") # identifying for single user => deleted
    
    # QI range in clusters after anonymization
    for h in headers:
        col_names.append("min"+h)
        col_names.append("max"+h)
     
    # original identifying data (deleted in anonymization process)
    col_names.append("orig_pid")
    
    if(n_users == 1):
        col_names.append("orig_address")

    # original QI data
    for h in headers:
        col_names.append("orig_"+h)
        if(h == "address"):
            col_names.append("orig_year") # == year in case of anonymization without year

    # CASTLE parameters
    col_names.extend(["delta", "k", "beta", "tau", "mu", "l", "dp", "tkc", "norm_il"])
    
    with open(output_file, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(col_names)


def main():
    ### adapted simulation call for dataset with ### Eletricity consumption ###
    args = app.parse_args()
    print("args: {}".format(args))

    seed = 42 # NEW same seed for all simulations. => randome seed or argument: args.seed if args.seed else np.random.randint(1e6)
    np.random.seed(seed)
    print("USING RANDOM SEED: {}".format(seed))
    print("START: ", dt.datetime.now())
    
    n_users = args.n_users # define how many users shall be considered. => complete dataset: 370
    user_id = args.user_id #210
    year = args.year #"2014"
    month = args.month #"11"
    transformed_date = True # date format was transformed to contain (year, week, weekday) instead of date. tihs might enable discovery of weekly trends at a later point in time
    
    path = "../consumption_data/"
    if(args.filename):
        filename = args.filename
    else:
        filename = "transformed_date_" + year + "-" + month + "-eletricity_consumption_sample_164102.csv"
        
    """
    NEW: artificial test frame to raise exception in split_l() function
        this frame will cause non-ks-anonymous clusters after anonymization,
            because only the value of the sensitive attribute is considered in the funciton
        in the check right before cluster publication this is discovered and an exception is raised
    """
    # filename = "example_data_raise_split_l_excep.csv"

    if(transformed_date):

        headers = ["address", "week", "weekday", "time"] # year might be added as QI, but can be left our in case of a single year (["address", "year", "week", "weekday", "time"])
        if(n_users == 1):
            filename = "PID_" + str(user_id) + "_" + filename
            path = "../consumption_data/singleUser/"
            headers = [ "week", "weekday", "time"] # !!! Address cannot be used as generalized attribute in case of a single individual. instead it is an identifying attribute
        
        sensitive_attr = "consumption"
        
        frame = pd.read_csv(( path + filename), index_col = False)
        
    
    ### PID is needed for further processing -> add random PID if missing
    if( "pid" not in frame.columns):
        frame["pid"] = np.arange(0, len(frame.iloc[0:,1]), 1)
    
    if(n_users == 1):
        frame["pid"] = frame.index # create artificial index to enable algorithm looking for ks-ano

    
    # extract an ordered sample if a specific sample_size is indicated
    # otherwise use whole file if sample_size == 0 or indicated sample_size is larger than file size
    # in the data preprocessing, the dataset was transformed such that only a random third of the tuples is included in the sample
    #   the size of the dataset with 1/3 of the data points of Nove,ber 2014 is 164102
    if((args.sample_size > 0) & (args.sample_size < len(frame))):
        frame = frame.iloc[:args.sample_size] # ORDERED SAMPLE

    params = Parameters(args)

    # create CASTLE instance
    stream = CASTLE(handler, headers, sensitive_attr, params)
    
    # delta == 0 indicates ground truth simulation -> look at whole dataset at once
    #   TODO: large deltas do not finish since the simulation does not seem to scale
    if(stream.delta == 0):
        stream.delta = len(frame)
        str_delta = "complete"
    else:
        str_delta = str(stream.delta)

    header_str = ''.join(headers)
    sample_size = len(frame) # args.sample_size # TODO: rather use specified size even if frame is smaller in case of a lot of varying frame sizes?! => that might make further processing easier, e.g., if sample_size == 0 (complete set)
    
    output_file = "anonymization_" + str(n_users) + "users"  + "_PID" + str(n_users) + "_" + year + "-" + month\
                        + "_delta" + str_delta + "_k" + str(stream.k) + "_sample" + str(sample_size)\
                        + "_headers-" + header_str + "_seed" + str(seed) + ".csv"
                        
    if(n_users == 1):
        output_file = "anonymization_" + str(n_users) + "users_" + "_PID" + str(user_id) + "_" + year + "-" + month\
                            + "_delta" + str_delta + "_k" + str(stream.k) + "_sample" + str(sample_size)\
                            + "_headers-" + header_str + "_seed" + str(seed) + ".csv"  
                            
    if(transformed_date):
        output_file = "transformed_date_" + output_file
           
    if("wo_high" in filename):
        output_file = "wo_high_" + output_file

    path = "../anonymized_data/"
    print(path+output_file)
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
