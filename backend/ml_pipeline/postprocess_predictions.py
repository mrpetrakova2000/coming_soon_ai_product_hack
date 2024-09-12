import pandas as pd

def get_future_dates(date_str):
    # Convert the input string to a pandas datetime object
    date = pd.to_datetime(date_str)
    
    # Calculate future dates
    one_day_later = date + pd.DateOffset(days=1)
    seven_days_later = date + pd.DateOffset(days=7)
    thirty_days_later = date + pd.DateOffset(days=30)
    
    # Return the results as a tuple
    return one_day_later, seven_days_later, thirty_days_later



def postproces_predictions(initial_data: pd.DataFrame, pred_1_d, pred_7_d, pred_30_d):
    """Return the updated dataframe with cnt and date, including predictions for future dates.

    Input: 
        - initial_data: pd.DataFrame with columns 'cnt' and 'date'
        - pred_1_d: Prediction value for 1 day ahead
        - pred_7_d: Prediction value for 7 days ahead
        - pred_30_d: Prediction value for 30 days ahead
    """
    
    last_date = initial_data[['date']].iloc[-1]['date']
    day_1, day_7, day_30 = get_future_dates(last_date)

    future_data = pd.DataFrame({
        'date': [day_1, day_7, day_30],
        'cnt': [pred_1_d, pred_7_d, pred_30_d]
    })
    
    
    return future_data

    
