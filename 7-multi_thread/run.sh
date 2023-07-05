#! /bin/bash

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

if [ "$CHEOPS23_SPDK_PERF" == "" ]; then
  echo "CHEOPS23_SPDK_PERF is not set\n"
  exit
fi


# Set local variables
SPDK_FIO_PLUGIN=$CHEOPS23_SPDK_FIO_PLUGIN
SPDK_SETUP_PATH=$CHEOPS23_SPDK_SETUP_PATH
SPDK_PERF_PATH=$CHEOPS23_SPDK_PERF

# Some arguments
FIO_RUN_TIME=5
FIO_RAMP_TIME=10

MAX_CPU_ID=19

DEVICES="/dev/nvme0n1:/dev/nvme1n1:/dev/nvme2n1:/dev/nvme3n1:/dev/nvme4n1:/dev/nvme6n1:/dev/nvme7n1"

FIO_OPTIONS="--time_based=1 --ramp_time=${FIO_RAMP_TIME}s --runtime=${FIO_RUN_TIME}s --size=100% --bs=4kb --norandommap=1 --group_reporting=1 --direct=1 --rw=randread --allow_file_create=0 --iodepth=128 --output-format=json --filename=${DEVICES} --name=1"

FIO_OPTIONS_SPDK="--time_based=1 --ioengine=spdk --ramp_time=${FIO_RAMP_TIME}s --runtime=${FIO_RUN_TIME}s --size=100% --bs=4kb --thread=1 --norandommap=1 --group_reporting=1 --direct=1 --rw=randread --allow_file_create=0 --iodepth=128 --output-format=json --name=1"

declare -a engine=("aio" "iou" "iou_c" "iou_s")
declare -a num_threads_socket1=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10")
declare -a num_threads_socket2=("11" "12" "13" "14" "15" "16" "17" "18" "19" "20")

# system-wide
RESULT='results'

echo "Execute: $SPDK_SETUP_PATH reset"
$SPDK_SETUP_PATH reset

echo "Execute: chcpu -d 0-${MAX_CPU_ID}"
chcpu -d 0-${MAX_CPU_ID}

# on socket 1
for t in "${num_threads_socket1[@]}"
do
    echo "Execute: chcpu -e $(((${MAX_CPU_ID}+1)-${t}))"
    chcpu -e $(((${MAX_CPU_ID}+1)-${t}))
    echo "Execute: fio --cpus_allowed=$(((${MAX_CPU_ID}+1)-${t}))-${MAX_CPU_ID} --ioengine=psync ${FIO_OPTIONS} --numjobs=${t} -o $RESULTS/psync_t_${t}.txt"
    fio --cpus_allowed=$(((${MAX_CPU_ID}+1)-${t}))-${MAX_CPU_ID} --ioengine=psync ${FIO_OPTIONS} --numjobs=${t} -o $RESULTS/psync_t_${t}.txt
    echo "Execute: fio --cpus_allowed=$(((${MAX_CPU_ID}+1)-${t}))-${MAX_CPU_ID} --ioengine=libaio ${FIO_OPTIONS} --numjobs=${t} -o $RESULTS/aio_t_${t}.txt"
    fio --cpus_allowed=$(((${MAX_CPU_ID}+1)-${t}))-${MAX_CPU_ID} --ioengine=libaio ${FIO_OPTIONS} --numjobs=${t} -o $RESULTS/aio_t_${t}.txt
    echo "Execute: fio --cpus_allowed=$(((${MAX_CPU_ID}+1)-${t}))-${MAX_CPU_ID} --ioengine=io_uring --registerfiles=1 --fixedbufs=1 ${FIO_OPTIONS} --numjobs=${t} -o $RESULTS/iou_t_${t}.txt"
    fio --cpus_allowed=$(((${MAX_CPU_ID}+1)-${t}))-${MAX_CPU_ID} --ioengine=io_uring --registerfiles=1 --fixedbufs=1 ${FIO_OPTIONS} --numjobs=${t} -o $RESULTS/iou_t_${t}.txt
    echo "Execute: fio --cpus_allowed=$(((${MAX_CPU_ID}+1)-${t}))-${MAX_CPU_ID} --ioengine=io_uring --hipri --registerfiles=1 --fixedbufs=1 ${FIO_OPTIONS} --numjobs=${t} -o $RESULTS/iou_c_t_${t}.txt"
    fio --cpus_allowed=$(((${MAX_CPU_ID}+1)-${t}))-${MAX_CPU_ID} --ioengine=io_uring --hipri --registerfiles=1 --fixedbufs=1 ${FIO_OPTIONS} --numjobs=${t} -o $RESULTS/iou_c_t_${t}.txt
