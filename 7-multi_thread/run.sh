#! /bin/bash
FIO_RUN_TIME=120
FIO_RAMP_TIME=20

SPDK_FIO_PLUGIN=
SPDK_SETUP_PATH=

declare -a engine=("aio" "iou" "iou_c" "iou_s")
declare -a num_threads_socket1=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10")
declare -a num_threads_socket2=("11" "12" "13" "14" "15" "16" "17" "18" "19" "20")

# system-wide
RESULT='results'

$SPDK_SETUP_PATH reset;

# on socket 1
for e in "${engine[@]}"
do
    for t in "${num_threads_socket1[@]}"
    do
    numactl -C $((20-${t}))-19 -m 1 env FIO_RUN_TIME=$FIO_RUN_TIME  FIO_RAMP_TIME=$FIO_RAMP_TIME fio ${e}.conf --thread=1 --output-format=json --numjobs=${t} -o $RESULT/${e}_t_${t}.txt;
    done
done

# both socket 1 and socket 2
for e in "${engine[@]}"
do
    for t in "${num_threads_socket2[@]}"
    do
    numactl -C $((20-${t}))-19 env FIO_RUN_TIME=$FIO_RUN_TIME  FIO_RAMP_TIME=$FIO_RAMP_TIME fio ${e}.conf --thread=1 --output-format=json --numjobs=${t} -o $RESULT/${e}_t_${t}.txt;
    done
done

declare -a num_threads=("1" "2" "3" "4" "5")

chcpu -d 1-9;

e='iou_s'

for t in "${num_threads[@]}"
do
FIO_RUN_TIME=$FIO_RUN_TIME FIO_RAMP_TIME=$FIO_RAMP_TIME fio ${e}.conf --ioscheduler=${s} --numjobs=${t} --thread=1 --output-format=json -o $RESULT/${e}_t_${t}.txt;
done


declare -a num_threads=("6" "7" "8" "9" "10")

chcpu -e 1-9;

for t in "${num_threads[@]}"
do
FIO_RUN_TIME=$FIO_RUN_TIME FIO_RAMP_TIME=$FIO_RAMP_TIME fio ${e}.conf --ioscheduler=${s} --numjobs=${t} --thread=1 --output-format=json -o $RESULT/${e}_t_${t}.txt;
done


$SPDK_SETUP_PATH;

# on socket 1
e='spdk_fio'

for t in "${num_threads_socket1[@]}"
do
numactl -C $((20-${t}))-19 -m 1 env FIO_RUN_TIME=$FIO_RUN_TIME FIO_RAMP_TIME=$FIO_RAMP_TIME LD_PRELOAD=$SPDK_FIO_PLUGIN fio ${e}.conf --thread=1 --output-format=json --numjobs=${t} -o $RESULT/${e}_t_${t}.txt;
done

# both socket 1 and socket 2

for t in "${num_threads_socket2[@]}"
do
numactl -C $((20-${t}))-19 env FIO_RUN_TIME=$FIO_RUN_TIME FIO_RAMP_TIME=$FIO_RAMP_TIME LD_PRELOAD=$SPDK_FIO_PLUGIN fio ${e}.conf --thread=1 --output-format=json --numjobs=${t} -o $RESULT/${e}_t_${t}.txt;
done

$SPDK_SETUP_PATH reset;


