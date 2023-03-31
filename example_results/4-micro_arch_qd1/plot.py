import os.path
import numpy as np
import fio
from multi_bar_graph import multi_bar_graph as bar_graph

import matplotlib.pyplot as plt

import matplotlib

# Switch to Type 1 Fonts.
# matplotlib.rcParams['ps.useafm'] = True
# matplotlib.rcParams['pdf.use14corefonts'] = True
matplotlib.rcParams['text.usetex'] = True
# matplotlib.rcParams["font.family"] = "sans-serif"
# matplotlib.rcParams["font.sans-serif"] = "helvet"
plt.rc('font', **{'family': 'serif', 'serif': ['Times']})

# csfont = {'fontname': 'Helvetica'}

# plt.switch_backend('pgf')
# plt.rcParams['pdf.use14corefonts'] = True
# # font = {'size': 18, 'family': 'Helvetica'}
# # plt.rc('font', **font)


def parse_perf_stat(filename):
    """_summary_

    Args:
        filename (_type_): _description_

    Returns:
        dict[name]: (value, stddev) value[int], percent
    """
    f = open(filename, 'r')
    contents = f.readlines()
    f.close()

    ret = {}
    data_start = 0
    for line in contents:
        if line[0] == '#' or line == '\n':
            data_start += 1
        else:
            break

    data_start += 1
    contents = contents[data_start:]
    data_start = 0
    for line in contents:
        if line == '\n':
            data_start += 1
        else:
            break
    contents = contents[data_start:]

    for line in contents:
        # print(line)
        if line == '\n':
            break
        # parse data
        splitted_contents = line.split(' ')
        splitted_contents = [x for x in splitted_contents if x != '']
        value = splitted_contents[0]
        key = splitted_contents[1]
        if key[-1] == '\n':
            key = key[0:-1]

        stddev = None
        # check if stddev exists, if exists, get it. if not exist, return None
        last_elem = splitted_contents[-1]
        if last_elem[-1] == '\n':
            last_elem = last_elem[:-1]
        if last_elem == ')':
            # stddev exists
            stddev = splitted_contents[-2][:-1]
            # stddev = float(stddev)

        ret[key] = (value, stddev)

    return ret


def load_inst_cycle(filename, sample_length, num_files):
    cycles = []
    inst = []
    ipc = []

    for i in range(num_files):
        cur_filename = filename + '_' + str(i) + '.txt'
        perf_stat = parse_perf_stat(cur_filename)

        cur_cycle = int(perf_stat['cycles'][0]) / sample_length
        cur_inst = int(perf_stat['instructions'][0]) / sample_length

        cycles.append(cur_cycle)
        inst.append(cur_inst)
        ipc.append(cur_inst / cur_cycle)

    # TODO: Return std or the list directly
    cycles_std = np.std(cycles)
    inst_std = np.std(inst)
    ipc_std = np.std(ipc)

    cycles = np.mean(cycles)
    inst = np.mean(inst)
    ipc = np.mean(ipc)

    return inst, cycles, ipc, inst_std, cycles_std, ipc_std


def load_cache(filename, num_files):
    cache_ref = []
    cache_miss = []
    cache_miss_rate = []

    for i in range(num_files):
        cur_filename = filename + '_' + str(i) + '.txt'
        perf_stat = parse_perf_stat(cur_filename)

        cur_cache_ref = int(perf_stat['cache-references'][0])
        cur_cache_miss = int(perf_stat['cache-misses'][0])
        cur_cache_miss_rate = cur_cache_miss / cur_cache_ref

        cache_ref.append(cur_cache_ref)
        cache_miss.append(cur_cache_miss)
        cache_miss_rate.append(cur_cache_miss_rate)

    cache_miss_std = np.std(cache_miss)
    cache_ref_std = np.std(cache_ref)
    cache_miss_rate_std = np.std(cache_miss_rate)

    cache_ref = np.mean(cache_ref)
    cache_miss = np.mean(cache_miss)
    cache_miss_rate = np.mean(cache_miss_rate)

    return cache_miss, cache_ref, cache_miss_rate, cache_miss_std, cache_ref_std, cache_miss_rate_std