done


# both socket 1 and socket 2
for t in "${num_threads_socket2[@]}"
do
    echo "Execute: chcpu -e $(((${MAX_CPU_ID}+1)-${t}))"
    chcpu -e $(((${MAX_CPU_ID}+1)-${t}))
    echo "Execute: fio --cpus_allowed=$(((${MAX_CPU_ID}+1)-${t}))-${MAX_CPU_ID} --ioengine=psync ${FIO_OPTIONS} --numjobs=${t} -o $RESULTS/psync_t_${t}.txt"
    fio --cpus_allowed=$(((${MAX_CPU_ID}+1)-${t}))-${MAX_CPU_ID} --ioengine=psync ${FIO_OPTIONS} --numjobs=${t} -o $RESULTS/psync_t_${t}.txt
    echo "Execute: fio --cpus_allowed=$(((${MAX_CPU_ID}+1)-${t}))-${MAX_CPU_ID} --ioengine=libaio ${FIO_OPTIONS} --numjobs=${t} -o $RESULTS/aio_t_${t}.txt"
    fio --cpus_allowed=$(((${MAX_CPU_ID}+1)-${t}))-${MAX_CPU_ID} --ioengine=libaio ${FIO_OPTIONS} --numjobs=${t} -o $RESULTS/aio_t_${t}.txt
    echo "Execute: fio --cpus_allowed=$(((${MAX_CPU_ID}+1)-${t}))-${MAX_CPU_ID} --ioengine=io_uring --registerfiles=1 --fixedbufs=1 ${FIO_OPTIONS} --numjobs=${t} -o $RESULTS/iou_t_${t}.txt"
    fio --cpus_allowed=$(((${MAX_CPU_ID}+1)-${t}))-${MAX_CPU_ID} --ioengine=io_uring --registerfiles=1 --fixedbufs=1 ${FIO_OPTIONS} --numjobs=${t} -o $RESULTS/iou_t_${t}.txt
    echo "Execute: fio --cpus_allowed=$(((${MAX_CPU_ID}+1)-${t}))-${MAX_CPU_ID} --ioengine=io_uring --hipri --registerfiles=1 --fixedbufs=1 ${FIO_OPTIONS} --numjobs=${t} -o $RESULTS/iou_c_t_${t}.txt"
    fio --cpus_allowed=$(((${MAX_CPU_ID}+1)-${t}))-${MAX_CPU_ID} --ioengine=io_uring --hipri --registerfiles=1 --fixedbufs=1 ${FIO_OPTIONS} --numjobs=${t} -o $RESULTS/iou_c_t_${t}.txt
done


declare -a num_threads=("1" "2" "3" "4" "5")

FIO_OPTIONS_IOUS="--time_based=1 --ramp_time=${FIO_RAMP_TIME}s --runtime=${FIO_RUN_TIME}s --size=100% --bs=4kb --norandommap=1 --group_reporting=1 --direct=1 --rw=randread --allow_file_create=0 --iodepth=128 --output-format=json --filename=${DEVICES}"

echo "Execute: chcpu -d 0-${MAX_CPU_ID}"
chcpu -d 0-${MAX_CPU_ID}

for t in "${num_threads[@]}"
do
    echo "Execute: chcpu -e $(((${MAX_CPU_ID}+1)-2*${t}+1))"
    chcpu -e $(((${MAX_CPU_ID}+1)-2*${t}+1))
    echo "Execute: chcpu -e $(((${MAX_CPU_ID}+1)-2*${t}))"
    chcpu -e $(((${MAX_CPU_ID}+1)-2*${t}))
    echo "Execute: fio --ioengine=io_uring --sqthread_poll=1 --registerfiles=1 --fixedbufs=1 ${FIO_OPTIONS} --cpus_allowed=$(((${MAX_CPU_ID}+1)-${t}))-${MAX_CPU_ID} --sqthread_poll_cpu=$(((${MAX_CPU_ID}+1)-2*${t}))-$(((${MAX_CPU_ID}+1)-${t}-1)) --numjobs=${t} -o $RESULTS/iou_s_t_${t}.txt"
    fio --ioengine=io_uring --sqthread_poll=1 --registerfiles=1 --fixedbufs=1 ${FIO_OPTIONS} --cpus_allowed=$(((${MAX_CPU_ID}+1)-${t}))-${MAX_CPU_ID} --sqthread_poll_cpu=$(((${MAX_CPU_ID}+1)-2*${t}))-$(((${MAX_CPU_ID}+1)-${t}-1)) --numjobs=${t} -o $RESULTS/iou_s_t_${t}.txt
