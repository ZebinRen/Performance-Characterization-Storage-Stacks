#! /bin/bash

## Unused
# PERF_LLC_SLEEP_TIME=5
# PERF_LLC_REPEAT_TIME=1
# PERF_DTLB_SLEEP_TIME=5
# PERF_DTLB_REPEAT_TIME=1
# PERF_ITLB_SLEEP_TIME=5
# PERF_ITLB_REPEAT_TIME=1
# PERF_BRANCH_SLEEP_TIME=5
# PERF_BRANCH_REPEAT_TIME=1
# PERF_CS_SLEEP_TIME=5
# PERF_CS_REPEAT_TIME=1

PERF_INST_SLEEP_TIME=5
PERF_INST_REPEAT_TIME=1
PERF_CACHE_SLEEP_TIME=5
PERF_CACHE_REPEAT_TIME=1

PERF_WAIT_TIME=20
FIO_RUN_TIME_ALL=200
FIO_RAMP_TIME=20


SPDK_FIO_PLUGIN=
SPDK_SETUP_PATH=

declare -a engine=("aio" "iou" "iou_s" "iou_c")
declare -a perf_seq=("0" "1" "2" "3" "4" "5" "6" "7" "8" "9")

# system-wide

RESULT='results_global'

$SPDK_SETUP_PATH reset

for e in "${engine[@]}"
do
numactl -N 1 -m 1 env FIO_RUN_TIME=$FIO_RUN_TIME_ALL FIO_RAMP_TIME=$FIO_RAMP_TIME fio ${e}.conf --output-format=json -o $RESULT/${e}.txt &
sleep $PERF_WAIT_TIME;
    for i in "${perf_seq[@]}"
    do
    perf stat -e cycles,instructions -a -r $PERF_INST_REPEAT_TIME -o $RESULT/${e}_inst_cycle_${i}.txt -- sleep $PERF_INST_SLEEP_TIME ; 
    perf stat -e cache-misses,cache-references -a -r $PERF_CACHE_REPEAT_TIME -o $RESULT/${e}_cache_${i}.txt -- sleep $PERF_CACHE_SLEEP_TIME;
    done
wait;
done

$SPDK_SETUP_PATH
e="spdk_fio"
numactl -N 1 -m 1 env FIO_RUN_TIME=$FIO_RUN_TIME_ALL FIO_RAMP_TIME=$FIO_RAMP_TIME LD_PRELOAD=$SPDK_FIO_PLUGIN fio ${e}.conf --output-format=json -o $RESULT/${e}.txt &
sleep $PERF_WAIT_TIME;
    for i in "${perf_seq[@]}"
    do
    perf stat -e cycles,instructions -a -r $PERF_INST_REPEAT_TIME -o $RESULT/${e}_inst_cycle_${i}.txt -- sleep $PERF_INST_SLEEP_TIME ; 
    perf stat -e cache-misses,cache-references -a -r $PERF_CACHE_REPEAT_TIME -o $RESULT/${e}_cache_${i}.txt -- sleep $PERF_CACHE_SLEEP_TIME;
    done
wait

$SPDK_SETUP_PATH reset

# process specific

RESULT='results_local'

for e in "${engine[@]}"
do

numactl -N 1 -m 1 env FIO_RUN_TIME=$FIO_RUN_TIME_ALL FIO_RAMP_TIME=$FIO_RAMP_TIME fio ${e}.conf --output-format=json -o $RESULT/${e}.txt &
sleep $PERF_WAIT_TIME;
    for i in "${perf_seq[@]}"
    do
    perf stat -e cycles,instructions -p `pidof fio` -r $PERF_INST_REPEAT_TIME -o $RESULT/${e}_inst_cycle_${i}.txt -- sleep $PERF_INST_SLEEP_TIME ; 
    perf stat -e cache-misses,cache-references -p `pidof fio` -r $PERF_CACHE_REPEAT_TIME -o $RESULT/${e}_cache_${i}.txt -- sleep $PERF_CACHE_SLEEP_TIME;
    done
wait;
done

$SPDK_SETUP_PATH

e="spdk_fio"

numactl -N 1 -m 1 env FIO_RUN_TIME=$FIO_RUN_TIME_ALL FIO_RAMP_TIME=$FIO_RAMP_TIME LD_PRELOAD=$SPDK_FIO_PLUGIN fio ${e}.conf --output-format=json -o $RESULT/${e}.txt &
sleep $PERF_WAIT_TIME;
    for i in "${perf_seq[@]}"
    do
    perf stat -e cycles,instructions -p `pidof fio` -r $PERF_INST_REPEAT_TIME -o $RESULT/${e}_inst_cycle_${i}.txt -- sleep $PERF_INST_SLEEP_TIME ; 
    perf stat -e cache-misses,cache-references -p `pidof fio` -r $PERF_CACHE_REPEAT_TIME -o $RESULT/${e}_cache_${i}.txt -- sleep $PERF_CACHE_SLEEP_TIME;
    done
wait

$SPDK_SETUP_PATH