def load_llc(filename, num_files):
    llc_load = []
    llc_load_miss = []
    llc_store = []
    llc_store_miss = []
    llc_load_miss_rate = []
    llc_store_miss_rate = []

    for i in range(num_files):
        cur_filename = filename + '_' + str(i) + '.txt'

        perf_stat = parse_perf_stat(cur_filename)
        cur_llc_load = int(perf_stat['LLC-loads'][0])
        cur_llc_load_miss = int(perf_stat['LLC-load-misses'][0])
        cur_llc_store = int(perf_stat['LLC-stores'][0])
        cur_llc_store_miss = int(perf_stat['LLC-store-misses'][0])
        cur_llc_load_miss_rate = cur_llc_load_miss / cur_llc_load
        cur_llc_store_miss_rate = cur_llc_store_miss / cur_llc_store

        llc_load.append(cur_llc_load)
        llc_load_miss.append(cur_llc_load_miss)
        llc_store.append(cur_llc_store)
        llc_store_miss.append(cur_llc_store_miss)
        llc_load_miss_rate.append(cur_llc_load_miss_rate)
        llc_store_miss_rate.append(cur_llc_store_miss_rate)

    llc_load = np.mean(llc_load)
    llc_load_miss = np.mean(llc_load_miss)
    llc_store = np.mean(llc_store)
    llc_store_miss = np.mean(llc_store_miss)
    llc_load_miss_rate = np.mean(llc_load_miss_rate)
    llc_store_miss_rate = np.mean(llc_store_miss_rate)

    return llc_load_miss, llc_load, llc_load_miss_rate, llc_store_miss, llc_store, llc_store_miss_rate


def load_dtlb(filename, num_files):
    dtlb_load_miss = []
    dtlb_loads = []
    dtlb_store_miss = []
    dtlb_stores = []

    for i in range(num_files):
        cur_filename = filename + '_' + str(i) + '.txt'
        perf_stat = parse_perf_stat(cur_filename)
        cur_dtlb_load_miss = int(perf_stat['dTLB-load-misses'][0])
        cur_dtlb_loads = int(perf_stat['dTLB-loads'][0])
        cur_dtlb_store_miss = int(perf_stat['dTLB-store-misses'][0])
        cur_dtlb_stores = int(perf_stat['dTLB-stores'][0])

        load_miss_rate = cur_dtlb_load_miss / cur_dtlb_loads
        store_miss_rate = cur_dtlb_store_miss / cur_dtlb_stores

        dtlb_load_miss.append(cur_dtlb_load_miss)
        dtlb_loads.append(cur_dtlb_loads)
        dtlb_store_miss.append(cur_dtlb_store_miss)
        dtlb_stores.append(cur_dtlb_stores)

    dtlb_load_miss = np.mean(dtlb_load_miss)
    dtlb_loads = np.mean(dtlb_loads)
    dtlb_store_miss = np.mean(dtlb_store_miss)
    dtlb_stores = np.mean(dtlb_stores)

    return dtlb_load_miss, dtlb_loads, load_miss_rate, dtlb_store_miss, dtlb_store_miss, store_miss_rate


def load_itlb(filename, num_files):
    itlb_load_miss = []
    itlb_loads = []
    load_miss_rate = []

    for i in range(num_files):
        cur_filename = filename + '_' + str(i) + '.txt'
        perf_stat = parse_perf_stat(cur_filename)
        cur_itlb_load_miss = int(perf_stat['iTLB-load-misses'][0])
        cur_itlb_loads = int(perf_stat['iTLB-loads'][0])
        cur_load_miss_rate = cur_itlb_load_miss / cur_itlb_loads

        itlb_load_miss.append(cur_itlb_load_miss)
        itlb_loads.append(cur_itlb_loads)
        load_miss_rate.append(cur_load_miss_rate)

    itlb_load_miss = np.mean(itlb_load_miss)
    itlb_loads = np.mean(itlb_loads)
    load_miss_rate = np.mean(load_miss_rate)

    return itlb_load_miss, itlb_loads, load_miss_rate


