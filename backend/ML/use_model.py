from dataset import LGBMDataset
from model import LGBMModel
from merging_datasets.merging import merging

# Example usage
file_path1 = 'shop_sales.csv'
file_path2 = 'shop_sales_dates.csv'
file_path3 = 'shop_sales_prices.csv'

dataset = LGBMDataset(merging(file_path1, file_path2, file_path3))

# Instantiate and train the model
model = LGBMModel()
model.train(dataset.lgbtrain, dataset.lgbval)

# Make predictions
predictions = model.predict(dataset.X_val)

# Save and load the model
model.save_model('lgbm_model.txt')
model.load_model('lgbm_model.txt')
