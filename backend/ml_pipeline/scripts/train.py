import hydra
from omegaconf import DictConfig
import lightgbm as lgb
import pandas as pd
from sklearn.model_selection import GridSearchCV
from backend.ml_pipeline.preprocess_for_inference import calculate_features_for_inference
from backend.ml_pipeline.configs.feature_params import one_day_params
from backend.ml_pipeline.model import LGBMModel


def run_training_with_grid_search(data: pd.DataFrame, config: DictConfig, use_grid_search: bool = False):
    # Shift target
    data['Y'] = data['cnt'].shift(-1)
    data = data.dropna()

    # Split the data into train and val
    train_size = int(len(data) * 0.8)
    train_data = data[:train_size]
    val_data = data[train_size:]

    # Separate data into features (X) and target (Y)
    X_train = train_data.drop(columns=['Y'])
    Y_train = train_data['Y']
    X_val = val_data.drop(columns=['Y'])
    Y_val = val_data['Y']

    # Prepare parameter dictionary without conflicts
    params = {
        'num_leaves': config.num_leaves,
        'learning_rate': config.learning_rate,
        'feature_fraction': config.feature_fraction,  # Keep only feature_fraction for LightGBM
        'max_depth': config.max_depth,
        'verbose': config.verbose,
        'early_stopping_rounds': config.early_stopping_rounds,  # Keep only early_stopping_rounds
        'n_jobs': config.nthread
    }

    # Initialize the LGBM model
    lgb_model = LGBMModel(**params)

    # Case 1: Normal training without grid search
    if not use_grid_search:
        # Fit the model with validation data for early stopping
        lgb_model.fit(X_train, Y_train, X_val=X_val, y_val=Y_val)
        val_pred = lgb_model.predict(X_val)
        print("Validation Predictions: ", val_pred)

    # Case 2: Training with grid search
    else:
        grid_search = GridSearchCV(
            estimator=lgb_model,
            param_grid={'num_leaves': [10, 20, 30], 
                        'learning_rate': [0.001, 0.01, 0.1],
                        'feature_fraction': [0.6, 0.8, 1.0], 
                        'max_depth': [5, 10, 15], 'n_estimators': [100, 500, 1000]
                        },
            cv=config.grid_search.cross_validation,
            scoring=config.grid_search.scoring,
            verbose=config.grid_search.verbose,
            n_jobs=config.grid_search.n_jobs
        )

        # Run grid search on training data
        grid_search.fit(X_train, Y_train)

        # Output best parameters and CV score
        print(f"Best parameters found: {grid_search.best_params_}")
        print(f"Best CV score: {grid_search.best_score_}")

        # Retrieve the best model from the grid search
        best_model = grid_search.best_estimator_

        # Evaluate the best model on validation data
        val_pred = best_model.predict(X_val)
        print("Validation Predictions after Grid Search: ", val_pred)

        # Optionally, save the best model
        best_model.save_model('best_lgb_model.txt')

@hydra.main(version_base=None, config_path="../configs", config_name="training_default.yaml")
def main(config: DictConfig):
    """
    Examples of how to run:
    
    python use_cases/hydra_with_pydantic.py
    python use_cases/hydra_with_pydantic.py -cn training_default.yaml
    python use_cases/hydra_with_pydantic.py batch_size=128
    """
    # Load data
    data = pd.read_csv(config.train_data_path)
    data = data[['cnt', 'date']]  # Using only the relevant columns

    # Feature generation
    if config.granularity == 'one_day':
        day_params = one_day_params

    # Generate features and drop date column
    data_with_features = calculate_features_for_inference(data=data, params=day_params)
    data_with_features = data_with_features.drop(columns=['date'])
    data = data_with_features.copy()

    # Run training or grid search based on the config
    run_training_with_grid_search(data, config, use_grid_search=config.use_grid_search)


if __name__ == "__main__":
    main()
