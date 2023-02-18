#! /bin/bash
FIO_RUN_TIME=120
FIO_RAMP_TIME=20

declare -a engine=("aio" "iou" "iou_c")
declare -a sched=("none" "bfq" "kyber" "mq-deadline")
declare -a num_threads=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10")


RESULT='results'

SPDK_SETUP_PATH=

$SPDK_SETUP_PATH reset

for e in "${engine[@]}"
do
    for s in "${sched[@]}"
    do
        for t in "${num_threads[@]}"
        do
        numactl -C $((20-${t}))-19 -m 1 env FIO_RUN_TIME=$FIO_RUN_TIME FIO_RAMP_TIME=$FIO_RAMP_TIME fio ${e}.conf --ioscheduler=${s} --numjobs=${t} --thread=1 --output-format=json -o $RESULT/${e}_${s}_threads_${t}.txt;
        done
    done
done

declare -a num_threads=("11" "12" "13" "14" "15" "16" "17" "18" "19" "20")

for e in "${engine[@]}"
do
    for s in "${sched[@]}"
    do
        for t in "${num_threads[@]}"
        do
        numactl -C $((20-${t}))-19 -m 1 env FIO_RUN_TIME=$FIO_RUN_TIME FIO_RAMP_TIME=$FIO_RAMP_TIME fio ${e}.conf --ioscheduler=${s} --numjobs=${t} --thread=1 --output-format=json -o $RESULT/${e}_${s}_threads_${t}.txt;
        done
    done
done

declare -a num_threads=("1" "2" "3" "4" "5")

chcpu -d 1-9

e='iou_s'
for s in "${sched[@]}"
do
    for t in "${num_threads[@]}"
    do
    FIO_RUN_TIME=$FIO_RUN_TIME FIO_RAMP_TIME=$FIO_RAMP_TIME fio ${e}.conf --ioscheduler=${s} --numjobs=${t} --thread=1 --output-format=json -o $RESULT/${e}_${s}_threads_${t}.txt;
    done
done

declare -a num_threads=("6" "7" "8" "9" "10")

chcpu -e 1-9

for s in "${sched[@]}"
do
    for t in "${num_threads[@]}"
    do
    FIO_RUN_TIME=$FIO_RUN_TIME FIO_RAMP_TIME=$FIO_RAMP_TIME fio ${e}.conf --ioscheduler=${s} --numjobs=${t} --thread=1 --output-format=json -o $RESULT/${e}_${s}_threads_${t}.txt;
    done
done