from backend.app.plots_lib import *
from backend.ml_pipeline.run import run_inference_on_sku

def fetch_prediction(data):
    last_n_days, prediction_data = run_inference_on_sku(data)
    return {"message": "CSV файл успешно загружен! Прогнозирование"
     , 
    "plots": [plot_sku_prediction(last_n_days, prediction_data)]
    }
    

