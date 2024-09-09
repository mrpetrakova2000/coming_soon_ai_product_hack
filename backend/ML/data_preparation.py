import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocess(data):
    data['sell_price'] = data['sell_price'].interpolate()
    data['quarter_of_year'] = data.date.dt.quarter
    data['week_of_year'] = data.date.dt.isocalendar().week
    data['day_of_year'] = data.date.dt.dayofyear
    data['day_of_month'] = data.date.dt.day
    data['day_of_week'] = data.date.dt.dayofweek
    data["is_wknd"] = data.date.dt.weekday // 4
    data['is_month_start'] = data.date.dt.is_month_start.astype(int)
    data['is_month_end'] = data.date.dt.is_month_end.astype(int)
    data.sort_values(by=['store_id', 'item_id', 'date'], axis=0, inplace=True)
    data = pd.get_dummies(data, columns=['event_name_1', 'event_type_1', 'event_name_2', 'event_type_2'])
    le = LabelEncoder()
    for col in ['store_id', 'item_id']:
        data[col] = le.fit_transform(data[col]) + 1
    return data