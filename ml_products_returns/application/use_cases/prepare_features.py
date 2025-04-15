import os
import tempfile
import shutil

from pyspark.sql.functions import when
from pyspark.ml.feature import StringIndexer

from ml_products_returns.infrastructure.data.minio_client import MinioClient
from ml_products_returns.infrastructure.data.spark_loader import get_spark_session


FEATURE_COLUMNS = [
    "category",
    "version",
    "final_quantity",
    "total_revenue",
    "price_reductions",
    "refunds",
    "final_revenue",
    "sales_tax",
    "overall_revenue",
    "purchased_item_count",
]


def prepare_features(cleaned_s3_path: str) -> str:
    minio = MinioClient()
    spark = get_spark_session()

    tmp_dir = tempfile.gettempdir()
    cleaned_local_path = os.path.join(tmp_dir, "cleaned_product_sales.parquet")
    ml_dataset_dir = os.path.join(tmp_dir, "ml_dataset.parquet")

    # 🧹 Nettoyage préventif si un dossier existe à ce nom
    if os.path.isdir(cleaned_local_path):
        shutil.rmtree(cleaned_local_path)
    elif os.path.isfile(cleaned_local_path):
        os.remove(cleaned_local_path)

    # Télécharger le fichier nettoyé
    minio.client.fget_object("datasets", "cleaned_product_sales.parquet", cleaned_local_path)

    # Chargement avec Spark
    df = spark.read.parquet(cleaned_local_path)

    # Sélection des colonnes utiles + refunded_item_count
    df = df.select(FEATURE_COLUMNS + ["refunded_item_count"])

    # Création de la target binaire "y"
    df = df.withColumn("y", when(df["refunded_item_count"] > 0, 1).otherwise(0)).drop("refunded_item_count")

    # Encodage avec StringIndexer pour les colonnes catégorielles
    for col_name in ["category", "version"]:
        indexer = StringIndexer(inputCol=col_name, outputCol=f"{col_name}_idx")
        df = indexer.fit(df).transform(df).drop(col_name).withColumnRenamed(f"{col_name}_idx", col_name)

    # Sauvegarde unique : coalesce(1) pour forcer un seul fichier
    df.coalesce(1).write.mode("overwrite").parquet(ml_dataset_dir, compression="snappy")

    # Retrouver le part-*.parquet
    for file_name in os.listdir(ml_dataset_dir):
        if file_name.endswith(".parquet"):
            single_parquet_file = os.path.join(ml_dataset_dir, file_name)
            break
    else:
        raise FileNotFoundError("Aucun fichier .parquet trouvé dans le dossier généré par Spark.")

    # Upload vers MinIO
    object_name = "ml_dataset.parquet"
    minio.upload_file("datasets", object_name, single_parquet_file)

    return minio.get_s3_uri("datasets", object_name)
