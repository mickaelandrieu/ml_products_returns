import pytest
from unittest.mock import Mock, patch
from ml_products_returns.ports.inputs.tasks.clean_dataset_task import CleanDatasetTask
from ml_products_returns.infrastructure.utils.safe_s3_target import SafeS3Target

class TestCleanDatasetTask:
    @pytest.fixture
    def task(self):
        return CleanDatasetTask()
    
    def test_requires(self, task):
        """Test que la tâche dépend bien de FetchDatasetTask."""
        from ml_products_returns.ports.inputs.tasks.fetch_dataset_task import FetchDatasetTask
        assert isinstance(task.requires(), FetchDatasetTask)
    
    def test_output(self, task):
        """Test que la sortie est bien un SafeS3Target avec le bon chemin."""
        output = task.output()
        assert isinstance(output, SafeS3Target)
        assert output.path == "s3://datasets/cleaned_product_sales.parquet"
    
    def test_run_success(self, task):
        """Test l'exécution réussie de la tâche."""
        # Mock de l'input et output
        mock_input = Mock(spec=SafeS3Target)
        mock_input.path = "s3://datasets/raw/olist_products_dataset.csv"
        
        mock_output = Mock(spec=SafeS3Target)
        mock_output.exists.return_value = False
        mock_output.path = "s3://datasets/cleaned_product_sales.parquet"
        
        with patch.object(task, 'input', return_value=mock_input), \
             patch.object(task, 'output', return_value=mock_output), \
             patch('ml_products_returns.application.use_cases.clean_dataset.clean_dataset') as mock_clean_dataset:
            task.run()
            
            # Vérifier que clean_dataset a été appelé avec le bon chemin
            mock_clean_dataset.assert_called_once_with(
                "s3://datasets/raw/olist_products_dataset.csv"
            )
    
    def test_run_file_exists(self, task):
        """Test que la tâche ne nettoie pas si le fichier existe déjà."""
        # Mock de l'output pour simuler un fichier qui existe
        mock_output = Mock(spec=SafeS3Target)
        mock_output.exists.return_value = True
        
        with patch.object(task, 'output', return_value=mock_output), \
             patch('ml_products_returns.application.use_cases.clean_dataset.clean_dataset') as mock_clean_dataset:
            task.run()
            
            # Vérifier que clean_dataset n'a pas été appelé
            mock_clean_dataset.assert_not_called() 