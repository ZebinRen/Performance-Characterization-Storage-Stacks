#! /bin/bash
FIO_RUN_TIME=10
FIO_RAMP_TIME=5

SPDK_FIO_PLUGIN=
SPDK_SETUP_PATH=

declare -a engine=("aio" "iou" "iou_s" "iou_c")
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