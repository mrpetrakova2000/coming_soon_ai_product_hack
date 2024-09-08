import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
import warnings
from sklearn.preprocessing import LabelEncoder

warnings.filterwarnings('ignore')

# Feature Engineering Functions
def random_noise(dataframe):
    return np.random.normal(scale=1.5, size=(len(dataframe),))

def lag_features(dataframe, lags):
    for lag in lags:
        dataframe['cnt_lag_' + str(lag)] = dataframe.groupby(["store_id", "item_id"])['cnt'].transform(
            lambda x: x.shift(lag)) + random_noise(dataframe)
    return dataframe

def roll_mean_features(dataframe, windows):
    for window in windows:
        dataframe['cnt_roll_mean_' + str(window)] = dataframe.groupby(["store_id", "item_id"])['cnt'].                                                           transform(
            lambda x: x.shift(1).rolling(window=window, min_periods=10, win_type="triang").mean()) + random_noise(
            dataframe)
    return dataframe

# Metrics
def smape(preds, target):
    n = len(preds)
    masked_arr = ~((preds == 0) & (target == 0))
    preds, target = preds[masked_arr], target[masked_arr]
    num = np.abs(preds - target)
    denom = np.abs(preds) + np.abs(target)
    smape_val = (200 * np.sum(num / denom)) / n
    return smape_val

def lgbm_smape(preds, train_data):
    labels = train_data.get_label()
    smape_val = smape(preds, labels)
    return 'SMAPE', smape_val, False

class LGBMDataset:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path, parse_dates=['date'], index_col=0)
        self.preprocess()
        self.split_and_get_features()

    def preprocess(self):

        # Fill missing values and feature engineering
        self.data['sell_price'] = self.data['sell_price'].interpolate()
        self.data['quarter_of_year'] = self.data.date.dt.quarter
        self.data['week_of_year'] = self.data.date.dt.weekofyear
        self.data['day_of_year'] = self.data.date.dt.dayofyear
        self.data['day_of_month'] = self.data.date.dt.day
        self.data['day_of_week'] = self.data.date.dt.dayofweek
        self.data["is_wknd"] = self.data.date.dt.weekday // 4
        self.data['is_month_start'] = self.data.date.dt.is_month_start.astype(int)
        self.data['is_month_end'] = self.data.date.dt.is_month_end.astype(int)
        self.data.sort_values(by=['store_id', 'item_id', 'date'], axis=0, inplace=True)
        # One-hot encoding for categorical variables
        self.data = pd.get_dummies(self.data, columns=['event_name_1', 'event_type_1', 'event_name_2', 'event_type_2'])
        # Label encoding
        le = LabelEncoder()
        for col in ['store_id', 'item_id']:
            self.data[col] = le.fit_transform(self.data[col]) + 1

    def split(self, val_size=0.2):
        splitting_date = self.data.date.min() + (1-val_size)*(self.data.date.max() - self.data.date.min())
        train = self.data.loc[(self.data["date"] < splitting_date), :]
        val = self.data.loc[(self.data["date"] >= splitting_date) & (self.data["date"] < self.data.date.max()), :]
        self.train_data = train
        self.val_data = val
        return train, val

    def apply_feature_engineering(self, data, lags=[1, 2, 6, 7, 13, 14], windows=[30, 91]):
        # Applying all the feature engineering steps
        data = lag_features(data, lags)
        data = roll_mean_features(data, windows)
        return data
    
    def get_Lgb_dataset(self, X_train, Y_train, X_val, Y_val):
        lgbtrain = lgb.Dataset(data=X_train, label=Y_train, feature_name=list(X_train.columns), free_raw_data=False)
        if not all(X_val) == None:
            lgbval = lgb.Dataset(data=X_val, label=Y_val, reference=lgbtrain, feature_name=list(X_val.columns), free_raw_data=False)
        else:
            lgbval = None
        return lgbtrain, lgbval

    def split_and_get_features(self, target_column='cnt'):
        train, val = self.split()
        train = self.apply_feature_engineering(train)
        val = self.apply_feature_engineering(val)
        cols = [col for col in train.columns if col not in ['date', 'date_id', "year", target_column]]
        X_train = train[cols]
        Y_train = train[target_column]
        X_val = val[cols]
        Y_val = val[target_column]
        self.lgbtrain, self.lgbval = self.get_Lgb_dataset(X_train, Y_train, X_val, Y_val)    


# Model Class
class Model:
    def __init__(self, params=None):
        if params is None:
            self.params = {'num_leaves': 10,
              'learning_rate': 0.01,
              'feature_fraction': 0.8,
              'max_depth': 5,
              'verbose': 0,
              'num_boost_round': 1000,
              'early_stopping_rounds': 3,
              'nthread': -1}
        else:
            self.params = params
        

    def train(self, lgbtrain, lgbval):
        if lgbval is not None:
            self.model = lgb.train(params=self.params, train_set=lgbtrain,
                    callbacks=
        [lgb.early_stopping(stopping_rounds=3)],
                  valid_sets=[lgbval],
                  num_boost_round=1000,
                  feval=lgbm_smape,
                    )
        else:
            self.model = lgb.train(params=self.params, train_set=lgbtrain,
                  num_boost_round=100,
                  feval=lgbm_smape
                    )

    def predict(self, X):
        return self.model.predict(X, num_iteration=self.model.best_iteration)

    def save_model(self, file_name):
        self.model.save_model(file_name, num_iteration=self.model.best_iteration)

if __name__ = "__main__":
    dataset = Dataset('merged_df.csv')
    model = Model()
    model.train(dataset.lgbtrain, dataset.lgbval)
    model.save_model('trial.txt')
