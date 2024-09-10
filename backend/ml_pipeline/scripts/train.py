import lightgbm as lgb
import pandas as pd

# # # remove during inference
# import os
# os.chdir('/mnt/c/Users/iurin/work/itmo-hackathon/coming_soon_ai_product_hack')

from backend.ml_pipeline.preprocess_for_inference import calculate_features_for_inference 
from backend.ml_pipeline.configs.feature_params import one_day_params

def train(data: pd.DataFrame):
    data_with_one_day_features = calculate_features_for_inference(data=data, params=one_day_params)
    data_with_one_day_features = data_with_one_day_features.drop(columns=['date'])
    data = data_with_one_day_features.copy()

    # shift target 
    data['Y'] = data['cnt'].shift(-1)
    data = data.dropna()

    # split the data into train and val
    train_size = int(len(data) * 0.8)
    train_data = data[:train_size]
    val_data = data[train_size:]

    # Separate data
    X_train = train_data.drop(columns=['Y'])
    Y_train = train_data['Y']
    X_val = val_data.drop(columns=['Y'])
    Y_val = val_data['Y']


    lgbtrain = lgb.Dataset(data=X_train, label=Y_train, feature_name=list(X_train.columns), free_raw_data=False, categorical_feature='')
    lgbval = lgb.Dataset(data=X_val, label=Y_val, reference=lgbtrain, feature_name=list(X_val.columns), free_raw_data=False) if X_val is not None else None


if __name__ == "__main__":
    data = pd.read_csv('C:\\Users\\iurin\\work\\itmo-hackathon\\coming_soon_ai_product_hack\\backend\\ML\\item_064.csv', parse_dates=['date'])
    data = data[['cnt', 'date']] # date column is useful for feature generation

    train(data)