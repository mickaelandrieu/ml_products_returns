from ml_products_returns.application.use_cases.fetch_dataset import fetch_dataset
from ml_products_returns.application.use_cases.clean_dataset import clean_dataset
from ml_products_returns.application.use_cases.prepare_features import prepare_features
from ml_products_returns.application.use_cases.train_model import train_model


def run_training_pipeline():
    dataset_uri = fetch_dataset()
    cleaned_uri = clean_dataset(dataset_uri)
    prepare_features(cleaned_uri)

    return train_model()
