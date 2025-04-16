import luigi
from .fetch_dataset_task import FetchDatasetTask
from .clean_dataset_task import CleanDatasetTask
from .prepare_features_task import PrepareFeaturesTask
from .train_model_task import TrainModelTask

class ModelPipeline(luigi.WrapperTask):
    """Pipeline complet pour l'entraînement du modèle de prédiction des retours.
    
    Ce pipeline orchestre l'ensemble du processus :
    1. Téléchargement des données depuis Kaggle
    2. Nettoyage des données
    3. Préparation des features
    4. Entraînement du modèle
    
    Returns:
        None: Cette tâche ne produit pas de sortie directe
    """
    
    def requires(self):
        """Définit les dépendances du pipeline.
        
        Returns:
            list: Liste des tâches requises dans l'ordre d'exécution
        """
        yield FetchDatasetTask()
        yield CleanDatasetTask()
        yield PrepareFeaturesTask()
        yield TrainModelTask() 