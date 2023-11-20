# Processing of IDS alerts in multi-step attacks

In this information age, we notice an increase in the quality of security threats. Organizations are forced to defend
themselves against attacks in several steps. To identify the individual steps of attackers, we use several security
technologies, among which we can include attack detection systems. Researchers or members of security teams have to deal
with a large number of security events and alerts. A tool can help with this, which allows filtering relevant alerts and
combining them into larger units without significant loss of information.

## Dataset configuration

Configuration of dataset is defined inside json file, which is located in `"<name of dataset>/config.json"`.
Inside this json are required and optional fields:
<details>
<summary>REQUIRED FIELDS</summary>

- `inputs` - defines list of paths to benign days in csv format, inputs are in csv format, each csv file represents one
  day from snort IDS.
- `classes` - this parameter defines path to classes in csv format, where are columns sid, rule_name and stage.
- `headers` - names of columns for input files
- `filters` - filter which can be executed on dataset, options are

    - ```
      "all_days": {
        "perc_diff_min": 0.0,
        "perc_diff_max": 2.0,
        "count_min": 0,
        "group_cols": [
          "sid",
          "rule_name",
          "file_path"
          ]
      },

    - ```
      "count_hours": {
        "perc_diff_min": 0.0,
        "perc_diff_max": 2.0,
        "count_min": 0,
        "count_max": 24,
        "group_cols_options": [
          [
            "file_path",
            "sid",
            "from_addr",
            "hour"
          ],
          [
            "file_path",
            "sid",
            "to_addr",
            "hour"
          ]
        ],
        "sub_mean_options": [
          true,
          false
        ],
        "from_mean_options": [
          "all_days",
          "benign_days"
        ]
      }

</details>
<details>
<summary>OPTIONAL FIELDS</summary>

- `timedelta` - defines how much datetime needs to be offset in order to have correct datetime values
- `timedelta_function` - there are only two options:
    - `"+"`
    - `"-"`
- `inputs_benign` - defines list of paths to benign days in csv format

</details>

## How to run

In order to run we need to define run configuration. This is later set as input argument for python script like
this, `"python -u ./code/main.py -c ./code/config-DARPA_ET_1.json"`. We have defined 9 of these configuration file, for
each dataset, and run script is inside `run` file.

#### Config run definition

<details>
<summary>REQUIRED FIELDS</summary>

- `dataset_path` - defines base path to dataset, for example `"data/DARPA_ET_1/"`
- `dataset_name` - defines name of dataset, for example `"DARPA_ET_1"`
- `agg_delta` - defines time window for aggregation over sliding time window aggregation
- `filters` - defines which filters are being used in current run. Parameters needs to fit the dataset config
  configuration. Can be set to `null`, if we do not want to run any filters. Example of all filters is below.

<details>
<summary>EXAMPLE OF FILTERS</summary>

```
"filters": [
    {
      "type": "all_days",
      "perc_diff": 0.2,
      "count": 6
    },
    {
      "type": "count_hours",
      "sub_mean": false,
      "perc_diff": 0.5,
      "count": 10,
      "group_cols": [
        "file_path",
        "sid",
        "from_addr",
        "hour"
      ]
    },
    {
      "type": "count_hours",
      "sub_mean": true,
      "mean_from": "benign_days",
      "perc_diff": 0.5,
      "count": 10,
      "group_cols": [
        "file_path",
        "sid",
        "from_addr",
        "hour"
      ]
    },
    {
      "type": "count_hours",
      "sub_mean": true,
      "mean_from": "all_days",
      "perc_diff": 0.5,
      "count": 10,
      "group_cols": [
        "file_path",
        "sid",
        "from_addr",
        "hour"
      ]
    },
    {
      "type": "count_hours",
      "sub_mean": false,
      "perc_diff": 0.5,
      "count": 10,
      "group_cols": [
        "file_path",
        "sid",
        "to_addr",
        "hour"
      ]
    },
    {
      "type": "count_hours",
      "sub_mean": true,
      "mean_from": "all_days",
      "perc_diff": 0.5,
      "count": 10,
      "group_cols": [
        "file_path",
        "sid",
        "to_addr",
        "hour"
      ]
    },
    {
      "type": "count_hours",
      "sub_mean": true,
      "mean_from": "benign_days",
      "perc_diff": 0.5,
      "count": 10,
      "group_cols": [
        "file_path",
        "sid",
        "to_addr",
        "hour"
      ]
    }
  ]
```
  
  
</details>
</details>
