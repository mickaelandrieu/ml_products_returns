import luigi
from ml_products_returns.application.use_cases.train_model import train_model
from ml_products_returns.infrastructure.utils.safe_s3_target import SafeS3Target
from ml_products_returns.ports.inputs.tasks.prepare_features_task import PrepareFeaturesTask


class TrainModelTask(luigi.Task):
    def requires(self):
        return PrepareFeaturesTask()

    def output(self):
        return SafeS3Target("s3://models/return_model.pkl")

    def run(self):
        model_uri = train_model()
