import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import plotly.io as pio
import math

from plotly.subplots import make_subplots
from matplotlib.widgets import Slider

data = pd.read_csv('merged_df.csv')

#######################################################
## 5. Пики продаж (день)
#######################################################

# Функция для пайплайна обработки данных

def sales_pipeline(dates_list, sales_list):
    data = pd.DataFrame({'Date': dates_list, 'Sales': sales_list})
    data['Date'] = pd.to_datetime(data['Date'])  # Преобразуем дату в формат datetime
    data.set_index('Date', inplace=True)
    return data

##################### 5.1 Пики продаж (день) с указанием месяца и года ######################

# Преобразование колонок 'date' и 'cnt' в списки
dates_list = data['date'].tolist()  # Преобразуем даты в список
sales_list = data['cnt'].tolist()   # Преобразуем количество продаж в список


def plot_sales_peaks_plotly(year, month, sales_data):
    # Фильтруем данные по выбранному году и месяцу
    filtered_data = sales_data[(sales_data.index.year == year) & (sales_data.index.month == month)]

    if filtered_data.empty:
        print(f"Нет данных для {year}-{month}.")
        return

    # Группируем данные по дням и считаем количество продаж
    daily_sales = filtered_data.groupby(filtered_data.index.day).sum()

    # Строим график
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=daily_sales.index,
        y=daily_sales['Sales'],
        mode='lines+markers',
        line=dict(color='green'),
        marker=dict(size=8),
        name="Количество продаж"
    ))

    # Настраиваем оформление графика
    fig.update_layout(
        title=f"Пики продаж по дням ({year}-{month})",
        xaxis_title="День",
        yaxis_title="Количество продаж",
        template='plotly_white',
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGrey'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGrey'),
        font=dict(size=14, color='Black'),
        height=600,
        width=900
    )

    # Отображаем график
    pio.show(fig)

# Запрашиваем у пользователя год и месяц
year = 2013
month = 3

processed_data = sales_pipeline(dates_list, sales_list)

plot_sales_peaks_plotly(year, month, processed_data)


##################### 5.2 Пики продаж (день) с наложением ######################

# Преобразование колонок 'date' и 'cnt' в списки
dates_list = data['date'].tolist()  # Преобразуем даты в список
sales_list = data['cnt'].tolist()   # Преобразуем количество продаж в список

def plot_sales_peaks_overlay_filled(year, months, sales_data):
    fig = go.Figure()

    # Используем цвета для линий
    colors = ['#FF6347', '#4682B4', '#3CB371']  # Цвета для трех месяцев

    # Проходим по каждому месяцу
    for i, month in enumerate(months):
        # Фильтруем данные по выбранному году и месяцу
        filtered_data = sales_data[(sales_data.index.year == year) & (sales_data.index.month == month)]

        if filtered_data.empty:
            print(f"Нет данных для {year}-{month}. Пропускаем...")
            continue

        # Группируем данные по дням и считаем количество продаж
        daily_sales = filtered_data.groupby(filtered_data.index.day).sum()

        # Строим график с линиями и заполнением под ними
        fig.add_trace(go.Scatter(
            x=daily_sales.index,
            y=daily_sales['Sales'],
            mode='lines+markers',
            line=dict(color=colors[i], width=2.5),
            fill='tozeroy',  # Заполняем пространство под линией
            name=f"{month} месяц"
        ))

    # Настраиваем оформление графика
    fig.update_layout(
        title=f"Наложение пиков продаж по дням с заполнением ({year})",
        xaxis_title="День",
        yaxis_title="Количество продаж",
        template='plotly_white',
        showlegend=True,
        width=900,
        height=600,
        font=dict(size=14, color="Black")
    )

    fig.show()

# Запрашиваем год и месяцы для наложения
year = 2015
months = [9, 10, 11]  # Сентябрь, октябрь и ноябрь

# Пропускаем данные через пайплайн
processed_data = sales_pipeline(dates_list, sales_list)

# Построение графика с наложением выбранных месяцев и заполнением
plot_sales_peaks_overlay_filled(year, months, processed_data)

