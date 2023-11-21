# IMPORTS
import argparse
import os
from tasks import (
    load_config,
    load_dataset,
    export_agg_data,
    export_filtered_data,
    load_classes
)
from filter import (
    filter_all_days,
    filter_count_hours
)
from aggregation import (
    create_events,
    aggregtion
)
from constants import (
    INPUTS_PATH,
    BENIGN_INPUTS,
    CLASSES
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
DATASET_INPUT_FILES = [INPUTS_PATH + x for x in os.listdir(f'{dataset_path}{INPUTS_PATH}')]
DATASET_BENIGN_FILES = [BENIGN_INPUTS + x for x in os.listdir(f'{dataset_path}{BENIGN_INPUTS}')]
DATASET_CLASSES = [CLASSES + x for x in os.listdir(f'{dataset_path}{CLASSES}')]

# LOAD dataset
data = load_dataset(
    dataset_path=dataset_path,
    inputs=DATASET_INPUT_FILES,
    inputs_benign=DATASET_BENIGN_FILES,
    timedelta=config['timedelta'] if 'timedelta' in config else False,
    timedelta_function=config['timedelta_function'] if 'timedelta_function' in config else '-'
)

all_data_filtered = data.copy()
print(f"Number of loaded events: {len(all_data_filtered)}")

# APPLY all defined filter from config file
for index, filter in enumerate(config['filters'] if config['filters'] is not None else []):
    if filter['type'] == 'all_days':
        all_data_filtered = filter_all_days(data, all_data_filtered, filter,
                                            paths=DATASET_INPUT_FILES + DATASET_BENIGN_FILES)
    elif filter['type'] == 'count_hours':
        all_data_filtered = filter_count_hours(data, all_data_filtered, filter, benign=DATASET_BENIGN_FILES,
                                               inputs=DATASET_INPUT_FILES)

    print(f"Number of events after {index} filter : {len(all_data_filtered)}")

# sort filtered data according
all_data_filtered = all_data_filtered.sort_values(by=['datetime'])

# EXPORT filtered events into json
if config['filters'] is not None:
    export_filtered_data(all_data_filtered, name=config['dataset_name'])

# CREATE classes for aggregation
all_filtered_events__class = create_events(filtered_data=all_data_filtered)

# RUN aggregation over moving window
classes = load_classes(dataset_path=dataset_path, path=DATASET_CLASSES[0])
agg_events = aggregtion(all_filtered_events=all_filtered_events__class, delta=config['agg_delta'], classes=classes)
print(f"Number of aggregated events: {len(agg_events)}")

# EXPORT aggregated events into json
export_agg_data(agg_events=agg_events, name=config['dataset_name'])
