import pandas as pd
import numpy as np


def filter_all_days_stats(data, conf):
    if 'perc_diff' not in conf:
        raise Exception('define perc_diff value for filter in conf file under filter.all_days')
    if conf['perc_diff'] is None:
        raise Exception('define perc_diff value for filter in conf file under filter.all_days')
    if 'count' not in conf:
        raise Exception('define count value for filter in conf file under filter.all_days')
    if conf['count'] is None:
        raise Exception('define count value for filter in conf file under filter.all_days')

    return data[((data['perc_diff'] < conf['perc_diff']) & (data['count'] >= conf['count']))]


def filter_perc_count(data, conf):
    if 'perc_diff' not in conf:
        raise Exception('define perc_diff value for filter in conf file under filter.all_days')
    if conf['perc_diff'] is None:
        raise Exception('define perc_diff value for filter in conf file under filter.all_days')
    if 'count' not in conf:
        raise Exception('define count value for filter in conf file under filter.all_days')
    if conf['count'] is None:
        raise Exception('define count value for filter in conf file under filter.all_days')
    if 'max' not in conf:
        raise Exception('define max value for filter in conf file under filter.all_days')
    if conf['max'] is None:
        raise Exception('define max value for filter in conf file under filter.all_days')

    asdf = data[((data['perc_diff'] < conf['perc_diff']) & (data['count'] >= conf['count']))]
    return pd.concat([data[(data['max'] == conf['max'])], asdf])
