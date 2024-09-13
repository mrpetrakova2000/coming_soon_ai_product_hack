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
from backend.app.cluster_prediction import *
from backend.merging_datasets.main import merging

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

@app.post("/getSkus/")
async def getSku(files: List[UploadFile] = File(...), prediction_period: int = Form(...)):
    merged_df = fetch_merged_df(files)

    return {"message": "CSV файл успешно загружен! Получение продуктов"
     ,
    "skus" : sorted(merged_df['item_id'].unique())
    }

@app.post("/getClusters/")
async def getClusters():
    with open('backend/app/categories.csv', encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=';')
        clusters = [item for sublist in reader for item in sublist]

    return {"message": "Получение категорий продуктов"
     ,
    "clusters" : sorted(clusters)
    }

@app.post("/prediction/")
async def prediction(files: List[UploadFile] = File(...), prediction_period: int = Form(...), choosed_sku: str = Form(...)):

    merged_df = fetch_merged_df(files)
    merged_df = merged_df.loc[merged_df['item_id'] == choosed_sku]
    
    return fetch_prediction(merged_df)


@app.post("/analytics/")
async def analytics(files: List[UploadFile] = File(...), prediction_period: int = Form(...), choosed_sku: str = Form(...)):
    merged_df = fetch_merged_df(files)
    merged_df_sku = merged_df.loc[merged_df['item_id'] == choosed_sku]
    return fetch_analytics(merged_df_sku, merged_df)

@app.post("/clustering/")
async def clustering(choosed_cluster: str = Form()):
    return fetch_cluster_prediction(choosed_cluster)


def fetch_merged_df(files):
    shop_sales = fetch_file_by_fullmatch_filename_to_regex(files, r'shop_sales(?!.*(?:prices|dates)).*\.csv$')
    shop_sales_dates = fetch_file_by_fullmatch_filename_to_regex(files, r'shop_sales_dates\w*\.csv$')
    shop_sales_prices = fetch_file_by_fullmatch_filename_to_regex(files, r'shop_sales_prices\w*\.csv$')

    merged_df = merging(shop_sales.file, shop_sales_dates.file, shop_sales_prices.file)
    return merged_df


def fetch_file_by_fullmatch_filename_to_regex(files, regex):
    for file in files:
        if re.fullmatch(regex, file.filename):
            return file
    return None



# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
