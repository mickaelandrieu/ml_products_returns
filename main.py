from ml_products_returns.application.orchestrator import run_training_pipeline

if __name__ == "__main__":
    model_uri = run_training_pipeline()
    print(f"✅ Modèle entraîné et sauvegardé ici : {model_uri}")
