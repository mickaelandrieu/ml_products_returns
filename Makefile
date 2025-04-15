.PHONY: up down build run bash logs install

up:
	@echo "Lancement des containers..."
	docker compose up --build -d

down:
	@echo "Arrêt des containers..."
	docker compose down

build:
	@echo "Build des images..."
	docker compose build

bash:
	@echo "Connexion au container..."
	docker exec -it app bash

run:
	@echo "Lancement du pipeline..."
	docker exec -it app poetry run python main.py

logs:
	@echo "Logs de l'application..."
	docker compose logs -f app

reinstall:
	@echo "Réinstallation des dépendances Poetry..."
	docker exec -it app poetry install
