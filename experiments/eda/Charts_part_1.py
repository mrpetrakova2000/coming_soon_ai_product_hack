import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import plotly.io as pio

from plotly.subplots import make_subplots
from matplotlib.widgets import Slider


data = pd.read_csv('merged_df.csv')

#######################################################
## 1. Количество продаж товара
#######################################################

def sales_pipeline_count_sales(dates, sales):
    """
    Принимает два списка: даты и количество продаж.

    Вход:
    - dates: Список с датами (должен быть тип np.array или list).
    - sales: Список с количеством продаж (должен быть тип np.array или list).

    Выход:
    - Возвращает массив дат и продаж для построения графика, фильтрованные по последним 100 записям.
    """

    if not isinstance(dates, (list, np.ndarray)) or not isinstance(sales, (list, np.ndarray)):
        raise ValueError("На вход должны подаваться списки или массивы.")

    # Преобразуем списки в numpy массивы для удобства
    dates = pd.to_datetime(np.array(dates))  # Преобразуем даты в формат datetime
    sales = np.array(sales)

    # Фильтруем последние 100 записей по дате
    filtered_dates = dates[-100:]
    filtered_sales = sales[-100:]

    return filtered_dates, filtered_sales

##################### Линейный график ######################

# Преобразование колонок 'date' и 'cnt' в списки
dates_list = data['date'].tolist()  # Преобразуем даты в список
sales_list = data['cnt'].tolist()   # Преобразуем количество продаж в список


def plot_sales_count_sales(dates, sales):
    """
    Строит интерактивный график количества продаж по указанным датам с использованием plotly.io.

    Вход:
    - dates: Массив с датами.
    - sales: Массив с количеством продаж.
    """

    fig = go.Figure()

    # Добавляем данные на график
    fig.add_trace(go.Bar(
        x=dates,
        y=sales,
        marker_color='blue',
        name='Количество продаж'
    ))

    # Настраиваем внешний вид графика
    fig.update_layout(
        title="Количество продаж за указанный период",
        xaxis_title="Дата",
        yaxis_title="Количество продаж",
        xaxis_tickformat='%b %d, %Y',
        xaxis_tickangle=-45,
        template="plotly_white"  # Изменение темы на светлую
    )

    # Показать график
    fig.show()

# Применение пайплайна для получения последних 100 записей
processed_dates, processed_sales = sales_pipeline_count_sales(dates_list, sales_list)

# Построение графика с использованием обработанных данных
plot_sales_count_sales(processed_dates, processed_sales)


#######################################################
## 2. Рост или падение продаж в сравнении с предыдущим периодом (в %)
#######################################################

def sales_pipeline_change_compared_prev_period(dates, sales):
    """
    Принимает два списка: даты и количество продаж.

    Вход:
    - dates: Список с датами (должен быть тип np.array или list).
    - sales: Список с количеством продаж (должен быть тип np.array или list).

    Выход:
    - Возвращает массив дат и продаж для построения графика, фильтрованные по последним 100 записям.
    """

    if not isinstance(dates, (list, np.ndarray)) or not isinstance(sales, (list, np.ndarray)):
        raise ValueError("На вход должны подаваться списки или массивы.")

    # Преобразуем списки в numpy массивы для удобства
    dates = pd.to_datetime(np.array(dates))  # Преобразуем даты в формат datetime
    sales = np.array(sales)

    # Фильтруем последние 100 записей по дате
    filtered_dates = dates[-100:]
    filtered_sales = sales[-100:]

    return filtered_dates, filtered_sales

##################### 2.1 График процентные изменения продаж по сравнению с предыдущим периодом для каждого дня (с подписями) ######################

# Преобразование колонок 'date' и 'cnt' в списки
dates_list = data['date'].tolist()  # Преобразуем даты в список
sales_list = data['cnt'].tolist()   # Преобразуем количество продаж в список

