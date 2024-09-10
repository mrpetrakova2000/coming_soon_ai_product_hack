import numpy as np

def random_noise(dataframe):
    return np.random.normal(scale=1.5, size=(len(dataframe),))

def lag_features(dataframe, lags):
    for lag in lags:
        dataframe = dataframe.copy()
        dataframe.loc[:,'cnt_lag_' + str(lag)] = dataframe.groupby(["store_id", "item_id"])['cnt'].transform(
            lambda x: x.shift(lag)) + random_noise(dataframe)
    return dataframe

def roll_mean_features(dataframe, windows):
    for window in windows:
        dataframe = dataframe.copy()
        dataframe.loc[:, 'cnt_roll_mean_' + str(window)] = dataframe.groupby(["store_id", "item_id"])['cnt'].transform(
            lambda x: x.shift(1).rolling(window=window, min_periods=10, win_type="triang").mean()) + random_noise(dataframe)
    return dataframe

def apply_feature_engineering(data, lags=[1, 2, 6, 7, 13, 14], windows=[30, 91]):
    data = lag_features(data, lags)
    data = roll_mean_features(data, windows)
    return data
