"""Train a Decision Tree demo model.

The project report describes training on historical loan applicant data. Since the
original dataset was not recovered, this script creates clearly synthetic sample
records for a reproducible demonstration. Replace this generator with a verified,
appropriately licensed real dataset before making performance claims.
"""
import os
import numpy as np
import pandas as pd
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

os.makedirs("models", exist_ok=True)
rng = np.random.default_rng(42)
n = 2500
df = pd.DataFrame({
    "age": rng.integers(21, 66, n),
    "annual_income": rng.integers(180000, 2500000, n),
    "employment_type": rng.choice(["Salaried", "Self-employed", "Business"], n),
    "education": rng.choice(["High School", "Graduate", "Postgraduate"], n),
    "marital_status": rng.choice(["Single", "Married"], n),
    "dependents": rng.integers(0, 5, n),
    "loan_amount": rng.integers(50000, 3000000, n),
    "loan_term": rng.choice([12, 24, 36, 60, 84, 120], n),
    "credit_score": rng.integers(300, 901, n),
    "existing_debt": rng.integers(0, 900000, n),
    "loan_purpose": rng.choice(["Home", "Education", "Vehicle", "Personal", "Business"], n)
})
risk = ((df.credit_score < 600).astype(int) +
        (df.loan_amount > df.annual_income * 2).astype(int) +
        (df.existing_debt > df.annual_income * .35).astype(int) +
        (df.dependents >= 3).astype(int) +
        (df.employment_type == "Self-employed").astype(int))
df["default"] = (risk >= 2).astype(int)

features = list(df.columns[:-1])
categorical = ["employment_type", "education", "marital_status", "loan_purpose"]
numeric = [c for c in features if c not in categorical]
pre = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
    ("num", "passthrough", numeric)
])
pipe = Pipeline([
    ("preprocess", pre),
    ("classifier", DecisionTreeClassifier(max_depth=6, min_samples_leaf=10, random_state=42))
])
X_train, X_test, y_train, y_test = train_test_split(df[features], df.default, test_size=.2,
                                                    random_state=42, stratify=df.default)
pipe.fit(X_train, y_train)
pred = pipe.predict(X_test)
print("Demo test accuracy:", round(accuracy_score(y_test, pred), 3))
print(classification_report(y_test, pred))
joblib.dump(pipe, "models/loan_model.pkl")
print("Saved models/loan_model.pkl")