#######################################################
## 6. График частоты повторных покупок
#######################################################

# Пайплайн для обработки данных
def repeat_purchase_pipeline(dates, sales):
    sales_by_date = pd.DataFrame({'Date': dates, 'Sales': sales}).groupby('Date').sum()
    repeat_rate = sales_by_date.rolling(window=7).mean()  # Скользящее среднее за 7 дней
    return sales_by_date.index, repeat_rate

##################### 6.1 Линейный график частоты повторных покупок ######################

# Преобразование колонок 'date' и 'cnt' в списки
dates_list = data['date'].tolist()  # Преобразуем даты в список
sales_list = data['cnt'].tolist()   # Преобразуем количество продаж в список

# Функция для построения графика
def plot_repeat_purchase_plotly(dates, repeat_rate):
    fig = go.Figure()

    # Добавляем линию и маркеры
    fig.add_trace(go.Scatter(
        x=dates,
        y=repeat_rate['Sales'],
        mode='lines+markers',
        line=dict(color='blue'),
        marker=dict(size=6, color='blue'),
        name='Частота покупок'
    ))

    # Настройка оформления графика
    fig.update_layout(
        title="Частота повторных покупок (скользящее среднее за 7 дней)",
        xaxis_title="Дата",
        yaxis_title="Частота покупок (среднее количество)",
        template='plotly_white',
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGrey'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGrey'),
        font=dict(size=14, color='Black'),
        height=600,
        width=900
    )

    fig.show()

processed_dates, repeat_rate = repeat_purchase_pipeline(dates_list, sales_list)

plot_repeat_purchase_plotly(processed_dates, repeat_rate)

##################### 6.2 Гистограмма частоты покупок ######################

# Преобразование колонок 'date' и 'cnt' в списки
dates_list = data['date'].tolist()  # Преобразуем даты в список
sales_list = data['cnt'].tolist()   # Преобразуем количество продаж в список

# Функция для построения гистограммы
def plot_histogram_plotly(sales_list):
    fig = go.Figure()

    # Добавляем гистограмму
    fig.add_trace(go.Histogram(
        x=sales_list,
        nbinsx=20,
        marker_color='green',
        opacity=0.7,
        marker_line=dict(color='black', width=1)
    ))

    # Настройка оформления графика
    fig.update_layout(
        title="Распределение частоты покупок (как часто покупают определённое количество товаров)",
        xaxis_title="Количество покупок",
        yaxis_title="Частота",
        template='plotly_white',
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGrey'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGrey'),
        font=dict(size=14, color='Black'),
        height=600,
        width=900
    )

    fig.show()

processed_dates, repeat_rate = repeat_purchase_pipeline(dates_list, sales_list)

plot_histogram_plotly(sales_list)

#######################################################
##  7. Востребованность продукта
#######################################################
import math


# Пайплайн для обработки данных
def product_sales_pipeline(data):
    """
    Пайплайн для обработки данных: подсчёт продаж каждого продукта и выбор топ 5 и bottom 5.
    """
    # Сгруппируем данные по продуктам и посчитаем общее количество продаж
    grouped_data = data.groupby('item_id')['cnt'].sum().reset_index()

    # Отсортируем данные для получения топ 5 востребованных и топ 5 невостребованных продуктов
    top_5 = grouped_data.nlargest(5, 'cnt')  # Топ 5 востребованных
    bottom_5 = grouped_data.nsmallest(5, 'cnt')  # Топ 5 невостребованных

    # Объединяем топ 5 и bottom 5
    top_and_bottom_5 = pd.concat([top_5, bottom_5])

    return top_and_bottom_5

##################### 7.1 Востребованность продукта - общий график для всех магазинов ######################

