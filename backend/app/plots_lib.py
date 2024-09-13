import pandas as pd
import numpy as np

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
            'width': 800,
            'height': 400,
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
            'width': 800,
            'height': 400,
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
            'width': 800,
            'height': 400,
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
            'width': 800,
            'height': 400,
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

##################### 4.1 Диаграмма с накоплением (Area Chart) — по годам сетка ######################


def plot_sales_peaks_area_grid(data):
    """
    Строит диаграмму пиков продаж по месяцам в виде сетки по годам.
    """

    # Преобразование колонок 'date' и 'cnt' в списки
    dates_list = data['date'].tolist()[max(len(data) - SIZE*3, 0):]  # Преобразуем даты в список
    sales_list = data['cnt'].tolist()[max(len(data) - SIZE*3, 0):]   # Преобразуем количество продаж в список

    # Вызов пайплайна для вычисления пиков продаж по месяцам
    processed_dates, monthly_peaks = sales_pipeline_peaks_months(dates_list, sales_list, period='M')

    # Преобразуем даты и создаем DataFrame для удобства фильтрации по годам
    df = pd.DataFrame({'Date': processed_dates, 'Sales': monthly_peaks})
    df['Year'] = df['Date'].dt.year
    unique_years = df['Year'].unique()

    # Задаем сетку 3x2
    rows, cols = 3, 2  # Сетка 3 строки и 2 столбца
    data_dict = []
    annotations = []

    # Построение графиков по каждому году
    for i, year in enumerate(unique_years):
        yearly_data = df[df['Year'] == year]

        # Индексы для расстановки графиков по сетке
        row = i // cols + 1
        col = i % cols + 1

        # Добавление данных на график
        data_dict.append({
            'x': yearly_data['Date'].dt.strftime('%Y-%m-%d').tolist(),  # Преобразуем даты в строку
            'y': yearly_data['Sales'].tolist(),
            'type': 'scatter',
            'mode': 'lines+markers',
            'marker': {'color': 'blue'},
            'name': f'Пики продаж за {year}',
            'fill': 'tozeroy',
            'subplot': f'subplot{row}_{col}'  # Указываем расположение подграфика
        })

        # Добавление подписей на пиковые точки
        for date, peak in zip(yearly_data['Date'], yearly_data['Sales']):
            annotations.append({
                'x': date.strftime('%Y-%m-%d'),  # Преобразуем дату в строку
                'y': peak,
                'text': f'{peak:.1f}',
                'showarrow': True,
                'arrowhead': 2,
                'ax': 0,
                'ay': -40,
                'subplot': f'subplot{row}_{col}'  # Указываем расположение подграфика
            })

    # Формирование словаря для возврата
    return {
        'data': data_dict,
        'layout': {
            'width': 800,
            'height': 400,
            'title': 'Диаграмма пиков продаж по годам',
            'xaxis': {
                'title': 'Дата'
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
            },
            'annotations': annotations,  # Добавление аннотаций сюда
            'subplots': {
                'rows': rows,
                'cols': cols,
                'subplot_titles': [f'Пики продаж за {year}' for year in unique_years]  # Заголовки подграфиков
            }
        }
    }

   