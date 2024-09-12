import pandas as pd
import numpy as np
from pathlib import Path
from backend.ml_pipeline.model import LGBMModel

def find_model_path(models_path: Path, granularity: str, assigned_cluster: int):
    model_pattern = f"granularity_{granularity}/model_cluster_{assigned_cluster}_smape_*.txt"
    matching_files = list(models_path.glob(model_pattern))
    return matching_files[0] if matching_files else None

def get_model(model_path):
    model = LGBMModel()
    model.load_model(str(model_path))
    return model

def get_prediction(model, feature_vector: np.ndarray):
    prediction = model.predict(feature_vector)
    return prediction

def inference_model_on_sku(feature_vector: np.ndarray, 
                           granularity: int, 
                           cluster: int, 
                           folder_with_models: Path):
    
    model_path = find_model_path(folder_with_models, granularity, cluster)
    model = get_model(model_path)
    prediction = get_prediction(model, feature_vector)

    rounded_predictions = int(np.abs(np.round(prediction)))

    return rounded_predictions
