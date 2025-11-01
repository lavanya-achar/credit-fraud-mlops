from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Initialize FastAPI app
app = FastAPI(title="Credit Fraud Detection API", version="1.0")

# Load the trained model
model = joblib.load("models/credit_model.pkl")

# Define input schema
class TransactionData(BaseModel):
    features: list

@app.get("/")
def root():
    return {"message": "Credit Fraud Detection API is running!"}

@app.post("/predict")
def predict(data: list[TransactionData]):
    try:
        # Convert list of transactions into numpy array
        X = np.array([item.features for item in data])
        predictions = model.predict(X)
        return {"predictions": predictions.tolist()}
    except Exception as e:
        return {"error": str(e)}
