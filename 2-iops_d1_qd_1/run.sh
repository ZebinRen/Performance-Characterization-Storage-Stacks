#/bin/bash

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

PINNED_CPU=19
PINNED_CPU_POLL=18

# Some arguments
FIO_RUN_TIME=20
FIO_RAMP_TIME=120

DEVICES="/dev/nvme0n1"
FIO_OPTIONS="--time_based=1 --ramp_time=${FIO_RAMP_TIME}s --runtime=${FIO_RUN_TIME}s --size=100% --bs=4kb --norandommap=1 --group_reporting=1 --direct=1 --rw=randread --allow_file_create=0 --iodepth=1 --cpus_allowed=${PINNED_CPU} --output-format=json --filename=${DEVICES} --name=1"

FIO_OPTIONS_SPDK="--time_based=1 --ioengine=spdk --ramp_time=${FIO_RAMP_TIME}s --runtime=${FIO_RUN_TIME}s --size=100% --bs=4kb --thread=1 --norandommap=1 --group_reporting=1 --direct=1 --rw=randread --allow_file_create=0 --iodepth=1 --cpus_allowed=${PINNED_CPU} --output-format=json --name=1"

echo "Execute: chcpu -d 0-19"
chcpu -d 0-19
echo "Execute: chcpu -e ${PINNED_CPU}"
chcpu -e ${PINNED_CPU}

echo "Execute: $SPDK_SETUP_PATH reset;"
$SPDK_SETUP_PATH reset;
echo "Execute: fio --ioengine=psync ${FIO_OPTIONS} -o $RESULTS/psync.txt"
fio --ioengine=psync ${FIO_OPTIONS} -o $RESULTS/psync.txt
echo "Execute: fio --ioengine=libaio ${FIO_OPTIONS} -o $RESULTS/aio.txt"
fio --ioengine=libaio ${FIO_OPTIONS} -o $RESULTS/aio.txt
echo "Execute: fio --ioengine=io_uring ${FIO_OPTIONS} -o $RESULTS/iou.txt"
fio --ioengine=io_uring ${FIO_OPTIONS} -o $RESULTS/iou.txt
echo "Execute: fio --ioengine=io_uring --hipri --registerfiles=1 --fixedbufs=1 ${FIO_OPTIONS} -o $RESULTS/iou_c.txt"
fio --ioengine=io_uring --hipri --registerfiles=1 --fixedbufs=1 ${FIO_OPTIONS} -o $RESULTS/iou_c.txt
echo "Execute: chcpu -e ${PINNED_CPU_POLL}"
chcpu -e ${PINNED_CPU_POLL}
echo "Execute: fio --ioengine=io_uring --sqthread_poll=${PINNED_CPU_POLL} --sqthread_poll_cpu=18 --registerfiles=1 --fixedbufs=1 ${FIO_OPTIONS} -o $RESULTS/iou_s.txt"
fio --ioengine=io_uring --sqthread_poll=${PINNED_CPU_POLL} --sqthread_poll_cpu=18 --registerfiles=1 --fixedbufs=1 ${FIO_OPTIONS} -o $RESULTS/iou_s.txt

echo "Execute: " $SPDK_SETUP_PATH
$SPDK_SETUP_PATH
echo "Execute: " LD_PRELOAD=$SPDK_FIO_PLUGIN fio ${FIO_OPTIONS_SPDK} -o $RESULTS/spdk_fio.txt
LD_PRELOAD=$SPDK_FIO_PLUGIN fio --filename="trtype=PCIe traddr=0000.b1.00.0 ns=1" ${FIO_OPTIONS_SPDK} -o $RESULTS/spdk_fio.txt
echo "Execute: $SPDK_SETUP_PATH reset"
$SPDK_SETUP_PATH reset

echo "Execute: chcpu -e 0-19"
chcpu -e 0-19