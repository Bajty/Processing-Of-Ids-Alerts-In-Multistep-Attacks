import pandas as pd
import json
import numpy as np


def perc_diff(a, b):
    if (a == b):
        return 0
    if (a + b) == 0:
        return 2
    return (abs(a - b) / abs((a + b) / 2))


def time_diff(bigger, smaller):
    return pd.Timedelta(bigger - smaller).seconds


def load_config(dataset_config) -> dir:
    file = open(dataset_config)
    config = json.load(file)
    return config


def load_dataset(dataset_path, inputs, inputs_benign, headers, timedelta, timedelta_function):
    all_data = pd.DataFrame()
    benign_days = []
    for file_path in inputs + inputs_benign:
        data = pd.read_csv(dataset_path + file_path, header=None, names=headers,
                           converters={'from_port': str, 'to_port': str})

        if timedelta != False:
            if timedelta_function == "+":
                data['datetime'] = pd.to_datetime(data['timestamp'], format='%m/%d-%H:%M:%S.%f',
                                                  exact=False) + pd.Timedelta(timedelta)
            if timedelta_function == "-":
                data['datetime'] = pd.to_datetime(data['timestamp'], format='%m/%d-%H:%M:%S.%f',
                                                  exact=False) - pd.Timedelta(timedelta)
        else:
            data['datetime'] = pd.to_datetime(data['timestamp'], format='%m/%d-%H:%M:%S.%f',
                                              exact=False)

        data['file_path'] = file_path
        data['hour'] = data["datetime"].apply(lambda t: str(t.hour))
        all_data = all_data._append(data)

    all_data = all_data.sort_values(by=['datetime'])
    return all_data


def check_filters(filters1, filters2):
    if filters1 is None and filters2 is None:
        return True
    for filter in filters1:
        if filter['type'] not in filters2:
            err_msg = f'ERROR: Filter {filter} is not applicable for this dataset'
            raise Exception(err_msg)

    return True

    return all(x in config for x in dataset_config)


def get_days(data):
    return list(data["datetime"].map(lambda t: str(t.date())).unique())


def get_file_paths(data):
    return list(data["file_path"].map(lambda t: t).unique())


def get_stats(data, col):
    data['mean'] = col.mean(axis=1)
    data['median'] = col.median(axis=1)
    data['perc_diff'] = data.apply(lambda row: perc_diff(row['mean'], row['median']), axis=1)
    data['std'] = col.std(axis=1)
    data['min'] = col.min(axis=1)
    data['max'] = col.max(axis=1)
    data['count'] = np.count_nonzero(col, axis=1)
    data['sum'] = col.sum(axis=1)
    return data


def get_counts_days(data, group_cols):
    all_days_data = data[group_cols].groupby(group_cols).size().unstack(fill_value=0)
    return all_days_data


def get_counts_hours(data, group_cols):
    paths = get_file_paths(data)
    data = data[group_cols]
    return_data = pd.DataFrame()
    for path in paths:
        selected_day_data = data.loc[data['file_path'] == path]
        selected_day_data = selected_day_data[group_cols].groupby(group_cols).size().unstack(fill_value=0)
        return_data = return_data._append(selected_day_data)
    return_data = return_data.sort_values(by=group_cols[:-1])
    return return_data


def get_counts_hours_sub_mean(data, group_cols, inputs):
    group_cols = group_cols
    grouped_data = get_counts_hours(data, group_cols).loc[:, '0':'23']
    selected_grouped_data = grouped_data[grouped_data.index.get_level_values('file_path').isin(inputs)]
    selected_grouped_data = selected_grouped_data.groupby(group_cols[1:-1]).mean()
    paths = get_file_paths(data)
    for index in selected_grouped_data.index.tolist():
        for path in paths:
            temp_idx = (path,) + index
            if temp_idx in grouped_data.index.tolist():
                grouped_data.loc[temp_idx] = grouped_data.loc[temp_idx] - selected_grouped_data.loc[index]
    grouped_data[grouped_data < 0] = 0
    grouped_data = grouped_data.sort_values(by=group_cols[:-1])
    return grouped_data


def export_filtered_data(data, name):
    data_copy = data.copy()
    data_copy = data_copy.drop('hour', axis=1)
    data_copy = data_copy.drop('datetime', axis=1)
    data_copy = data_copy.drop('file_path', axis=1)
    base_path = 'results'
    data_copy.to_csv(f'{base_path}/{name}.csv', index=False, header=False)


def load_classes(dataset_path, path):
    return pd.read_csv(f'{dataset_path}/{path}')


def export_agg_data(agg_events, name):
    base_path = 'results'
    serialized_events = []
    for agg_event in agg_events:
        serialized_events.append(agg_event.serialize())
    with open(f"{base_path}/{name}.json", "w") as write_file:
        json.dump(serialized_events, write_file)
