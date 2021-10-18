#/bin/sh

# warning: you won't be able to easily interrupt this process

for numworkers in 14 16
do
    for batch_size in 8 32 64 128
    do
        for bmul_size in 8 16 20 22 24
        do
            python3 closed_beta.py $numworkers 50000 $batch_size $bmul_size
        done
    done
done