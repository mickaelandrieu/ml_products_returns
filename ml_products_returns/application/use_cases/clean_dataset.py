import os
import tempfile

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from ml_products_returns.infrastructure.data.minio_client import MinioClient
from ml_products_returns.infrastructure.data.spark_loader import get_spark_session


def clean_dataset(raw_s3_path: str) -> str:
    minio = MinioClient()
    spark = get_spark_session()

    tmp_dir = tempfile.gettempdir()
    raw_local_path = os.path.join(tmp_dir, "raw_dataset.csv")
    cleaned_dir_path = os.path.join(tmp_dir, "cleaned_product_sales.parquet")

    # Téléchargement depuis MinIO
    minio.client.fget_object("datasets", "product_sales.csv", raw_local_path)

    # Lecture du CSV avec inférence de schéma
    df = spark.read.option("header", True).csv(raw_local_path, inferSchema=True)

    # Harmonisation des noms de colonnes
    for col_name in df.columns:
        new_name = (
            col_name.strip()
            .lower()
            .replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
        )
        df = df.withColumnRenamed(col_name, new_name)

    # Suppression des lignes avec valeurs nulles
    df_cleaned = df.dropna()

    # Forcer Spark à n’écrire qu’un seul fichier Parquet
    df_cleaned.coalesce(1).write.mode("overwrite").parquet(cleaned_dir_path, compression="snappy")

    # Trouver le fichier part-*.parquet généré
    for file_name in os.listdir(cleaned_dir_path):
        if file_name.endswith(".parquet"):
            single_parquet_file = os.path.join(cleaned_dir_path, file_name)
            break
    else:
        raise FileNotFoundError("Aucun fichier .parquet trouvé dans le dossier généré par Spark.")

    # Upload vers MinIO
    cleaned_object_name = "cleaned_product_sales.parquet"
    minio.upload_file("datasets", cleaned_object_name, single_parquet_file)

    return minio.get_s3_uri("datasets", cleaned_object_name)
