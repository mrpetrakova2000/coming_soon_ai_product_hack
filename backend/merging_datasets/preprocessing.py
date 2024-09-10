import pandas as pd

def prepare_shop_sales(shop_sales):
    df = shop_sales.reset_index(drop=True)
    df['date_id'] = pd.to_numeric(df['date_id'], errors='coerce').astype(float)
    df['item_id'] = df['item_id'].astype(str)
    df['store_id'] = df['store_id'].astype(str)
    df['cnt'] = pd.to_numeric(df['cnt'], errors='coerce').astype(float)
    return df

def prepare_shop_sales_dates(shop_sales_dates):
    df = shop_sales_dates.reset_index(drop=True)
    df['date_id'] = pd.to_numeric(df['date_id'], errors='coerce').astype(float)
    df['wm_yr_wk'] = pd.to_numeric(df['wm_yr_wk'], errors='coerce').astype(int)
    df['wday'] = pd.to_numeric(df['wday'], errors='coerce').astype(int)
    df['month'] = pd.to_numeric(df['month'], errors='coerce').astype(int)
    df['year'] = pd.to_numeric(df['year'], errors='coerce').astype(int)
    df['cashback_store_1'] = pd.to_numeric(df['cashback_store_1'], errors='coerce').astype(float)
    df['cashback_store_2'] = pd.to_numeric(df['cashback_store_2'], errors='coerce').astype(float)
    df['cashback_store_3'] = pd.to_numeric(df['cashback_store_3'], errors='coerce').astype(float)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    df = df.drop(columns=['weekday'])

    event_cols = ['event_name_1', 'event_type_1', 'event_name_2', 'event_type_2']
    df[event_cols] = df[event_cols].fillna('Unknown')

    cashback_cols = ['cashback_store_1', 'cashback_store_2', 'cashback_store_3']
    df[cashback_cols] = df[cashback_cols].fillna(0)

    return df

def prepare_shop_sales_prices(shop_sales_prices):
    df = shop_sales_prices.reset_index(drop=True)
    df['wm_yr_wk'] = pd.to_numeric(df['wm_yr_wk'], errors='coerce').astype(float)
    df['sell_price'] = pd.to_numeric(df['sell_price'], errors='coerce').astype(float)
    df = df.sort_values(by=['item_id', 'wm_yr_wk']).reset_index(drop=True)
    return df