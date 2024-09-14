from backend.app.plots_lib import *
from backend.prediction_by_category.train_and_predict import *
from backend.ml_pipeline.analyze_data_with_chatgpt import send_dataframe_to_chatgpt
from backend.prediction_by_category.new_product_launch.return_the_launch_period import launch_plot

import os
key = os.getenv('API_KEY', None)
print("API_KEY " + str(key))

def fetch_cluster_prediction(data):
    prev_data, one_day_pred, seven_days_pred, thirty_days_pred = predict_by_category(data)
    #print(prev_data, one_day_pred, seven_days_pred, thirty_days_pred)
    chat_gpt_msg = None
    if key != None:
        try:
            chat_gpt_msg = send_dataframe_to_chatgpt(data)
        except Exception as e:
            print(e)
    # print(chat_gpt_msg)

    return {"message": "CSV файл успешно загружен! Прогнозирование по категории"
     , 
    "plots": [plot_cluster_prediction(prev_data, one_day_pred, seven_days_pred, thirty_days_pred),
            plot_cluster_launch(launch_plot(data))
    ]
    ,
    "chatgpt": chat_gpt_msg
    }
    

