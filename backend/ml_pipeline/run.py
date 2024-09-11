import pandas as pd
import numpy as np
from pathlib import Path

from backend.ml_pipeline.preprocess_for_inference import calculate_features_for_inference
from backend.ml_pipeline.configs.feature_params import one_day_params, seven_day_params, thirty_day_params
from backend.ml_pipeline.inference import inference_model_on_sku

FOLDER_WITH_MODELS = Path('backend/ml_pipeline/models')
CLUSTERS = Path('backend/ml_pipeline/assets/clusters.csv')

def get_feature_vector(data: pd.DataFrame, day=-1) -> np.ndarray:
    # if day = -1 last day with features will be taken
    return np.array(data.iloc[day])

def get_cluster(data: pd.DataFrame) -> int:
    pass

def run_inference_on_sku(input_data: pd.DataFrame) -> dict:
    
    #TODO: run data preprocessing -> merged_df (pd.Dataframe)
    inpute_data = pd.read_csv('./item_064.csv')
    data = inpute_data[['cnt', 'date']] 

    #TODO: assign cluster
    cluster = 0

    # Get features for each granularity value
    data_with_one_day_features = calculate_features_for_inference(data=data, params=one_day_params, train=False)
    data_with_seven_day_features = calculate_features_for_inference(data=data, params=seven_day_params, train=False)
    data_with_thirty_day_features = calculate_features_for_inference(data=data, params=thirty_day_params, train=False)

    # Get feature vectors 
    feature_vector_gran_1 = get_feature_vector(data_with_one_day_features)
    feature_vector_gran_7 = get_feature_vector(data_with_seven_day_features)
    feature_vector_gran_30 = get_feature_vector(data_with_thirty_day_features)

    # inference and save to prediction
    predictions = {
        1: inference_model_on_sku(feature_vector_gran_1, 1, cluster, FOLDER_WITH_MODELS),
        7: inference_model_on_sku(feature_vector_gran_7, 7, cluster, FOLDER_WITH_MODELS),
        30: inference_model_on_sku(feature_vector_gran_30, 30, cluster, FOLDER_WITH_MODELS),
    }

    return predictions