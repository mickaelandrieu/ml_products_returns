import os
from pyspark.sql import SparkSession, DataFrame

def get_spark_session(app_name: str = "MLProductReturns") -> SparkSession:
    return SparkSession.builder \
        .appName(app_name) \
        .master("local[*]") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.access.key", os.environ["MINIO_ACCESS_KEY"]) \
        .config("spark.hadoop.fs.s3a.secret.key", os.environ["MINIO_SECRET_KEY"]) \
        .config("spark.hadoop.fs.s3a.endpoint", os.environ["MINIO_ENDPOINT"]) \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
        .config("spark.hadoop.hadoop.security.access.control.enabled", "false") \
        .config("spark.driver.host", "localhost") \
        .getOrCreate()

def load_dataset_from_s3(spark: SparkSession, s3_path: str) -> DataFrame:
    return spark.read.option("header", "true").csv(s3_path)
