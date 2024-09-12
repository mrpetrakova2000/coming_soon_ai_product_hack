import pandas as pd
from preprocessing import prepare_shop_sales, prepare_shop_sales_dates, prepare_shop_sales_prices
from utils import load_dataset, safe_merge

# Load datasets (user uploads the files)
def merging(shop_sales_path, shop_sales_dates_path, shop_sales_prices_path):
    shop_sales = load_dataset(shop_sales_path)
    shop_sales_dates = load_dataset(shop_sales_dates_path)
    shop_sales_prices = load_dataset(shop_sales_prices_path)

    # Preprocess each dataset
    shop_sales_processed = prepare_shop_sales(shop_sales)
    shop_sales_dates_processed = prepare_shop_sales_dates(shop_sales_dates)
    shop_sales_prices_processed = prepare_shop_sales_prices(shop_sales_prices)

    # Merge the datasets
    merged_df = safe_merge(shop_sales_processed, shop_sales_dates_processed, shop_sales_prices_processed)
    print(merged_df.head())

    return merged_df

merging('shop_sales.csv', 'shop_sales_dates.csv', 'shop_sales_prices.csv')