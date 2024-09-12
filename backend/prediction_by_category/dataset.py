import pandas as pd
import lightgbm as lgb
from backend.prediction_by_category.preprocess import calculate_features

def get_Lgb_dataset(X_train, Y_train, X_val, Y_val):
    lgbtrain = lgb.Dataset(data=X_train, label=Y_train, feature_name=list(X_train.columns), free_raw_data=False, categorical_feature='')
    lgbval = lgb.Dataset(data=X_val, label=Y_val, reference=lgbtrain, feature_name=list(X_val.columns), free_raw_data=False) if X_val is not None else None
    return lgbtrain, lgbval

def split_and_generate_features(data, params, target_column='Y', val_size=0.2):

    data = calculate_features(data, params)
    splitting_date = data.date.min() + (1-val_size)*(data.date.max() - data.date.min())

    train = data.loc[(data["date"] < splitting_date), :]
    val = data.loc[(data["date"] >= splitting_date) & (data["date"] < data.date.max()), :]

    today = val.iloc[-1]
    val = val.iloc[:-1]

    cols = [col for col in train.columns if col not in ['date', target_column]]

    X_train = train[cols]
    Y_train = train[target_column]
    X_val = val[cols]
    Y_val = val[target_column]

    today = today[cols]

    lgbtrain, lgbval = get_Lgb_dataset(X_train, Y_train, X_val, Y_val)
    
    return X_train, Y_train, X_val, Y_val, lgbtrain, lgbval, today

class LGBMDataset:
    def __init__(self, data, params):
        self.data = data
        self.X_train, self.Y_train, self.X_val, self.Y_val, self.lgbtrain, self.lgbval, self.today = split_and_generate_features(data, params)

    def __getitem__(self, index):
        if index < len(self.X_train):
            return self.X_train.iloc[index], self.Y_train.iloc[index]
        raise IndexError("Index out of range")

    def __len__(self):
        return len(self.X_train)
