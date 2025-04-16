from unittest.mock import patch, MagicMock
from ml_products_returns.infrastructure.data.kaggle_downloader import KaggleDownloader


@patch("ml_products_returns.infrastructure.data.kaggle_downloader.kagglehub.dataset_download")
def test_kaggle_downloader_download_and_upload(mock_dataset_download):
    # Préparer les mocks
    mock_minio = MagicMock()
    mock_minio.get_s3_uri.return_value = "s3a://datasets/product_sales.csv"

    mock_dataset_download.return_value = "/tmp/fake_kaggle_dataset"

    # Simule la présence du fichier CSV
    with patch("os.path.exists", return_value=True):
        downloader = KaggleDownloader(
            minio_client=mock_minio,
            bucket="datasets",
            object_name="product_sales.csv"
        )

        s3_path = downloader.download_and_upload()

        # Vérifications
        mock_minio.upload_file.assert_called_once()
        mock_minio.get_s3_uri.assert_called_once()
        assert s3_path == "s3a://datasets/product_sales.csv"
