from minio import Minio
from minio.error import S3Error
import os


class MinioClient:
    def __init__(self):
        self.endpoint = os.environ["MINIO_ENDPOINT"].replace("http://", "").replace("https://", "")
        self.secure = os.environ["MINIO_ENDPOINT"].startswith("https")
        self.access_key = os.environ["MINIO_ACCESS_KEY"]
        self.secret_key = os.environ["MINIO_SECRET_KEY"]

        self.client = Minio(
            endpoint=self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=self.secure
        )

    def ensure_bucket_exists(self, bucket: str):
        print(f"🗑️ Vérification / création du bucket : {bucket}")
        if not self.client.bucket_exists(bucket):
            print(f"🆕 Création du bucket {bucket}...")
            self.client.make_bucket(bucket)
        else:
            print(f"✅ Bucket {bucket} déjà existant")


    def upload_file(self, bucket: str, object_name: str, file_path: str):
        self.ensure_bucket_exists(bucket)
        self.client.fput_object(bucket, object_name, file_path)

    def get_s3_uri(self, bucket: str, object_name: str) -> str:
        return f"s3a://{bucket}/{object_name}"
