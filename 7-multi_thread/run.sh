#! /bin/bash
FIO_RUN_TIME=5
FIO_RAMP_TIME=3

SPDK_FIO_PLUGIN=
SPDK_SETUP_PATH= 
SPDK_PERF_PATH=

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
FIO_RUN_TIME=$FIO_RUN_TIME FIO_RAMP_TIME=$FIO_RAMP_TIME fio ${e}.conf --numjobs=${t} --thread=1 --output-format=json -o $RESULT/${e}_t_${t}.txt;
done

declare -a num_threads=("6" "7" "8" "9" "10")

chcpu -e 1-9;

for t in "${num_threads[@]}"
do
FIO_RUN_TIME=$FIO_RUN_TIME FIO_RAMP_TIME=$FIO_RAMP_TIME fio ${e}.conf --numjobs=${t} --thread=1 --output-format=json -o $RESULT/${e}_t_${t}.txt;
done


$SPDK_SETUP_PATH;

# on socket 1
e='spdk_fio'
declare -a spdk_mask=("palceholder" "80000" "c0000" "e0000" "f0000" "f8000" "fc000" "fe000" "ff000" "ff800" "ffc00" "ffe00" "fff00" "fff80" "fffc0" "fffe0" "ffff0" "ffff8" "ffffc" "ffffe" "fffff")

for t in "${num_threads_socket1[@]}"
do
numactl -C $((20-${t}))-19 -m 1 env FIO_RUN_TIME=$FIO_RUN_TIME FIO_RAMP_TIME=$FIO_RAMP_TIME LD_PRELOAD=$SPDK_FIO_PLUGIN fio ${e}.conf --thread=1 --output-format=json --numjobs=${t} -o $RESULT/${e}_t_${t}.txt;
numactl -C $((20-${t}))-19 -m 1 $SPDK_PERF_PATH -q 128 -o 4096 -w randread -r 'trtype:PCIe traddr:0000:af:00.0' -r 'trtype:PCIe traddr:0000:b0:00.0' -r 'trtype:PCIe traddr:0000:b1:00.0' -r 'trtype:PCIe traddr:0000:b2:00.0' -r 'trtype:PCIe traddr:0000:d8:00.0' -r 'trtype:PCIe traddr:0000:da:00.0' -r 'trtype:PCIe traddr:0000:db:00.0' -t $FIO_RUN_TIME -a $FIO_RAMP_TIME -c ${spdk_mask[$t]}  > $RESULT/spdk_perf_t_${t}.txt;
done

# # both socket 1 and socket 2

for t in "${num_threads_socket2[@]}"
do
numactl -C $((20-${t}))-19 env FIO_RUN_TIME=$FIO_RUN_TIME FIO_RAMP_TIME=$FIO_RAMP_TIME LD_PRELOAD=$SPDK_FIO_PLUGIN fio ${e}.conf --thread=1 --output-format=json --numjobs=${t} -o $RESULT/${e}_t_${t}.txt;
numactl -C $((20-${t}))-19 $SPDK_PERF_PATH -q 128 -o 4096 -w randread -r 'trtype:PCIe traddr:0000:af:00.0' -r 'trtype:PCIe traddr:0000:b0:00.0' -r 'trtype:PCIe traddr:0000:b1:00.0' -r 'trtype:PCIe traddr:0000:b2:00.0' -r 'trtype:PCIe traddr:0000:d8:00.0' -r 'trtype:PCIe traddr:0000:da:00.0' -r 'trtype:PCIe traddr:0000:db:00.0' -t $FIO_RUN_TIME -a $FIO_RAMP_TIME -c ${spdk_mask[$t]} > $RESULT/spdk_perf_t_${t}.txt;
done

## SPDK PERF

$SPDK_SETUP_PATH reset;
