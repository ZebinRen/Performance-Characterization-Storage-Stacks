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


def read_data(engines, num_processes, dir):
    ret = {}
    for e in engines:
        ret[e] = []

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

    return ret


dir = 'results'
engines = ['aio', 'iou', 'iou_s', 'iou_c', 'spdk_fio']
num_process = 20

ret = read_data(engines, num_process, dir)
ret['spdk_perf'] = [
    4133.77276, 4197.766320000001, 4168.74538, 4157.8478700000005, 4154.96826,
    4152.52495, 4149.81391, 4145.44371, 4140.99606, 4137.21565, 4133.73131,
    4129.60008, 4125.95598, 4121.80574, 4121.7533300000005, 4121.75361,
    4121.73139, 4121.66921, 4121.66537, 4121.68699
]

bar_width = 0.4
axis_label_font_size = 34
axis_tick_font_size = 34
legend_font_size = 34
datalabel_size = 26
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

    plt.xlabel('Number of threads', fontsize=axis_label_font_size)
    plt.ylabel('MIOPS', fontsize=axis_label_font_size)
    plt.grid(True)

    ax.tick_params(axis='both', which='major', labelsize=axis_tick_font_size)
    ax.xaxis.set_ticks([1] + list(range(2, 21, 2)))
    ax.set_ylim([0, 5])

    group_label = {
        'aio': 'aio',
        'iou': 'iou',
        'iou_s': 'iou-s',
        'iou_c': 'iou-c',
        'spdk_fio': 'spdk-fio',
        'spdk_perf': 'spdk-perf'
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

    plt.legend(fontsize=legend_font_size, labelspacing=0.1)

    plt.savefig(fig_save_path, bbox_inches='tight')


draw_graph(ret, engines + ['spdk_perf'], 'inc_process.pdf')
