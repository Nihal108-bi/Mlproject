# Student Performance Prediction - MLOps Practice Project

This is an end-to-end machine learning project to predict `math_score` from student information and exam context.  
The project is used for deployment practice on **AWS and Azure separately**.

## Problem Statement
Predict student math performance using:
- `gender`
- `race_ethnicity`
- `parental_level_of_education`
- `lunch`
- `test_preparation_course`
- `reading_score`
- `writing_score`

Target:
- `math_score`

Dataset location:
- `notebook/data/stud.csv`

## What Is Implemented In This Repository
- Flask web app: `app.py`
- Training components:
  - `src/components/data_ingestion.py`
  - `src/components/data_transformation.py`
  - `src/components/model_trainer.py`
- Inference pipeline:
  - `src/pipeline/predict_pipeline.py`
- Utilities/logging/exception:
  - `src/utils.py`
  - `src/logger.py`
  - `src/exception.py`
- UI templates:
  - `templates/index.html`
  - `templates/home.html`
- Docker image build:
  - `Dockerfile`
- AWS CI/CD workflow:
  - `.github/workflows/main.yaml`

## End-to-End Pipeline (Code-Based)
1. **Data ingestion**
   - Reads `notebook/data/stud.csv`
   - Splits train/test
   - Saves to `artifacts/data.csv`, `artifacts/train.csv`, `artifacts/test.csv`

2. **Data transformation**
   - Numeric pipeline: median imputation + scaling (`reading_score`, `writing_score`)
   - Categorical pipeline: most-frequent imputation + one-hot encoding + scaling
   - Saves preprocessor to `artifacts/preprocessor.pkl`

3. **Model training**
   - Tries multiple regressors with `GridSearchCV`:
     - RandomForest
     - DecisionTree
     - GradientBoosting
     - LinearRegression
     - XGBoost
     - CatBoost
     - AdaBoost
   - Saves selected model to `artifacts/model.pkl`

4. **Prediction service**
   - `/predictdata` form input
   - Loads `model.pkl` + `preprocessor.pkl`
   - Returns predicted math score in UI

## Project Structure
```text
Student-Performance/
|- app.py
|- Dockerfile
|- requirements.txt
|- .github/workflows/main.yaml
|- notebook/
|  |- data/stud.csv
|  |- 1 . EDA STUDENT PERFORMANCE .ipynb
|  |- 2. MODEL TRAINING.ipynb
|- src/
|  |- components/
|  |- pipeline/
|  |- utils.py
|  |- logger.py
|  |- exception.py
|- templates/
|  |- index.html
|  |- home.html
|- artifacts/   (generated after training)
```

## Local Setup
### 1) Create environment and install dependencies
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Run training pipeline
The training flow is triggered from:
```bash
python src/components/data_ingestion.py
```
This runs ingestion -> transformation -> model training and generates artifacts.

### 3) Run Flask app
```bash
python app.py
```
Open:
- `http://localhost:8080/`
- Prediction form: `http://localhost:8080/predictdata`

## Docker Usage
Build and run:
```bash
docker build -t student-performance:latest .
docker run -d -p 8080:8080 --name studentperformance student-performance:latest
```

## AWS Deployment Practice (Implemented In Repo)
AWS CI/CD is defined in `.github/workflows/main.yaml`:
- Trigger: push to `main` (except README-only changes)
- Job 1: basic integration steps (lint/test placeholders)
- Job 2: build and push Docker image to Amazon ECR
- Job 3: deploy on **self-hosted runner** by pulling latest ECR image and running container on port `8080`

### Required GitHub Secrets
Set these in repository secrets:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `ECR_REPOSITORY_NAME`

### EC2 Self-Hosted Runner (Docker Prerequisite)
```bash
sudo apt-get update -y
sudo apt-get upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

## Azure Deployment Practice (Done Separately)
Azure deployment was practiced separately from this repo's AWS workflow.

This repository currently **does not contain Azure CI/CD YAML**.  
For Azure practice, deploy the same Docker image manually (for example, to Azure Web App for Containers or Azure Container Apps).

Example Azure CLI flow (Web App for Containers):
```bash
az login
az group create --name <rg-name> --location <region>
az appservice plan create --name <plan-name> --resource-group <rg-name> --is-linux --sku B1
az webapp create --resource-group <rg-name> --plan <plan-name> --name <app-name> \
  --deployment-container-image-name <image>
az webapp config appsettings set --resource-group <rg-name> --name <app-name> \
  --settings WEBSITES_PORT=8080
```

## Notes
- `src/pipeline/train_pipeline.py` is currently empty; training is executed from `src/components/data_ingestion.py` main block.
- Current CI integration job uses placeholder commands for lint/tests and can be extended.
- This project is primarily built for MLOps learning and deployment practice.