def load_branches(filename, num_files):
    branch_misses = []
    branches = []
    branch_miss_rate = []

    for i in range(num_files):
        cur_filename = filename + '_' + str(i) + '.txt'
        perf_stat = parse_perf_stat(cur_filename)
        cur_branch_misses = int(perf_stat['branch-misses'][0])
        cur_branches = int(perf_stat['branches'][0])
        cur_branch_miss_rate = cur_branch_misses / cur_branches

        branch_misses.append(cur_branch_misses)
        branches.append(cur_branches)
        branch_miss_rate.append(cur_branch_miss_rate)

    print(branch_miss_rate)
    print(np.std(branch_miss_rate))
    # # exit(1)
    branch_misses_std = np.std(branch_misses)
    branches_std = np.std(branches)
    branch_miss_rate_std = np.std(branch_miss_rate)

    branch_misses = np.mean(branch_misses)
    branches = np.mean(branches)
    branch_miss_rate = np.mean(branch_miss_rate)

    # print(branch_miss_rate)
    # print(branch_miss_rate_std)
    # exit(0)

    return branch_misses, branches, branch_miss_rate, branch_misses_std, branches_std, branch_miss_rate_std


def load_context_switch(filename, sample_length, num_files):
    cs = []

    for i in range(num_files):
        cur_filename = filename + '_' + str(i) + '.txt'
        perf_stat = parse_perf_stat(cur_filename)
        cur_cs = int(perf_stat['cs'][0])

        cs.append(cur_cs / sample_length)

    cs_std = np.std(cs)
    cs = np.mean(cs)

    return cs, cs_std


def read_data(engines, dir, inst_sample_length, cs_sample_length,
              num_perf_files):
    all_inst_per_io = []
    all_inst_per_io_std = []
    all_ipc = []
    all_ipc_std = []
    all_cache_miss_r = []
    all_cache_miss_r_std = []
    all_llc_load_miss_r = []
    all_llc_store_miss_r = []
    all_dtlb_load_miss_r = []
    all_dtlb_store_miss_r = []
    all_itlb_miss_r = []
    all_branch_miss_rate = []
    all_branch_miss_rate_std = []
    all_cs_per_ses = []
    all_cs_per_sec_per_io = []
    all_cs_per_sec_per_io_std = []

    global_rk = []
    jobs_rk = ['read:lat_ns:mean', 'read:iops', 'read:lat_ns:stddev']
    for e in engines:
        fname_cycles = os.path.join(dir, e + '_1_inst_cycle')
        fname_cahce = os.path.join(dir, e + '_1_cache')
        fname_llc = os.path.join(dir, e + '_1_LLC')
        fname_dtlb = os.path.join(dir, e + '_1_DTLB')
        fname_itlb = os.path.join(dir, e + '_1_ITLB')
        fname_branch = os.path.join(dir, e + '_1_branch')
        fname_cs = os.path.join(dir, e + '_1_cs')

        inst, cycle, ipc, inst_std, _, ipc_std = load_inst_cycle(
            fname_cycles, inst_sample_length, num_perf_files)
        cache_miss, cache_ref, cache_miss_rate, _, _, cache_miss_rate_std = load_cache(
            fname_cahce, num_perf_files)
        # _, _, llc_load_miss_rate, _, _, llc_store_miss_rate = load_llc(
        #     fname_llc,num_perf_files)
        # _, _, dtlb_load_miss_rate, _, _, dtlb_store_miss_rate = load_dtlb(
        #     fname_dtlb,num_perf_files)
        # _, _, itlb_load_miss_rate = load_itlb(fname_itlb,num_perf_files)
        _, _, branch_miss_rate, _, _, branch_miss_rate_std = load_branches(
            fname_branch, num_perf_files)
        cs_per_sec, cs_per_sec_std = load_context_switch(
            fname_cs, cs_sample_length, num_perf_files)

        # multiply all rate by 100
        # Divide inst per io by 100
        all_ipc.append(ipc)
        all_ipc_std.append(ipc_std)
        all_cache_miss_r.append(cache_miss_rate * 100)
        all_cache_miss_r_std.append(cache_miss_rate_std * 100)
        # all_llc_load_miss_r.append(llc_load_miss_rate * 100)
        # all_llc_store_miss_r.append(llc_store_miss_rate * 100)
        # all_dtlb_load_miss_r.append(dtlb_load_miss_rate * 100)
        # all_dtlb_store_miss_r.append(dtlb_store_miss_rate * 100)
        # all_itlb_miss_r.append(itlb_load_miss_rate * 100)
        all_branch_miss_rate.append(branch_miss_rate * 100)
        all_branch_miss_rate_std.append(branch_miss_rate_std * 100)
        all_cs_per_ses.append(cs_per_sec)
        # all_cs_per_sec_per_io_std.append(cs_per_sec_std)

        fname_fio_1 = os.path.join(dir, e + '_1.txt')
        _, j_res = fio.parse_experiment(fname_fio_1, global_rk, jobs_rk)
        iops_1 = j_res[0]['read:iops']
        all_inst_per_io.append(inst / iops_1 / 1000)
        all_inst_per_io_std.append(inst_std / iops_1 / 1000)
        all_cs_per_sec_per_io.append(cs_per_sec / iops_1)
        all_cs_per_sec_per_io_std.append(cs_per_sec_std / iops_1)

    ret = {
        'all_ipc': all_ipc,
        'all_ipc_std': all_ipc_std,
        'all_cache_miss_r': all_cache_miss_r,
        'all_cache_miss_r_std': all_cache_miss_r_std,
        'all_llc_load_miss_r': all_llc_load_miss_r,
        'all_llc_store_miss_r': all_llc_store_miss_r,
        'all_dtlb_load_miss_r': all_dtlb_load_miss_r,
        'all_dtlb_store_miss_r': all_dtlb_store_miss_r,
        'all_itlb_miss_r': all_itlb_miss_r,
        'all_inst_per_io': all_inst_per_io,
        'all_inst_per_io_std': all_inst_per_io_std,
        'all_branch_miss_rate': all_branch_miss_rate,
        'all_branch_miss_rate_std': all_branch_miss_rate_std,
        'all_cs_per_ses': all_cs_per_ses,
        'all_cs_per_sec_per_io': all_cs_per_sec_per_io,
        'all_cs_per_sec_per_io_std': all_cs_per_sec_per_io_std
    }
    return ret


