import uvicorn

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import time
from typing import List

from backend.ML.dataset import LGBMDataset
from backend.ML.model import LGBMModel


file_path = 'merged_df.csv'
dataset = LGBMDataset(file_path)

model = LGBMModel()
model.train(dataset.lgbtrain, dataset.lgbval)
print("model trained")

# model.load_model("new_model.txt")
# print("model loaded")

model.save_model("new_model.txt")
print("model saved")

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

@app.post("/getSkus/")
async def getSku(files: List[UploadFile] = File(...), prediction_period: int = Form(...)):

    return {"message": "CSV файл успешно загружен! Получение продуктов"
     ,
    "metrics": {
        "accuracy": 0.87,
        "recall": 0.7
    },
    "skus" : ["Один", "Два"]
    }

@app.post("/prediction/")
async def prediction(files: List[UploadFile] = File(...), prediction_period: int = Form(...)):
    # df = read_data()
    # model.predict(df)
    # data = prepare_data_fo_plot_from_original_dataset()
    # predict = prepare_data_fo_plot_from_predict()
    # metrics = extract_metrics(predict)
    for file in files:
        print(file)
    
    print("prediction period")
    print(prediction_period)

    print("length of prediction")
    y = model.predict(dataset.X_val)
    f = open('file.txt', 'w')
    for y_i in y:
        f.write(str(y_i) + ' ')
    f.close()
    #print(model.predict(dataset.X_val))

    print("end predict")

    x1 = ['2013-10-04 22:23:00', '2013-10-05 22:23:00', '2013-10-06 22:23:00']
    y1 = [1, 3, 6]
    x2 = ['2013-10-06 22:23:00', '2013-10-07 22:23:00', '2013-10-08 22:23:00', '2013-10-09 22:23:00']
    y2 = [6, 5, 3, 6]
    title = 'Предсказание продаж товара X'
    x_axis_title = 'Дата'
    y_axis_title = 'Число продаж'
    trace1_name = 'Реальные данные'
    trace2_name = 'Предсказанные данные'

    plots = [standart_plot(x1, y1, x2, y2, title, x_axis_title, y_axis_title, trace1_name, trace2_name)]

    time.sleep(3)
    return {"message": "CSV файл успешно загружен! Прогнозирование"
     , 
    "plots": plots,
    "metrics": {
        "accuracy": 0.87,
        "recall": 0.7
    },
    "skus" : ["Один", "Два"]
    }

@app.post("/analytics/")
async def analytics(files: List[UploadFile] = File(...), prediction_period: int = Form(...)):

    return {"message": "CSV файл успешно загружен! Аналитика"
     ,
    "metrics": {
        "accuracy": 0.87,
        "recall": 0.7
    },
    "skus" : ["Один", "Два"]
    }

@app.post("/clustering/")
async def clustering(files: List[UploadFile] = File(...), prediction_period: int = Form(...)):

    return {"message": "CSV файл успешно загружен! Кластеризация"
     ,
    "metrics": {
        "accuracy": 0.87,
        "recall": 0.7
    },
    "skus" : ["Один", "Два"]
    }


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
            }
        }
    }

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
    
