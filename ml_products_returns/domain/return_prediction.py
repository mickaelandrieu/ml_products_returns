from dataclasses import dataclass

@dataclass
class ReturnPrediction:
    product_id: str
    customer_id: str
    return_probability: float
