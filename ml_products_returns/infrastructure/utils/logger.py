import sys
from loguru import logger

def setup_logging(log_level: str = "INFO") -> None:
    """
    Configure loguru pour écrire les logs en JSON vers STDOUT, compatible avec Promtail/Loki.
    
    Args:
        log_level: Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logger.remove()

    # Ajoute un handler JSON en STDOUT (pour Promtail)
    logger.add(
        sys.stdout,
        level=log_level,
        serialize=True  # JSON format, indispensable pour Loki
    )