def plot_sales_change_compared_prev_period(dates, sales_change):
    """
    Строит интерактивный график изменения продаж с подписями пиков и обработкой одинаковых значений.

    Вход:
    - dates: Массив с датами.
    - sales_change: Массив с процентным изменением продаж.
    """

    fig = go.Figure()

    # Добавляем данные на график
    fig.add_trace(go.Scatter(
        x=dates,
        y=sales_change,
        mode='lines+markers',
        marker=dict(color='green', size=8),
        line=dict(color='green'),
        name='Изменение продаж (%)'
    ))

    # Логика для добавления подписей на максимумы и минимумы
    for i in range(1, len(sales_change) - 1):
        if (sales_change[i] > sales_change[i - 1] and sales_change[i] > sales_change[i + 1]) or \
                (sales_change[i] < sales_change[i - 1] and sales_change[i] < sales_change[i + 1]):
            fig.add_annotation(x=dates[i], y=sales_change[i],
                               text=f'{sales_change[i]:.1f}%', showarrow=True, arrowhead=2)

    # Обработка одинаковых последовательных значений (подпись в начале и в конце серии)
    previous_value = None
    repeat_series_start = None
    for i, value in enumerate(sales_change):
        if previous_value is None:
            previous_value = value
            continue

        # Если значение повторяется
        if value == previous_value:
            if repeat_series_start is None:
                repeat_series_start = i - 1  # Начало серии повторяющихся значений
        else:
            if repeat_series_start is not None:
                # Добавляем подпись в начале и в конце серии
                fig.add_annotation(x=dates[repeat_series_start], y=sales_change[repeat_series_start],
                                   text=f'{sales_change[repeat_series_start]:.1f}%', showarrow=True, arrowhead=2)
                fig.add_annotation(x=dates[i - 1], y=sales_change[i - 1],
                                   text=f'{sales_change[i - 1]:.1f}%', showarrow=True, arrowhead=2)
                repeat_series_start = None  # Сброс серии
            previous_value = value

    # Обработка последнего элемента
    if repeat_series_start is not None:
        fig.add_annotation(x=dates[repeat_series_start], y=sales_change[repeat_series_start],
                           text=f'{sales_change[repeat_series_start]:.1f}%', showarrow=True, arrowhead=2)
        fig.add_annotation(x=dates[-1], y=sales_change[-1],
                           text=f'{sales_change[-1]:.1f}%', showarrow=True, arrowhead=2)

    # Настраиваем внешний вид графика
    fig.update_layout(
        title="Рост/падение продаж с подписями пиков",
        xaxis_title="Дата",
        yaxis_title="Изменение продаж (%)",
        template="plotly_white",
        xaxis_tickformat='%b %d, %Y',
        xaxis_tickangle=-45
    )

    # Показать график
    fig.show()

# Применение пайплайна для получения последних 100 записей
processed_dates, processed_sales = sales_pipeline_change_compared_prev_period(dates_list, sales_list)

# Вычисление процентного изменения продаж с обработкой деления на ноль
sales_change = np.where(
    processed_sales[:-1] == 0,
    0,
    np.diff(processed_sales) / processed_sales[:-1] * 100
)

# Построение графика изменения продаж с подписями
plot_sales_change_compared_prev_period(processed_dates[1:], sales_change)


##################### 2.1 График процентные изменения продаж по сравнению с предыдущим периодом для каждого дня (цветные вершины) ######################

# Преобразование колонок 'date' и 'cnt' в списки
dates_list = data['date'].tolist()  # Преобразуем даты в список
sales_list = data['cnt'].tolist()   # Преобразуем количество продаж в список

def plot_sales_change_compared_color(dates, values, y_axis_title, graph_title):
    """
    Вход:
    - dates: Массив с датами.
    - values: Массив с изменениями (например, процент изменений или абсолютные значения).
    - y_axis_title: Название оси Y.
    - graph_title: Название графика.
    """

    fig = go.Figure()

    # Добавляем линию и метки на цветных вершинах
    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode='lines+markers',
        marker=dict(
            size=8,
            color=np.where(values > 0, 'green', np.where(values < 0, 'red', 'darkgoldenrod')),
        ),
        line=dict(color='gray'),
        name='Значения'
    ))

    # Логика для добавления подписей
    for i, (date, value) in enumerate(zip(dates, values)):
        if value != 0:
            fig.add_annotation(
                x=date,
                y=value,
                text=f'{value:.1f}%',
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-20
            )

    # Настраиваем оси и заголовок
    fig.update_layout(
        title=graph_title,
        xaxis_title="Дата",
        yaxis_title=y_axis_title,
        template="plotly_white",
        legend=dict(x=0.01, y=0.99)
    )

    # Отображение графика
    fig.show()

# Применение пайплайна для получения последних 100 записей
processed_dates, processed_sales = sales_pipeline_change_compared_prev_period(dates_list, sales_list)

# Пример вызова функции с аргументами
plot_sales_change_compared_color(
    processed_dates[1:],            # Даты
    sales_change,                   # Процентные изменения продаж
    "Изменение продаж (%)",         # Название оси Y
    "График процентных изменений продаж по сравнению с предыдущим периодом"  # Заголовок графика
)


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

