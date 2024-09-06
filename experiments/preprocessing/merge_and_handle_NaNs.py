import pandas as pd

def load_dataset(df_name):
    if not df_name.endswith('.csv'):
        raise ValueError("Only CSV files are supported.")
    try:
        df = pd.read_csv(df_name)
        if df.empty or len(df.columns) == 1:
            raise ValueError(f"Error in file '{df_name}' - empty or incorrect separator.")
        df.columns = df.columns.str.lower()
        return df
    except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError) as e:
        raise ValueError(f"Error loading file '{df_name}': {e}")

def fill_missing_values_shop_sales(df):
    df['date_id'] = pd.to_numeric(df['date_id'], errors='coerce')
    df['cnt'] = pd.to_numeric(df['cnt'], errors='coerce')
    df[['item_id', 'store_id']] = df[['item_id', 'store_id']].astype(str)

    max_date_id = df['date_id'].max()
    for i in range(1, len(df)):
        if pd.isna(df.at[i, 'date_id']):
            if pd.isna(df.at[i - 1, 'date_id']):
                raise ValueError(f"Consecutive NaN in 'date_id' at index {i}")
            df.at[i, 'date_id'] = 1 if df.at[i - 1, 'date_id'] == max_date_id else df.at[i - 1, 'date_id'] + 1

    df['item_id'].fillna(method='ffill', inplace=True)
    df['store_id'] = df['item_id'].str.split('_').str[0]

    return df

def preprocess_shop_sales_dates(df):
    df = df.drop(columns=['weekday']).reset_index(drop=True)
    df[['wm_yr_wk', 'wday', 'month', 'year']] = df[['wm_yr_wk', 'wday', 'month', 'year']].apply(pd.to_numeric, errors='coerce')
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    df['date_id'] = df['date_id'].interpolate().fillna(method='ffill')
    df['date'] = df['date'].interpolate().fillna(method='ffill')
    df['wday'], df['month'], df['year'] = df['date'].dt.weekday + 1, df['date'].dt.month, df['date'].dt.year

    df[['event_name_1', 'event_type_1', 'event_name_2', 'event_type_2']] = df[['event_name_1', 'event_type_1', 'event_name_2', 'event_type_2']].fillna('Unknown')
    df[['cashback_store_1', 'cashback_store_2', 'cashback_store_3']] = df[['cashback_store_1', 'cashback_store_2', 'cashback_store_3']].fillna(0)

    return df

def preprocess_shop_sales_prices(df):
    df[['wm_yr_wk', 'sell_price']] = df[['wm_yr_wk', 'sell_price']].apply(pd.to_numeric, errors='coerce')
    df['wm_yr_wk'] = df['wm_yr_wk'].interpolate().round().fillna(method='ffill')
    df.sort_values(by=['item_id', 'wm_yr_wk'], inplace=True)
    df['sell_price'] = df['sell_price'].interpolate()
    return df

def safe_merge(shop_sales, shop_sales_dates, shop_sales_prices):
    for df in [shop_sales, shop_sales_dates, shop_sales_prices]:
        df.columns = df.columns.str.lower()

    merged_df = pd.merge(shop_sales, shop_sales_dates, on='date_id', how='outer')

    merged_df['item_id_wm_yr_wk'] = merged_df['item_id'] + '_' + merged_df['wm_yr_wk'].astype(str)
    shop_sales_prices['item_id_wm_yr_wk'] = shop_sales_prices['item_id'] + '_' + shop_sales_prices['wm_yr_wk'].astype(str)

    merged_df['sell_price'] = merged_df['item_id_wm_yr_wk'].map(shop_sales_prices.set_index('item_id_wm_yr_wk')['sell_price'])
    merged_df.sort_values(by=['item_id', 'date_id'], inplace=True)
    merged_df.drop(columns=['item_id_wm_yr_wk'], inplace=True)

    return merged_df

def main(shop_sales_path, shop_sales_dates_path, shop_sales_prices_path):
    shop_sales = load_dataset(shop_sales_path)
    shop_sales_dates = load_dataset(shop_sales_dates_path)
    shop_sales_prices = load_dataset(shop_sales_prices_path)

    shop_sales_processed = fill_missing_values_shop_sales(shop_sales)
    shop_sales_dates_processed = preprocess_shop_sales_dates(shop_sales_dates)
    shop_sales_prices_processed = preprocess_shop_sales_prices(shop_sales_prices)

    return safe_merge(shop_sales_processed, shop_sales_dates_processed, shop_sales_prices_processed)


if __name__ == '__main__':
    main('./data/shop_sales.csv', './data/shop_sales_dates.csv', './data/shop_sales_prices.csv')
