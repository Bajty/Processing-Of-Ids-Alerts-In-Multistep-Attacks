# Processing of IDS alerts in multi-step attacks

In this information age, we notice an increase in the quality of security threats. Organizations are forced to defend
themselves against attacks in several steps. To identify the individual steps of attackers, we use several security
technologies, among which we can include attack detection systems. Researchers or members of security teams have to deal
with a large number of security events and alerts. A tool can help with this, which allows filtering relevant alerts and
combining them into larger units without significant loss of information. We designed software that covers preprocessing and aggregation phases and is composed of three parts:
- The first stage is the preprocessing of alerts. In this stage, alerts are prepared for the following stages.
- The second stage is the alert filtration. It selects a smaller portion of analyzed data to reduce the number of alerts passing to other stages of analyses.
- The third stage of the software flow involves consolidating the preprocessed alerts into aggregated alerts (aggregation stage).
The tool can process csv output from Snort IDS.

## Prerequisites

Ensure you have the following installed on your system:

- Python (==3.8.5)
- `pipenv`

### Steps
1. Clone repository
2. Navigate to the project directory:
   - `cd your-project`
3. Install dependencies using pipenv:
   - `pipenv install`
4. Activate the virtual environment:
   - `pipenv shell`
5. Run using python -c <config_file>.json


## Dataset configuration

In order to use this code, dataset need to be in specific folder organization. There are 3 required folder.

- inputs
- benign (can be empty, if we do not use filters based on benign days)
- classes

**Inputs and benign** folders store .csv files. Each csv file represents one day from snort IDS.

In **classes** folder is csv file, which defines class for SID. There are three required
columns: `sid, rule_name and stage`.

## How to run

In order to run we need to define run configuration. This is later set as input argument for python script like
this, `"python -u ./code/main.py -c ./code/config-DARPA_ET_1.json"`. We have defined  of these configuration file, for
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

## License

This project is licensed under the MIT - see the `code/LICENSE` file for details.

Data in this project are licensed under the Attribution (CC BY) - see the `data/LICENSE` file for details.

## Contact

- tomas.bajtos@upjs.sk
- frantisek.kurimsky@upjs.sk
