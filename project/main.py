import pandas as pd
import numpy as np
from tasks import perc_diff
import uuid
import argparse
import os
from datetime import datetime

from tasks import (
    load_config,
    load_dataset_iscx,
    get_quantity,
    get_days,
    get_file_paths,
    get_stats,
    get_counts_days,
    get_counts_hours,
    get_counts_hours_sub_mean,
    check_filters,
    export_agg_data
)
from filter import (
    filter_all_days_stats,
    filter_perc_count
)
from aggregation import (
    create_events,
    aggregtion
)

# add flag option for donfig json file
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", required=True, help="Path to config file", dest="config")
args = parser.parse_args()
config = args.config

config = load_config(config)

dataset_path = config['dataset']
dataset_config = load_config(f'{dataset_path}config.json')

data = load_dataset_iscx(dataset_path=dataset_path, inputs=dataset_config['inputs'],
                         inputs_benign=dataset_config['inputs_benign'], headers=dataset_config['headers'])
quantity = get_quantity(data=data, columns=["rule_name", "sid"])

paths = get_file_paths(data=data)
if check_filters(config['filters'], dataset_config['filters']):
    all_data_filtered = data.copy()
    print(len(all_data_filtered))
    for filter in config['filters']:
        if filter['type'] == 'all_days':
            group_cols = dataset_config['filters'][filter['type']]['group_cols']
            stats = get_counts_days(data=data, group_cols=group_cols)
            col = stats[paths]
            stats = get_stats(stats, col)
            stats.reset_index(inplace=True)
            filtered_stats = filter_all_days_stats(stats, dataset_config['filters'][filter['type']])
            filter_list = filtered_stats['sid'].unique().tolist()
            # Filter data based on all days stats
            all_data_filtered = all_data_filtered[~all_data_filtered.set_index('sid').index.isin(filter_list)]

        elif filter['type'] == 'count_hours':
            if filter['group_cols'] not in dataset_config['filters'][filter['type']]['group_cols_options']:
                raise Exception('wrong input for group_cols option in filter options')
            group_cols = filter['group_cols']
            if filter['sub_mean'] is True:
                if filter['mean_from'] not in dataset_config['filters'][filter['type']]['from_mean_options']:
                    raise Exception('wrong input for mean_from option in filter options')
                if filter['mean_from'] == 'benign_days':
                    inputs = dataset_config['inputs_benign']
                else:
                    inputs = dataset_config['inputs']

                stats = get_counts_hours_sub_mean(data, group_cols=group_cols, inputs=inputs)
            else:
                stats = get_counts_hours(data=data, group_cols=group_cols)
            col = stats.loc[:, '0':'23']
            stats = get_stats(stats, col)
            stats.reset_index(inplace=True)
            filtered_stats = filter_perc_count(stats, dataset_config['filters'][filter['type']])
            filter_list = set(list(filtered_stats[group_cols[:-1]].itertuples(index=False, name=None)))
            all_data_filtered = all_data_filtered[~all_data_filtered.set_index(group_cols[:-1]).index.isin(filter_list)]

        print(len(all_data_filtered))

    # print(all_data_filtered.loc[(all_data_filtered['file_path'] == 'inputs/ET_alert_testbed-13jun.csv')])

    pocetnost_end = all_data_filtered[["rule_name", "sid"]].value_counts()
    # print(pocetnost_end)

    # sort filtered data according
    all_data_filtered = all_data_filtered.sort_values(by=['timestamp'])
    all_filtered_events__class = create_events(filtered_data=all_data_filtered)
    agg_events = aggregtion(all_filtered_events=all_filtered_events__class, delta=1800)
    print(len(agg_events))
    export_agg_data(agg_events=agg_events)