# 2. Функция для построения графика
def plot_top_bottom_5_products(data):
    """
    Построение графика для топ 5 востребованных и топ 5 невостребованных продуктов.
    """
    # Разделение на топ 5 и bottom 5
    top_5 = data.nlargest(5, 'cnt')
    bottom_5 = data.nsmallest(5, 'cnt')

    # Создаем фигуру
    fig = go.Figure()

    # Добавляем бары для топ 5 продуктов
    fig.add_trace(go.Bar(
        x=top_5['item_id'],
        y=top_5['cnt'],
        name="Топ 5 востребованных продуктов",
        marker_color='green'
    ))

    # Добавляем бары для bottom 5 продуктов
    fig.add_trace(go.Bar(
        x=bottom_5['item_id'],
        y=bottom_5['cnt'],
        name="Топ 5 невостребованных продуктов",
        marker_color='red'
    ))

    # Настройка оформления графика
    fig.update_layout(
        title="Топ 5 востребованных и невостребованных продуктов",
        xaxis_title="Идентификатор продукта",
        yaxis_title="Количество продаж",
        template='plotly_white',
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGrey'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGrey'),
        font=dict(size=14, color='Black'),
        height=600,
        width=900,
        barmode='group'  # Для группировки столбцов
    )

    fig.show()

# Обработка данных через пайплайн
processed_data = product_sales_pipeline(data)

plot_top_bottom_5_products(processed_data)

##################### 7.2 Востребованность продукта - по укаждому магазину ######################

# Пайплайн для обработки данных для каждого магазина (оставляем только топ 5 товаров)
def store_top5_sales_pipeline(data):
    """
    Пайплайн для обработки данных по магазинам. Возвращает топ 5 товаров для каждого магазина.
    """
    grouped_data = data.groupby(['store_id', 'item_id'])['cnt'].sum().reset_index()
    stores_data = {}

    for store in grouped_data['store_id'].unique():
        store_data = grouped_data[grouped_data['store_id'] == store]
        top_5 = store_data.nlargest(5, 'cnt')
        stores_data[store] = {'top_5': top_5}

    return stores_data

