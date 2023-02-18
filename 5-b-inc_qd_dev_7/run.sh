#!/bin/bash
# NOTE: DISABLE other cpu when running this experiment

SPDK_FIO_PLUGIN=
SPDK_SETUP_PATH=

FIO_RUN_TIME=5
FIO_RAMP_TIME=3

declare -a engine=("aio" "iou" "iou_s" "iou_c")
declare -a qd=("1" "2" "4" "8" "16" "32" "64" "128")

RESULT='results'

$SPDK_SETUP_PATH reset;

for e in "${engine[@]}"
do
    for q in "${qd[@]}"
    do
    $NUMA_PIN env FIO_RUN_TIME=$FIO_RUN_TIME FIO_RAMP_TIME=$FIO_RAMP_TIME fio --iodepth=$q ${e}.conf --output-format=json -o $RESULT/${e}_qd_${q}.txt;
    done    
done

$SPDK_SETUP_PATH;

e='spdk_fio'
for q in "${qd[@]}"
do
$NUMA_PIN env LD_PRELOAD=$SPDK_FIO_PLUGIN FIO_RUN_TIME=$FIO_RUN_TIME FIO_RAMP_TIME=$FIO_RAMP_TIME fio --iodepth=$q ${e}.conf --output-format=json -o $RESULT/${e}_qd_${q}.txt;
done

$SPDK_SETUP_PATH reset;