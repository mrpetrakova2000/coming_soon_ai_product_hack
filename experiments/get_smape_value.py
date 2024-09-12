import pandas as pd
import numpy as np
import argparse
import matplotlib.pyplot as plt

def smape(actual, predicted):
    denominator = (np.abs(actual) + np.abs(predicted)) / 2
    diff = np.abs(actual - predicted)
    return np.mean(diff / denominator) * 100

def get_smape_value(data, num_previous_days):
    data = data.rename(columns={'cnt': 'sales'})
    data = data[['date', 'sales']]
    data.loc[:, 'prediction'] = data.loc[:, 'sales'].rolling(window=num_previous_days).mean().shift(1).round()
    data = data[data['prediction'].notna()]
    smape_value = smape(data['sales'], data['prediction'])

    return smape_value, data

def visualize_data(data):
    data['date'] = pd.to_datetime(data['date'])
    
    data_to_visualize = data.tail(250)
    
    plt.figure(figsize=(10, 6))
    
    # Plot sales (original) and predictions as continuous time-series lines
    plt.plot(data_to_visualize['date'], data_to_visualize['sales'], label='Original Sales', color='blue', linestyle='-')
    plt.plot(data_to_visualize['date'], data_to_visualize['prediction'], label='Prediction', color='red', linestyle='-')
    
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.title('Original vs Prediction')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Sales Prediction using Rolling Mean and SMAPE Calculation")
    parser.add_argument('csv_file', type=str, help='Path to the CSV file containing sales data')
    parser.add_argument('num_previous_days', type=int, help='Number of previous days for calculating rolling mean')
    parser.add_argument('--visualize', action='store_true', help='Visualize the original vs prediction data')
    
    args = parser.parse_args()

    data = pd.read_csv(args.csv_file)
    num_previous_days = args.num_previous_days

    smape_value, processed_data = get_smape_value(data, num_previous_days)

    # Print SMAPE Value
    print(f"SMAPE Value : {smape_value:.2f}%")

    # Visualize the data if --visualize is passed
    if args.visualize:
        visualize_data(processed_data)

if __name__ == '__main__':
    main()
