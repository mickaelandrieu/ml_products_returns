from unittest.mock import MagicMock, patch
from ml_products_returns.infrastructure.data.minio_client import MinioClient


@patch("ml_products_returns.infrastructure.data.minio_client.Minio")
def test_upload_file_creates_bucket_if_missing(MockMinio):
    # Mock des méthodes de l'objet Minio
    mock_client = MagicMock()
    MockMinio.return_value = mock_client
    mock_client.bucket_exists.return_value = False

    client = MinioClient()
    client.upload_file("my-bucket", "my-object.csv", "/tmp/test.csv")

    mock_client.make_bucket.assert_called_once_with("my-bucket")
    mock_client.fput_object.assert_called_once_with("my-bucket", "my-object.csv", "/tmp/test.csv")


@patch("ml_products_returns.infrastructure.data.minio_client.Minio")
def test_get_s3_uri_format(MockMinio):
    client = MinioClient()
    uri = client.get_s3_uri("my-bucket", "my-object.csv")
    assert uri == "s3a://my-bucket/my-object.csv"
