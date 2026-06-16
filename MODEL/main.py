from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pickle
import numpy as np
from typing import Optional
import os

# ---------------------------------------------------------------------------
# Load model
# ---------------------------------------------------------------------------
MODEL_PATH = "house_price_model.pkl"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file '{MODEL_PATH}' not found.")

with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="House Price Prediction API",
    description="Predicts house prices based on size and number of bedrooms.",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
class HouseData(BaseModel):
    size_sqft: float = Field(..., gt=0, description="Size of the house in square feet")
    bedrooms: int = Field(..., ge=1, le=20, description="Number of bedrooms")

class PredictionResponse(BaseModel):
    predicted_price: float
    confidence_interval: dict  # {"lower": float, "upper": float}
    currency: str = "USD"

class MetricsResponse(BaseModel):
    model_type: str
    r2_score: Optional[float]
    mae: Optional[float]
    rmse: Optional[float]
    training_note: str

# ---------------------------------------------------------------------------
# Helper: extract metrics from model if available
# ---------------------------------------------------------------------------
def get_model_metrics() -> dict:
    """
    Attempts to read evaluation metrics stored on the model object itself.
    When training, attach them like:
        model.r2_score_ = r2_score(y_test, y_pred)
        model.mae_      = mean_absolute_error(y_test, y_pred)
        model.rmse_     = mean_squared_error(y_test, y_pred, squared=False)
    """
    return {
        "r2_score": getattr(model, "r2_score_", None),
        "mae":      getattr(model, "mae_",       None),
        "rmse":     getattr(model, "rmse_",      None),
    }

# Rough confidence margin — replace with actual residual std from training
CONFIDENCE_MARGIN_FRACTION = 0.10  # ±10 % of prediction

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/", tags=["General"])
def home():
    return {"message": "Welcome to the House Price Prediction API. Visit /docs for usage."}


@app.get("/health", tags=["General"])
def health_check():
    """Returns service liveness and basic model info."""
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "model_type": type(model).__name__,
    }


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict_price(data: HouseData):
    """
    Predict house price given size (sqft) and number of bedrooms.
    Returns the predicted price plus a ±10 % confidence interval.
    """
    try:
        features = np.array([[data.size_sqft, data.bedrooms]])
        raw = model.predict(features)
        price = float(np.ravel(raw)[0])  # safely flatten any shape
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    margin = price * CONFIDENCE_MARGIN_FRACTION
    return PredictionResponse(
        predicted_price=round(price, 2),
        confidence_interval={
            "lower": round(price - margin, 2),
            "upper": round(price + margin, 2),
        },
    )


@app.get("/metrics", response_model=MetricsResponse, tags=["Model"])
def model_metrics():
    """
    Returns model evaluation metrics (R², MAE, RMSE).

    To populate these automatically, attach them to your model before saving:

        from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
        model.r2_score_ = r2_score(y_test, y_pred)
        model.mae_      = mean_absolute_error(y_test, y_pred)
        model.rmse_     = mean_squared_error(y_test, y_pred, squared=False)
        with open("house_price_model.pkl", "wb") as f:
            pickle.dump(model, f)
    """
    metrics = get_model_metrics()
    return MetricsResponse(
        model_type=type(model).__name__,
        r2_score=metrics["r2_score"],
        mae=metrics["mae"],
        rmse=metrics["rmse"],
        training_note=(
            "Metrics are populated when r2_score_, mae_, and rmse_ attributes "
            "are attached to the model before pickling. See /metrics docstring."
            if metrics["r2_score"] is None
            else "Metrics loaded from model attributes."
        ),
    )