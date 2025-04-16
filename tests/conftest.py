import os
import pytest
from unittest.mock import Mock

@pytest.fixture(autouse=True)
def setup_env():
    """Configure les variables d'environnement pour les tests."""
    os.environ["LUIGI_S3_ENDPOINT"] = "http://localhost:9000"
    os.environ["MINIO_ACCESS_KEY"] = "minioadmin"
    os.environ["MINIO_SECRET_KEY"] = "minioadmin"
    os.environ["MINIO_BUCKET"] = "datasets"
    yield
    # Nettoyage après les tests
    os.environ.pop("LUIGI_S3_ENDPOINT", None)
    os.environ.pop("MINIO_ACCESS_KEY", None)
    os.environ.pop("MINIO_SECRET_KEY", None)
    os.environ.pop("MINIO_BUCKET", None)

@pytest.fixture
def mock_minio_client():
    """Crée un mock du client MinIO."""
    return Mock()

@pytest.fixture
def mock_kaggle_downloader(mock_minio_client):
    """Crée un mock du téléchargeur Kaggle."""
    from ml_products_returns.infrastructure.data.kaggle_downloader import KaggleDownloader
    return Mock(spec=KaggleDownloader) 