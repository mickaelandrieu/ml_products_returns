import pandas as pd
from unittest.mock import patch, MagicMock
from ml_products_returns.application.use_cases.train_model import train_model


@patch("ml_products_returns.application.use_cases.train_model.get_spark_session")
@patch("ml_products_returns.application.use_cases.train_model.MinioClient")
@patch("ml_products_returns.application.use_cases.train_model.mlflow")
@patch("ml_products_returns.application.use_cases.train_model.joblib.dump")
def test_train_model_runs_successfully(
    mock_dump,
    mock_mlflow,
    mock_minio_client_class,
    mock_get_spark
):
    # Mock DataFrame Spark → Pandas
    mock_spark = MagicMock()
    mock_df_spark = MagicMock()
    mock_df_spark.toPandas.return_value = pd.DataFrame({
        "feature1": [10, 20, 30, 40],
        "feature2": [1.0, 2.0, 3.0, 4.0],
        "y": [0, 1, 0, 1],
    })

    mock_spark.read.parquet.return_value = mock_df_spark
    mock_get_spark.return_value = mock_spark

    # Mock MinIO
    mock_minio = MagicMock()
    mock_minio.get_s3_uri.return_value = "s3a://models/return_model.pkl"
    mock_minio_client_class.return_value = mock_minio

    # Appel
    result = train_model()

    # Assertions
    assert result == "s3a://models/return_model.pkl"
    mock_minio.upload_file.assert_called_once()
    mock_mlflow.log_param.assert_any_call("model_type", "RandomForestClassifier")
    mock_mlflow.log_metric.assert_called_once()
