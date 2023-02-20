import os.path
import numpy as np
import fio

import matplotlib.pyplot as plt


def parse_spdk_perf(filename):
    f = open(filename)
    contents = f.readlines()
    f.close()

    contents.reverse()

    last_line = ''
    for l in contents:
        if l != '\n':
            last_line = l
            break
    data = l.split(' ')

    data = [x for x in data if x != '']
    iops = float(data[2])
    latency = float(data[4])

    return iops, latency


def read_data(engines, num_processes, dir):
    ret = {}
    for e in engines:
        ret[e] = []
    ret['spdk_perf'] = []

    global_rk = []
    jobs_rk = ['read:lat_ns:mean', 'read:iops', 'read:lat_ns:stddev']
    for e in engines:
        for num_p in range(1, num_processes + 1):
            # qd = 1
            cur_filename = e + '_t_' + str(num_p) + '.txt'
            cur_filename = os.path.join(dir, cur_filename)

            _, j_res = fio.parse_experiment(cur_filename, global_rk, jobs_rk)
            all_iops = []
            for single_job_res in j_res:
                all_iops.append(single_job_res['read:iops'])

            iops = np.sum(all_iops)
            iops = iops / 1000
            ret[e].append(iops)

    for num_p in range(1, num_processes + 1):
        cur_filename = 'spdk_perf_t_' + str(num_p) + '.txt'
        cur_filename = os.path.join(dir, cur_filename)
        cur_iops, cur_latency = parse_spdk_perf(cur_filename)
        ret['spdk_perf'].append(cur_iops / 1000)
    return ret


dir = 'results'
engines = ['aio', 'iou', 'iou_s', 'iou_c', 'spdk_fio', 'spdk_perf']
num_process = 20

ret = read_data(engines[:-1], num_process, dir)

x_label = 'Engines'
bar_width = 0.4
axis_label_font_size = 28
axis_tick_font_size = 26
legend_font_size = 26
datalabel_size = 18
datalabel_va = 'bottom'  #'bottom'
linewidth = 4
markersize = 15

matplotlib_colors = [
    'blue', 'green', 'red', 'cyan', 'magenta', 'yellw', 'white'
]

dot_style = [
    '+',
    'X',
    'o',
    'v',
    's',
    'P',
]


def draw_graph(
    data,
    # xlabel,
    # ylabel,
    group_list,
    fig_save_path,
):
    # group_label=None,
    # axis_tick_font_size=None,
    # axis_label_font_size=None,
    # legend_font_size=None,
    #    linewidth=None,
    #    datalabel_size=None,
    #    markersize=None

    fig, ax = plt.subplots(figsize=(12, 8))

    # plt.xlabel('xlabel', fontsize=axis_label_font_size)
    plt.ylabel('MIOPS', fontsize=axis_label_font_size)
    plt.grid(True)

    ax.tick_params(axis='both', which='major', labelsize=axis_tick_font_size)
    ax.xaxis.set_ticks([1, 4, 8, 12, 16, 20])
    ax.set_ylim([0, 5])

    group_label = {
        'aio': 'aio',
        'iou': 'iou',
        'iou_s': 'iou-s',
        'iou_c': 'iou-c',
        'spdk_fio': 'spdk_fio',
        'spdk_perf': 'spdk_perf'
    }

    for (index, group_name) in zip(range(len(group_list)), group_list):
        # x, y, std_dev, data_label = data[group_name]
        x = range(1, 21)
        y = data[group_name]
        y = [i / 1000 for i in y]
        if group_name == 'iou_s':
            x = list(range(2, 21, 2))
            y = y[:10]

        plt.errorbar(
            x,
            y,
            # yerr=std_dev,
            label=group_label[group_name],
            marker=dot_style[index % len(dot_style)],
            linewidth=linewidth,
            markersize=markersize,
        )  # TODO: Add more options, may be passing from the arguments
        # for i in range(len(data_label)):
        #     ax.text(x[i], y[i], data_label[i], size=datalabel_size)

    plt.legend(fontsize=legend_font_size)

    plt.savefig(fig_save_path, bbox_inches='tight')


draw_graph(ret, engines, 'inc_process.pdf')