global_dir = './results_global'
local_dir = './results_local'
# engines = ['iou', 'iou_s', 'iou_c', 'spdk_fio']
engines = ['psync', 'aio', 'iou', 'iou_c', 'iou_s', 'spdk_fio']
inst_sample_length = 5
cs_sample_length = 5
num_perf_files = 10
# global_inst_per_io_1, global_inst_1, global_ipc_1, global_cache_miss_1 = read_data(
#     engines, global_dir, sample_length)
# local_inst_per_io_1, local_inst_1, local_ipc_1, local_cache_miss_1 = read_data(
#     engines, local_dir, sample_length)

global_data = read_data(engines, global_dir, inst_sample_length,
                        cs_sample_length, num_perf_files)
local_data = read_data(engines, local_dir, inst_sample_length,
                       cs_sample_length, num_perf_files)

print(global_data)
# print('global_data')
# print(global_data)
# print('local data')
# print(local_data)

# all_data = [(global_inst_per_io_1, local_inst_per_io_1),
#             (global_ipc_1, local_ipc_1),
#             (global_cache_miss_1, local_cache_miss_1)]

# # name, y-lable
# name = [('instructions-IO', 'instructions-IO(k)'), ('ipc', 'ipc'),
#         ('cache_miss', 'cache miss rate(%)')]

x_label = 'Engines'
bar_width = 0.4
axis_label_font_size = 28
axis_tick_font_size = 26
legend_font_size = 23
datalabel_size = 24
datalabel_va = 'bottom'  #'bottom'


