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
matplotlib_color = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5']

m_color_index = 0


def get_next_color():
    global m_color_index
    c = matplotlib_color[m_color_index]
    m_color_index += 1

    return c


def reset_color():
    global m_color_index
    m_color_index = 0


def read_data(engines, schedulers, num_processes, dir):
    ret = {}
    ret_node1 = {}
    for e in engines:
        ret[e] = {}
        ret_node1[e] = {}
        for s in schedulers:
            ret[e][s] = []
            ret_node1[e][s] = []

    global_rk = []
    jobs_rk = ['read:lat_ns:mean', 'read:iops', 'read:lat_ns:stddev']
    for e in engines:
        for s in schedulers:
            for num_t in range(1, num_processes + 1):
                if e == 'iou_s' and num_t > 10:
                    break
                cur_filename = e + '_{}_threads_{}.txt'.format(s, num_t)
                cur_filename = os.path.join(dir, cur_filename)

                _, j_res = fio.parse_experiment(cur_filename, global_rk,
                                                jobs_rk)
                all_iops = []
                for single_job_res in j_res:
                    all_iops.append(single_job_res['read:iops'])

                iops = np.sum(all_iops)
                iops = iops / 1000
                ret[e][s].append(iops)

    for e in engines:
        for s in schedulers:
            for num_t in range(1, num_processes + 1):
                if e == 'iou_s' and num_t > 10:
                    break
                cur_filename = e + '_{}_threads_{}_node1.txt'.format(s, num_t)
                cur_filename = os.path.join(dir, cur_filename)

                _, j_res = fio.parse_experiment(cur_filename, global_rk,
                                                jobs_rk)
                all_iops = []
                for single_job_res in j_res:
                    all_iops.append(single_job_res['read:iops'])

                iops = np.sum(all_iops)
                iops = iops / 1000
                ret_node1[e][s].append(iops)

    return ret, ret_node1


dir = 'results'
engines = ['iou', 'iou_s', 'iou_c']
schedulers = ['none', "bfq", "kyber", "mq-deadline"]
num_process = 20

ret, ret_node1 = read_data(engines, schedulers, num_process, dir)

x_label = 'Engines'
bar_width = 0.4
axis_label_font_size = 28
axis_tick_font_size = 26
legend_font_size = 20  #26
datalabel_size = 18
datalabel_va = 'bottom'  #'bottom'
linewidth = 4
markersize = 15

x_label = 'Engines'
bar_width = 0.4
axis_label_font_size = 34
axis_tick_font_size = 34
legend_font_size = 30
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

line_style = []


def draw_graph(
        data,
        data_node1,
        # xlabel,
        # ylabel,
        group_list,
        fig_save_path,
        if_iou_s=False):
    reset_color()
    fig, ax = plt.subplots(figsize=(12, 8))

    plt.xlabel('Number of threads', fontsize=axis_label_font_size)
    plt.ylabel('MIOPS', fontsize=axis_label_font_size)
    plt.grid(True)

    ax.tick_params(axis='both', which='major', labelsize=axis_tick_font_size)
    ax.xaxis.set_ticks([1] + list(range(2, 21, 2)))
    ax.set_xlim(0.5, 20.5)
    ax.set_ylim([0, 5])

    group_label = {
        'none': 'none',
        "bfq": 'BFQ',
        "kyber": "Kyber",
        "mq-deadline": "mq-deadline"
    }

    for (index, group_name) in zip(range(len(group_list)), group_list):
        # x, y, std_dev, data_label = data[group_name]
        x = range(1, len(data[group_name]) + 1)
        y = data[group_name]
        y = [i / 1000 for i in y]
        if if_iou_s:
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

    for (index, group_name) in zip(range(len(group_list)), group_list):
        # x, y, std_dev, data_label = data[group_name]
        x = range(1, len(data_node1[group_name]) + 1)
        y = data_node1[group_name]
        y = [i / 1000 for i in y]
        if if_iou_s:
            x = list(range(2, 21, 2))
            y = y[:10]

        plt.errorbar(
            x,
            y,
            # yerr=std_dev,
            #label=group_label[group_name] + '-node1',
            marker=dot_style[index % len(dot_style)],
            linewidth=linewidth,
            markersize=markersize,
            linestyle='dotted',
            color=get_next_color()
        )  # TODO: Add more options, may be passing from the arguments
        # for i in range(len(data_label)):
        #
    reset_color()
    plt.errorbar(
        [],
        [],
        # yerr=std_dev,
        label='node1',
        # marker=dot_style[index % len(dot_style)],
        linewidth=linewidth,
        markersize=markersize,
        linestyle='dotted',
        color=get_next_color())

    plt.legend(fontsize=legend_font_size, labelspacing=0.1)

    plt.savefig(fig_save_path, bbox_inches='tight')


draw_graph(ret['iou'], ret_node1['iou'], schedulers,
           'sched_inc_thread_iou_two.pdf')
draw_graph(ret['iou_s'], ret_node1['iou_s'], schedulers,
           'sched_inc_thread_iou_s_two.pdf', True)
draw_graph(ret['iou_c'], ret_node1['iou_c'], schedulers,
           'sched_inc_thread_iou_c_two.pdf')
