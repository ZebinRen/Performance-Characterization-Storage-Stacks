#!/bin/bash

grep $1 spdk_input_srcline.txt | tr -s ' ' | cut -d ' ' -f 3 | awk '{ sum += $1 } END { print sum }'