# Преобразование колонок 'date' и 'cnt' в списки
dates_list = data['date'].tolist()  # Преобразуем даты в список
sales_list = data['cnt'].tolist()   # Преобразуем количество продаж в список


def plot_sales_speed_dynamics(dates, sales):
    """
    Вход:
    - dates: Массив с датами.
    - sales: Массив с количеством продаж.
    """

    fig = go.Figure()

    # Добавляем данные на график
    fig.add_trace(go.Scatter(
        x=dates,
        y=sales,
        mode='lines+markers',
        marker=dict(color='blue', size=8),
        line=dict(color='blue'),
        name='Продажи'
    ))

    # Настраиваем внешний вид графика
    fig.update_layout(
        title="Динамика продаж товара",
        xaxis_title="Дата",
        yaxis_title="Продажи",
        template="plotly_white",
        xaxis_tickformat='%b %Y',
        xaxis_tickangle=-45
    )

    # Показать график
    fig.show()

# Применение пайплайна для получения данных
resampled_dates, speed_sales, cumulative_sales = sales_pipeline_speed(dates_list, sales_list, period='M')

# Построение графика динамики продаж
plot_sales_speed_dynamics(resampled_dates, speed_sales)

##################### 3.2 Скорость продаж с цветовым градиентом ######################

# Преобразование колонок 'date' и 'cnt' в списки
dates_list = data['date'].tolist()  # Преобразуем даты в список
sales_list = data['cnt'].tolist()   # Преобразуем количество продаж в список


def plot_sales_speed_dynamics_color_dots(dates, speed_sales, color_scale='rainbow'):
    """
    Строит интерактивный график скорости продаж с цветовой шкалой.

    Вход:
    - dates: Массив с датами.
    - speed_sales: Массив со скоростью продаж.
    - color_scale: Цветовая шкала для скорости продаж
    """

    fig = go.Figure()

    # Добавляем линию с изменением цвета по градиенту скорости продаж
    fig.add_trace(go.Scatter(
        x=dates,
        y=speed_sales,
        mode='lines+markers',
        marker=dict(
            size=8,
            color=speed_sales,  # Цветовой градиент
            colorscale=color_scale,  # Выбранная цветовая шкала
            showscale=True,
            colorbar=dict(title="Скорость продаж")
        ),
        line=dict(color='black', width=2),
        name="Скорость продаж"
    ))

    # Настраиваем график
    fig.update_layout(
        title="Скорость продаж товара",
        xaxis_title="Дата",
        yaxis_title="Скорость продаж",
        template="plotly_white",
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGrey'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGrey'),
        font=dict(size=14, color='Black'),
    )

    fig.show()

# Применение пайплайна для получения данных
resampled_dates, speed_sales, cumulative_sales = sales_pipeline_speed(dates_list, sales_list, period='M')

# Построение графика динамики продаж
plot_sales_speed_dynamics_color_dots(resampled_dates, speed_sales)

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

# Преобразование колонок 'date' и 'cnt' в списки
dates_list = data['date'].tolist()  # Преобразуем даты в список
sales_list = data['cnt'].tolist()   # Преобразуем количество продаж в список


def plot_sales_peaks_area_grid(dates, sales_peaks):
    """
    Строит диаграмму пиков продаж по месяцам в виде сетки по годам.

    Вход:
    - dates: Массив с датами.
    - sales_peaks: Массив с пиками продаж.
    """

    # Преобразуем даты и создаем DataFrame для удобства фильтрации по годам
    data = pd.DataFrame({'Date': dates, 'Sales': sales_peaks})
    data['Year'] = data['Date'].dt.year
    unique_years = data['Year'].unique()

    # Задаем сетку 3x2
    rows, cols = 3, 2  # Сетка 3 строки и 2 столбца
    fig = make_subplots(
        rows=rows, cols=cols,
        subplot_titles=[f'Пики продаж за {year}' for year in unique_years]
    )

    # Построение графиков по каждому году
    for i, year in enumerate(unique_years):
        yearly_data = data[data['Year'] == year]

        # Индексы для расстановки графиков по сетке
        row = i // cols + 1
        col = i % cols + 1

        # Добавление данных на график
        fig.add_trace(go.Scatter(
            x=yearly_data['Date'],
            y=yearly_data['Sales'],
            fill='tozeroy',
            mode='lines+markers',
            marker=dict(color='blue'),
            line=dict(color='blue'),
            name=f'Пики продаж за {year}'
        ), row=row, col=col)

        # Добавление подписей на пиковые точки
        for date, peak in zip(yearly_data['Date'], yearly_data['Sales']):
            fig.add_annotation(x=date, y=peak, text=f'{peak:.1f}', showarrow=True, row=row, col=col)

    # Настройка макета
    fig.update_layout(
        title="Диаграмма пиков продаж по годам",
        template="plotly_white",
        height=1000,  # Увеличиваем высоту
        width=1500,  # Увеличиваем ширину
        margin=dict(t=50, l=50, r=50, b=50),  # Отступы
        font=dict(size=12)  # Увеличиваем размер шрифта
    )

    pio.show(fig)

