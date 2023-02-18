# Instructions

## Environment

### Install fio

```bash
git clone https://github.com/axboe/fio.git
git checkout 77c758db876d93022e8f2bb4fd4c1acbbf7e76ac
cd fio
./configure
make
```

### Install SPDK

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

NOTE: Please add fio to $PATH

## Figure 2

### Figure 2-a Random 4K read, single CPU, QD=1

### Figure 2-b Instructions breakdown, single CPU, QD=1

## Figure 3

## Figure 4

## Figure 5

## Figure 6

## Figure 7