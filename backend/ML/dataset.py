import pandas as pd
import lightgbm as lgb
from data_preparation import preprocess, split
from feature_engineering import apply_feature_engineering

def get_Lgb_dataset(X_train, Y_train, X_val, Y_val):
    lgbtrain = lgb.Dataset(data=X_train, label=Y_train, feature_name=list(X_train.columns), free_raw_data=False, categorical_feature='')
    lgbval = lgb.Dataset(data=X_val, label=Y_val, reference=lgbtrain, feature_name=list(X_val.columns), free_raw_data=False) if X_val is not None else None
    return lgbtrain, lgbval

def split_and_get_features(data, target_column='cnt'):
    train, val = split(data)
    train = apply_feature_engineering(train)
    val = apply_feature_engineering(val)
    cols = [col for col in train.columns if col not in ['date', 'date_id', "year", target_column]]
    X_train = train[cols]
    Y_train = train[target_column]
    X_val = val[cols]
    Y_val = val[target_column]
    lgbtrain, lgbval = get_Lgb_dataset(X_train, Y_train, X_val, Y_val)
    return X_train, Y_train, X_val, Y_val, lgbtrain, lgbval

class LGBMDataset:
    def __init__(self, data):
        self.data = data
        self.data = preprocess(self.data)
        self.X_train, self.Y_train, self.X_val, self.Y_val, self.lgbtrain, self.lgbval = split_and_get_features(self.data)

    def __getitem__(self, index):
        if index < len(self.X_train):
            return self.X_train.iloc[index], self.Y_train.iloc[index]
        raise IndexError("Index out of range")

    def __len__(self):
        return len(self.X_train)
