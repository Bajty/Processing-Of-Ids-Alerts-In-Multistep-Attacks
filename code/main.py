# IMPORTS
import argparse

from tasks import (
    load_config,
    load_dataset_iscx,
    get_file_paths,
    get_stats,
    get_counts_days,
    get_counts_hours,
    get_counts_hours_sub_mean,
    check_filters,
    export_agg_data,
    export_filtered_data
)
from filter import (
    filter_all_days_stats,
    filter_perc_count
)
from aggregation import (
    create_events,
    aggregtion
)

# ARGPARSER for configuration file
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", required=True, help="Path to config file", dest="config")
args = parser.parse_args()
config = args.config

# LOAD defined configuration
config = load_config(config)
print(f"LOADING === config dataset {config['dataset_name']}")

# LOAD specs file for dataset
print(f"DEFINING headers, allowed filters, input files, input benign files for {config['dataset_name']}")
dataset_path = config['dataset_path']
dataset_config = load_config(f'{dataset_path}config.json')

# LOAD dataset
data = load_dataset_iscx(
    dataset_path=dataset_path, inputs=dataset_config['inputs'],
    inputs_benign=dataset_config['inputs_benign'] if 'inputs_benign' in dataset_config else [],
    headers=dataset_config['headers']
)

# DEFINE unique paths, file_path represents in dataset value for each row from which file is specific row loaded
# basically this is the same as inputs benign and inputs from defined dataset
paths = get_file_paths(data=data)

# CHECK if all filters are correctly defined for this run
if check_filters(config['filters'], dataset_config['filters']):

    all_data_filtered = data.copy()
    print(f"Number of loaded events: {len(all_data_filtered)}")

    # APPLY all defined filter from config file
    for index, filter in enumerate(config['filters'] if config['filters'] is not None else []):
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

        print(f"Number of events after {index} filter : {len(all_data_filtered)}")

    # sort filtered data according
    all_data_filtered = all_data_filtered.sort_values(by=['timestamp'])

    # EXPORT filtered events into json
    if config['filters'] is not None:
        export_filtered_data(all_data_filtered, name=config['dataset_name'])

    # CREATE classes for aggregation
    all_filtered_events__class = create_events(filtered_data=all_data_filtered)

    # RUN aggregation over moving window
    agg_events = aggregtion(all_filtered_events=all_filtered_events__class, delta=1800)
    print(f"Number of aggregated events: {len(agg_events)}")

    # EXPORT aggregated events into json
    export_agg_data(agg_events=agg_events, name=config['dataset_name'])
