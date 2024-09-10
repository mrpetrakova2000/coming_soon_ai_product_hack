from dataset import LGBMDataset
from model import LGBMModel

# Example usage
file_path = 'test.csv'
dataset = LGBMDataset(file_path, training_mode=False)

# Instantiate and train the model
model = LGBMModel()
# model.train(dataset.lgbtrain, dataset.lgbval)

# Make predictions

# Save and load the model
# model.save_model('lgbm_model.txt')
model.load_model('lgbm_model.txt')

predictions = model.predict(dataset.data)
print(predictions[:10])
