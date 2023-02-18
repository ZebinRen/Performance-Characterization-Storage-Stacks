import os.path
import json

import matplotlib.pyplot as plt


def select_data_from_dict(data, reterieve_key):
    '''
    Select data from dict using given keys
    
    Args:
        data(dict):
        reterieve_key(list):
    Returns:
    '''
    ret = {}

    for k in reterieve_key:
        cur_keys = k.split(':')
        selected_data = data
        for single_key in cur_keys:
            selected_data = selected_data[single_key]
        ret[k] = selected_data

    return ret


def parse_global(data, reterieve_key):
    return select_data_from_dict(data, reterieve_key)


def parse_one_job(data, reterieve_key):
    return select_data_from_dict(data, reterieve_key)


## TODO: Add job specific key
def parse_experiment(filename, global_reterive_key, job_reterive_key):
    """
    Parse outputs from one experiment

    Args:
        filename (str): _description_
        global_reterive_key (list(str)): _description_
        job_reterive_key (list(str)): _description_

    Returns:
        dict: parsed global results
        list(dict): parsed results for each job
    """
    f = open(filename, 'r')

    try:
        data = json.load(f)
    except:
        raise (Exception(
            'File {} can not loaded by json.load()'.format(filename)))
    f.close()

    num_jobs = len(data['jobs'])

    global_result = parse_global(data['global options'], global_reterive_key)
    jobs_result = []
    for job in data['jobs']:
        jobs_result.append(parse_one_job(job, job_reterive_key))

    return global_result, jobs_result


# files: {some_key: file_name}
def parse_one_group(files, global_reterive_key, job_reterive_key):
    """
    Parse the all experiments from one group

    Args:
        dir (str): Dir path to the results folder
        files (list(str)): Output filenames
        global_reterive_key (list(str)): 
        job_reterive_key (list(str)):

    Returns:
        dict: parsed results for the group
    """
    ret = {}
    for k in files.keys():
        cur_file_path = files[k]
        parsed_output = parse_experiment(cur_file_path, global_reterive_key,
                                         job_reterive_key)
        ret[k] = parsed_output

    return ret


def parse_all(files, global_reterive_key, job_reterive_key):
    """
    Parse output from all groups

    Args:
        files (_type_): _description_
        global_reterive_key (_type_): _description_
        job_reterive_key (_type_): _description_

    Returns:
        _type_: _description_
    """
    ret = {}
    for group in files.keys():
        group_dir, group_files = files[group]
        ret[group] = parse_one_group(group_dir, group_files,
                                     global_reterive_key, job_reterive_key)

    return ret


def plot_staked_bar(labels, bar_names, bar_value, title, ylabel,
                    fig_save_path):

    fig, ax = plt.subplots()

    #plt.title(title)
    #plt.ylable(ylabel)

    print('--------')
    for cur_bar in bar_names:
        print(cur_bar)
        print(bar_value[cur_bar])
        ax.bar(labels, bar_value[cur_bar], label=cur_bar)

    plt.legend()
    plt.savefig(fig_save_path)


def parsed_to_array(reterieve_outputs, get_x_y_label):
    """
    Get data from the reterieve keys

    Args:
        reterieve_outputs (dict): KV of reterieved values
        get_x_y_label (func()): Parse reterieve_outputs and get x, y and label

    Returns:
        list : x values
        list : y values
        list : label values
    """
    x = []
    y = []
    std_dev = []
    label = []

    for k in reterieve_outputs:
        global_output = reterieve_outputs[k][0]
        jobs_output = reterieve_outputs[k][1]

        cur_x, cur_y, cur_label, cur_std_dev = get_x_y_label(
            global_output, jobs_output)

        x.append(cur_x)
        y.append(cur_y)
        std_dev.append(cur_std_dev)
        label.append(cur_label)

    return x, y, std_dev, label


def get_all_data(outputs, get_x_y_label):
    """
    Get all data from a group

    Args:
        outputs (dict): Parsed data
        get_x_y_label (func): 

    Returns:
        dict: (x, y label) for each experiment
    """
    ret = {}
    for group_name in outputs.keys():
        group_output = outputs[group_name]
        group_data = parsed_to_array(group_output, get_x_y_label)
        ret[group_name] = group_data

    return ret


def parse_spdk_perf():
    pass


if __name__ == '__main__':
    test_file = '/home/user/test_script/tmp/1/output_iodepth_1.josn'

    global_rk = ["iodepth"]
    jobs_rk = ["jobname", "read:slat_ns:mean"]

    gr, jr = parse_experiment(test_file, global_rk, jobs_rk)
    print(gr)
    print(jr)
