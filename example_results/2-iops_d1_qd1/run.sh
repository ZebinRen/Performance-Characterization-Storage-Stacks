SPDK_FIO_PLUGIN='/mnt/sdb/zebin/local/spdk/build/fio/spdk_nvme'
RESULTS=results
NUMA_PIN='numactl -N 1 -m 1'

/mnt/sdb/zebin/local/spdk/scripts/setup.sh reset;
$NUMA_PIN fio psync_dev1.conf --output-format=json -o $RESULTS/psync_dev1.txt;
$NUMA_PIN fio aio_dev1.conf --output-format=json -o $RESULTS/aio_dev1.txt;
$NUMA_PIN fio iou_dev1.conf --output-format=json -o $RESULTS/iou_dev1.txt;
$NUMA_PIN fio iou_c_dev1.conf --output-format=json -o $RESULTS/iou_c_dev1.txt;
$NUMA_PIN fio iou_s_dev1.conf --output-format=json -o $RESULTS/iou_s_dev1.txt;

/mnt/sdb/zebin/local/spdk/scripts/setup.sh;
LD_PRELOAD=$SPDK_FIO_PLUGIN fio spdk_fio_dev1.conf --output-format=json -o $RESULTS/spdk_fio_dev1.txt;
# /mnt/sdb/zebin/local/spdk/build/examples/perf -q 8 -o 4096 -w randread -r 'trtype:PCIe traddr:0000:b1:00.0'  -t 140 -c 1000> $RESULTS/spdk_perf_dev1.txt;
/mnt/sdb/zebin/local/spdk/scripts/setup.sh reset;