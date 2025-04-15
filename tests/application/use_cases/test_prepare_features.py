from unittest.mock import patch, MagicMock
from ml_products_returns.application.use_cases.prepare_features import prepare_features


@patch("ml_products_returns.application.use_cases.prepare_features.MinioClient")
@patch("ml_products_returns.application.use_cases.prepare_features.get_spark_session")
def test_prepare_features_runs_successfully(mock_get_spark, mock_minio_class):
    # Mock de la session Spark
    mock_spark = MagicMock()
    mock_df = MagicMock()

    mock_df.columns = [
        "category", "version", "final_quantity", "total_revenue",
        "price_reductions", "refunds", "final_revenue", "sales_tax",
        "overall_revenue", "purchased_item_count", "refunded_item_count"
    ]

    mock_spark.read.parquet.return_value = mock_df
    mock_df.select.return_value = mock_df
    mock_df.withColumn.return_value = mock_df
    mock_df.drop.return_value = mock_df
    mock_df.withColumnRenamed.return_value = mock_df
    mock_df.write.mode.return_value.parquet.return_value = None

    # Empêche l'erreur "MagicMock > 0"
    mock_df.__getitem__.return_value.__gt__.return_value = MagicMock()

    mock_get_spark.return_value = mock_spark

    # Mock MinIO
    mock_minio = MagicMock()
    mock_minio_class.return_value = mock_minio
    mock_minio.get_s3_uri.return_value = "s3a://datasets/ml_dataset.parquet"

    # Appel de la fonction
    result = prepare_features("s3a://datasets/cleaned_product_sales.parquet")

    # Vérifications
    mock_minio.client.fget_object.assert_called_once()
    mock_df.write.mode.return_value.parquet.assert_called_once()
    mock_minio.upload_file.assert_called_once()
    assert result == "s3a://datasets/ml_dataset.parquet"
