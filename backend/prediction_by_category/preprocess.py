import pandas as pd

from backend.ml_pipeline.feature_engineering_tools import *

def calculate_features(data: pd.DataFrame, params: dict, train: bool = True) -> pd.DataFrame:
    # import parameters
    target_column = params.get('target_column')
    datetime_column = params.get('datetime_column', None)
    lag_range = params.get('lag_range', None)
    lag_difference = params.get('lag_difference', None)
    rolling_mean_range = params.get('rolling_mean_range', None)
    rolling_std_range = params.get('rolling_std_range', None)
    shift = params.get('shift')

    # self check
    data[datetime_column] = pd.to_datetime(data[datetime_column], errors='coerce')

    # feature preprocessing
    data = apply_rolling_mean_range(data, rolling_mean_range, target_column) if rolling_mean_range else data
    data = apply_rolling_std_range(data, rolling_std_range, target_column) if rolling_std_range else data
    data = apply_lag_by_day_range(data, lag_range, target_column) if lag_range else data
    data = apply_lag_difference_range(data, lag_difference, target_column) if lag_difference else data
    data = extract_day_of_week(data, datetime_column) if params.get('day_of_week') else data
    data = extract_month(data, datetime_column) if params.get('month') else data
    data = extract_hour(data, datetime_column) if params.get('hour') else data
    
    if train:
        data = data.copy()
        data.loc[:, 'Y'] = data[target_column].shift(shift)

    data = data.dropna()

    return data
    