from dataclasses import dataclass

@dataclass
class ProductFeatures:
    product_id: str
    category: str
    price: float
    customer_id: str
    customer_type: str
    delivery_time_days: int
    payment_method: str
    quantity: int
