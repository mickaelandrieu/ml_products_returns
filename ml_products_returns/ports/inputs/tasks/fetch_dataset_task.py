import luigi
from ml_products_returns.infrastructure.utils.safe_s3_target import SafeS3Target
from ml_products_returns.application.use_cases.fetch_dataset import fetch_dataset

class FetchDatasetTask(luigi.Task):
    def output(self):
        return SafeS3Target('s3://luigi-checkpoints/fetch_dataset.done')

    def run(self):
        s3_path = fetch_dataset()
        with self.output().open("w") as f:
            f.write(f"{s3_path}\n")