def draw_inst_io(system_wide, process_specific, engine_only, system_wide_std,
                 process_specific_std, fig_save_path):
    group_list = ['system_wide', 'process_specific']
    x_ticks = ['psync', 'aio', 'iou', 'iou-c', 'iou-s', ' spdk-fio']
    value = {'system_wide': system_wide, 'process_specific': process_specific}
    std_dev = {
        'system_wide': system_wide_std,
        'process_specific': process_specific_std
    }
    # std_dev
    bar_width = 0.4
    fig_save_path = fig_save_path
    legend_label = {
        'system_wide': 'system-wide',
        'process_specific': 'process-specific'
    }
    ylabel = '(K) Instructions per I/O'
    # axis_tick_font_size = axis_tick_font_size
    # axis_label_font_size = axis_label_font_size
    # legend_font_size = legend_font_size
    # datalabel_size = datalabel_size
    datalabel_va = 'bottom'

    fig, ax = plt.subplots(figsize=(12, 8))

    # plt.title(title)
    # plt.xlabel(xlabel, fontsize=axis_label_font_size)
    plt.ylabel(ylabel, fontsize=axis_label_font_size)
    plt.grid(axis='y')

    ax.tick_params(axis='both', which='major', labelsize=axis_tick_font_size)

    if legend_label == None:
        legend_label = {}
        for group in group_list:
            legend_label[group] = group

    x_axis = np.arange(len(x_ticks))

    # compute bar offset
    bar_offset = []
    mid_point = (len(group_list) * bar_width) / 2

    for i in range(len(group_list)):
        bar_offset.append(bar_width * i + 0.5 * bar_width - mid_point)

    print(bar_offset)
    print(x_axis)
    x_axis - 0.1

    for (index, group_name) in zip(range(len(group_list)), group_list):
        y = value[group_name]
        cur_stddev = std_dev[group_name]
        bar_pos = x_axis + bar_offset[index]
        plt.bar(bar_pos,
                y,
                width=bar_width,
                label=legend_label[group_name],
                yerr=cur_stddev)

        # print(bar_pos, y)
        for (x, y, engine) in zip(bar_pos, y, x_ticks):
            text = '{:.1f}'.format(y)
            if group_name == 'process_specific':
                if engine == 'iou-c':
                    x += 0.16
            if group_name == 'process_specific' and engine == 'iou-s':
                x += 0.21
            if group_name == 'process_specific' and engine == ' spdk-fio':
                x = x + 0.2
            if group_name == 'system_wide' and engine == 'iou-s':
                x = x - 0.2

            plt.text(
                x,
                y,
                '$' + text + '$',
                size=datalabel_size,
                ha='center',
                # rotation='vertical',
                va=datalabel_va,
            )  # 'bottom', 'baseline', 'center', 'center_baseline', 'top'
    bar_pos = x_axis + bar_offset[1]
    cur_stddev = None
    y = engine_only
    # for (x, y, engine) in zip(bar_pos, y, x_ticks):
    #     text = '{:.1f}'.format(y)
    #     # if group_name == 'system_wide':
    #     #     if engine == 'iou-s':
    #     #         x = x - 0.13
    #     #     else:
    #     #         x = x - 0.08
    #     # if group_name == 'process_specific' and engine == 'iou-s':
    #     #     if engine == 'iou-s':
    #     #         x = x + 0.13
    #     #     else:
    #     #         x = x + 0.08
    #     if group_name == 'process_specific':
    #         if engine == 'psync' or engine == 'iou':
    #             y = y - 6
    #     plt.text(
    #         x,
    #         y,
    #         text,
    #         size=datalabel_size,
    #         ha='center',
    #         # rotation='vertical',
    #         va=datalabel_va)
    plt.xticks(x_axis, x_ticks)

    plt.legend(fontsize=legend_font_size, loc='upper left')

    plt.savefig(fig_save_path, bbox_inches='tight')


