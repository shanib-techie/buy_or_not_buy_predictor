# Mall Buyer Predictor

mall-ui/
  main.py            FastAPI example (serves static/ + POST /predict)
  requirements.txt
  static/
    index.html  style.css  script.js

Run: pip install -r requirements.txt && uvicorn main:app --reload

API contract (POST /predict)
  request : {"age": 29, "annual_income": 60, "spending_score": 90, "gender": "Male"}
  response: {"prediction": 1, "probability": 0.87}

If the API is hosted separately, set API_BASE in static/script.js and enable CORS.
