import os
import tempfile
import joblib
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from ml_products_returns.infrastructure.data.spark_loader import get_spark_session
from ml_products_returns.infrastructure.data.minio_client import MinioClient


def train_model() -> str:
    # Initialisation Spark
    spark = get_spark_session()
    minio = MinioClient()
    minio.ensure_bucket_exists("mlflow-artifacts")

    # Lecture depuis MinIO
    s3_path = os.environ.get("DATASET_S3_URI", "s3a://datasets/ml_dataset.parquet")
    df_spark = spark.read.parquet(s3_path)

    # Préparation des données
    df = df_spark.toPandas()
    X = df.drop(columns=["y"])
    y = df["y"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Initialisation MLflow
    mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
    mlflow.set_experiment("product-returns-model")

    with mlflow.start_run():
        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"✅ Accuracy = {acc:.4f}")

        # Log des hyperparamètres
        mlflow.log_param("n_estimators", model.n_estimators)
        mlflow.log_param("max_depth", model.max_depth)

        # Log de la métrique
        mlflow.log_metric("accuracy", acc)

        # Signature + input_example
        signature = infer_signature(X_train, model.predict(X_train))
        mlflow.sklearn.log_model(
            model,
            artifact_path="model",
            input_example=X_train.iloc[:5],
            signature=signature
        )

        # Enregistrement local du modèle pour MinIO
        tmp_dir = tempfile.gettempdir()
        model_path = os.path.join(tmp_dir, "return_model.pkl")
        joblib.dump(model, model_path)

        # Upload vers MinIO
        print(f"📁 Envoi vers Minio : {model_path}")
        
        minio.upload_file("models", "return_model.pkl", model_path)
        s3_uri = minio.get_s3_uri("models", "return_model.pkl")

        # Log dans MLflow (référencement externe)
        mlflow.log_artifact(model_path, artifact_path="minio-backup")

    return s3_uri
