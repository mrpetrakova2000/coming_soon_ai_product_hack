from backend.app.plots_lib import *

def fetch_analytics(data):
    return {"message": "CSV файл успешно загружен! Аналитика"
     ,
    "plots": [plot_sales(data)],
    "parameters": [
        { "Анализ продаж": { "кол-во проданных товаров": 10, "выручка": 11 } },
        { "Анализ трендов": { "среднее кол-во проданных товаров за месяц": 2 } }
    ]
    }