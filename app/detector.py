# app/detector.py

import joblib
import os
import pandas as pd

class FlowAnomalyDetector:
    def __init__(self, model_path="flow_model.pkl"):
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
        else:
            raise FileNotFoundError(f"Model file not found at: {model_path}")

    def detect(self, df: pd.DataFrame) -> pd.DataFrame:
        features = df[['duration', 'bytes_sent', 'bytes_received']]
        df['anomaly'] = self.model.predict(features)
        return df
