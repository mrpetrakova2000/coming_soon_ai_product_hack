import pandas as pd
from backend.prediction_by_category.feature_params import one_day_params, seven_day_params, thirty_day_params
import os
from backend.prediction_by_category.dataset import LGBMDataset
from backend.ml_pipeline.model import LGBMModel
from datetime import datetime, timedelta

def predict_by_category(category):

    base_path = 'backend/prediction_by_category/data_categories/'
    
    data = pd.read_csv(base_path + f'data_{category}.csv', index_col=0)
    preds = {}
    
    for day, params in zip(['one_day', 'seven_days', 'thirty_days'], [one_day_params, seven_day_params, thirty_day_params]):
        model = LGBMModel()
        dataset = LGBMDataset(data, params)
        model.train(dataset.lgbtrain, dataset.lgbval)
        preds[day] = model.predict(dataset.today.values.reshape(1, -1))
    
    prev_data = dataset.data[['date', 'cnt']]

    today_date = dataset.data.iloc[-1].date.to_pydatetime()

    one_day_pred = pd.DataFrame({
        'date': [today_date + timedelta(days=1)],
        'cnt': [preds['one_day'][0]]
    })
    seven_days_pred = pd.DataFrame({
        'date': [today_date + timedelta(days=7)],
        'cnt': [preds['seven_days'][0]]
    })
    thirty_days_pred = pd.DataFrame({
        'date': [today_date + timedelta(days=30)],
        'cnt': [preds['thirty_days'][0]]
    })
    return prev_data, one_day_pred, seven_days_pred, thirty_days_pred

prev_data, one_day_pred, seven_days_pred, thirty_days_pred = predict_by_category('Красота')
