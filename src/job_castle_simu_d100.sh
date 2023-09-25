#!/bin/bash -
echo "set parameters"

a_k=(10 25 50 100)
a_d=(100)
beta=200000 # do not want this parameter to influence the results
mu=100000
l=1
tkc=50

# all users simulation for centralized scenario
n_users=370
year="2014"
month="11"
norm_il=0
max_header="week"
filename="transformed_date_2014-11-eletricity_consumption_sample_164102.csv"

echo "start bash script now"

### all users simulation for centralized scenario
for d in "${a_d[@]}"
do
    for k in "${a_k[@]}"
    do
        echo $k
        echo $d
        python3 main.py --k $k --sample-size 0 --delta $d --beta $beta --mu $mu --l $l --tkc $tkc --disable-dp --year $year --month $month --n_users $n_users -f $filename
    done
done

echo "finished successfully"


