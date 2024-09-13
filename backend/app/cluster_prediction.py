from backend.app.plots_lib import *
from backend.prediction_by_category.train_and_predict import *

def fetch_cluster_prediction(data):
    prev_data, one_day_pred, seven_days_pred, thirty_days_pred = predict_by_category(data)
    #print(prev_data, one_day_pred, seven_days_pred, thirty_days_pred)
    return {"message": "CSV файл успешно загружен! Прогнозирование по категории"
     , 
    "plots": [plot_cluster_prediction(prev_data, one_day_pred, seven_days_pred, thirty_days_pred)]
    }
    