def draw_cache_miss(system_wide, process_specific, system_wide_std,
                    process_specific_std, fig_save_path):
    group_list = ['system_wide', 'process_specific']
    x_ticks = ['psync', 'aio', 'iou', 'iou-c', 'iou-s', ' spdk-fio']
    value = {'system_wide': system_wide, 'process_specific': process_specific}
    std_dev = {
        'system_wide': system_wide_std,
        'process_specific': process_specific_std
    }
    # std_dev
    bar_width = 0.4
    fig_save_path = fig_save_path
    legend_label = {
        'system_wide': 'system-wide',
        'process_specific': 'process-specific'
    }
    ylabel = 'Cache miss rate (\%)'
    # axis_tick_font_size = axis_tick_font_size
    # axis_label_font_size = axis_label_font_size
    # legend_font_size = legend_font_size
    # datalabel_size = datalabel_size
    datalabel_va = 'bottom'

    fig, ax = plt.subplots(figsize=(12, 8))

    # plt.title(title)
    # plt.xlabel(xlabel, fontsize=axis_label_font_size)
    plt.ylabel(ylabel, fontsize=axis_label_font_size)
    plt.grid(axis='y')
    plt.ylim([0, 15])
    ax.tick_params(axis='both', which='major', labelsize=axis_tick_font_size)

    if legend_label == None:
        legend_label = {}
        for group in group_list:
            legend_label[group] = group

    x_axis = np.arange(len(x_ticks))

    # compute bar offset
    bar_offset = []
    mid_point = (len(group_list) * bar_width) / 2

    for i in range(len(group_list)):
        bar_offset.append(bar_width * i + 0.5 * bar_width - mid_point)

    print(bar_offset)
    print(x_axis)
    x_axis - 0.1

    for (index, group_name) in zip(range(len(group_list)), group_list):
        y = value[group_name]
        cur_stddev = std_dev[group_name]
        bar_pos = x_axis + bar_offset[index]
        plt.bar(bar_pos,
                y,
                width=bar_width,
                label=legend_label[group_name],
                yerr=cur_stddev)

        # print(bar_pos, y)
        for (x, y, engine) in zip(bar_pos, y, x_ticks):
            text = '{:.1f}'.format(y)
            # if group_name == 'system_wide' and engine == 'iou-s':
            #     x = x - 0.3
            #     y = y - 25
            # if group_name == 'process_specific' and engine == 'iou-s':
            #     x = x + 0.32
            #     y = y - 10
            plt.text(
                x,
                y,
                '$' + text + '$',
                size=datalabel_size,
                ha='center',
                # rotation='vertical',
                va=datalabel_va
            )  # 'bottom', 'baseline', 'center', 'center_baseline', 'top'

    plt.xticks(x_axis, x_ticks)

    if legend_font_size:
        plt.legend(fontsize=legend_font_size)
    else:
        plt.legend()

    plt.savefig(fig_save_path, bbox_inches='tight')


def draw_ipc(system_wide, process_specific, system_wide_std,
             process_specific_std, fig_save_path):
    group_list = ['system_wide', 'process_specific']
    x_ticks = ['psync', 'aio', 'iou', 'iou-c', 'iou-s', ' spdk-fio']
    value = {'system_wide': system_wide, 'process_specific': process_specific}
    std_dev = {
        'system_wide': system_wide_std,
        'process_specific': process_specific_std
    }
    # std_dev
    bar_width = 0.4
    fig_save_path = fig_save_path
    legend_label = {
        'system_wide': 'system-wide',
        'process_specific': 'process-specific'
    }
    ylabel = 'IPC'
    # axis_tick_font_size = axis_tick_font_size
    # axis_label_font_size = axis_label_font_size
    # legend_font_size = legend_font_size
    # datalabel_size = datalabel_size
    datalabel_va = 'bottom'

    fig, ax = plt.subplots(figsize=(12, 8))

    # plt.title(title)
    # plt.xlabel(xlabel, fontsize=axis_label_font_size)
    plt.ylabel(ylabel, fontsize=axis_label_font_size)
    plt.grid(axis='y')
    plt.ylim([0, 4])

    ax.tick_params(axis='both', which='major', labelsize=axis_tick_font_size)

    if legend_label == None:
        legend_label = {}
        for group in group_list:
            legend_label[group] = group

    x_axis = np.arange(len(x_ticks))

    # compute bar offset
    bar_offset = []
    mid_point = (len(group_list) * bar_width) / 2

    for i in range(len(group_list)):
        bar_offset.append(bar_width * i + 0.5 * bar_width - mid_point)

    print(bar_offset)
    print(x_axis)
    x_axis - 0.1

    for (index, group_name) in zip(range(len(group_list)), group_list):
        y = value[group_name]
        cur_stddev = std_dev[group_name]
        bar_pos = x_axis + bar_offset[index]
        plt.bar(bar_pos,
                y,
                width=bar_width,
                label=legend_label[group_name],
                yerr=cur_stddev)

        # print(bar_pos, y)
        for (x, y, engine) in zip(bar_pos, y, x_ticks):
            text = '{:.1f}'.format(y)
            if group_name == 'system_wide':
                x = x - 0.1
            if group_name == 'process_specific' and engine == 'iou-s':
                x = x + 0.1
            # if group_name == 'system_wide' and engine == ' spdk-fio':
            #     x = x - 0.32
            #     y = y - 0.3
            # if group_name == 'process_specific' and engine == ' spdk-fio':
            #     x = x + 0.32
            #     y = y - 0.3
            plt.text(
                x,
                y,
                '$' + text + '$',
                size=datalabel_size,
                ha='center',
                # rotation='vertical',
                va=datalabel_va
            )  # 'bottom', 'baseline', 'center', 'center_baseline', 'top'

    plt.xticks(x_axis, x_ticks)

    if legend_font_size:
        plt.legend(fontsize=legend_font_size)
    else:
        plt.legend()

    plt.savefig(fig_save_path, bbox_inches='tight')


