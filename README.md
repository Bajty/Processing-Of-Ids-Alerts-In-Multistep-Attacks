# Processing of IDS alerts in multi-step attacks

In this information age, we notice an increase in the quality of security threats. Organizations are forced to defend
themselves against attacks in several steps. To identify the individual steps of attackers, we use several security
technologies, among which we can include attack detection systems. Researchers or members of security teams have to deal
with a large number of security events and alerts. A tool can help with this, which allows filtering relevant alerts and
combining them into larger units without significant loss of information.

## Dataset configuration

In order to use this code, dataset need to be in specific folder organization. There are 3 required folder.

- inputs
- benign (can be empty, if we do not use filters based on benign days)
- classes

**Inputs and benign** folders store .csv files. Each csv file needs to represent one day from snort IDS.

In **classes** folder is csv file, which defines class for each SID. There are three required
columns: `sid, rule_name and stage`.

## How to run

In order to run we need to define run configuration. This is later set as input argument for python script like
this, `"python -u ./code/main.py -c ./code/config-DARPA_ET_1.json"`. We have defined 9 of these configuration file, for
each dataset, and run script is inside `run` file.

### Config run definition

We need to specify config json for the dataset. In json there are required fields.

- `dataset_path` - defines base path to dataset, for example `"data/DARPA_ET_1/"`
- `dataset_name` - defines name of dataset, for example `"DARPA_ET_1"`
- `agg_delta` - defines time window for aggregation over sliding time window aggregation
- `timedelta`: defines how much we need to change time for correct timezone, for example "05:00:00"
- `timedelta_function`: defines if we use plus or minus, possible values are "+" or "-"
- `filters` - defines list of filter, which are being used in current run. Can be set to `null`, if we do not want to
  run any filters. Example of all filters is below.

<details>
<summary>ALL FILTERS</summary>

  ```
    {
      "type": "all_days",
      "perc_diff": 0.2,
      "count": 2
    }
  ``` 

  ```
    {
      "type": "count_hours",
      "sub_mean": false,
      "perc_diff": 0.5,
      "count": 10,
      "addr": "from_addr"
    }
  ```

  ```
    {
      "type": "count_hours",
      "sub_mean": true,
      "mean_from": "benign_days",
      "perc_diff": 0.5,
      "count": 10,
      "addr": "from_addr"
    }
  ```

  ```
    {
      "type": "count_hours",
      "sub_mean": true,
      "mean_from": "all_days",
      "perc_diff": 0.5,
      "count": 10,
      "addr": "from_addr"
    }
  ```

  ```
    {
      "type": "count_hours",
      "sub_mean": false,
      "perc_diff": 0.5,
      "count": 10,
      "addr": "to_addr"
    }
  ```

  ```
    {
      "type": "count_hours",
      "sub_mean": true,
      "mean_from": "all_days",
      "perc_diff": 0.5,
      "count": 10,
      "addr": "to_addr"
    }
  ```

  ```
    {
      "type": "count_hours",
      "sub_mean": true,
      "mean_from": "benign_days",
      "perc_diff": 0.5,
      "count": 10,
      "addr": "to_addr"
    }
  ```

</details>