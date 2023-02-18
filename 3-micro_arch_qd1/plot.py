import os.path
import numpy as np
import fio

import matplotlib.pyplot as plt


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


def read_data(engines, dir, inst_sample_length, cs_sample_length,
              num_perf_files):
    all_inst_per_io = []
    all_inst_per_io_std = []
    all_ipc = []
    all_ipc_std = []
    all_cache_miss_r = []
    all_cache_miss_r_std = []

    global_rk = []
    jobs_rk = ['read:lat_ns:mean', 'read:iops', 'read:lat_ns:stddev']
    for e in engines:
        fname_cycles = os.path.join(dir, e + '_inst_cycle')
        fname_cahce = os.path.join(dir, e + '_cache')

        inst, cycle, ipc, inst_std, _, ipc_std = load_inst_cycle(
            fname_cycles, inst_sample_length, num_perf_files)
        cache_miss, cache_ref, cache_miss_rate, _, _, cache_miss_rate_std = load_cache(
            fname_cahce, num_perf_files)

        # multiply all rate by 100
        # Divide inst per io by 100
        all_ipc.append(ipc)
        all_ipc_std.append(ipc_std)
        all_cache_miss_r.append(cache_miss_rate * 100)
        all_cache_miss_r_std.append(cache_miss_rate_std * 100)

        fname_fio_1 = os.path.join(dir, e + '.txt')
        _, j_res = fio.parse_experiment(fname_fio_1, global_rk, jobs_rk)
        iops_1 = j_res[0]['read:iops']
        all_inst_per_io.append(inst / iops_1 / 1000)
        all_inst_per_io_std.append(inst_std / iops_1 / 1000)

    ret = {
        'all_ipc': all_ipc,
        'all_ipc_std': all_ipc_std,
        'all_cache_miss_r': all_cache_miss_r,
        'all_cache_miss_r_std': all_cache_miss_r_std,
        'all_inst_per_io': all_inst_per_io,
        'all_inst_per_io_std': all_inst_per_io_std,
    }
    return ret


global_dir = './results_global'
local_dir = './results_local'
engines = ['aio', 'iou', 'iou_c', 'iou_s', 'spdk_fio']
inst_sample_length = 5
cs_sample_length = 5
num_perf_files = 10

global_data = read_data(engines, global_dir, inst_sample_length,
                        cs_sample_length, num_perf_files)
local_data = read_data(engines, local_dir, inst_sample_length,
                       cs_sample_length, num_perf_files)

x_label = 'Engines'
bar_width = 0.4
axis_label_font_size = 28
axis_tick_font_size = 26
legend_font_size = 23
datalabel_size = 24
datalabel_va = 'bottom'  #'bottom'


def draw_inst_io(system_wide, process_specific, system_wide_std,
                 process_specific_std, fig_save_path):
    group_list = ['system_wide', 'process_specific']
    x_ticks = ['aio', 'iou', 'iou-c', 'iou-s', ' spdk-fio']
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
    ylabel = 'Instructions per I/O (K)'
    datalabel_va = 'bottom'

    fig, ax = plt.subplots(figsize=(12, 8))

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
                if engine == 'iou-s':
                    x = x - 0.13
                else:
                    x = x - 0.08
            if group_name == 'process_specific' and engine == 'iou-s':
                if engine == 'iou-s':
                    x = x + 0.13
                else:
                    x = x + 0.08
            plt.text(
                x, y, text, size=datalabel_size, ha='center', va=datalabel_va
            )  # 'bottom', 'baseline', 'center', 'center_baseline', 'top'

    plt.xticks(x_axis, x_ticks)

    plt.legend(fontsize=legend_font_size, loc='upper left')

    plt.savefig(fig_save_path, bbox_inches='tight')


def draw_cache_miss(system_wide, process_specific, system_wide_std,
                    process_specific_std, fig_save_path):
    group_list = ['system_wide', 'process_specific']
    x_ticks = ['aio', 'iou', 'iou-c', 'iou-s', ' spdk-fio']
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
    ylabel = 'Cache miss rate (%)'
    datalabel_va = 'bottom'

    fig, ax = plt.subplots(figsize=(12, 8))

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

        for (x, y, engine) in zip(bar_pos, y, x_ticks):
            text = '{:.1f}'.format(y)
            plt.text(
                x, y, text, size=datalabel_size, ha='center', va=datalabel_va
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
    x_ticks = ['aio', 'iou', 'iou-c', 'iou-s', ' spdk-fio']
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
    datalabel_va = 'bottom'

    fig, ax = plt.subplots(figsize=(12, 8))

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

        for (x, y, engine) in zip(bar_pos, y, x_ticks):
            text = '{:.1f}'.format(y)
            if group_name == 'system_wide':
                x = x - 0.1
            if group_name == 'process_specific' and engine == 'iou-s':
                x = x + 0.1
            plt.text(
                x, y, text, size=datalabel_size, ha='center', va=datalabel_va
            )  # 'bottom', 'baseline', 'center', 'center_baseline', 'top'

    plt.xticks(x_axis, x_ticks)

    if legend_font_size:
        plt.legend(fontsize=legend_font_size)
    else:
        plt.legend()

    plt.savefig(fig_save_path, bbox_inches='tight')


draw_inst_io(global_data['all_inst_per_io'], local_data['all_inst_per_io'],
             global_data['all_inst_per_io_std'],
             local_data['all_inst_per_io_std'], 'inst_per_io_d1_qd1.pdf')
draw_ipc(global_data['all_ipc'], local_data['all_ipc'],
         global_data['all_ipc_std'], local_data['all_ipc_std'],
         'ipc_d1_qd1.pdf')
draw_cache_miss(global_data['all_cache_miss_r'],
                local_data['all_cache_miss_r'],
                global_data['all_cache_miss_r_std'],
                local_data['all_cache_miss_r_std'], 'cache_miss_d1_qd1.pdf')
