import uvicorn

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import time
import re
import csv
from typing import List
from backend.app.analytics import *
from backend.app.prediction import *
from backend.merging_datasets.main import merging


# from backend.ML.dataset import LGBMDataset
# from backend.ML.model import LGBMModel


# file_path = 'merged_df.csv'
# dataset = LGBMDataset(file_path)

# model = LGBMModel()
# model.train(dataset.lgbtrain, dataset.lgbval)
# print("model trained")

# model.load_model("new_model.txt")
# print("model loaded")

# model.save_model("new_model.txt")
# print("model saved")

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000", 
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Load the model
# with open("app/churn_model.pkl", "rb") as f:
#     model = pickle.load(f)

skus = ["Один", "Два", "Три", "Четыре", "Пять", "Шесть", "Семь", "Восемь"]
clusters = ["Хлеб", "Мясная продукция", "Молочная продукция", "Детское питание"]

x1 = ['2013-10-04 22:23:00', '2013-10-05 22:23:00', '2013-10-06 22:23:00']
y1 = [1, 3, 6]
x2 = ['2013-10-06 22:23:00', '2013-10-07 22:23:00', '2013-10-08 22:23:00', '2013-10-09 22:23:00']
y2 = [6, 5, 3, 6]
title = 'Прогнозирование продаж товара X'
x_axis_title = 'Дата'
y_axis_title = 'Число продаж'
trace1_name = 'Реальные данные'
trace2_name = 'Прогноз'

def standart_plot(x1, y1, x2, y2, title, x_axis_title, y_axis_title, trace1_name='Trace 1', trace2_name='Trace 2'):
    return {
        'data': [
            {
                'x': x1,
                'y': y1,
                'type': 'scatter',
                'mode': 'lines+markers',
                'marker': {'color': '#000'},
                'name': trace1_name
            },
            {
                'x': x2,
                'y': y2,
                'type': 'scatter',
                'mode': 'lines+markers',
                'marker': {'color': '#cd78f0'},
                'name': trace2_name
            }
        ],
        'layout': {
            'width': 800,
            'height': 400,
            'title': title,
            'xaxis': {
                'title': x_axis_title #,
                #rangeslider': {
                #    'visible': True
                #}
            },
            'yaxis': {
                'title': y_axis_title
            },
            'legend': {
                'orientation': 'h',
                'yanchor': 'bottom',
                'y': -0.5,
                'xanchor': 'center',
                'x': 0.5
            }
        }
    }

# plots = [standart_plot(x1, y1, x2, y2, title, x_axis_title, y_axis_title, trace1_name, trace2_name)]

@app.post("/getSkus/")
async def getSku(files: List[UploadFile] = File(...), prediction_period: int = Form(...)):
    merged_df = fetch_merged_df(files)

    return {"message": "CSV файл успешно загружен! Получение продуктов"
     ,
    "skus" : sorted(merged_df['item_id'].unique())
    }

@app.post("/getClusters/")
async def getClusters():
    with open('categories.csv', encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=';')
        clusters = [item for sublist in reader for item in sublist]

    print(clusters)

    return {"message": "Получение категорий продуктов"
     ,
    "clusters" : sorted(clusters)
    }

@app.post("/prediction/")
async def prediction(files: List[UploadFile] = File(...), prediction_period: int = Form(...), choosed_sku: str = Form(...)):
    # df = read_data()
    # model.predict(df)
    # data = prepare_data_fo_plot_from_original_dataset()
    # predict = prepare_data_fo_plot_from_predict()
    # metrics = extract_metrics(predict)

    # for file in files:
    #     print(file.filename)
    
    # print("prediction period")
    # print(prediction_period)

    # print("length of prediction")
    # y = model.predict(dataset.X_val)
    # f = open('file.txt', 'w')
    # for y_i in y:
    #     f.write(str(y_i) + ' ')
    # f.close()
    #print(model.predict(dataset.X_val))

    # print("end predict")

    merged_df = fetch_merged_df(files)
    merged_df = merged_df.loc[merged_df['item_id'] == choosed_sku]
    # print(merged_df)
    # print(run_inference_on_sku(merged_df))
    
    return fetch_prediction(merged_df)


@app.post("/analytics/")
async def analytics(files: List[UploadFile] = File(...), prediction_period: int = Form(...), choosed_sku: str = Form(...)):
    merged_df = fetch_merged_df(files)
    merged_df = merged_df.loc[merged_df['item_id'] == choosed_sku]
    return fetch_analytics(merged_df)

@app.post("/clustering/")
async def clustering(choosed_cluster: str = Form()):
    time.sleep(3)

    return {"message": "CSV файл успешно загружен! Прогноз по категориям"
     ,
    }


def fetch_merged_df(files):
    shop_sales = fetch_file_by_fullmatch_filename_to_regex(files, r'shop_sales(?!.*(?:prices|dates)).*\.csv$')
    shop_sales_dates = fetch_file_by_fullmatch_filename_to_regex(files, r'shop_sales_dates\w*\.csv$')
    shop_sales_prices = fetch_file_by_fullmatch_filename_to_regex(files, r'shop_sales_prices\w*\.csv$')
    print(shop_sales, shop_sales_dates, shop_sales_prices)
    merged_df = merging(shop_sales.file, shop_sales_dates.file, shop_sales_prices.file)
    return merged_df


def fetch_file_by_fullmatch_filename_to_regex(files, regex):
    for file in files:
        if re.fullmatch(regex, file.filename):
            return file
    return None



# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
