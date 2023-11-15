import pandas as pd
import numpy as np


def filter_all_days_stats(data, conf):
    return data[((data['perc_diff'] < conf['perc_diff']) & (data['count'] >= conf['count']))]


def filter_perc_count(data, conf):
    cond_filter = data[((data['perc_diff'] < conf['perc_diff']) & (data['count'] >= conf['count']))]
    return pd.concat([data[(data['max'] == 0)], cond_filter])
