import os.path

import fio
from multi_bar_graph import multi_bar_graph as bar_graph

import matplotlib

# Switch to Type 1 Fonts.
matplotlib.rcParams['ps.useafm'] = True
matplotlib.rcParams['pdf.use14corefonts'] = True
matplotlib.rcParams['text.usetex'] = True

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
    dev1_path = os.path.join(dir, e + '_dev1.txt')
    _, j_res = fio.parse_experiment(dev1_path, global_rk, jobs_rk)
    cur_lat = j_res[0]['read:lat_ns:mean'] / 1000  # us
    cur_iops = j_res[0]['read:iops'] / 1000  #kiops
    # iops.append('{:.2f}'.format(cur_iops))
    # lat.append('{:.2f}'.format(cur_lat))
    iops.append(cur_iops)
    lat.append(cur_lat)

print('engines', engines)
print('throughput', '=', iops)
print('latency =', lat)

x_label = 'Engines'
y_label = 'Throughput (KIOPS)'
bar_width = 0.6
axis_label_font_size = 28
axis_tick_font_size = 26
legend_font_size = 26
datalabel_size = 18
datalabel_va = 'bottom'
legend_label = None  #{'throughput': 'throughput'}

x_label = 'Engines'
bar_width = 0.4
axis_label_font_size = 34
axis_tick_font_size = 34
legend_font_size = 34
datalabel_size = 26
datalabel_va = 'bottom'  #'bottom'
linewidth = 4
markersize = 15

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
