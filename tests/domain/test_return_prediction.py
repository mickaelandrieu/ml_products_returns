from ml_products_returns.domain.return_prediction import ReturnPrediction

def test_return_prediction_creation():
    prediction = ReturnPrediction(
        product_id="P123",
        customer_id="C456",
        return_probability=0.75
    )
    assert prediction.return_probability == 0.75
