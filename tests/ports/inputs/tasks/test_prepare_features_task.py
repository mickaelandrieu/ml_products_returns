import pytest
from unittest.mock import Mock, patch
from ml_products_returns.ports.inputs.tasks.prepare_features_task import PrepareFeaturesTask
from ml_products_returns.infrastructure.utils.safe_s3_target import SafeS3Target

class TestPrepareFeaturesTask:
    @pytest.fixture
    def task(self):
        return PrepareFeaturesTask()
    
    def test_requires(self, task):
        """Test que la tâche dépend bien de CleanDatasetTask."""
        from ml_products_returns.ports.inputs.tasks.clean_dataset_task import CleanDatasetTask
        assert isinstance(task.requires(), CleanDatasetTask)
    
    def test_output(self, task):
        """Test que la sortie est bien un SafeS3Target avec le bon chemin."""
        output = task.output()
        assert isinstance(output, SafeS3Target)
        assert output.path == "s3://datasets/processed/features.parquet"
    
    def test_run_success(self, task):
        """Test l'exécution réussie de la tâche."""
        # Mock de l'input et output
        mock_input = Mock(spec=SafeS3Target)
        mock_input.path = "s3://datasets/cleaned_product_sales.parquet"
        
        mock_output = Mock(spec=SafeS3Target)
        mock_output.path = "s3://datasets/processed/features.parquet"
        
        with patch.object(task, 'input', return_value=mock_input), \
             patch.object(task, 'output', return_value=mock_output), \
             patch('ml_products_returns.application.use_cases.prepare_features.prepare_features') as mock_prepare_features:
            task.run()
            
            # Vérifier que prepare_features a été appelé avec le bon chemin
            mock_prepare_features.assert_called_once_with(
                "s3://datasets/cleaned_product_sales.parquet"
            ) 