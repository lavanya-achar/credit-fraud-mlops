import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os

# Load dataset
data_path = os.path.join("data", "creditcard.csv")
df = pd.read_csv(data_path)

# Separate features and target
X = df.drop("Class", axis=1)
y = df["Class"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=10, max_depth=5, random_state=42)

model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
print(classification_report(y_test, preds))

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/fraud_model.pkl")
print("✅ Model trained and saved to models/fraud_model.pkl")
