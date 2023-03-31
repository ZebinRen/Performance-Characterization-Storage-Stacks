# Instructions

## IMPORTANT

There are predefined devices in the fio configuration files. PLEASE REPLACE THEM WITH YOUR OWN DEVICE.

## Environment

### Install fio

```bash
git clone https://github.com/axboe/fio.git
git checkout 77c758db876d93022e8f2bb4fd4c1acbbf7e76ac
cd fio
./configure
make
```

NOTE: Please add fio to $PATH

### Install SPDK

[SPDK setup](https://spdk.io/doc/getting_started.html)
[fio spdk setup manual](https://github.com/spdk/spdk/blob/master/examples/nvme/fio_plugin/README.md)

```bash
git clone https://github.com/spdk/spdk.git
cd spdk
git checkout aed4ece93c659195d4b56399a181f41e00a7a25e
git submodule update --init
sudo scripts/pkgdep.sh

# Configure with fio
./configure --with-fio=/path/to/fio/repo <other configuration options>

make

# bind and unbind device

sudo scripts/setup.sh

sudo scripts/setup.sh reset

```

Make sure there are huge pages on the node where SPDK will be run on. For example:

```bash
sudo HUGENODE="nodes_hp[0]=4096,nodes_hp[1]=4096" $SPDK/scripts/setup.sh
```



### Prepare

Fully write the devices 10 times before the experiment
```bash
cd write_device
sudo ./run.sh
```

### NOTE

* Set the 'SPDK_FIO_PLUGIN' and 'SPDK_SETUP_PATH' before run the script
* Fill your own devices in the fio configurations file before running.
* In fig 7 and fig 8, the script will automatically turn down the CPU 0 using chcpu. Replace it with your cpu id in socket 1, or delete them if there is only one NUMA node on your machine.

## Figure 2

Before running the script:

* Set the 'SPDK_SETUP_PATH' environment variable.
* Disable the CPU core that are not in the same socket with the device

Run the script and plot:

```bash
cd 2-iops_d1_qd_1
mkdir results
sudo ./run.sh
python3 plot.py
```

## Figure 3

* Set the 'SPDK_SETUP_PATH' environment variable.
* Disable the CPU core that are not in the same socket with the device

Run the script and plot:

```bash
cd 2-iops_d1_qd_1
mkdir fio perf_graph perf_list perf_output
sudo ./run.sh
python3 plot.py
```

NOTE:

The work breakdown of iou-s might not be parsed correctly by the script. The work breakdown needs to be calculated manually for the perf report.

### For spdk

* Parse the perf file with srcline(set your vmlinux path):

```bash
perf report --vmlinux $VMLINUX -n -m --stdio --full-source-path --source -s symbol,srcline -i perf_output/spdk_fio.perf.out >> spdk_srcline.txt;

```

* Delete all the lines that does not contain the actual data
* Get the number of instructions and instructions taken by SPDK

```bash
# all
cat spdk_srcline.txt | tr -s ' ' | cut -d ' ' -f 3 | awk '{ sum += $1 } END { print sum }'
# spdk
grep $YOUR_SPDK_PATH spdk_srcline.txt | tr -s ' ' | cut -d ' ' -f 3 | awk '{ sum += $1 } END { print sum }'
```

* fill the overhead of spdk and fio in plot.py:112


## Figure 4

Before running the script:

* Set up the 'SPDK_FIO_PLUGIN', 'SPDK_SETUP_PATH'
* Disable the CPU core that are not in the same socket with the device

Run the script and plot:

```bash
cd 4-micro_arch_qd1
mkdir results_global results_local
sudo ./run.sh
python3 plot.py
```

## Figure 5-a-b

Before running the script:

* Set the 'SPDK_SETUP_PATH' and 'SPDK_FIO_PLUGIN' environment variable.
* Disable the CPU core that are not in the same socket with the device

Run the script and plot:

```bash
sudo ./run.sh
mkdir results
python3 plot.py
```

## Figure 5-c

see figure 3

## Figure 6

see figure 4

## Figure 7

Before running the script:

* Set the 'SPDK_SETUP_PATH', 'SPDK_FIO_PLUGIN' environment variable.

Run the script and plot:

```bash
cd 7-multi_thread
sudo ./run.sh
mkdir results
python3 plot.py
```

## Figure 8

Before running the script:

* Set the 'SPDK_SETUP_PATH' environment variable.

Run the script and plot:

```bash
cd 8-scheduler_multi_thread
mkdir results
sudo ./run.sh
python3 plot.py
```

# License 
This code and artifact is distributed under the MIT license. 

```
MIT License

Copyright (c) 2022 @Large Research

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