done

declare -a num_threads=("6" "7" "8" "9" "10")

for t in "${num_threads[@]}"
do
    echo "Execute: chcpu -e $(((${MAX_CPU_ID}+1)-2*${t}+1))"
    chcpu -e $(((${MAX_CPU_ID}+1)-2*${t}+1))
    echo "Execute: chcpu -e $(((${MAX_CPU_ID}+1)-2*${t}))"
    chcpu -e $(((${MAX_CPU_ID}+1)-2*${t}))
    echo "Execute: fio --ioengine=io_uring --sqthread_poll=1 --registerfiles=1 --fixedbufs=1 ${FIO_OPTIONS} --cpus_allowed=$(((${MAX_CPU_ID}+1)-${t}))-${MAX_CPU_ID} --sqthread_poll_cpu=$(((${MAX_CPU_ID}+1)-2*${t}))-$(((${MAX_CPU_ID}+1)-${t}-1)) --numjobs=${t} -o $RESULTS/iou_s_t_${t}.txt"
    fio --ioengine=io_uring --sqthread_poll=1 --registerfiles=1 --fixedbufs=1 ${FIO_OPTIONS} --cpus_allowed=$(((${MAX_CPU_ID}+1)-${t}))-${MAX_CPU_ID} --sqthread_poll_cpu=$(((${MAX_CPU_ID}+1)-2*${t}))-$(((${MAX_CPU_ID}+1)-${t}-1)) --numjobs=${t} -o $RESULTS/iou_s_t_${t}.txt
done

echo "Execute: chcpu -d 0-${MAX_CPU_ID}"
chcpu -d 0-${MAX_CPU_ID}

$SPDK_SETUP_PATH

# SPDK FIO: socket 1

for t in "${num_threads_socket1[@]}"
do
    echo "Execute: chcpu -e $(((${MAX_CPU_ID}+1)-${t}))"
    chcpu -e $(((${MAX_CPU_ID}+1)-${t}))
    echo "Execute: LD_PRELOAD=$SPDK_FIO_PLUGIN fio ${FIO_OPTIONS_SPDK} --cpus_allowed=$(((${MAX_CPU_ID}+1)-${t}))-${MAX_CPU_ID} --filename="trtype=PCIe traddr=0000.af.00.0 ns=1:traddr=0000.b0.00.0 ns=1:traddr=0000.b1.00.0 ns=1:traddr=0000.b2.00.0 ns=1:traddr=0000.d8.00.0 ns=1:traddr=0000.da.00.0 ns=1:traddr=0000.db.00.0 ns=1" --numjobs=${t} -o $RESULT/spdk_fio_t_${t}.txt;"
    LD_PRELOAD=$SPDK_FIO_PLUGIN fio ${FIO_OPTIONS_SPDK} --cpus_allowed=$(((${MAX_CPU_ID}+1)-${t}))-${MAX_CPU_ID} --filename="trtype=PCIe traddr=0000.af.00.0 ns=1:traddr=0000.b0.00.0 ns=1:traddr=0000.b1.00.0 ns=1:traddr=0000.b2.00.0 ns=1:traddr=0000.d8.00.0 ns=1:traddr=0000.da.00.0 ns=1:traddr=0000.db.00.0 ns=1" --numjobs=${t} -o $RESULT/spdk_fio_t_${t}.txt
done

# SPDK FIO: socket 2
for t in "${num_threads_socket2[@]}"
do
    echo "Execute: chcpu -e ${t}"
    chcpu -e ${t}
    echo "Execute: LD_PRELOAD=$SPDK_FIO_PLUGIN fio ${FIO_OPTIONS_SPDK} --cpus_allowed=$(((${MAX_CPU_ID}+1)-${t}))-${MAX_CPU_ID} --filename="trtype=PCIe traddr=0000.af.00.0 ns=1:traddr=0000.b0.00.0 ns=1:traddr=0000.b1.00.0 ns=1:traddr=0000.b2.00.0 ns=1:traddr=0000.d8.00.0 ns=1:traddr=0000.da.00.0 ns=1:traddr=0000.db.00.0 ns=1" --numjobs=${t} -o $RESULT/spdk_fio_t_${t}.txt;"
    LD_PRELOAD=$SPDK_FIO_PLUGIN fio ${FIO_OPTIONS_SPDK} --cpus_allowed=$(((${MAX_CPU_ID}+1)-${t}))-${MAX_CPU_ID} --filename="trtype=PCIe traddr=0000.af.00.0 ns=1:traddr=0000.b0.00.0 ns=1:traddr=0000.b1.00.0 ns=1:traddr=0000.b2.00.0 ns=1:traddr=0000.d8.00.0 ns=1:traddr=0000.da.00.0 ns=1:traddr=0000.db.00.0 ns=1" --numjobs=${t} -o $RESULT/spdk_fio_t_${t}.txt
