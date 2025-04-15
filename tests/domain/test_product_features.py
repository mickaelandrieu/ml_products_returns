from ml_products_returns.domain.product_features import ProductFeatures

def test_product_features_creation():
    features = ProductFeatures(
        product_id="P123",
        category="Clothing",
        price=49.99,
        customer_id="C456",
        customer_type="Returning",
        delivery_time_days=3,
        payment_method="CreditCard",
        quantity=2
    )
    assert features.product_id == "P123"
    assert features.price == 49.99
