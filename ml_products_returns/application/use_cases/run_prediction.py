import os
import joblib
import pandas as pd

from ml_products_returns.infrastructure.data.minio_client import MinioClient
from ml_products_returns.domain.product_features import ProductFeatures
from ml_products_returns.domain.prediction_service import PredictionService


def run_prediction(features_df: pd.DataFrame) -> pd.DataFrame:
    # Téléchargement du modèle
    model_path = "/tmp/return_model.pkl"
    minio = MinioClient()
    minio.client.fget_object("models", "return_model.pkl", model_path)

    model = joblib.load(model_path)

    service = PredictionService(model)

    results = []
    for _, row in features_df.iterrows():
        features = ProductFeatures(**row.to_dict())
        pred = service.predict_return(features)
        results.append({
            "product_id": pred.product_id,
            "customer_id": pred.customer_id,
            "return_probability": pred.return_probability
        })

    return pd.DataFrame(results)
