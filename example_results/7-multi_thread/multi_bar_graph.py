import matplotlib.pyplot as plt
import numpy as np


def multi_bar_graph(x_ticks,
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
                    datalabel_va=None):

    # def multi_bar_graph(data,
    #                     title,
    #                     xlabel,
    #                     ylabel,
    #                     x_ticks,
    #                     group_list,
    #                     fig_save_path,
    #                     bar_width,
    #                     group_label=None,
    #                     axis_tick_font_size=None,
    #                     axis_label_font_size=None,
    #                     legend_font_size=None,
    #                     datalabel_size=None):

    fig, ax = plt.subplots(figsize=(12, 8))

    if title:
        plt.title(title)
    if axis_label_font_size:
        plt.xlabel(xlabel, fontsize=axis_label_font_size)
        plt.ylabel(ylabel, fontsize=axis_label_font_size)
    else:
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
    plt.grid(True)

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

    print(bar_offset)
    print(x_axis)
    x_axis - 0.1

    for (index, group_name) in zip(range(len(group_list)), group_list):
        y = value[group_name]
        bar_pos = x_axis + bar_offset[index]
        plt.bar(bar_pos, y, width=bar_width, label=legend_label[group_name])

        # print(bar_pos, y)
        for (x, y) in zip(bar_pos, y):
            text = '{:.2f}'.format(y)
            plt.text(
                x,
                y,
                text,
                size=datalabel_size,
                ha='center',
                rotation='vertical',
                va=datalabel_va
            )  # 'bottom', 'baseline', 'center', 'center_baseline', 'top'

    plt.xticks(x_axis, x_ticks)

    if legend_font_size:
        plt.legend(fontsize=legend_font_size)
    else:
        plt.legend()

    plt.savefig(fig_save_path, bbox_inches='tight')