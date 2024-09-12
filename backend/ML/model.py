import lightgbm as lgb
from backend.ML.metrics import lgbm_smape

class LGBMModel:
    def __init__(self, params=None):
        self.default_params = {
            'num_leaves': 10,
            'learning_rate': 0.01,
            'feature_fraction': 0.8,
            'max_depth': 5,
            'verbose': 0,
            'num_boost_round': 1000,
            'early_stopping_rounds': 3,
            'nthread': -1
        }
        self.params = params if params is not None else self.default_params
        self.model = None

    def train(self, lgbtrain, lgbval=None, callbacks=None):
        default_callbacks = [lgb.early_stopping(stopping_rounds=self.params.get('early_stopping_rounds', 3))]
        if callbacks is None:
            callbacks = default_callbacks
        else:
            callbacks = callbacks + default_callbacks
        
        self.model = lgb.train(
            params=self.params,
            train_set=lgbtrain,
            valid_sets=[lgbval] if lgbval is not None else None,
            num_boost_round=self.params['num_boost_round'],
            callbacks=callbacks,
            feval=lgbm_smape
        )

    def predict(self, X):
        if self.model is None:
            raise RuntimeError("Model has not been trained yet.")
        return self.model.predict(X, num_iteration=self.model.best_iteration)

    def save_model(self, file_name):
        if self.model is None:
            raise RuntimeError("Model has not been trained yet.")
        self.model.save_model(file_name, num_iteration=self.model.best_iteration)

    def load_model(self, file_name):
        self.model = lgb.Booster(model_file=file_name)
