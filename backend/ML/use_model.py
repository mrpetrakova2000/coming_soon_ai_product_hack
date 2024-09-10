from dataset import LGBMDataset
from backend.ml_pipeline.model import LGBMModel

# Example usage
file_path = 'path/to/your/data.csv'
dataset = LGBMDataset(file_path)

# Instantiate and train the model
model = LGBMModel()
model.train(dataset.lgbtrain, dataset.lgbval)

# Make predictions
predictions = model.predict(dataset.X_val)

# Save and load the model
model.save_model('lgbm_model.txt')
model.load_model('lgbm_model.txt')
