# 💳 Credit Card Fraud Detection — MLOps Project

## 🧠 Overview
This project demonstrates an **end-to-end Machine Learning and MLOps pipeline** for detecting fraudulent credit card transactions.  
It includes **data preprocessing, model training, evaluation, Docker-based deployment**, and **automated CI/CD with GitHub Actions**.

---

## 🚀 Features

✅ **Machine Learning Model**
- Built using Scikit-learn, XGBoost, and Random Forest.  
- Focused on fraud detection from imbalanced datasets.  
- Evaluated using metrics like Accuracy, Precision, Recall, F1-score, and ROC-AUC.  

✅ **Data Pipeline**
- Data cleaning and transformation.  
- Feature scaling and encoding.  
- SMOTE-based resampling to handle class imbalance.  

✅ **MLOps Automation**
- Continuous Integration/Continuous Deployment (CI/CD) using **GitHub Actions**.  
- Automatic build, test, and Docker image creation on every push to `main`.  

✅ **Containerization**
- Fully containerized with **Docker** for consistent deployment across environments.  

✅ **Streamlit Dashboard (Optional)**
- Simple and interactive interface to visualize predictions.  

---

## 🏗️ Project Structure

credit-fraud-mlops/
│
├── data/ # Dataset folder (CSV excluded from GitHub due to size)
│
├── src/ # Source code
│ ├── preprocess.py # Data cleaning and feature engineering
│ ├── train_model.py # Model training and saving
│ ├── evaluate.py # Model evaluation and reporting
│ └── predict.py # Single prediction script
│
├── models/ # Saved trained models
│
├── dashboard.py # Streamlit or Flask app
│
├── requirements.txt # Python dependencies
│
├── Dockerfile # Docker image configuration
│
├── .github/
│ └── workflows/
│ └── cicd.yml # GitHub Actions CI/CD pipeline
│
└── README.md # Documentation (you are here)


## 🐳 Docker Setup
Build Docker Image
docker build -t credit-fraud-mlops .

Run the Container
docker run -p 8080:8080 credit-fraud-mlops


Now open http://localhost:8080
 to access the app.
--

## 🧪 How to Run Locally
Step 1️⃣ Clone the repository
git clone https://github.com/lavanya-achar/credit-fraud-mlops.git
cd credit-fraud-mlops

Step 2️⃣ Create a virtual environment
python -m venv venv
venv\Scripts\activate    # (On Windows)

Step 3️⃣ Install dependencies
pip install -r requirements.txt

Step 4️⃣ Train the model (if needed)
python src/train_model.py

Step 5️⃣ Run the application
python dashboard.py


 ## 📈 Model Performance
-Metric	Value
-Accuracy	98.7%
-Precision	94.5%
-Recall	91.2%
-F1-Score	92.8%
- ROC-AUC	0.98

📊 The model performs exceptionally well at detecting fraudulent transactions while maintaining a low false positive rate.
Feature importance shows that transaction amount, time, and feature V14 were the most significant predictors.

## 🧩 MLOps Lifecycle Summary

Data Versioning – Maintain datasets locally or via DVC.

Model Training – Executed locally or within a CI/CD workflow.

Containerization – Docker ensures consistent deployment environments.

CI/CD Automation – GitHub Actions runs automatically on every code update.

Deployment Ready – Dockerized app can be deployed on AWS / Azure / Render.

## 🔮 Future Improvements

Integrate MLflow for experiment tracking.

Add Prometheus + Grafana for real-time monitoring.

Automate Docker image push to Docker Hub.

Deploy container to AWS ECS, Azure Container Apps, or Render.
