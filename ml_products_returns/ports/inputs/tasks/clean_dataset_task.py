import luigi

from ml_products_returns.application.use_cases.clean_dataset import clean_dataset
from ml_products_returns.infrastructure.utils.safe_s3_target import SafeS3Target
from ml_products_returns.ports.inputs.tasks.fetch_dataset_task import FetchDatasetTask


class CleanDatasetTask(luigi.Task):
    def requires(self):
        return FetchDatasetTask()

    def output(self):
        return SafeS3Target("s3://datasets/cleaned_product_sales.parquet")

    def run(self):
        raw_s3_path = self.input().path
        cleaned_s3_path = clean_dataset(raw_s3_path)
