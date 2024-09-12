import hydra
from omegaconf import DictConfig
import lightgbm as lgb
import pandas as pd
from pathlib import Path


from backend.ml_pipeline.preprocess_for_inference import calculate_features_for_inference 
from backend.ml_pipeline.configs.feature_params import one_day_params
from backend.ml_pipeline.model import LGBMModel


def run_training(train_data: pd.DataFrame, val_data: pd.DataFrame, config: DictConfig):
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

    best_smape = model.model.best_score['valid_0']['SMAPE']
    
    path_to_save = Path(config.save_model_to)
    base_path = path_to_save.stem  
    parent_directory = path_to_save.parent  # 'path/to/file'
    file_extension = path_to_save.suffix  # '.txt'

    new_filename = f"{base_path}_smape_{best_smape:.2f}{file_extension}"
    new_path = parent_directory / new_filename

    model.save_model(new_path)

@hydra.main(version_base=None, config_path="../configs", config_name="training_on_cluster.yaml")
def main(config: DictConfig):
    """
    Examples How to run:

    python use_cases/hydra_with_pydantic.py
    python use_cases/hydra_with_pydantic.py -cn training_default.yaml
    python use_cases/hydra_with_pydantic.py batch_size=128
    """
    train_data = pd.read_csv(config.cluster_train)
    val_data = pd.read_csv(config.cluster_val)

    run_training(train_data, val_data, config)


if __name__ == "__main__":
    main()