# Вызов пайплайна для вычисления пиков продаж по месяцам
processed_dates, monthly_peaks = sales_pipeline_peaks_months(dates_list, sales_list, period='M')

# Построение диаграммы пиков продаж
plot_sales_peaks_area_grid(processed_dates, monthly_peaks)

##################### 4.2 Круговая диаграмма (Pie Chart) — по годам сетка ######################

# Преобразование колонок 'date' и 'cnt' в списки
dates_list = data['date'].tolist()  # Преобразуем даты в список
sales_list = data['cnt'].tolist()   # Преобразуем количество продаж в список


def plot_sales_peaks_months_pie_grid(dates, sales_peaks):
    """
    Вход:
    - dates: Массив с датами.
    - sales_peaks: Массив с пиками продаж.
    """

    # Преобразуем даты и создаем DataFrame для удобства фильтрации по годам
    data = pd.DataFrame({'Date': dates, 'Sales': sales_peaks})
    data['Year'] = data['Date'].dt.year
    unique_years = data['Year'].unique()

    # Убираем пустой график, если количество лет меньше чем 6
    rows, cols = (len(unique_years) + 2) // 3, 3

    # Создаем сетку с типом подграфиков "domain" для круговых диаграмм
    fig = make_subplots(
        rows=rows, cols=3,
        specs=[[{'type': 'domain'} for _ in range(3)] for _ in range(rows)],
        subplot_titles=[f'Пики продаж за {year}' for year in unique_years]
    )

    # Построение круговых диаграмм по каждому году
    for i, year in enumerate(unique_years):
        yearly_data = data[data['Year'] == year]

        # Индексы для расстановки графиков по сетке
        row = i // 3 + 1
        col = i % 3 + 1

        # Добавление данных на круговую диаграмму
        fig.add_trace(go.Pie(
            labels=yearly_data['Date'].dt.strftime('%b'),
            values=yearly_data['Sales'],
            hole=0.3,
            textinfo='label+percent',
            showlegend=False
        ), row=row, col=col)

    # Настройка макета с увеличенным отступом сверху
    fig.update_layout(
        title="Круговые диаграммы пиков продаж по годам",
        template="plotly_white",
        height=700,  # Увеличим высоту для большего отступа
        margin=dict(t=100, l=10, r=10, b=10)  # Увеличиваем отступ сверху (t=100)
    )

    # Показываем график
    fig.show()

# Вызов пайплайна для вычисления пиков продаж по месяцам
processed_dates, monthly_peaks = sales_pipeline_peaks_months(dates_list, sales_list, period='MS')

# Построение круговой диаграммы пиков продаж по годам
plot_sales_peaks_months_pie_grid(processed_dates, monthly_peaks)

##################### 4.3 Обычный ######################

# Преобразование колонок 'date' и 'cnt' в списки
dates_list = data['date'].tolist()  # Преобразуем даты в список
sales_list = data['cnt'].tolist()   # Преобразуем количество продаж в список


def plot_sales_peaks_months_line(dates, sales_peaks):
    """
    Вход:
    - dates: Массив с датами.
    - sales_peaks: Массив с пиками продаж.
    """

    # Создание линейного графика
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=sales_peaks,
        mode='lines+markers',
        line=dict(color='blue'),
        marker=dict(size=8, color='blue'),
        name='Пики продаж'
    ))

    # Добавление подписей на пиковые точки
    for date, peak in zip(dates, sales_peaks):
        fig.add_annotation(x=date, y=peak, text=f'{peak:.1f}', showarrow=True, ax=0, ay=-20)

    # Настройка макета
    fig.update_layout(
        title="Пики продаж (месяц)",
        xaxis_title="Дата",
        yaxis_title="Максимальные продажи (единиц/месяц)",
        template="plotly_white",
        height=600,
        width=1000
    )

    pio.show(fig)

# Вызов пайплайна для вычисления пиков продаж по месяцам
processed_dates, monthly_peaks = sales_pipeline_peaks_months(dates_list, sales_list, period='MS')

plot_sales_peaks_months_line(processed_dates, monthly_peaks)






