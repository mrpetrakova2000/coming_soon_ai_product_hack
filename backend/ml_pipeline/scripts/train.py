import hydra
from omegaconf import DictConfig
import lightgbm as lgb
import pandas as pd


from backend.ml_pipeline.preprocess_for_inference import calculate_features_for_inference 
from backend.ml_pipeline.configs.feature_params import one_day_params
from backend.ml_pipeline.model import LGBMModel


def run_training(data: pd.DataFrame, config: DictConfig):
    # shift target 
    data['Y'] = data['cnt'].shift(-1)
    data = data.dropna()

    # split the data into train and val
    train_size = int(len(data) * 0.8)
    train_data = data[:train_size]
    val_data = data[train_size:]

    # Separate data
    X_train = train_data.drop(columns=['Y'])
    Y_train = train_data['Y']
    X_val = val_data.drop(columns=['Y'])
    Y_val = val_data['Y']


    lgbtrain = lgb.Dataset(data=X_train, label=Y_train, feature_name=list(X_train.columns), free_raw_data=False, categorical_feature='')
    lgbval = lgb.Dataset(data=X_val, label=Y_val, reference=lgbtrain, feature_name=list(X_val.columns), free_raw_data=False) if X_val is not None else None

    params = {
            'num_leaves': config.num_leaves,
            'learning_rate': config.learning_rate,
            'feature_fraction': config.feature_fraction,
            'max_depth': config.max_depth,
            'verbose': config.verbose,
            'early_stopping_rounds': config.early_stopping_rounds,
            'nthread': config.nthread
        }

    model = LGBMModel(params=params)
    model.train(lgbtrain, lgbval)

@hydra.main(version_base=None, config_path="../configs", config_name="training_default.yaml")
def main(config: DictConfig):
    """
    Examples How to run:

    python use_cases/hydra_with_pydantic.py
    python use_cases/hydra_with_pydantic.py -cn training_default.yaml
    python use_cases/hydra_with_pydantic.py batch_size=128
    """
    data = pd.read_csv(config.train_data_path)
    data = data[['cnt', 'date']] # date column is useful for feature generation

    if config.granularity == 'one_day':
        day_params = one_day_params
    
    if config.granularity == 'seven_days':
        pass

    if config.granularity == 'thirty_days':
        pass
    
    data_with_features = calculate_features_for_inference(data=data, params=day_params)
    data_with_features = data_with_features.drop(columns=['date'])
    data = data_with_features.copy()

    run_training(data, config)


if __name__ == "__main__":
    main()