#/bin/bash

# SPDK_FIO_PLUGIN
# SPDK_SETUP_PATH
RESULTS=results

FIO_RUN_TIME=120
FIO_RAMP_TIME=20
NUMA_PIN='numactl -N 1 -m 1'
 
$SPDK_SETUP_PATH reset;
$NUMA_PIN env FIO_RUN_TIME=$FIO_RUN_TIME FIO_RAMP_TIME=$FIO_RAMP_TIME fio psync.conf --output-format=json -o $RESULTS/psync.txt;
$NUMA_PIN env FIO_RUN_TIME=$FIO_RUN_TIME FIO_RAMP_TIME=$FIO_RAMP_TIME fio aio.conf --output-format=json -o $RESULTS/aio.txt;
$NUMA_PIN env FIO_RUN_TIME=$FIO_RUN_TIME FIO_RAMP_TIME=$FIO_RAMP_TIME fio iou.conf --output-format=json -o $RESULTS/iou.txt;
$NUMA_PIN env FIO_RUN_TIME=$FIO_RUN_TIME FIO_RAMP_TIME=$FIO_RAMP_TIME fio iou_c.conf --output-format=json -o $RESULTS/iou_c.txt;
$NUMA_PIN env FIO_RUN_TIME=$FIO_RUN_TIME FIO_RAMP_TIME=$FIO_RAMP_TIME fio iou_s.conf --output-format=json -o $RESULTS/iou_s.txt;

$SPDK_SETUP_PATH;
$NUMA_PIN env LD_PRELOAD=$SPDK_FIO_PLUGIN FIO_RUN_TIME=$FIO_RUN_TIME FIO_RAMP_TIME=$FIO_RAMP_TIME fio spdk_fio.conf --output-format=json -o $RESULTS/spdk_fio.txt;
$SPDK_SETUP_PATH reset;