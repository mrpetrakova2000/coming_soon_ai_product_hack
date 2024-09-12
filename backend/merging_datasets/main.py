import pandas as pd
from backend.merging_datasets.preprocessing import prepare_shop_sales, prepare_shop_sales_dates, prepare_shop_sales_prices
from backend.merging_datasets.utils import load_dataset, safe_merge

def merging(shop_sales_path, shop_sales_dates_path, shop_sales_prices_path):
    shop_sales = load_dataset(shop_sales_path)
    shop_sales_dates = load_dataset(shop_sales_dates_path)
    shop_sales_prices = load_dataset(shop_sales_prices_path)

    # Convert data types, fill NaNs in categorical columns
    shop_sales_processed = prepare_shop_sales(shop_sales)
    shop_sales_dates_processed = prepare_shop_sales_dates(shop_sales_dates)
    shop_sales_prices_processed = prepare_shop_sales_prices(shop_sales_prices)

    # Merge the datasets
    merged_df = safe_merge(shop_sales_processed, shop_sales_dates_processed, shop_sales_prices_processed)
    merged_df = merged_df.set_index('date').resample('D').apply(lambda x: x).reset_index()

    if len(merged_df[merged_df.cnt == 0]) / len(merged_df) > 0.5 or merged_df.cnt.isna().sum() / len(merged_df) > 0.5:
    ### Возвращаем датасет пользователю
        return None
    else:
        cat_cols = ['item_id', 'store_id', 'cashback_store_1', 'cashback_store_2', 'cashback_store_3']
        num_cols = ['cnt', 'sell_price', 'wday', 'month', 'year']
        event_cat_cols = ['event_name_1', 'event_type_1', 'event_name_2', 'event_type_2']
        for col in cat_cols:
            merged_df.loc[:,col] = merged_df[col].fillna('ffill')
            merged_df.loc[:,col] = merged_df[col].fillna('bfill')
        for col in num_cols:
            merged_df.loc[:,col] = merged_df[col].interpolate()
        for col in event_cat_cols:
            merged_df.loc[:,col] = merged_df[col].fillna('Unknown')
        return merged_df
