import pandas as pd

def load_dataset(df_name):
    try:
        if not df_name.endswith('.csv'):
            raise ValueError("Only CSV files are supported.")
        df = pd.read_csv(df_name)
        if df.empty:
            raise ValueError(f"The dataset '{df_name}' is empty.")
        if len(df.columns) == 1:
            raise ValueError(f"The file '{df_name}' might have an incorrect separator.")
        df.columns = df.columns.str.lower()
        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{df_name}' was not found.")
    except pd.errors.EmptyDataError:
        raise ValueError(f"The file '{df_name}' is empty or contains only headers.")
    except pd.errors.ParserError:
        raise ValueError(f"There was an error parsing the file '{df_name}'.")
    except UnicodeDecodeError:
        raise ValueError(f"Failed to decode the file '{df_name}'.")
    except Exception as e:
        raise ValueError(f"An unexpected error occurred: {e}")
    
def safe_merge(shop_sales, shop_sales_dates, shop_sales_prices):
    try:
        shop_sales.columns = shop_sales.columns.str.lower()
        shop_sales_dates.columns = shop_sales_dates.columns.str.lower()
        shop_sales_prices.columns = shop_sales_prices.columns.str.lower()

        if 'date_id' not in shop_sales.columns:
            raise ValueError("'date_id' column is missing in 'shop_sales' dataset.")
        if 'date_id' not in shop_sales_dates.columns:
            raise ValueError("'date_id' column is missing in 'shop_sales_dates' dataset.")
        
        merged_df = pd.merge(shop_sales, shop_sales_dates, how='outer', left_on='date_id', right_on='date_id')
        merged_df['item_id_wm_yr_wk'] = merged_df.item_id.astype(str) + '_' + merged_df.wm_yr_wk.astype(float).astype(str)
        shop_sales_prices['item_id_wm_yr_wk'] = shop_sales_prices.item_id.astype(str) + '_' + shop_sales_prices.wm_yr_wk.astype(float).astype(str)
        map_prices_dict = dict(tuple(zip(shop_sales_prices.item_id_wm_yr_wk, shop_sales_prices.sell_price)))
        merged_df['sell_price'] = merged_df.item_id_wm_yr_wk.map(map_prices_dict)

        merged_df.sort_values(by=['item_id', 'date_id'], inplace=True)
        merged_df.drop(columns=['item_id_wm_yr_wk'], inplace=True)

        return merged_df
    
    except ValueError as e:
        raise ValueError(f"Error in merging process: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")

    
