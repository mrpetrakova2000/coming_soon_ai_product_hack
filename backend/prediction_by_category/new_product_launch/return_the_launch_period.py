import numpy as np
import pandas as pd

def launch_plot(family):
    df = pd.read_csv('backend/prediction_by_category/data_categories/data_' + family + '.csv', index_col=0).set_index('date')
    df.index = pd.to_datetime(df.index)
    weekly_sales = df['cnt'].resample('W').mean()
    values = weekly_sales[:60].values
    X = [f'Week {i + 1}' for i in range(60)]
    graph_data = pd.DataFrame({'Week': X, 'Sales': values})
    print(graph_data)
    return graph_data