# ML Products Returns

Une entreprise de e-commerce souhaite prédire la probabilité de retour d’un produit après un achat, afin d’optimiser ses recommandations et ses stocks. L’objectif est d’industrialiser ce modèle de machine learning dans un pipeline de traitement distribué (PySpark), avec un focus sur la testabilité et la maintenabilité grâce à une architecture hexagonale.

## Architecture cible : Hexagonale
### Couches définies :

* Domaine : logique métier indépendante (entités, services de prédiction, validation).
* Application : orchestration, cas d’usage (entraînement, prédiction, scoring).
* Infrastructure : persistance (HDFS, S3, DB), lecture/écriture de fichiers, interaction avec Spark, modèles sérialisés, etc.
* Ports (interfaces) : abstractions vers l’intérieur (use cases) ou l’extérieur (adaptateurs).

### Workflow global

1. Ingestion des données depuis un data lake (S3 ou HDFS).
2. Pré-traitement et feature engineering (PySpark).
3. Entraînement du modèle (scikit-learn).
4. Sérialisation du modèle (MLflow, Pickle ou Joblib).
5. API ou Batch de prédiction (Spark ou REST Flask/FastAPI).
6. Monitoring / Logging (MLflow + logs PySpark).
7. Tests automatisés (Pytest avec mocks sur l’infrastructure).

##  Stack technique

| Besoin                   | Outil(s)                          |
|--------------------------|-----------------------------------|
| Traitement distribué     | PySpark                           |
| Modélisation             | scikit-learn                      |
| Sérialisation du modèle  | MLflow / Joblib                   |
| Orchestration            | Luigi                             |
| Architecture             | Clean / Hexagonale                |
| Tests                    | pytest + unittest.mock            |
| CI/CD                    | GitHub Actions                    |
| Packaging                | Poetry                            |
| Lint                     | Ruff                              |
| Typage                   | mypy                              |
| Logs                     | loguru                            |

## Installation/Execution via Docker

1. Créer des credentials sur Kaggle, et obtenir des clés API.
2. Créer le fichier `.env` à partir du fichier `.env.dist`

Enfin :

```
make build
make up
```
### Apps

* Minio => http://localhost:9001/
* MLflow => http://localhost:5000/
* Luigi (à activer) => http://localhost:8082/


## Installation via Windows (😭😭)

### Prérequis système
#### Python & gestion de projet

* Python 3.12
* Poetry pour gérer les dépendances

#### Java

* Java 21 recommandé

>⚠️ Java 24 non supporté par Hadoop/Spark → UnsupportedOperationException: getSubject)

Ajoute JAVA_HOME dans ton environnement :

```
$env:JAVA_HOME = "C:\Program Files\Java\jdk-21"
$env:Path = "$env:JAVA_HOME\bin;$env:Path"
```

### Minio

```
$env:MINIO_ENDPOINT="http://localhost:9000"
$env:MINIO_ACCESS_KEY="minio"
$env:MINIO_SECRET_KEY="minio123"
```

### Kaggle Hub

```
$env:KAGGLE_USERNAME="mickaelandrieu"
$env:KAGGLE_KEY="d929b44284f3ea32a994136a87fcd365"
```

### Luigi (configuration de la Target Minio)

```
$env:AWS_ACCESS_KEY_ID="minio"
$env:AWS_SECRET_ACCESS_KEY="minio123"
$env:LUIGI_S3_ENDPOINT="http://localhost:9000"
```

### MLFlow

```
$env:MLFLOW_S3_ENDPOINT_URL="http://localhost:9000"
$env:AWS_ACCESS_KEY_ID="minio"
$env:AWS_SECRET_ACCESS_KEY="minio123"
```

### Spécifique Java/Spark sur Windows

```
$env:PYSPARK_SUBMIT_ARGS="--conf spark.driver.extraJavaOptions=--add-opens=java.base/javax.security.auth=ALL-UNNAMED pyspark-shell"
$env:JAVA_TOOL_OPTIONS="--enable-native-access=ALL-UNNAMED"
```



### Apache Spark & Hadoop
#### Spark

* Spark 3.5.5 (précompilé avec Hadoop 3)

```
$env:SPARK_HOME = "C:\spark"
$env:PYSPARK_SUBMIT_ARGS="--conf spark.driver.extraJavaOptions=--add-opens=java.base/javax.security.auth=ALL-UNNAMED pyspark-shell"
```

(Windows → zip à extraire dans C:\spark\...)

#### Hadoop

```
$env:HADOOP_HOME = "C:\spark"
$env:hadoop_home_dir = "C:\spark"
```

### MinIO (S3 local)
Lancer MinIO dans Docker :

```
docker run -p 9000:9000 -p 9001:9001 \
  -e MINIO_ACCESS_KEY=minio \
  -e MINIO_SECRET_KEY=minio123 \
  quay.io/minio/minio server /data --console-address ":9001"
```

Accès web : http://localhost:9001

Buckets à créer (automatiquement si besoin) :

* datasets
* models
* luigi-checkpoints

### 📦 JARs Hadoop à ajouter manuellement (dans spark/jars/)
Pour que Spark puisse lire/écrire sur MinIO via S3A :

* hadoop-aws-3.3.4.jar
* aws-java-sdk-bundle-1.11.1026.jar

A placer dans le dossier `C:\spark\jars\`