def draw_branch_miss(system_wide, process_specific, system_wide_std,
                     process_specific_std, fig_save_path):
    group_list = ['system_wide', 'process_specific']
    x_ticks = ['psync', 'aio', 'iou', 'iou-c', 'iou-s', ' spdk-fio']
    value = {'system_wide': system_wide, 'process_specific': process_specific}
    std_dev = {
        'system_wide': system_wide_std,
        'process_specific': process_specific_std
    }
    # std_dev
    bar_width = 0.4
    fig_save_path = fig_save_path
    legend_label = {
        'system_wide': 'system-wide',
        'process_specific': 'process-specific'
    }
    ylabel = 'Branch miss rate (%)'
    # axis_tick_font_size = axis_tick_font_size
    # axis_label_font_size = axis_label_font_size
    # legend_font_size = legend_font_size
    # datalabel_size = datalabel_size
    datalabel_va = 'bottom'

    fig, ax = plt.subplots(figsize=(12, 8))

    # plt.title(title)
    # plt.xlabel(xlabel, fontsize=axis_label_font_size)
    plt.ylabel(ylabel, fontsize=axis_label_font_size)
    plt.grid(axis='y')

    ax.tick_params(axis='both', which='major', labelsize=axis_tick_font_size)

    if legend_label == None:
        legend_label = {}
        for group in group_list:
            legend_label[group] = group

    x_axis = np.arange(len(x_ticks))

    # compute bar offset
    bar_offset = []
    mid_point = (len(group_list) * bar_width) / 2

    for i in range(len(group_list)):
        bar_offset.append(bar_width * i + 0.5 * bar_width - mid_point)

    print(bar_offset)
    print(x_axis)
    x_axis - 0.1

    for (index, group_name) in zip(range(len(group_list)), group_list):
        y = value[group_name]
        cur_stddev = std_dev[group_name]
        bar_pos = x_axis + bar_offset[index]
        plt.bar(bar_pos,
                y,
                width=bar_width,
                label=legend_label[group_name],
                yerr=cur_stddev)

        # print(bar_pos, y)
        for (x, y, engine) in zip(bar_pos, y, x_ticks):
            text = '{:.1f}'.format(y)
            if group_name == 'system_wide':
                x = x - 0.1
            if group_name == 'process_specific' and engine == 'iou-s':
                x = x + 0.1
            plt.text(
                x,
                y,
                '$' + text + '$',
                size=datalabel_size,
                ha='center',
                # rotation='vertical',
                va=datalabel_va
            )  # 'bottom', 'baseline', 'center', 'center_baseline', 'top'

    plt.xticks(x_axis, x_ticks)

    if legend_font_size:
        plt.legend(fontsize=legend_font_size)
    else:
        plt.legend()

    plt.savefig(fig_save_path, bbox_inches='tight')


