import matplotlib.pyplot as plt
import os.path
import fio

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

dot_index = 0


def get_dot():
    global dot_index
    ret_styl = dot_style[dot_index]
    dot_index += 1
    return ret_styl


dir = './results'
global_rk = ["iodepth"]
jobs_rk = ["jobname", "read:lat_ns:mean", 'read:iops', 'read:lat_ns:stddev']

qd = [1, 2, 4, 8, 16, 32, 64, 128]

iops = []
lat = []
lat_stdev = []

engines = ['aio', 'iou', 'iou_c', 'iou_s', 'spdk_fio']
iops_data = {}
lat_data = {}
lat_std_data = {}

for e in engines:
    iops_data[e] = []
    lat_data[e] = []
    lat_std_data[e] = []
    for cur_qd in qd:
        filename = os.path.join(dir, e + '_qd_' + str(cur_qd) + '.txt')
        _, j_res = fio.parse_experiment(filename, global_rk, jobs_rk)
        cur_lat = j_res[0]['read:lat_ns:mean'] / 1000  # us
        cur_iops = j_res[0]['read:iops'] / 1000  #kiops
        cur_lat_std = j_res[0]['read:lat_ns:stddev'] / 1000
        iops_data[e].append(cur_iops)
        lat_data[e].append(cur_lat)
        lat_std_data[e].append(cur_lat_std)

title = None
xlabel = None
ylabel = 'Latency (us)'
group_list = ['aio', 'iou', 'iou_p_s', 'iou_p_c', 'spdk']
fig_save_path = 'iops_lat_d1.pdf'
group_label = {
    'aio': 'aio',
    'iou': 'iou',
    'iou_s': 'iou-s',
    'iou_c': 'iou-c',
    'spdk_fio': 'spdk'
}

axis_label_font_size = 28
axis_tick_font_size = 28
legend_font_size = 26
linewidth = 4
datalabel_size = 18
markersize = 15

fig, ax = plt.subplots(figsize=(12, 8))
plt.xlabel(xlabel, fontsize=axis_label_font_size)
plt.ylabel(ylabel, fontsize=axis_label_font_size)
plt.grid(True)

if axis_tick_font_size:
    ax.tick_params(axis='both', which='major', labelsize=axis_tick_font_size)

for e in engines:
    x = iops_data[e]
    y = lat_data[e]
    stddev = lat_std_data[e]
    plt.errorbar(
        x,
        y,
        yerr=stddev,
        label=group_label[e],
        marker=get_dot(),
        linewidth=linewidth,
        markersize=markersize,
    )
    for i in range(len(qd)):
        ax.text(x[i], y[i], qd[i], size=datalabel_size)

plt.legend(fontsize=legend_font_size)

plt.savefig(fig_save_path, bbox_inches='tight')
