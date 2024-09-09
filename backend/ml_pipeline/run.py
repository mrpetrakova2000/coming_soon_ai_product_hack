import pandas as pd

from preprocess_for_inference import calculate_features_for_inference
from configs.feature_params import one_day_params

def run_inference_pipeline(data: pd.DataFrame) -> dict:
    
    #TODO: run data preprocessing -> merged_df (pd.Dataframe)
    data = pd.read_csv('..\\ML\\item_064.csv')
    data = data[['item_id', 'cnt', 'date']]

    #TODO: assign cluster
    #TODO: load model

    #TODO: preprocess data to be able to inference on 1, 7 and 30 days
    data_with_one_day_features = calculate_features_for_inference(data=data, params=one_day_params)

    #TODO: run inference on the given data
    
    return None