done

# SPDK with spdk perf

declare -a spdk_mask=("palceholder" "80000" "c0000" "e0000" "f0000" "f8000" "fc000" "fe000" "ff000" "ff800" "ffc00" "ffe00" "fff00" "fff80" "fffc0" "fffe0" "ffff0" "ffff8" "ffffc" "ffffe" "fffff")

echo "Execute: chcpu -d 0-${MAX_CPU_ID}"
chcpu -d 0-${MAX_CPU_ID}

for t in "${num_threads_socket1[@]}"
do
    echo "Execute: chcpu -e ${t}"
    chcpu -e ${t}
    echo "Execute: $SPDK_PERF_PATH -q 128 -o 4096 -w randread -r 'trtype:PCIe traddr:0000:af:00.0' -r 'trtype:PCIe traddr:0000:b0:00.0' -r 'trtype:PCIe traddr:0000:b1:00.0' -r 'trtype:PCIe traddr:0000:b2:00.0' -r 'trtype:PCIe traddr:0000:d8:00.0' -r 'trtype:PCIe traddr:0000:da:00.0' -r 'trtype:PCIe traddr:0000:db:00.0' -t $FIO_RUN_TIME -a $FIO_RAMP_TIME -c ${spdk_mask[$t]}  > $RESULT/spdk_perf_t_${t}.txt"
    $SPDK_PERF_PATH -q 128 -o 4096 -w randread -r 'trtype:PCIe traddr:0000:af:00.0' -r 'trtype:PCIe traddr:0000:b0:00.0' -r 'trtype:PCIe traddr:0000:b1:00.0' -r 'trtype:PCIe traddr:0000:b2:00.0' -r 'trtype:PCIe traddr:0000:d8:00.0' -r 'trtype:PCIe traddr:0000:da:00.0' -r 'trtype:PCIe traddr:0000:db:00.0' -t $FIO_RUN_TIME -a $FIO_RAMP_TIME -c ${spdk_mask[$t]}  > $RESULT/spdk_perf_t_${t}.txt
done

# both socket 1 and socket 2

for t in "${num_threads_socket2[@]}"
do
    echo "Execute: chcpu -e ${t}"
    chcpu -e ${t}
    echo "Execute: $SPDK_PERF_PATH -q 128 -o 4096 -w randread -r 'trtype:PCIe traddr:0000:af:00.0' -r 'trtype:PCIe traddr:0000:b0:00.0' -r 'trtype:PCIe traddr:0000:b1:00.0' -r 'trtype:PCIe traddr:0000:b2:00.0' -r 'trtype:PCIe traddr:0000:d8:00.0' -r 'trtype:PCIe traddr:0000:da:00.0' -r 'trtype:PCIe traddr:0000:db:00.0' -t $FIO_RUN_TIME -a $FIO_RAMP_TIME -c ${spdk_mask[$t]}  > $RESULT/spdk_perf_t_${t}.txt"
    $SPDK_PERF_PATH -q 128 -o 4096 -w randread -r 'trtype:PCIe traddr:0000:af:00.0' -r 'trtype:PCIe traddr:0000:b0:00.0' -r 'trtype:PCIe traddr:0000:b1:00.0' -r 'trtype:PCIe traddr:0000:b2:00.0' -r 'trtype:PCIe traddr:0000:d8:00.0' -r 'trtype:PCIe traddr:0000:da:00.0' -r 'trtype:PCIe traddr:0000:db:00.0' -t $FIO_RUN_TIME -a $FIO_RAMP_TIME -c ${spdk_mask[$t]}  > $RESULT/spdk_perf_t_${t}.txt
done


chcpu -e 0-${MAX_CPU_ID}
$SPDK_SETUP_PATH reset;
