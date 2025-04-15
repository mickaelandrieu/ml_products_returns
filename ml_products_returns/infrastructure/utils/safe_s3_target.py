import os
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
from luigi.contrib.s3 import S3Target


class SafeS3Target(S3Target):
    """
    Version sécurisée de S3Target pour Luigi, adaptée à MinIO.
    - Force l'utilisation d'un client boto3 configuré manuellement.
    - Crée le bucket si nécessaire.
    - Évite les erreurs 403 en cas d'objet absent.
    """

    def __init__(self, path: str, **kwargs):
        super().__init__(path, **kwargs)

        # Forcer la configuration explicite de boto3 pour MinIO
        self.fs.s3 = boto3.resource(
            service_name="s3",
            endpoint_url=os.environ["LUIGI_S3_ENDPOINT"],
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            config=Config(signature_version="s3v4"),
            region_name="us-east-1",
        )

        self.s3_client = self.fs.s3.meta.client

    def exists(self) -> bool:
        self.ensure_bucket_exists(self.bucket)
        return self.safe_object_exists(self.bucket, self.key)

    @property
    def bucket(self) -> str:
        return self.path.replace("s3://", "").split("/")[0]

    @property
    def key(self) -> str:
        return "/".join(self.path.replace("s3://", "").split("/")[1:])

    def ensure_bucket_exists(self, bucket_name: str):
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
        except ClientError as e:
            code = e.response["Error"]["Code"]
            if code in ["404", "NoSuchBucket"]:
                print(f"🆕 Création du bucket MinIO : {bucket_name}")
                self.s3_client.create_bucket(Bucket=bucket_name)
            elif code == "403":
                raise PermissionError(f"🚫 Accès refusé au bucket '{bucket_name}'")
            else:
                raise

    def safe_object_exists(self, bucket_name: str, key: str) -> bool:
        try:
            self.s3_client.head_object(Bucket=bucket_name, Key=key)
            return True
        except ClientError as e:
            code = e.response["Error"]["Code"]
            if code in ["404", "NoSuchKey"]:
                return False
            elif code == "403":
                print("⚠️ MinIO a renvoyé un 403 sur head_object. L'objet n'existe probablement pas.")
                return False
            else:
                raise
