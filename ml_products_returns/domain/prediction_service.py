from .product_features import ProductFeatures
from .return_prediction import ReturnPrediction
from typing import Protocol


class ReturnPredictor(Protocol):
    def predict(self, features: ProductFeatures) -> float:
        ...


class PredictionService:
    def __init__(self, model: ReturnPredictor):
        self.model = model

    def predict_return(self, features: ProductFeatures) -> ReturnPrediction:
        probability = self.model.predict(features)
        return ReturnPrediction(
            product_id=features.product_id,
            customer_id=features.customer_id,
            return_probability=probability,
        )
