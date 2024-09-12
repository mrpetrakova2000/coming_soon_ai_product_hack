import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import StandardScaler
import os

from backend.ml_pipeline.preprocess_for_inference import calculate_features_for_inference
from backend.ml_pipeline.configs.feature_params import one_day_params, seven_day_params, thirty_day_params
from backend.ml_pipeline.inference_tools import inference_model_on_sku
from backend.ml_pipeline.postprocess_predictions import postproces_predictions

#print(os.getcwd())

FOLDER_WITH_MODELS = Path('../ml_pipeline/models')
CLUSTERS = Path('../ml_pipeline/assets/clusters.csv')
clusters_df = pd.read_csv(CLUSTERS)

def get_feature_vector(data: pd.DataFrame, day=-1) -> np.ndarray:
    """Return the feature vector (as a 2D array) for a given day, with day = -1 returning the last day."""
    return np.array([data.iloc[day].values])  # Return 2D array with the features of the selected day

def get_cluster(data: pd.DataFrame, cluster_df: pd.DataFrame) -> int:
    scaler = StandardScaler()
    scaler.mean_ = np.array([23.20140492, 14.25831427])
    scaler.scale_ = np.array([28.19352783, 19.14103925])

    features = ['feature_1', 'feature_2']
    data_mean_std = np.array([data['cnt'].mean(), data['cnt'].std()]).reshape(1, -1)
    normalized_data = scaler.transform(data_mean_std)

    cluster_features = cluster_df[features]
    distances = np.linalg.norm(cluster_features.values - normalized_data, axis=1)
    closest_cluster_idx = np.argmin(distances)

    return cluster_df.iloc[closest_cluster_idx]['cluster']


def run_inference_on_sku(input_data: pd.DataFrame) -> tuple:
    """
    input_data : pd.Dataframe ; should contain 'cnt' and 'date' columns
    """
    data = input_data[['cnt', 'date']] 
   
    # Assign cluster
    cluster = get_cluster(data.copy(), clusters_df)

    # Get features for each granularity value
    data_with_one_day_features = calculate_features_for_inference(data=data.copy(), params=one_day_params, train=False)
    data_with_seven_day_features = calculate_features_for_inference(data=data.copy(), params=seven_day_params, train=False)
    data_with_thirty_day_features = calculate_features_for_inference(data=data.copy(), params=thirty_day_params, train=False)

    # Get feature vectors 
    feature_vector_gran_1 = get_feature_vector(data_with_one_day_features)
    feature_vector_gran_7 = get_feature_vector(data_with_seven_day_features)
    feature_vector_gran_30 = get_feature_vector(data_with_thirty_day_features)

    # print(feature_vector_gran_30)

    # Make predictions
    prediction_1_day = inference_model_on_sku(feature_vector_gran_1, 1, cluster, FOLDER_WITH_MODELS)
    prediction_7_days = inference_model_on_sku(feature_vector_gran_7, 7, cluster, FOLDER_WITH_MODELS)
    prediction_30_days = inference_model_on_sku(feature_vector_gran_30, 30, cluster, FOLDER_WITH_MODELS)
    
    # zip the predictions dates with predictions
    prediction_data = postproces_predictions(data, prediction_1_day, prediction_7_days, prediction_30_days)
    last_n_days = input_data.iloc[-20:]

    return last_n_days, prediction_data

# UNCOMMENT FOR USING
# if __name__ == "__main__":
#     inpute_data = pd.read_csv('./item_064.csv')
#     initial_data, prediction_data = run_inference_on_sku(inpute_data)
#     print(prediction_data)
