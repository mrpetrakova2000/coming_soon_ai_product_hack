import pandas as pd

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

def plot_sales(dates, sales):
    df = pd.DataFrame({'Дата': dates, 'Продажи': sales})

    # Используем Plotly для построения линейного графика
    fig = px.line(df, x='Дата', y='Продажи',
                  title='Количество продаж товара за указанный период',
                  labels={'Дата': 'Дата', 'Продажи': 'Количество продаж'},
                  markers=True)

    # Настройки осей и разметки
    fig.update_xaxes(title_text='Дата', tickangle=45)
    fig.update_yaxes(title_text='Количество продаж')
    fig.update_layout(title_x=0.5)


    fig.show()

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