# Построение сетки графиков
def plot_store_top5_sales_grid(stores_data):
    """
    Построение сетки графиков для каждого магазина с топ 5 товаров.
    """
    num_stores = len(stores_data)
    cols = 2  # Фиксируем количество колонок на 2
    rows = math.ceil(num_stores / cols)  # Автоматический расчет количества строк

    fig = make_subplots(rows=rows, cols=cols, subplot_titles=[f"Магазин {store}" for store in stores_data.keys()])

    for i, (store, data) in enumerate(stores_data.items()):
        row = (i // cols) + 1
        col = (i % cols) + 1

        # Добавляем топ 5 товаров
        fig.add_trace(go.Bar(
            x=data['top_5']['item_id'],
            y=data['top_5']['cnt'],
            name=f"Топ 5 для магазина {store}",
            marker_color='green'
        ), row=row, col=col)

    fig.update_layout(
        height=600 + (rows * 300),
        width=1000,
        title_text="Топ 5 востребованных товаров по магазинам",
        showlegend=False,
        template='plotly_white'
    )

    fig.show()

stores_data = store_top5_sales_pipeline(data)

plot_store_top5_sales_grid(stores_data)

##################### 7.3 Построение круговой диаграммы востребованности  для каждого магазина ######################

# Пайплайн для расчета долей продаж каждого товара в магазине
def store_sales_share_pipeline(data):
    """
    Пайплайн для расчета доли продаж товаров по магазинам.
    Возвращает долю каждого товара по магазину.
    """
    grouped_data = data.groupby(['store_id', 'item_id'])['cnt'].sum().reset_index()
    total_sales_by_store = grouped_data.groupby('store_id')['cnt'].sum().reset_index()

    grouped_data = pd.merge(grouped_data, total_sales_by_store, on='store_id', suffixes=('', '_total'))
    grouped_data['share'] = grouped_data['cnt'] / grouped_data['cnt_total'] * 100  # Расчет доли в процентах

    stores_data = {}

    for store in grouped_data['store_id'].unique():
        store_data = grouped_data[grouped_data['store_id'] == store]
        stores_data[store] = store_data

    return stores_data

# Построение сетки круговых диаграмм
def plot_store_sales_share_grid(stores_data):
    """
    Построение сетки круговых диаграмм для каждого магазина с долями продаж товаров.
    """
    num_stores = len(stores_data)
    cols = 2  # Фиксируем количество колонок на 2
    rows = math.ceil(num_stores / cols)  # Автоматический расчет количества строк

    fig = make_subplots(rows=rows, cols=cols, subplot_titles=[f"Магазин {store}" for store in stores_data.keys()],
                        specs=[[{'type': 'domain'} for _ in range(cols)] for _ in range(rows)])

    for i, (store, data) in enumerate(stores_data.items()):
        row = (i // cols) + 1
        col = (i % cols) + 1

        # Добавляем круговую диаграмму для каждого магазина
        fig.add_trace(go.Pie(
            labels=data['sales_share']['item_id'],
            values=data['sales_share']['sales_share'],
            name=f"Магазин {store}",
            hole=0.4
        ), row=row, col=col)

    fig.update_layout(
        height=600 + (rows * 300),
        width=1000,
        title_text="Доли продаж товаров по магазинам",
        showlegend=False,
        template='plotly_white'
    )

    fig.show()

stores_share_data = store_sales_share_pipeline(data)

plot_store_sales_share_pie(stores_share_data)


#######################################################
##  8 Выручка по магазинам
#######################################################

data['date'] = pd.to_datetime(data['date'])


# Функция для расчета выручки по дням и неделям
def store_revenue_pipeline(data):
    # Создаем столбец выручки (цена * количество)
    data['revenue'] = data['sell_price'] * data['cnt']

    # Группируем данные по магазинам, дням и неделям
    stores_data = {}
    for store in data['store_id'].unique():
        store_data = data[data['store_id'] == store]

        # Выручка за каждый день
        daily_revenue = store_data.groupby('date')['revenue'].sum()

        # Выручка за каждую неделю
        weekly_revenue = store_data.groupby(pd.Grouper(key='date', freq='W'))['revenue'].sum()

        stores_data[store] = {'daily_revenue': daily_revenue, 'weekly_revenue': weekly_revenue}

    return stores_data


# Функция для построения графиков в сетке
def plot_store_revenue_grid(stores_data):
    # Определяем количество строк и колонок для сетки графиков
    rows = len(stores_data)
    cols = 2  # Одна колонка для дневной выручки, другая для недельной

    # Создаем фигуру с сеткой графиков
    fig = make_subplots(
        rows=rows, cols=cols,
        subplot_titles=[f"{store} - Выручка за дни" for store in stores_data.keys()] +
                       [f"{store} - Выручка за недели" for store in stores_data.keys()],
        vertical_spacing=0.1
    )

    # Добавляем графики для каждого магазина
    row = 1
    for store, revenues in stores_data.items():
        # График выручки за дни
        fig.add_trace(
            go.Scatter(x=revenues['daily_revenue'].index, y=revenues['daily_revenue'], mode='lines+markers',
                       name=f'{store} - Выручка за дни'),
            row=row, col=1
        )

        # График выручки за недели
        fig.add_trace(
            go.Scatter(x=revenues['weekly_revenue'].index, y=revenues['weekly_revenue'], mode='lines+markers',
                       name=f'{store} - Выручка за недели'),
            row=row, col=2
        )

        row += 1

    # Настраиваем оформление графика
    fig.update_layout(
        height=rows * 400, width=1000,
        title_text="Выручка магазина за каждый день и неделю",
        template="plotly_white"
    )

    # Показываем график
    fig.show()

# Применяем пайплайн для получения данных по каждому магазину
stores_data = store_revenue_pipeline(data)

# Строим график
plot_store_revenue_grid(stores_data)

#######################################################
##  9. Сравнение продаж пр будням и выходным
#######################################################

dates_list = data['date'].tolist()
sales_list = data['cnt'].tolist()

# Функция для определения будний это день или выходной
def is_weekend(date):
    return date.weekday() >= 5  # 5 и 6 это суббота и воскресенье


# Пайплайн для обработки данных и получения продаж по будним и выходным дням за каждый месяц
def sales_weekday_weekend_by_month_pipeline(dates, sales_list):
    # Преобразуем список дат в формат datetime
    dates = pd.to_datetime(dates)

    # Отбираем только данные за 2015 год
    mask_2015 = dates.year == 2015
    dates = dates[mask_2015]
    sales_list = pd.Series(sales_list)[mask_2015].tolist()

    # Создаем DataFrame для удобной группировки
    df = pd.DataFrame({"date": dates, "sales": sales_list})

    # Добавляем колонку "Месяц"
    df['month'] = df['date'].dt.month

    # Группируем данные по месяцам и подсчитываем продажи по будням и выходным
    monthly_sales = df.groupby('month').apply(lambda x: {
        'weekday_sales': sum(x['sales'][~x['date'].apply(is_weekend)]),
        'weekend_sales': sum(x['sales'][x['date'].apply(is_weekend)])
    })

    return monthly_sales


# Функция для построения графика
def plot_weekday_weekend_sales_by_month(monthly_sales):
    months = range(1, 13)  # Список месяцев

    # Разбиваем данные на будние и выходные
    weekday_sales = [monthly_sales[m]['weekday_sales'] for m in months]
    weekend_sales = [monthly_sales[m]['weekend_sales'] for m in months]

    labels = ['Будни', 'Выходные']
    width = 0.35  # Ширина колонок

    plt.figure(figsize=(10, 6))
    p1 = plt.bar(months, weekday_sales, width, label='Будни', color='blue')
    p2 = plt.bar(months, weekend_sales, width, bottom=weekday_sales, label='Выходные', color='orange')

    plt.ylabel('Объем продаж')
    plt.title('Продажи по будним и выходным дням по месяцам 2015 года')
    plt.xticks(months)
    plt.legend()

    plt.show()


# Основной контроллер для обработки данных и построения графика
def main_controller(dates_list, sales_list):
    # Получаем продажи по будним и выходным за каждый месяц
    monthly_sales = sales_weekday_weekend_by_month_pipeline(dates_list, sales_list)

    # Строим график
    plot_weekday_weekend_sales_by_month(monthly_sales)

main_controller(dates_list, sales_list)

#######################################################
##  10. Анализ по праздникам
#######################################################

##################### 10.1 Сравнение продаж в периоды проведения праздников ######################

# Функция для проверки, идет ли праздние в день
def is_event_day(row):
    return row['event_name_1'] != 'Unknown' or row['event_name_2'] != 'Unknown'


# Пайплайн для разделения данных на периоды с праздниками и без
def sales_with_without_events_pipeline(data):
    # Определяем дни с акциями
    data['is_event_day'] = data.apply(is_event_day, axis=1)

    # Продажи в дни с праздгником
    sales_with_events = data[data['is_event_day']]['cnt'].sum()

    # Продажи в дни без  праздгника
    sales_without_events = data[~data['is_event_day']]['cnt'].sum()

    return sales_with_events, sales_without_events


# Функция для построения графика сравнения продаж
def plot_sales_comparison(sales_with, sales_without):
    labels = ['В день проведения праздника', 'Без праздника']
    sales_values = [sales_with, sales_without]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, sales_values, color=['green', 'red'])
    plt.ylabel('Объем продаж')
    plt.title('Сравнение продаж в периоды проведения праздников')
    plt.show()

# Основной контроллер для обработки данных и построения графика
def main_sales_comparison(data):
    sales_with_events, sales_without_events = sales_with_without_events_pipeline(data)
    plot_sales_comparison(sales_with_events, sales_without_events)

main_sales_comparison(data)

##################### 10.2 Влияние праздников на объем продаж ######################

# Функция для вычисления продаж по праздникам
def sales_by_event(data):
    event_sales = data.groupby('event_name_1')['cnt'].sum().reset_index()
    event_sales = event_sales[event_sales['event_name_1'] != 'Unknown']

    return event_sales

# Функция для построения графика по праздникам
def plot_sales_by_event(event_sales):
    plt.figure(figsize=(10, 6))
    plt.bar(event_sales['event_name_1'], event_sales['cnt'], color='blue')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Объем продаж')
    plt.title('Влияние праздников на объем продаж')
    plt.show()

# Основной контроллер для обработки данных и построения графика
def main_sales_by_event(data):
    event_sales = sales_by_event(data)
    plot_sales_by_event(event_sales)

main_sales_by_event(data)
