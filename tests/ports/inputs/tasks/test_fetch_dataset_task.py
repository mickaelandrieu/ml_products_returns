import pytest
from unittest.mock import Mock, patch
from ml_products_returns.ports.inputs.tasks.fetch_dataset_task import FetchDatasetTask
from ml_products_returns.infrastructure.utils.safe_s3_target import SafeS3Target

class TestFetchDatasetTask:
    @pytest.fixture
    def task(self, mock_kaggle_downloader):
        with patch('ml_products_returns.infrastructure.data.kaggle_downloader.KaggleDownloader', 
                  return_value=mock_kaggle_downloader):
            return FetchDatasetTask()
    
    def test_output(self, task):
        """Test que la sortie est bien un SafeS3Target avec le bon chemin."""
        output = task.output()
        assert isinstance(output, SafeS3Target)
        assert output.path == "s3://datasets/raw/olist_products_dataset.csv"
    
    def test_run_success(self, task, mock_kaggle_downloader):
        """Test l'exécution réussie de la tâche."""
        # Mock de l'output pour simuler un fichier qui n'existe pas
        mock_output = Mock(spec=SafeS3Target)
        mock_output.exists.return_value = False
        mock_output.path = "s3://datasets/raw/olist_products_dataset.csv"
        
        with patch.object(task, 'output', return_value=mock_output):
            task.run()
            
            # Vérifier que download_dataset a été appelé avec le bon chemin
            mock_kaggle_downloader.download_dataset.assert_called_once_with(
                "s3://datasets/raw/olist_products_dataset.csv"
            )
    
    def test_run_file_exists(self, task, mock_kaggle_downloader):
        """Test que la tâche ne télécharge pas si le fichier existe déjà."""
        # Mock de l'output pour simuler un fichier qui existe
        mock_output = Mock(spec=SafeS3Target)
        mock_output.exists.return_value = True
        
        with patch.object(task, 'output', return_value=mock_output):
            task.run()
            
            # Vérifier que download_dataset n'a pas été appelé
            mock_kaggle_downloader.download_dataset.assert_not_called() 