def draw_cs_per_sec_io(system_wide, process_specific, system_wide_std,
                       process_specific_std, fig_save_path):
    group_list = ['system_wide', 'process_specific']
    x_ticks = ['psync', 'aio', 'iou', 'iou-c', 'iou-s', ' spdk-fio']
    value = {'system_wide': system_wide, 'process_specific': process_specific}
    std_dev = {
        'system_wide': system_wide_std,
        'process_specific': process_specific_std
    }
    # std_dev
    bar_width = 0.4
    fig_save_path = fig_save_path
    legend_label = {
        'system_wide': 'system-wide',
        'process_specific': 'process-specific'
    }
    ylabel = None
    # axis_tick_font_size = axis_tick_font_size
    # axis_label_font_size = axis_label_font_size
    # legend_font_size = legend_font_size
    # datalabel_size = datalabel_size
    datalabel_va = 'bottom'

    fig, ax = plt.subplots(figsize=(12, 8))

    # plt.title(title)
    # plt.xlabel(xlabel, fontsize=axis_label_font_size)
    # plt.ylabel(ylabel, fontsize=axis_label_font_size)
    plt.grid(axis='y')

    ax.tick_params(axis='both', which='major', labelsize=axis_tick_font_size)

    if legend_label == None:
        legend_label = {}
        for group in group_list:
            legend_label[group] = group

    x_axis = np.arange(len(x_ticks))

    # compute bar offset
    bar_offset = []
    mid_point = (len(group_list) * bar_width) / 2

    for i in range(len(group_list)):
        bar_offset.append(bar_width * i + 0.5 * bar_width - mid_point)

    print(bar_offset)
    print(x_axis)
    x_axis - 0.1

    for (index, group_name) in zip(range(len(group_list)), group_list):
        y = value[group_name]
        cur_stddev = std_dev[group_name]
        bar_pos = x_axis + bar_offset[index]
        plt.bar(bar_pos,
                y,
                width=bar_width,
                label=legend_label[group_name],
                yerr=cur_stddev)

        # print(bar_pos, y)
        for (x, y, engine) in zip(bar_pos, y, x_ticks):
            text = '{:.1f}'.format(y)
            # if group_name == 'system_wide' and engine == 'psync':
            #     x = x + 0.32
            #     y = y - 0.12
            # if group_name == 'system_wide' and engine == 'aio':
            #     x = x + 0.32
            #     y = y - 0.18
            # if group_name == 'system_wide' and engine == 'iou':
            #     x = x + 0.32
            #     y = y - 0.18
            plt.text(
                x,
                y,
                '$' + text + '$',
                size=datalabel_size,
                ha='center',
                # rotation='vertical',
                va=datalabel_va
            )  # 'bottom', 'baseline', 'center', 'center_baseline', 'top'

    plt.xticks(x_axis, x_ticks)

    if legend_font_size:
        plt.legend(fontsize=legend_font_size)
    else:
        plt.legend()

    plt.savefig(fig_save_path, bbox_inches='tight')


#split_part = [1 - 0.1292, 1 - 0.1360, 1 - 0.1566, 1 - 0.4670, 1 - 0.73]
split_part = [1 - 0.137, 1 - 0.9, 1 - 0.117, 1 - 0.26, 1 - 0.492, 1 - 0.17]
engine_speci = []
for (a, b) in zip(local_data['all_inst_per_io'], split_part):
    engine_speci.append(a * b)
draw_inst_io(global_data['all_inst_per_io'], local_data['all_inst_per_io'],
             engine_speci, global_data['all_inst_per_io_std'],
             local_data['all_inst_per_io_std'], 'inst_per_io_d1_qd1.pdf')
draw_ipc(global_data['all_ipc'], local_data['all_ipc'],
         global_data['all_ipc_std'], local_data['all_ipc_std'],
         'ipc_d1_qd1.pdf')
draw_branch_miss(global_data['all_branch_miss_rate'],
                 local_data['all_branch_miss_rate'],
                 global_data['all_branch_miss_rate_std'],
                 local_data['all_branch_miss_rate_std'], 'branch_d1_qd1.pdf')
draw_cs_per_sec_io(global_data['all_cs_per_sec_per_io'],
                   local_data['all_cs_per_sec_per_io'],
                   global_data['all_cs_per_sec_per_io_std'],
                   local_data['all_cs_per_sec_per_io_std'],
                   'cs_per_io_d1_qd1.pdf')
draw_cache_miss(global_data['all_cache_miss_r'],
                local_data['all_cache_miss_r'],
                global_data['all_cache_miss_r_std'],
                local_data['all_cache_miss_r_std'], 'cache_miss_d1_qd1.pdf')
