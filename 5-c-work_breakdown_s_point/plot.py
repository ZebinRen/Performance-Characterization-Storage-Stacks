import os.path
import matplotlib.pyplot as plt

from process_report_graph import parse_report_file

legend_name = {
    'app': 'fio',
    'interface': 'I/O lib',
    'block': 'block_layer',
    'driver': 'nvme driver',
    'sys': 'kernel'
}

legend_name = {
    'app': 'fio',
    'interface': 'I/O lib',
    'block': 'block_layer',
    'driver': 'nvme driver',
    'sys': 'kernel'
}

CB_color_cycle = [
    '#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3',
    '#999999', '#e41a1c', '#dede00'
]

color_index = 0


def get_color():
    global color_index
    prev_c = color_index
    color_index += 1
    color_index %= len(CB_color_cycle)
    return CB_color_cycle[prev_c]


def plot(labels,
         bar_names,
         bar_value,
         title,
         xlabel,
         ylabel,
         fig_save_path,
         axis_label_font_size=None,
         axis_tick_font_size=None,
         legend_font_size=None,
         datalabel_size=None,
         datalabel_va=None):

    fig, ax = plt.subplots()
    plt.grid(True)
    if title:
        plt.title(title)
    if axis_label_font_size:
        plt.xlabel(xlabel, fontsize=axis_label_font_size)
        plt.ylabel(ylabel, fontsize=axis_label_font_size)
    else:
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

    if axis_tick_font_size:
        ax.tick_params(axis='both',
                       which='major',
                       labelsize=axis_tick_font_size)

    print('--------')
    bottom = [0] * len(labels)
    for index, cur_bar in zip(range(len(bar_names)), bar_names):
        # print(cur_bar)
        # print(bar_value[cur_bar])
        cur_ax = ax.bar(
            labels,
            bar_value[cur_bar],
            label=legend_name[cur_bar],
            bottom=bottom,
            #width=0.3,
            #fill=False,
            edgecolor='black',
            color=get_color()
            #hatch=hatch[index % len(bar_names)]
        )

        cur_bar_label = bar_value[cur_bar]
        cur_bar_label = ["{:.2f}".format(x) for x in cur_bar_label]
        ax.bar_label(cur_ax, cur_bar_label, label_type='center', size=14)
        for i in range(len(bottom)):
            bottom[i] += bar_value[cur_bar][i]

    plt.legend(loc='upper center',
               bbox_to_anchor=(0.5, 1.22),
               ncol=3,
               fancybox=True,
               shadow=True,
               fontsize=14)

    #plt.legend()
    plt.savefig(fig_save_path, bbox_inches="tight")


engines = ["aio", "iou", "iou_c", "iou_s"]  #, "spdk_fio_s"]
result_path = 'perf_graph'

data = []
for e in engines:
    fname = os.path.join(result_path, 'perf_parsed_' + e + '_g.txt')
    res = parse_report_file(fname)
    res = [i * 100 for i in res]
    data.append(res)

# TODO: PLEASE CLASSIFY THE DATA BY YOURSELF
data.append([73, 0, 0, 27, 0])

labels = ["aio", "iou", "iou-c", "iou-s", "spdk-fio"]
bar_names = ['app', 'interface', 'block', 'driver', 'sys']

bar_value = {'app': [], 'interface': [], 'block': [], 'driver': [], 'sys': []}

for split in data:
    for (index, cost_class) in enumerate(bar_names):
        bar_value[cost_class].append(split[index])

print(bar_value)

title = None
xlabel = 'Engines'
ylabel = 'Percentage'
fig_save_path = 'work_breakdown_s_point.pdf'
axis_label_font_size = 20
axis_tick_font_size = 16
legend_font_size = 18
datalabel_size = 20
datalabel_va = 'bottom'
plot(labels,
     bar_names,
     bar_value,
     title,
     xlabel,
     ylabel,
     fig_save_path,
     axis_tick_font_size=axis_tick_font_size,
     axis_label_font_size=axis_label_font_size,
     legend_font_size=legend_font_size,
     datalabel_size=datalabel_size,
     datalabel_va=datalabel_va)
