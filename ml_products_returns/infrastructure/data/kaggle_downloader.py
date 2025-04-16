import os
import kagglehub
from ml_products_returns.infrastructure.data.minio_client import MinioClient
from loguru import logger

class KaggleDownloader:
    def __init__(self, minio_client: MinioClient, bucket: str, object_name: str):
        self.minio_client = minio_client
        self.bucket = bucket
        self.object_name = object_name

    def download_and_upload(self) -> str:
        dataset_path = kagglehub.dataset_download("yaminh/product-sales-and-returns-dataset")
        csv_path = os.path.join(dataset_path, "order_dataset.csv")

        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV not found into the Dataset path : {csv_path}")

        # Upload vers MinIO
        logger.info(f"📤 Upload vers MinIO : bucket '{self.bucket}', objet '{self.object_name}'")
        self.minio_client.upload_file(self.bucket, self.object_name, csv_path)

        return self.minio_client.get_s3_uri(self.bucket, self.object_name)
