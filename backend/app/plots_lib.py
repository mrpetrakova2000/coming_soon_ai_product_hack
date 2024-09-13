import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import colorsys
from plotly.io import to_json
import json
from plotly.utils import PlotlyJSONEncoder
import math

SIZE = 100

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
            'width': 1000,
            'height': 600,
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

#######################################################
## Количество продаж товара
#######################################################

def plot_sales(data):
    dates_list = data['date'].tolist() # Преобразуем даты в список
    sales_list = data['cnt'].tolist()

    dates_list = dates_list[max(len(dates_list) - 1 - SIZE, 0):]
    sales_list = sales_list[max(len(sales_list) - 1 - SIZE, 0):]

    return {
        'data': [
            {
                'x': dates_list,
                'y': sales_list,
                'type': 'scatter',
                'mode': 'lines+markers',
                'marker': {'color': '#cd78f0'},
                'name': 'Продажи'
            }
        ],
        'layout': {
            'width': 1000,
            'height': 600,
            'title': 'Количество продаж товара',
            'xaxis': {
                'title': 'Дата' #,
                #rangeslider': {
                #    'visible': True
                #}
            },
            'yaxis': {
                'title': 'Продажи'
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

#######################################################
## Прогнозирование спроса по выбранному товару
#######################################################

def plot_sku_prediction(last_n_days, prediction_data):
    dates_list_init = last_n_days['date'].tolist() # Преобразуем даты в список
    sales_list_init = last_n_days['cnt'].tolist()
    
    dates_list_predict = [dates_list_init[-1]] + prediction_data['date'].tolist() # Преобразуем даты в список
    sales_list_predict = [sales_list_init[-1]] + prediction_data['cnt'].tolist()
    return {
        'data': [
            {
                'x': dates_list_predict,
                'y': sales_list_predict,
                'type': 'scatter',
                'mode': 'lines+markers',
                'marker': {'color': '#cd78f0'},
                'name': 'Прогноз'
            },
            {
                'x': dates_list_init,
                'y': sales_list_init,
                'type': 'scatter',
                'mode': 'lines+markers',
                'marker': {'color': '#000'},
                'name': 'Реальные данные'
            }
        ],
        'layout': {
            'width': 1000,
            'height': 600,
            'title': 'Прогнозирование спроса по выбранному товару',
            'xaxis': {
                'title': 'Дата' #,
                #rangeslider': {
                #    'visible': True
                #}
            },
            'yaxis': {
                'title': 'Количество продаж'
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

#######################################################
## Прогнозирование спроса по выбранной категории
#######################################################

def plot_cluster_prediction(prev_data, one_day_pred, seven_days_pred, thirty_days_pred):
    dates_list_init = prev_data['date'].tolist()[max(len(prev_data) - 14, 0):] # Преобразуем даты в список
    sales_list_init = prev_data['cnt'].tolist()[max(len(prev_data) - 14, 0):]
    
    dates_list_predict = [dates_list_init[-1]] + one_day_pred['date'].tolist() + seven_days_pred['date'].tolist() + thirty_days_pred['date'].tolist()
    sales_list_predict = [sales_list_init[-1]] + one_day_pred['cnt'].tolist() + seven_days_pred['cnt'].tolist() + thirty_days_pred['cnt'].tolist()
    return {
        'data': [
            {
                'x': dates_list_predict,
                'y': sales_list_predict,
                'type': 'scatter',
                'mode': 'lines+markers',
                'marker': {'color': '#cd78f0'},
                'name': 'Прогноз'
            },
            {
                'x': dates_list_init,
                'y': sales_list_init,
                'type': 'scatter',
                'mode': 'lines+markers',
                'marker': {'color': '#000'},
                'name': 'Реальные данные'
            }
        ],
        'layout': {
            'width': 1000,
            'height': 600,
            'title': 'Прогнозирование спроса по выбранной категории',
            'xaxis': {
                'title': 'Дата' #,
                #rangeslider': {
                #    'visible': True
                #}
            },
            'yaxis': {
                'title': 'Количество продаж'
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


# def plot_sales_change_compared_prev_period(data):
#     dates_list = data['date'].tolist()  # Преобразуем даты в список
#     sales_list = data['cnt'].tolist()

#     # Вычисление процентного изменения продаж с обработкой деления на ноль
#     sales_change = np.where(
#         sales_list[:-1] == 0,
#         0,
#         np.diff(sales_list) / sales_list[:-1] * 100
#     )

#     dates_for_plot = dates_list[1:]

#     annotations = []

#     # Логика для добавления подписей на максимумы и минимумы
#     for i in range(1, len(sales_change) - 1):
#         if (sales_change[i] > sales_change[i - 1] and sales_change[i] > sales_change[i + 1]) or (sales_change[i] < sales_change[i - 1] and sales_change[i] < sales_change[i + 1]):
#             annotations.append({
#                 'x': dates_for_plot[i],
#                 'y': sales_change[i],
#                 'text': f'{sales_change[i]:.1f}%',  # Форматирование текста
#                 'showarrow': True,  # Исправлено на True
#                 'arrowhead': 2,
#                 'ax': 0,
#                 'ay': -40
#             })

#     # Обработка одинаковых последовательных значений (подпись в начале и в конце серии)
#     previous_value = None
#     repeat_series_start = None

#     for i, value in enumerate(sales_change):
#         if previous_value is None:
#             previous_value = value
#             continue

#         # Если значение повторяется
#         if value == previous_value:
#             if repeat_series_start is None:
#                 repeat_series_start = i - 1  # Начало серии повторяющихся значений
#         else:
#             if repeat_series_start is not None:
#                 # Добавляем подпись в начале и в конце серии
#                 annotations.append({
#                     'x': dates_for_plot[repeat_series_start],
#                     'y': sales_change[repeat_series_start],
#                     'text': f'{sales_change[repeat_series_start]:.1f}%', 
#                     'showarrow': True, 
#                     'arrowhead': 2,
#                     'ax': 0,
#                     'ay': -40
#                 })
#                 annotations.append({
#                     'x': dates_for_plot[i - 1],
#                     'y': sales_change[i - 1],
#                     'text': f'{sales_change[i - 1]:.1f}%', 
#                     'showarrow': True, 
#                     'arrowhead': 2,
#                     'ax': 0,
#                     'ay': -40
#                 })
#                 repeat_series_start = None  # Сброс серии
#             previous_value = value
    
#     # Обработка последнего элемента
#     if repeat_series_start is not None:
#         annotations.append({
#             'x': dates_for_plot[repeat_series_start],
#             'y': sales_change[repeat_series_start],
#             'text': f'{sales_change[repeat_series_start]:.1f}%', 
#             'showarrow': True, 
#             'arrowhead': 2,
#             'ax': 0,
#             'ay': -40
#         })
#         annotations.append({
#             'x': dates_for_plot[-1],  # Исправлено на dates_for_plot
#             'y': sales_change[-1],
#             'text': f'{sales_change[-1]:.1f}%', 
#             'showarrow': True, 
#             'arrowhead': 2,
#             'ax': 0,
#             'ay': -40
#         })
    
#     return {
#         'data': [
#             {
#                 'x': dates_for_plot,
#                 'y': sales_change,
#                 'type': 'scatter',
#                 'mode': 'lines+markers',
#                 'marker': {'color': '#cd78f0'},
#                 'name': 'Изменение продаж (%)'
#             }
#         ],
#         'layout': {
#             'width': 800,
#             'height': 400,
#             'title': 'Рост/падение продаж с подписями пиков',
#             'xaxis': {
#                 'title': 'Дата'
#             },
#             'yaxis': {
#                 'title': 'Изменение продаж (%)'
#             },
#             'legend': {
#                 'orientation': 'h',
#                 'yanchor': 'bottom',
#                 'y': -0.5,
#                 'xanchor': 'center',
#                 'x': 0.5
#             },
#             'annotations': annotations  # Добавление аннотаций сюда
#         }
#     }

#######################################################
## 3. Скорость продажи товара (как быстро распродаются товары)
#######################################################

def sales_pipeline_speed(dates, sales, period='D'):
    """
    Вход:
    - dates: Список с датами.
    - sales: Список с количеством продаж.
    - period: Период для ресемплирования данных ('D' - дни, 'M' - месяцы и т.д.).

    Выход:
    - Возвращает три массива: даты, скорость продаж, накопительные продажи.
    """

    dates = pd.to_datetime(np.array(dates))  # Преобразуем даты в формат datetime
    sales = np.array(sales)

    # Вычисляем скорость продаж (разница между днями)
    speed_sales = pd.Series(sales).diff().fillna(0).abs().tolist()

    # Вычисляем накопительные продажи
    cumulative_sales = pd.Series(sales).cumsum().tolist()

    # Создание DataFrame для ресемплирования данных
    data = pd.DataFrame({'Date': dates, 'Sales': sales})
    data.set_index('Date', inplace=True)

    # Агрегируем данные по указанному периоду
    resampled_data = data.resample(period).sum()

    return resampled_data.index.tolist(), speed_sales[:len(resampled_data)], cumulative_sales[:len(resampled_data)]

##################### 3.1 Динамика продаж товара ######################

def plot_sales_speed_dynamics(data):
    dates_list = data['date'].tolist()[max(len(data) - SIZE*3, 0):]  # Преобразуем даты в список
    sales_list = data['cnt'].tolist()[max(len(data) - SIZE*3, 0):]   # Преобразуем количество продаж в список

    # Применение пайплайна для получения данных
    resampled_dates, speed_sales, cumulative_sales = sales_pipeline_speed(dates_list, sales_list, period='M')

    return {
        'data': [
            {
                'x': resampled_dates,
                'y': speed_sales,
                'type': 'scatter',
                'mode': 'lines+markers',
                'marker': {'color': '#cd78f0'},
                'name': 'Продажи'
            }
        ],
        'layout': {
            'width': 1000,
            'height': 600,
            'title': 'Динамика продаж товара',
            'xaxis': {
                'title': 'Дата' #,
                #rangeslider': {
                #    'visible': True
                #}
            },
            'yaxis': {
                'title': 'Количество продаж'
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

#######################################################
## 4. Пики продаж (месяц)
#######################################################

def sales_pipeline_peaks_months(dates, sales, period='M'):
    """
    Вход:
    - dates: Список с датами.
    - sales: Список с продажами.
    - period: Период для ресемплирования ('M' для месяцов).

    Выход:
    - Месяцы и максимальные продажи за этот период.
    """

    # Преобразуем даты в формат datetime и создаем DataFrame
    data = pd.DataFrame({'Date': dates, 'Sales': sales})
    data['Date'] = pd.to_datetime(data['Date'])

    # Устанавливаем индекс
    data.set_index('Date', inplace=True)

    # Ресемплируем по месяцам и находим максимальные продажи
    monthly_peaks = data.resample(period).max()

    return monthly_peaks.index, monthly_peaks['Sales']

# ##################### 4.1 Диаграмма с накоплением (Area Chart) — по годам сетка ######################

# def plot_sales_peaks_area_grid(data):
#     """
#     Строит диаграмму пиков продаж по месяцам в виде сетки по годам и возвращает словарь для использования в JavaScript.
#     """

#     # Преобразование колонок 'date' и 'cnt' в списки
#     dates_list = data['date'].tolist()  # Преобразуем даты в список
#     sales_list = data['cnt'].tolist()    # Преобразуем количество продаж в список

#     # Вызов пайплайна для вычисления пиков продаж по месяцам
#     processed_dates, monthly_peaks = sales_pipeline_peaks_months(dates_list, sales_list, period='M')

#     # Преобразуем даты и создаем DataFrame для удобства фильтрации по годам
#     df = pd.DataFrame({'Date': processed_dates, 'Sales': monthly_peaks})
#     df['Year'] = df['Date'].dt.year
#     unique_years = df['Year'].unique()

#     # Создаем массив цветов с плавным увеличением яркости
#     base_color = '#cd78f0'
    
#     # Создаем массив цветов с увеличением яркости и насыщенности
#     colors = []
#     h, s, v = colorsys.rgb_to_hsv(
#         int('0x{}'.format(base_color[1:3]), 16) / 255,
#         int('0x{}'.format(base_color[3:5]), 16) / 255,
#         int('0x{}'.format(base_color[5:7]), 16) / 255
#     )

#     for i in range(len(unique_years)):
#         # Увеличиваем насыщенность и яркость на основе индекса
#         s = min(1, s + (0.2 * (i % 2)))  # Увеличиваем насыщенность на 20% для первых 5 графиков
#         v = min(1, v + (0.2 * (i // 2)))  # Увеличиваем яркость на 10% для каждой группы из 5 графиков
        
#         r, g, b = colorsys.hsv_to_rgb(h, s, v)
#         colors.append('#{:02X}{:02X}{:02X}'.format(int(r * 255), int(g * 255), int(b * 255)))

#     # Создаем список для хранения данных для каждого графика
#     plots = []

#     # Построение графиков по каждому году
#     for year in unique_years:
#         yearly_data = df[df['Year'] == year]

#         # Создаем данные для графика
#         plot_data = {
#             'x': yearly_data['Date'].dt.strftime('%Y-%m-%d').tolist(),  # Преобразуем даты в строку
#             'y': yearly_data['Sales'].tolist(),
#             'type': 'scatter',
#             'mode': 'lines+markers',
#             'marker': {'color': colors[len(plots)]},  # Установите нужный цвет
#             'name': f'Пики продаж за {year}',
#             'fill': 'tozeroy',
#             'xaxis': {'title': 'Дата'},
#             'yaxis': {'title': str(year)}
#         }

#         # Добавляем данные графика в список
#         plots.append(plot_data)

#     # Создаем макет для графиков
#     layout = {
#         'title': 'Пики продаж по годам',
#         'width': 800,
#         'height': 400,
#         'grid': {
#             'rows': (len(unique_years) + 1) // 2,  # Количество строк
#             'cols': 2,  # Количество столбцов
#             'pattern': 'independent'
#         },
#         'legend': {
#                 'orientation': 'h',
#                 'yanchor': 'bottom',
#                 'y': -0.5,
#                 'xanchor': 'center',
#                 'x': 0.5
#             }
#     }

#     return {
#         'data': plots,
#         'layout': layout
#     }

##################### 4.3 Обычный ######################

def plot_sales_peaks_months_line(data):
    dates_list = data['date'].tolist()#[max((len(data)-4*SIZE), 0):]  # Преобразуем даты в список
    sales_list = data['cnt'].tolist()#[max((len(data)-4*SIZE), 0):]    # Преобразуем количество продаж в список

    # Вызов пайплайна для вычисления пиков продаж по месяцам
    processed_dates, monthly_peaks = sales_pipeline_peaks_months(dates_list, sales_list, period='MS')

    # Создание данных для графика
    plot_data = {
        'x': processed_dates.tolist(),  # Даты для оси X
        'y': monthly_peaks.tolist(),     # Пики продаж для оси Y
        'type': 'scatter',
        'mode': 'lines+markers',
        'line': {'color': '#a86bc3'},
        'marker': {'size': 8, 'color': '#cd78f0'},
        'name': 'Пики продаж'
    }

    # Создание аннотаций для пиковых точек
    annotations = []
    for date, peak in zip(processed_dates, monthly_peaks):
        annotations.append({
            'x': date,
            'y': peak,
            'text': f'{peak:.1f}',
            'showarrow': True,
            'ax': 0,
            'ay': -20
        })

    # Создание макета для графика
    layout = {
        'title': "Пики продаж (месяц)",
        'xaxis': {'title': "Дата"},
        'yaxis': {'title': "Максимальные продажи (единиц/месяц)"},
        'annotations': annotations,
        'template': "plotly_white",
        'width': 1000,
        'height': 600,
    }

    return {
        'data': [plot_data],
        'layout': layout
    }


# ##################### 7.1 Востребованность продукта - общий график для всех магазинов ######################

# # Пайплайн для обработки данных
# def product_sales_pipeline(data):
#     """
#     Пайплайн для обработки данных: подсчёт продаж каждого продукта и выбор топ 5 и bottom 5.
#     """
#     # Сгруппируем данные по продуктам и посчитаем общее количество продаж
#     grouped_data = data.groupby('item_id')['cnt'].sum().reset_index()

#     # Отсортируем данные для получения топ 5 востребованных и топ 5 невостребованных продуктов
#     top_5 = grouped_data.nlargest(5, 'cnt')  # Топ 5 востребованных
#     bottom_5 = grouped_data.nsmallest(5, 'cnt')  # Топ 5 невостребованных

#     # Объединяем топ 5 и bottom 5
#     top_and_bottom_5 = pd.concat([top_5, bottom_5])

#     return top_and_bottom_5


# # 2. Функция для построения графика
# def plot_top_bottom_5_products(data):

#     # Обработка данных через пайплайн
#     processed_data = product_sales_pipeline(data)

#     """
#     Построение графика для топ 5 востребованных и топ 5 невостребованных продуктов.
#     """
#     # Разделение на топ 5 и bottom 5
#     top_5 = data.nlargest(5, 'cnt')
#     bottom_5 = data.nsmallest(5, 'cnt')

#     # Создаем фигуру
#     fig = go.Figure()

#     # Добавляем бары для топ 5 продуктов
#     fig.add_trace(go.Bar(
#         x=top_5['item_id'],
#         y=top_5['cnt'],
#         name="Топ 5 востребованных продуктов",
#         marker_color='green'
#     ))

#     # Добавляем бары для bottom 5 продуктов
#     fig.add_trace(go.Bar(
#         x=bottom_5['item_id'],
#         y=bottom_5['cnt'],
#         name="Топ 5 невостребованных продуктов",
#         marker_color='red'
#     ))

#     # Настройка оформления графика
#     fig.update_layout(
#         title="Топ 5 востребованных и невостребованных продуктов",
#         xaxis_title="Идентификатор продукта",
#         yaxis_title="Количество продаж",
#         template='plotly_white',
#         xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGrey'),
#         yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGrey'),
#         font=dict(size=14, color='Black'),
#         height=600,
#         width=1000,
#         barmode='group'  # Для группировки столбцов
#     )

#     #json_fig = to_json(fig)
#     # json_acceptable_string = json_fig.replace("'", "\"")
#     # result = json.loads(json_acceptable_string)

#     graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
#     json_acceptable_string = graphJSON.replace("'", "\"")
#     result = json.loads(json_acceptable_string)

   
#     return result

    
##################### 7.3 Построение круговой диаграммы востребованности  для каждого магазина ######################

# # Пайплайн для расчета долей продаж каждого товара в магазине
# def store_sales_share_pipeline(data):
#     """
#     Пайплайн для расчета доли продаж товаров по магазинам.
#     Возвращает долю каждого товара по магазину.
#     """
#     grouped_data = data.groupby(['store_id', 'item_id'])['cnt'].sum().reset_index()
#     total_sales_by_store = grouped_data.groupby('store_id')['cnt'].sum().reset_index()

#     grouped_data = pd.merge(grouped_data, total_sales_by_store, on='store_id', suffixes=('', '_total'))
#     grouped_data['sales_share'] = grouped_data['cnt'] / grouped_data['cnt_total'] * 100  # Расчет доли в процентах

#     stores_data = {}

#     for store in grouped_data['store_id'].unique():
#         store_data = grouped_data[grouped_data['store_id'] == store]
#         stores_data[store] = store_data

#     return stores_data

# # Построение сетки круговых диаграмм
# def plot_store_sales_share_grid(data):
#     """
#     Построение сетки круговых диаграмм для каждого магазина с долями продаж товаров.
#     """
#     stores_data = store_sales_share_pipeline(data)

#     num_stores = len(stores_data)
#     cols = 2  # Фиксируем количество колонок на 2
#     rows = math.ceil(num_stores / cols)  # Автоматический расчет количества строк

#     fig = make_subplots(rows=rows, cols=cols, subplot_titles=[f"Магазин {store}" for store in stores_data.keys()],
#                         specs=[[{'type': 'domain'} for _ in range(cols)] for _ in range(rows)])

#     for i, (store, data) in enumerate(stores_data.items()):
#         row = (i // cols) + 1
#         col = (i % cols) + 1

#         # Добавляем круговую диаграмму для каждого магазина
#         fig.add_trace(go.Pie(
#             labels=data['sales_share']['item_id'],
#             values=data['sales_share']['sales_share'],
#             name=f"Магазин {store}",
#             hole=0.4
#         ), row=row, col=col)

#     fig.update_layout(
#         height=600 + (rows * 300),
#         width=1000,
#         title_text="Доли продаж товаров по магазинам",
#         showlegend=False,
#         template='plotly_white'
#     )

#     graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
#     json_acceptable_string = graphJSON.replace("'", "\"")
#     result = json.loads(json_acceptable_string)
#     return result

#######################################################
##  8 Выручка по магазинам
#######################################################

import colorsys

# Функция для генерации массива цветов от черного к заданному цвету
def generate_colors(base_color, num_colors):
    # Преобразуем базовый цвет в RGB
    r_base = int(base_color[1:3], 16) / 255
    g_base = int(base_color[3:5], 16) / 255
    b_base = int(base_color[5:7], 16) / 255

    # Создаем массив цветов
    colors = []
    
    for i in range(num_colors):
        # Интерполяция от черного (0, 0, 0) к базовому цвету
        r = r_base * (i / (num_colors - 1))
        g = g_base * (i / (num_colors - 1))
        b = b_base * (i / (num_colors - 1))
        
        # Преобразуем обратно в шестнадцатеричный формат
        colors.append('#{:02X}{:02X}{:02X}'.format(int(r * 255), int(g * 255), int(b * 255)))

    return colors


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
def plot_store_revenue_grid(data):

    # Применяем пайплайн для получения данных по каждому магазину
    stores_data = store_revenue_pipeline(data)
    # Определяем количество строк и колонок для сетки графиков
    rows = len(stores_data)
    cols = 2  # Одна колонка для дневной выручки, другая для недельной
    print(stores_data)
    # Создаем фигуру с сеткой графиков
    fig = make_subplots(
        rows=rows, cols=cols,
        subplot_titles=[f"{store} - Выручка за дни" for store in stores_data.keys()] +
                       [f"{store} - Выручка за недели" for store in stores_data.keys()],
        vertical_spacing=0.1
    )

    # Пример использования
    base_color = '#cd78f0'
    num_colors = len(stores_data)  # Количество цветов в градиенте
    colors = generate_colors(base_color, num_colors)

    # Добавляем графики для каждого магазина
    row = 1
    for store, revenues in stores_data.items():
        # График выручки за дни
        fig.add_trace(
            go.Scatter(x=revenues['daily_revenue'].index, y=revenues['daily_revenue'], mode='lines+markers',
                       name=f'{store} - Выручка за дни', line=dict(color=colors[row - 1])),
            row=row, col=1
        )

        # График выручки за недели
        fig.add_trace(
            go.Scatter(x=revenues['weekly_revenue'].index, y=revenues['weekly_revenue'], mode='lines+markers',
                       name=f'{store} - Выручка за недели', line=dict(color=colors[row - 1])),
            row=row, col=2
        )

        row += 1

    # Настраиваем оформление графика
    fig.update_layout(
        height=rows * 400, width=1000,
        title_text="Выручка магазина за каждый день и неделю",
    )

    fig.update_layout(
        legend=dict(
            orientation='h',  # Горизонтальная ориентация
            yanchor='bottom', # Якорь легенды снизу
            y=-0.1,           # Позиция легенды ниже графиков
            xanchor='center', # Центрирование легенды
            x=0.5             # Позиция легенды по центру
        )
    )

    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
    json_acceptable_string = graphJSON.replace("'", "\"")
    result = json.loads(json_acceptable_string)

    return result


#######################################################
##  9. Сравнение продаж пр будням и выходным
#######################################################

# Функция для определения будний это день или выходной
def is_weekend(date):
    return date.weekday() >= 5  # 5 и 6 это суббота и воскресенье


# Пайплайн для обработки данных и получения продаж по будним и выходным дням за каждый месяц
def sales_weekday_weekend_by_month_pipeline(dates, sales_list):
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
def plot_weekday_weekend_sales_by_month(data):
    months = [i for i in range(1,13)]  # Список месяцев

    dates_list = data['date'].tolist()
    sales_list = data['cnt'].tolist()

    monthly_sales = sales_weekday_weekend_by_month_pipeline(dates_list, sales_list)

    # Разбиваем данные на будние и выходные
    weekday_sales = [monthly_sales[m]['weekday_sales'] for m in months]
    weekend_sales = [monthly_sales[m]['weekend_sales'] for m in months]

    # Создание фигуры
    fig = go.Figure()

    # Добавление столбцов для будних дней
    fig.add_trace(go.Bar(
        x=months,
        y=weekday_sales,
        name='Будни',
        marker_color='black'
    ))

    # Добавление столбцов для выходных дней
    fig.add_trace(go.Bar(
        x=months,
        y=weekend_sales,
        name='Выходные',
        marker_color='#cd78f0'
    ))

    # Настройка макета
    fig.update_layout(
        barmode='stack',  # Режим отображения столбцов
        xaxis_title='Месяц',
        yaxis_title='Объем продаж',
        title='Продажи по будним и выходным дням по месяцам 2015 года (по SKU)',
        legend_title='Дни недели',
        height=600,
        width=1000
    )

    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
    json_acceptable_string = graphJSON.replace("'", "\"")
    result = json.loads(json_acceptable_string)

    return result

#######################################################
##  10. Анализ по праздникам
#######################################################

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
def plot_sales_comparison(data):
    sales_with, sales_without = sales_with_without_events_pipeline(data)
    labels = ['В день проведения праздника', 'Без праздника']
    sales_values = [sales_with, sales_without]

    # Создание фигуры
    fig = go.Figure()

    # Добавление столбцов
    fig.add_trace(go.Bar(
        x=labels,
        y=sales_values,
        marker_color=['#cd78f0', 'black']  # Цвета для столбцов
    ))

    # Настройка макета
    fig.update_layout(
        title='Сравнение продаж в периоды проведения праздников (по SKU)',
        xaxis_title='Периоды',
        yaxis_title='Объем продаж',
        height=600,
        width=1000
    )

    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
    json_acceptable_string = graphJSON.replace("'", "\"")
    result = json.loads(json_acceptable_string)

    return result

##################### 10.2 Влияние праздников на объем продаж ######################

# Функция для вычисления продаж по праздникам
def sales_by_event(data):
    # Удаление специальных символов из названий событий
    data['event_name_1'] = data['event_name_1'].str.replace(r'[^\w\s]', '', regex=True)
    event_sales = data.groupby('event_name_1')['cnt'].sum().reset_index()
    event_sales = event_sales[event_sales['event_name_1'] != 'Unknown']

    return event_sales

def plot_sales_by_event(data):
    event_sales = sales_by_event(data)
    # Создание фигуры
    fig = go.Figure()

    # Добавление столбцов
    fig.add_trace(go.Bar(
        x=event_sales['event_name_1'],
        y=event_sales['cnt'],
        marker_color='#cd78f0'  # Цвет столбцов
    ))

    # Настройка макета
    fig.update_layout(
        title='Влияние праздников на объем продаж (по SKU)',
        xaxis_title='Праздники',
        yaxis_title='Объем продаж',
        height=600,
        width=1000
    )

    graphJSON = to_json(fig)
    json_acceptable_string = graphJSON.replace("'", "\"")
    result = json.loads(json_acceptable_string)

    return result
    event_sales = event_sales[event_sales['event_name_1'] != 'Unknown']

    return event_sales

def plot_sales_by_event(data):
    event_sales = sales_by_event(data)
    # Создание фигуры
    fig = go.Figure()

    # Добавление столбцов
    fig.add_trace(go.Bar(
        x=event_sales['event_name_1'],
        y=event_sales['cnt'],
        marker_color='#cd78f0'  # Цвет столбцов
    ))

    # Настройка макета
    fig.update_layout(
        title='Влияние праздников на объем продаж (по SKU)',
        xaxis_title='Праздники',
        yaxis_title='Объем продаж',
        height=600,
        width=1000
    )

    graphJSON = to_json(fig)
    json_acceptable_string = graphJSON.replace("'", "\"")
    result = json.loads(json_acceptable_string)

    return result






