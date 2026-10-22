from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()

# Load Model
model = joblib.load("model.pkl")
model_columns = joblib.load("model_columns.pkl")


# Request Body
class Detail(BaseModel):
    age: int
    annual_income: float
    spending_score: int
    gender: str


@app.post("/prediction")
def buy_or_not(data: Detail):

    df_new = pd.DataFrame([{
        "Age": data.age,
        "Annual Income (k$)": data.annual_income,
        "Spending Score (1-100)": data.spending_score,
        "Gender": data.gender
    }])

    # One Hot Encoding
    df_new = pd.get_dummies(
        df_new,
        columns=[
            "Gender"
        ]
    )

    # Missing columns add
    df_new = df_new.reindex(columns=model_columns, fill_value=0)

    # Prediction
    result = model.predict(df_new)
    prob = model.predict_proba(df_new)

    return {
        "prediction": int(result[0]),
        "probability_buy": round(float(prob[0][1]), 4)
    }


# Static Files
app.mount("/", StaticFiles(directory="static", html=True), name="static")