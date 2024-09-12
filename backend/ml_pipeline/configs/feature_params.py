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

seven_day_params = {
        'target_column': 'cnt',               
        'datetime_column': 'date',
        'shift': 7,               
        'lag_range': (1, 30),     
        'lag_difference': (1, 30),
        'rolling_mean_range': (5, 30),
        'rolling_std_range': (5, 30), 
        'day_of_week': True,          
        'month': True,                
        'hour': False                 
}

thirty_day_params = {
        'target_column': 'cnt',
        'datetime_column': 'date',
        'shift': 30,              
        'lag_range': (1, 90),     
        'lag_difference': (1, 90),
        'rolling_mean_range': (7, 90),
        'rolling_std_range': (7, 90), 
        'day_of_week': False,         
        'month': True,                
        'hour': False                 
}
