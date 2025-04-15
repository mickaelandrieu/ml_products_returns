from ml_products_returns.domain.prediction_service import PredictionService
from ml_products_returns.domain.return_prediction import ReturnPrediction
from ml_products_returns.domain.product_features import ProductFeatures

class DummyModel:
    def predict(self, features: ProductFeatures) -> float:
        return 0.42  # Dummy fixed prediction

def test_prediction_service_with_dummy_model():
    features = ProductFeatures(
        product_id="P123",
        category="Shoes",
        price=89.99,
        customer_id="C456",
        customer_type="New",
        delivery_time_days=5,
        payment_method="Paypal",
        quantity=1
    )

    service = PredictionService(model=DummyModel())
    prediction = service.predict_return(features)

    assert isinstance(prediction, ReturnPrediction)
    assert prediction.return_probability == 0.42
