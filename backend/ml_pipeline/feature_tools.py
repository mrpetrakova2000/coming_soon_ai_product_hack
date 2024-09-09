import pandas as pd

# +----------------------------+
# |           Lag              |
# +----------------------------+

def apply_lag_by_day(data: pd.DataFrame, day: int, target_column: str):
    """This function applies a lag by a specified number of days to the target column in the dataset"""
    lag_column_name = f'lag_{day}'
    data[lag_column_name] = data[target_column].shift(day)
    return data

def apply_lag_by_day_range(data: pd.DataFrame, lag_range: tuple, target_columns: str):
    for i in range(lag_range[0], lag_range[1] + 1):
        data = apply_lag_by_day(data, i, target_columns)
    return data



# +----------------------------+
# |        Rolling Mean        |
# +----------------------------+


def apply_rolling_mean(data: pd.DataFrame, window: int, target_column: str):
    """This function applies a rolling mean with a specified window size to the target column in the dataset"""
    rolling_column_name = f'rolling_mean_{window}'
    data[rolling_column_name] = data[target_column].rolling(window=window).mean()
    return data

def apply_rolling_mean_range(data: pd.DataFrame, window_range: tuple, target_column: str):
    for window in range(window_range[0], window_range[1] + 1):
        data = apply_rolling_mean(data, window, target_column)
    return data


# +----------------------------+
# |        Rolling Std         |
# +----------------------------+


def apply_rolling_std(data: pd.DataFrame, window: int, target_column: str):
    """This function applies a rolling standard deviation with a specified window size to the target column."""
    rolling_std_column_name = f'rolling_std_{window}'
    data[rolling_std_column_name] = data[target_column].rolling(window=window).std()
    return data

def apply_rolling_std_range(data: pd.DataFrame, window_range: tuple, target_column: str):
    for window in range(window_range[0], window_range[1] + 1):
        data = apply_rolling_std(data, window, target_column)
    return data

# +----------------------------+
# |        Lag Diff            |
# +----------------------------+


def apply_lag_difference(data: pd.DataFrame, day: int, target_column: str):
    """This function calculates the difference between a value and its lag (i.e., the first difference)."""
    lag_diff_column_name = f'lag_diff_{day}'
    data[lag_diff_column_name] = data[target_column] - data[target_column].shift(day)
    return data

def apply_lag_difference_range(data: pd.DataFrame, window_range: tuple, target_column: str):
    for window in range(window_range[0], window_range[1] + 1):
        data = apply_lag_difference(data, window, target_column)
    return data


# +----------------------------+
# |        Time Features       |
# +----------------------------+


def extract_day_of_week(data: pd.DataFrame, datetime_column: str):
    data['day_of_week'] = data[datetime_column].dt.dayofweek
    return data


def extract_month(data: pd.DataFrame, datetime_column: str):
    data['month'] = data[datetime_column].dt.month
    return data


def extract_hour(data: pd.DataFrame, datetime_column: str):
    data['hour'] = data[datetime_column].dt.hour
    return data