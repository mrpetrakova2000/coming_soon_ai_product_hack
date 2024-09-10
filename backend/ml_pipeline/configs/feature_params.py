one_day_params = {
        'target_column': 'cnt',
        'datetime_column': 'date',
        'shift': 1,
        'lag_range': (1, 10),
        'lag_difference': (1, 10),
        'rolling_mean_range': (5, 10),
        'rolling_std_range': (5, 10),
        'day_of_week': True,
        'month': True, 
        'hour': False
}