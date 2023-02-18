import os.path
import matplotlib.pyplot as plt
import numpy as np

import fio


def bar_graph(x_ticks,
              value,
              std_dev,
              group_list,
              bar_width,
              fig_save_path,
              legend_label,
              title=None,
              xlabel=None,
              ylabel=None,
              axis_tick_font_size=None,
              axis_label_font_size=None,
              legend_font_size=None,
              datalabel_size=None,
              datalabel_va=None,
              print_legend=True):
    fig, ax = plt.subplots(figsize=(12, 8))

    if title:
        plt.title(title)
    if axis_label_font_size:
        plt.xlabel(xlabel, fontsize=axis_label_font_size)
        plt.ylabel(ylabel, fontsize=axis_label_font_size)
    else:
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
    plt.grid(axis='y')

    if axis_tick_font_size:
        ax.tick_params(axis='both',
                       which='major',
                       labelsize=axis_tick_font_size)

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

    x_axis - 0.1
    for (index, group_name) in zip(range(len(group_list)), group_list):
        y = value[group_name]
        bar_pos = x_axis + bar_offset[index]
        plt.bar(bar_pos, y, width=bar_width, label=legend_label[group_name])
        y_origin = y
        for (index, x, y) in zip(list(range(len(y_origin))), bar_pos,
                                 y_origin):
            text = '{:.1f}'.format(y)
            plt.text(x,
                     y,
                     text,
                     size=datalabel_size,
                     ha='center',
                     va=datalabel_va)

    plt.xticks(x_axis, x_ticks)

    if print_legend:
        plt.legend(fontsize=legend_font_size)

    plt.savefig(fig_save_path, bbox_inches='tight')


dir = './results'
engines = ['psync', 'aio', 'iou', 'iou_c', 'iou_s', 'spdk_fio']
files = {
    'psync': 'psync.txt',
    'aio': 'aio.txt',
    'iou': 'iou.txt',
    'iou_s': 'iou_s.txt',
    'iou_c': 'iou_c.txt',
    'spdk_fio': 'spdk_fio.txt'
}

global_rk = []
jobs_rk = ['read:lat_ns:mean', 'read:iops', 'read:lat_ns:stddev']

iops = []
iops_stddev = []
lat = []
lat_stdev = []

for e in engines:
    dev1_path = os.path.join(dir, e + '.txt')
    _, j_res = fio.parse_experiment(dev1_path, global_rk, jobs_rk)
    cur_lat = j_res[0]['read:lat_ns:mean'] / 1000  # us
    cur_iops = j_res[0]['read:iops'] / 1000  #kiops
    iops.append(cur_iops)
    lat.append(cur_lat)

# print('engines', engines)
# print('throughput', '=', iops)
# print('latency =', lat)

x_label = 'Engines'
y_label = 'Throughput(KIOPS)'
bar_width = 0.6
axis_label_font_size = 28
axis_tick_font_size = 26
legend_font_size = 26
datalabel_size = 18
datalabel_va = 'bottom'
legend_label = None

data = {'throughput': iops}
group_list = ['throughput']
fig_save_path = 'iops_d1_qd1.pdf'
x_ticks = ['psync', 'aio', 'iou', 'iou-c', 'iou-s', 'spdk-fio']
bar_graph(x_ticks,
          data,
          None,
          group_list,
          bar_width,
          fig_save_path,
          legend_label,
          xlabel=None,
          ylabel=y_label,
          axis_tick_font_size=axis_tick_font_size,
          axis_label_font_size=axis_label_font_size,
          legend_font_size=legend_font_size,
          datalabel_size=datalabel_size,
          datalabel_va=datalabel_va,
          print_legend=False)
