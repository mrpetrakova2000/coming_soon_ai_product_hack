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

def fill_missing_values_shop_sales(initial_df):

    df = initial_df.reset_index(drop=True)
    df['date_id'] = pd.to_numeric(df['date_id'], errors='coerce').astype(float)
    df['item_id'] = df['item_id'].astype(str)
    df['store_id'] = df['store_id'].astype(str)
    df['cnt'] = pd.to_numeric(df['cnt'], errors='coerce').astype(float)
    df['date_id'] = df['date_id'].interpolate()
    max_date_id = df['date_id'].max() 


    if df['item_id'].isna().sum() > 0:  
        for i in range(len(df)):
            if pd.isna(df.at[i, 'item_id']):
                if df.at[i, 'date_id'] == 1:
                    df.at[i, 'item_id'] = df.at[i + 1, 'item_id'] if i + 1 < len(df) else df.at[i - 1, 'item_id']
                elif df.at[i, 'date_id'] == max_date_id:
                    df.at[i, 'item_id'] = df.at[i - 1, 'item_id']
                else:
                    df.at[i, 'item_id'] = df.at[i - 1, 'item_id']

    if df['store_id'].isna().sum() > 0:
        df['store_id'] = df['item_id'].str.split('_').str[0] + '_' + df['item_id'].str.split('_').str[1]

    return df


def preprocess_shop_sales_dates(initial_df):

    df = initial_df.reset_index(drop=True)
    df['date_id'] = pd.to_numeric(df['date_id'], errors='coerce')
    df['wm_yr_wk'] = pd.to_numeric(df['wm_yr_wk'], errors='coerce').astype(int)
    df['wday'] = pd.to_numeric(df['wday'], errors='coerce').astype(int)
    df['month'] = pd.to_numeric(df['month'], errors='coerce').astype(int)
    df['year'] = pd.to_numeric(df['year'], errors='coerce').astype(int)
    df['cashback_store_1'] = pd.to_numeric(df['cashback_store_1'], errors='coerce').astype(float)
    df['cashback_store_2'] = pd.to_numeric(df['cashback_store_2'], errors='coerce').astype(float)
    df['cashback_store_3'] = pd.to_numeric(df['cashback_store_3'], errors='coerce').astype(float)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    df['date_id'] = df['date_id'].interpolate(method='linear')

    df = df.drop(columns=['weekday'])

    df['wday'] = df['wday'].fillna(df['date'].dt.dayofweek + 1)
    df['month'] = df['month'].fillna(df['date'].dt.month)
    df['year'] = df['year'].fillna(df['date'].dt.year)

    event_cols = ['event_name_1', 'event_type_1', 'event_name_2', 'event_type_2']
    df[event_cols] = df[event_cols].fillna('Unknown')

    cashback_cols = ['cashback_store_1', 'cashback_store_2', 'cashback_store_3']
    df[cashback_cols] = df[cashback_cols].fillna(0)

    return df

def preprocess_shop_sales_prices(initial_df):

    df = initial_df.reset_index(drop=True)

    df['wm_yr_wk'] = pd.to_numeric(df['wm_yr_wk'], errors='coerce').astype(float)
    df['sell_price'] = pd.to_numeric(df['sell_price'], errors='coerce').astype(float)

    max_item_id = df['item_id'].max()

    if df['item_id'].isna().sum() > 0: 
        for i in range(1, len(df)):
            if pd.isna(df.at[i, 'item_id']):
                if df.at[i, 'wm_yr_wk'] == 1:
                    df.at[i, 'item_id'] = df.at[i + 1, 'item_id'] if i + 1 < len(df) else df.at[i - 1, 'item_id']
                elif df.at[i, 'wm_yr_wk'] == max_item_id:
                    df.at[i, 'item_id'] = df.at[i - 1, 'item_id']
                else:
                    df.at[i, 'item_id'] = df.at[i - 1, 'item_id']

    if df['store_id'].isna().sum() > 0:
        df['store_id'] = df['item_id'].str.split('_').str[0] + '_' + df['item_id'].str.split('_').str[1]

    df['wm_yr_wk'] = df['wm_yr_wk'].interpolate(method='linear').round(0)
    df = df.sort_values(by=['item_id', 'wm_yr_wk']).reset_index(drop=True)
    df['sell_price'] = df['sell_price'].interpolate(method='linear')

    return df

def safe_merge(shop_sales, shop_sales_dates, shop_sales_prices):
    try:
        shop_sales.columns = shop_sales.columns.str.lower()
        shop_sales_dates.columns = shop_sales_dates.columns.str.lower()
        shop_sales_prices.columns = shop_sales_prices.columns.str.lower()
        
        merged_df = pd.merge(shop_sales, shop_sales_dates, how='outer', left_on='date_id', right_on='date_id')

        merged_df['item_id_wm_yr_wk'] = merged_df.item_id.astype(str) + '_' + merged_df.wm_yr_wk.astype(float).astype(str)
        shop_sales_prices['item_id_wm_yr_wk'] = shop_sales_prices.item_id.astype(str) + '_' + shop_sales_prices.wm_yr_wk.astype(float).astype(str)

        map_prices_dict = dict(tuple(zip(shop_sales_prices.item_id_wm_yr_wk, shop_sales_prices.sell_price)))
        merged_df['sell_price'] = merged_df.item_id_wm_yr_wk.map(map_prices_dict)

        merged_df.sort_values(by=['item_id', 'date_id'], inplace=True)
        merged_df.drop(columns=['item_id_wm_yr_wk'], inplace=True)

        merged_df.to_csv('merged_df.csv')
    
    except ValueError as e:
        raise ValueError(f"Error in merging process: {e}")
    
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")



def main(shop_sales_path, shop_sales_dates_path, shop_sales_prices_path):

    shop_sales = load_dataset(shop_sales_path)
    shop_sales_dates = load_dataset(shop_sales_dates_path)
    shop_sales_prices = load_dataset(shop_sales_prices_path)

    shop_sales_processed = fill_missing_values_shop_sales(shop_sales)
    shop_sales_dates_processed = preprocess_shop_sales_dates(shop_sales_dates)
    shop_sales_prices_processed = preprocess_shop_sales_prices(shop_sales_prices)

    safe_merge(shop_sales_processed, shop_sales_dates_processed, shop_sales_prices_processed)


if __name__ == '__main__':
    main('./data/shop_sales.csv', './data/shop_sales_dates.csv', './data/shop_sales_prices.csv')
