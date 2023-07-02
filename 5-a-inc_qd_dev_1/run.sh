#!/bin/bash
# NOTE: DISABLE other cpu when running this experiment

RESULTS=results

# Check if all the needed 
if [ $CHEOPS23_SPDK_FIO_PLUGIN == "" ]; then
  echo 'CHEOPS23_SPDK_FIO_PLUGIN is not set\n'
  exit
fi

if [ "$CHEOPS23_SPDK_SETUP_PATH" == "" ]; then
  echo "CHEOPS23_SPDK_SETUP_PATH is not set\n"
  exit
fi

# Set local variables
SPDK_FIO_PLUGIN=$CHEOPS23_SPDK_FIO_PLUGIN
SPDK_SETUP_PATH=$CHEOPS23_SPDK_SETUP_PATH

# constuct home directory and home directory
# if [ $"CHEOPS23_EXPR_HOME"=="" ]; then
# fi

PINNED_CPU=9
PINNED_CPU_POLL=8
MAX_CPU=9

# Some arguments
FIO_RAMP_TIME=20
FIO_RUN_TIME=120


DEVICES="/dev/nvme0n1"
FIO_OPTIONS="--time_based=1 --ramp_time=${FIO_RAMP_TIME}s --runtime=${FIO_RUN_TIME}s --size=100% --bs=4kb --norandommap=1 --group_reporting=1 --direct=1 --rw=randread --allow_file_create=0 --cpus_allowed=${PINNED_CPU} --output-format=json --filename=${DEVICES} --name=1"

FIO_OPTIONS_SPDK="--time_based=1 --ioengine=spdk --ramp_time=${FIO_RAMP_TIME}s --runtime=${FIO_RUN_TIME}s --size=100% --bs=4kb --thread=1 --norandommap=1 --group_reporting=1 --direct=1 --rw=randread --allow_file_create=0 --cpus_allowed=${PINNED_CPU} --output-format=json --name=1"

declare -a qd=("1" "2" "4" "8" "16" "32" "64" "128")

# Linux kernel stack
echo "Execute: $SPDK_SETUP_PATH reset;"
$SPDK_SETUP_PATH reset;


for q in "${qd[@]}"
do
    echo "Execute: fio --ioengine=libaio ${FIO_OPTIONS} -o $RESULTS/aio_qd_${q}.txt"
    fio --iodepth=${q}  --ioengine=libaio ${FIO_OPTIONS} -o $RESULTS/aio_qd_${q}.txt
    echo "Execute: fio --ioengine=io_uring ${FIO_OPTIONS} -o $RESULTS/iou_qd_${q}.txt"
    fio --iodepth=${q} --ioengine=io_uring ${FIO_OPTIONS} -o $RESULTS/iou_qd_${q}.txt
    echo "Execute: fio --ioengine=io_uring --hipri --registerfiles=1 --fixedbufs=1 ${FIO_OPTIONS} -o $RESULTS/iou_c_qd_${q}.txt"
    fio --iodepth=${q} --ioengine=io_uring --hipri --registerfiles=1 --fixedbufs=1 ${FIO_OPTIONS} -o $RESULTS/iou_c_qd_${q}.txt
    
    echo "Execute: chcpu -e ${PINNED_CPU_POLL}"
    chcpu -e ${PINNED_CPU_POLL}
    echo "Execute: fio --iodepth=${q} --ioengine=io_uring --sqthread_poll=1 --sqthread_poll_cpu=${PINNED_CPU_POLL} --registerfiles=1 --fixedbufs=1 ${FIO_OPTIONS} -o $RESULTS/iou_s_qd_${q}.txt"
    fio --iodepth=${q} --ioengine=io_uring --sqthread_poll=1 --sqthread_poll_cpu=${PINNED_CPU_POLL} --registerfiles=1 --fixedbufs=1 ${FIO_OPTIONS} -o $RESULTS/iou_s_qd_${q}.txt
    echo "Execute: chcpu -d ${PINNED_CPU_POLL}"
    chcpu -d ${PINNED_CPU_POLL}
done

echo "Execute: " $SPDK_SETUP_PATH
$SPDK_SETUP_PATH

for q in "${qd[@]}"
do
echo "Execute: LD_PRELOAD=$SPDK_FIO_PLUGIN fio --iodepth=${q} --filename="trtype=PCIe traddr=0000.65.00.0 ns=1" ${FIO_OPTIONS_SPDK} -o $RESULTS/spdk_fio_qd_${q}.txt"
LD_PRELOAD=$SPDK_FIO_PLUGIN fio --iodepth=${q} --filename="trtype=PCIe traddr=0000.65.00.0 ns=1" ${FIO_OPTIONS_SPDK} -o $RESULTS/spdk_fio_qd_${q}.txt
done

echo "Execute: $SPDK_SETUP_PATH reset"
$SPDK_SETUP_PATH reset

echo "Execute: chcpu -e 0-${MAX_CPU}"
chcpu -e 0-${MAX_CPU}
