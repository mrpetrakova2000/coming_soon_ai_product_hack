import lightgbm as lgb
from lightgbm import LGBMRegressor
from backend.ml_pipeline.metrics import lgbm_smape

class LGBMModel:
    def __init__(self, **params):
        # Initialize the LGBMRegressor with parameters
        self.model = LGBMRegressor(**params)

    # Train the model (normal training)
    def fit(self, X_train, y_train, X_val=None, y_пшеval=None):
        if X_val is not None and y_val is not None:
            # If validation data is provided, use early stopping
            self.model.fit(X_train, y_train, eval_set=[(X_val, y_val)], eval_metric=lgbm_smape, early_stopping_rounds=10)
        else:
            # If no validation data, train without early stopping
            self.model.fit(X_train, y_train)

    # Predict method to make predictions
    def predict(self, X):
        return self.model.predict(X)

    # Get parameters (needed for GridSearchCV)
    def get_params(self, deep=True):
        return self.model.get_params(deep)

    # Set parameters (needed for GridSearchCV)
    def set_params(self, **params):
        return self.model.set_params(**params)

    # Save the model to file
    def save_model(self, file_name):
        self.model.booster_.save_model(file_name)

    # Load the model from file
    def load_model(self, file_name):
        self.model = lgb.Booster(model_file=file_name)
