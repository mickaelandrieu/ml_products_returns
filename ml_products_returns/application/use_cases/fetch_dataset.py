from ml_products_returns.infrastructure.data.minio_client import MinioClient
from ml_products_returns.infrastructure.data.kaggle_downloader import KaggleDownloader


def fetch_dataset() -> str:
    minio_client = MinioClient()

    downloader = KaggleDownloader(
        minio_client=minio_client,
        bucket="datasets",
        object_name="product_sales.csv"
    )

    return downloader.download_and_upload()
