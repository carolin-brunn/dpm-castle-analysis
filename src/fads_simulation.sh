#! /bin/bash

a_k=(10 25 50 100)
a_d=(100 200 400)
beta=200000 # do not want this parameter to influence the results
mu=100000
l=1
tkc=50

# all users simulatino for centralized scenario
n_users=370
year="2011"
month="01"

echo "start bash script now"

### all users simulation for centralized scenario
#for d in "${a_d[@]}"
#do
#    for k in "${a_k[@]}"
#    do
#        echo $k
#        echo $d
#        python3 main.py --k $k --sample-size 0 --delta $d --beta $beta --mu $mu --l $l --tkc $tkc --disable-dp --year $year --month $month --n_users $n_users --user_id $n_users
#    done
#done


### ground truth for all n_users
#n_users=370
#user_id=370
#d=40000
#beta=200000
#mu=100000
#k=100
#python3 main.py --k $k --sample-size 0 --delta $d --beta $beta --mu $mu --l $l --tkc $tkc --disable-dp --year $year --month $month --n_users $n_users --user_id $user_id


### single user simulation for decentralized scenario
a_d=(100 200 400)
beta=200000
mu=100000
n_users=1
#user_id=(3 10 13 98 134 150 210 278 310 345)
#user_range=100
for d in "${a_d[@]}"
do
    for k in "${a_k[@]}"
    do
        for id in $(seq 100 371)
        do
            echo $k
            echo $d
            echo $id
            python3 main.py --k $k --sample-size 0 --delta $d --beta $beta --mu $mu --l $l --tkc $tkc --disable-dp --year $year --month $month --n_users $n_users --user_id $id
        done
    done
done

### ground truth for single users
d=0 #=> ground truth simulation on whole dataset at once
beta=200000
mu=100000
n_users=1
#user_id=(3 10 13 98 134 150 210 278 310 345)
#user_range=100
for k in "${a_k[@]}"
do
    #for id in "${user_id[@]}"
    for id in $(seq 100 370)
    do
        echo $k
        echo $d
        echo $id
        python3 main.py --k $k --sample-size 0 --delta $d --beta $beta --mu $mu --l $l --tkc $tkc --disable-dp --year $year --month $month --n_users $n_users --user_id $id
    done
done

