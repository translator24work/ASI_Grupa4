from fastapi import FastAPI, HTTPException, Request
from autogluon.tabular import TabularPredictor
import pandas as pd
from datetime import datetime
from pathlib import Path

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    global predictor

    model_directory = Path('AutogluonModels')
    if not model_directory.exists():
        raise FileNotFoundError(f"Nie znaleziono katalogu modelu: {model_directory}")

    # Znajdowanie najnowszego modelu
    latest_model_path = max(model_directory.iterdir(), key=lambda x: x.stat().st_mtime)

    if not latest_model_path.is_dir():
        raise FileNotFoundError(f"Nie znaleziono modelu: {latest_model_path}")

    print(latest_model_path)

    predictor = TabularPredictor.load(str(latest_model_path))


@app.post("/predict")
async def predict(request: Request):
    try:
        input_data = await request.json()
        data = pd.DataFrame([input_data])
        prediction = predictor.predict(data)
        return {"prediction": prediction.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))