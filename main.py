from ml_products_returns.application.orchestrator import run_training_pipeline
from ml_products_returns.infrastructure.utils.logger import setup_logging
from loguru import logger

if __name__ == "__main__":
    setup_logging()
    model_uri = run_training_pipeline()
    logger.success(f"Modèle entraîné et sauvegardé ici : {model_uri}")

