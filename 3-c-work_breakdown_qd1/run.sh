#! /bin/bash
# FLAMEGRAPH=/mnt/sdb/zebin/stor_bench/iouring_tests/flame_graph.sh

VMLINUX=
SPDK_FIO_PLUGIN=
SPDK_SETUP_PATH=

FIO_RUN_TIME=30
FIO_RAMP_TIME=5

FIO_RES='./fio'
PERF_RES='./perf_output'
PERF_PARSED_LIST='./perf_list'
PERF_PARSED_GRAPH='./perf_graph'
FLAMEGRAPH_OUT='./flamegraph'

declare -a engines=("aio" "iou" "iou_s" "iou_c")

chcpu -d 1-9

$SPDK_SETUP_PATH reset

for e in "${engines[@]}"
do
perf record -e instructions -F 99 -o $PERF_RES/${e}.perf.out env FIO_RUN_TIME=$FIO_RUN_TIME FIO_RAMP_TIME=$FIO_RAMP_TIME fio ${e}.conf --thread=1 --output-format=json -o $FIO_RES/${e}_fio.txt;

perf record -g -e instructions -F 99 -o $PERF_RES/${e}_g.perf.out env FIO_RUN_TIME=$FIO_RUN_TIME FIO_RAMP_TIME=$FIO_RAMP_TIME fio ${e}.conf --thread=1 --output-format=json -o $FIO_RES/${e}_g.txt;
done

e="spdk_fio"

$SPDK_SETUP_PATH

perf record -e instructions -F 99 -o $PERF_RES/${e}.perf.out env FIO_RUN_TIME=$FIO_RUN_TIME FIO_RAMP_TIME=$FIO_RAMP_TIME LD_PRELOAD=$SPDK_FIO_PLUGIN fio ${e}.conf --thread=1 --output-format=json -o $FIO_RES/${e}_fio.txt;

perf record -g -e instructions -F 99 -o $PERF_RES/${e}_g.perf.out env FIO_RUN_TIME=$FIO_RUN_TIME FIO_RAMP_TIME=$FIO_RAMP_TIME LD_PRELOAD=$SPDK_FIO_PLUGIN fio ${e}.conf --thread=1 --output-format=json -o $FIO_RES/${e}_g.txt;

$SPDK_SETUP_PATH reset

# parse

for e in "${engines[@]}"
do
perf report --vmlinux $VMLINUX -n -m --stdio --full-source-path --source -s symbol -i $PERF_RES/${e}.perf.out >> $PERF_PARSED_LIST/perf_parsed_${e}.txt;

perf report --vmlinux $VMLINUX -n -m --stdio --full-source-path --source -s symbol --call-graph=graph,0,caller,function,count -i $PERF_RES/${e}_g.perf.out >> $PERF_PARSED_GRAPH/perf_parsed_${e}_g.txt;
done

chcpu -e 1-9