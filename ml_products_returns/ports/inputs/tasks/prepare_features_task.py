import luigi
from ml_products_returns.application.use_cases.prepare_features import prepare_features
from ml_products_returns.infrastructure.utils.safe_s3_target import SafeS3Target
from ml_products_returns.ports.inputs.tasks.clean_dataset_task import CleanDatasetTask


class PrepareFeaturesTask(luigi.Task):
    def requires(self):
        return CleanDatasetTask()

    def output(self):
        return SafeS3Target("s3://datasets/ml_dataset.parquet")

    def run(self):
        cleaned_s3_path = self.input().path
        features_s3_path = prepare_features(cleaned_s3_path)
