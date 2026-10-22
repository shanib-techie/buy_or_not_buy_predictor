# Run once:  python train_model.py
# Creates model.pkl and model_columns.pkl (main.py loads these).
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

CSV_PATH = "mall_data.csv"   # keep the CSV next to this file (or put your full path here)

df = pd.read_csv(CSV_PATH)

# Create the "buy" label only if the CSV doesn't already have it
if "buy" not in df.columns:
    df["buy"] = (
        (df["Age"] >= 50)
        & ((df["Annual Income (k$)"] >= 55) | (df["Spending Score (1-100)"] >= 55))
    ).astype(int)

df = df.drop(columns=["Unnamed: 0", "CustomerID"], errors="ignore")
df = pd.get_dummies(df, columns=["Gender"])

X = df.drop(columns=["buy"])
y = df["buy"].astype(int)

# 1) Evaluate on a held-out test set
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
pred = model.predict(X_test)

print("ACCURACY :", accuracy_score(y_test, pred))
print("CONFUSION MATRIX :\n", confusion_matrix(y_test, pred))
print("\nFEATURE WEIGHTS :")
print(pd.Series(model.coef_[0], index=X.columns).sort_values(ascending=False))

# 2) Final model on ALL data, then save
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

joblib.dump(model, "model.pkl")
joblib.dump(list(X.columns), "model_columns.pkl")
print("\nSaved model.pkl and model_columns.pkl")
