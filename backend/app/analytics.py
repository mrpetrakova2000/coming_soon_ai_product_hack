from backend.app.plots_lib import *

def fetch_analytics(data, data_all_sku):

    # # Группируем по item_id и вычисляем сумму cnt
    # sales_sum = data_all_sku.groupby('item_id')['cnt'].sum()

    # # Находим item_id с максимальной суммой
    # bestseller = sales_sum.idxmax()
    # max_sales = sales_sum.max()

    # Вычисляем выручку
    revenue = data_all_sku['cnt'] * data_all_sku['sell_price']
    data_all_sku['revenue'] = revenue

    # 1. Магазин с максимальными продажами за все время
    max_sales_store = data_all_sku.groupby('store_id')['cnt'].sum().idxmax()

    # 2. Магазин с максимальной выручкой за все время
    store_revenue = data_all_sku.groupby('store_id')['revenue'].sum()
    max_revenue_store = store_revenue.idxmax()
    max_revenue_value = store_revenue.max()

    # 3. Товар с максимальными продажами за все время
    max_sales_item = data_all_sku.groupby('item_id')['cnt'].sum().idxmax()

    # 4. Товар с максимальной выручкой за все время
    item_revenue = data_all_sku.groupby('item_id')['revenue'].sum()
    max_revenue_item = item_revenue.idxmax()
    max_item_revenue_value = item_revenue.max()

    # 5. Максимальная выручка за месяц
    max_monthly_revenue = data_all_sku.groupby(['year', 'month'])['revenue'].sum().max()

    # 6. Максимальная выручка за год и год
    max_yearly_revenue = data_all_sku.groupby('year')['revenue'].sum().max()
    max_year = int(data_all_sku.groupby('year')['revenue'].sum().idxmax())

    # 7. Максимальная выручка за день
    max_daily_revenue = data_all_sku.groupby('date')['revenue'].sum().max()
    max_daily_date = data_all_sku.groupby('date')['revenue'].sum().idxmax().date()

    # 8. Максимальная выручка в праздник
    holiday_revenue = data_all_sku[data_all_sku['event_name_1'] != 'Unknown']
    max_holiday_revenue = holiday_revenue.groupby('event_name_1')['revenue'].sum().max()
    max_holiday_name = holiday_revenue.groupby('event_name_1')['revenue'].sum().idxmax()

    # 9. Среднее количество продаж за год
    average_sales_per_year = data_all_sku.groupby('year')['cnt'].sum().mean()

    # 10. Среднее количество продаж за месяц
    average_sales_per_month = data_all_sku.groupby(['year', 'month'])['cnt'].sum().mean()

    # 11. Среднее количество продаж за день
    average_sales_per_day = data_all_sku.groupby(['date'])['cnt'].sum().mean()

    return {"message": "CSV файл успешно загружен! Аналитика"
     ,
    "plots": [plot_sales(data), plot_sales_speed_dynamics(data), 
        plot_sales_peaks_months_line(data_all_sku), plot_store_revenue_grid(data_all_sku), 
        plot_weekday_weekend_sales_by_month(data_all_sku), plot_sales_comparison(data),
        plot_sales_by_event(data)],
    "parameters": [
        { "Анализ продаж": { "Общая выручка": f"{revenue.sum():.2f}", 
                            "Магазин с максимальными продажами за все время": max_sales_store, 
                            "Магазин с максимальной выручкой за все время": f"{max_revenue_store} ({max_revenue_value:.2f})",
                            'Товар с максимальными продажами за все время': max_sales_item, 
                            "Товар с максимальной выручкой за все время": f"{max_revenue_item} ({max_item_revenue_value:.2f})"
        }},
        {"Анализ трендов": {
                            "Максимальная выручка за месяц": f"{max_monthly_revenue:.2f}", 
                            "Максимальная выручка за год": f"{max_yearly_revenue:.2f} ({max_year})",
                            "Максимальная выручка за день": f"{max_daily_revenue:.2f} ({max_daily_date})", 
                            "Максимальная выручка в праздник": f"{max_holiday_revenue:.2f} ({max_holiday_name})",
                            "Среднее количество продаж за год": f"{average_sales_per_year.mean():.2f}",
                            "Среднее количество продаж за месяц": f"{average_sales_per_month.mean():.2f}",
                            "Среднее количество продаж за день": f"{average_sales_per_day.mean():.2f}",
        }}
    ]
    }