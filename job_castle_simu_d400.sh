#!/bin/bash --login
#$ -cwd
#$ -N castle_normIL
#$ -o /work/XXX/castle_normIL/stdouts/$JOB_ID.$TASK_ID.$HOSTNAME
#$ -j y
#$ -l el8
#$ -l h_rt=04:00:00
#$ -m beas
#$ -pe mp 8
#$ -M carolin.brunn@gmx.de

echo "set parameters"

a_k=(10 25 50 50 100)
a_d=(400)
beta=200000 # do not want this parameter to influence the results
mu=100000
l=1
tkc=50

# all users simulatino for centralized scenario
n_users=370
year="2011"
month="01"
norm_il=1
max_header="week"

echo "start bash script now"

### all users simulation for centralized scenario
for d in "${a_d[@]}"
do
    for k in "${a_k[@]}"
    do
        echo $k
        echo $d
        python3 main.py --k $k --sample-size 0 --delta $d --beta $beta --mu $mu --l $l --tkc $tkc --disable-dp --year $year --month $month --n_users $n_users --user_id $n_users --norm_il $norm_il --max_header $max_header
    done
done

echo "finished successfully"

