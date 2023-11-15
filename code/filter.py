import pandas as pd
from constants import (
    PERC_DIFF_MIN,
    PERC_DIFF_MAX,
    COUNT_MIN,
    COUNT_MAX_HOURS
)
from tasks import (
    get_counts_days,
    get_stats,
    get_counts_hours_sub_mean,
    get_counts_hours
)


def filter_all_days_stats(data, conf):
    return data[((data['perc_diff'] < conf['perc_diff']) & (data['count'] >= conf['count']))]


def filter_perc_count(data, conf):
    cond_filter = data[((data['perc_diff'] < conf['perc_diff']) & (data['count'] >= conf['count']))]
    return pd.concat([data[(data['max'] == 0)], cond_filter])


def filter_all_days(data, all_data_filtered, filter, paths):
    if PERC_DIFF_MIN < filter['perc_diff'] < PERC_DIFF_MAX and \
            COUNT_MIN < filter['count'] <= len(paths) and \
            type(filter['count']) == int and type(filter['perc_diff']) == float:
        group_cols = ["sid", "rule_name", "file_path"]
        stats = get_counts_days(data=data, group_cols=group_cols)
        col = stats[paths]
        stats = get_stats(stats, col)
        stats.reset_index(inplace=True)
        filtered_stats = filter_all_days_stats(stats, filter)
        filter_list = filtered_stats['sid'].unique().tolist()
        # Filter data based on all days stats
        return all_data_filtered[~all_data_filtered.set_index('sid').index.isin(filter_list)]
    else:
        raise Exception('Wrong value for perc_dif and count')


def filter_count_hours(data, all_data_filtered, filter, benign, inputs):
    if PERC_DIFF_MIN < filter['perc_diff'] <= PERC_DIFF_MAX and \
            COUNT_MIN < filter['count'] <= COUNT_MAX_HOURS and \
            type(filter['count']) == int and type(filter['perc_diff']) == float:
        group_cols = ["file_path", "sid"] + [filter['addr']] + ["hour"]
        if filter['sub_mean'] is True:
            if filter['mean_from'] == 'benign_days':
                calculate_from = benign
            elif filter['mean_from'] == 'all_days':
                calculate_from = inputs + benign
            else:
                raise Exception('WRONG OPTION FOR mean_from')

            stats = get_counts_hours_sub_mean(data, group_cols=group_cols, inputs=calculate_from, paths=inputs + benign)
        elif filter['sub_mean'] is False:
            stats = get_counts_hours(data=data, group_cols=group_cols, paths=inputs + benign)
        else:
            raise Exception('WRONG OPTION FOR sub_mean')
        col = stats.loc[:, '0':'23']
        stats = get_stats(stats, col)
        stats.reset_index(inplace=True)
        filtered_stats = filter_perc_count(stats, filter)
        filter_list = set(list(filtered_stats[group_cols[:-1]].itertuples(index=False, name=None)))
        return all_data_filtered[
            ~all_data_filtered.set_index(group_cols[:-1]).index.isin(filter_list)]
    else:
        raise Exception('Wrong value for perc_dif and count')
