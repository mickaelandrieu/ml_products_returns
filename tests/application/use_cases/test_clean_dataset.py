from unittest.mock import patch, MagicMock
from ml_products_returns.application.use_cases.clean_dataset import clean_dataset


@patch("ml_products_returns.application.use_cases.clean_dataset.MinioClient")
@patch("ml_products_returns.application.use_cases.clean_dataset.get_spark_session")
def test_clean_dataset_runs_successfully(mock_get_spark, mock_minio_class):
    # Mock SparkSession + DataFrame
    mock_spark = MagicMock()
    mock_df = MagicMock()
    mock_df.columns = [" Product ID ", "Product Name", "Refunded Item Count"]

    mock_spark.read.option.return_value.csv.return_value = mock_df
    mock_df.dropna.return_value = mock_df
    mock_df.withColumnRenamed.side_effect = lambda old, new: mock_df

    mock_get_spark.return_value = mock_spark

    # Mock MinIO
    mock_minio = MagicMock()
    mock_minio_class.return_value = mock_minio
    mock_minio.get_s3_uri.return_value = "s3a://datasets/cleaned_product_sales.parquet"

    # Appel
    result = clean_dataset("s3a://datasets/product_sales.csv")

    # Vérifications
    mock_minio.client.fget_object.assert_called_once()
    mock_df.write.mode.return_value.parquet.assert_called_once()
    mock_minio.upload_file.assert_called_once()
    assert result == "s3a://datasets/cleaned_product_sales.parquet"
