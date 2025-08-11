
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
from .engine import Inputs, evaluate

app = FastAPI(title="Plant Watering Expert System API", version="1.0.0")

class RecommendRequest(BaseModel):
    soil_moisture: int = Field(ge=0, le=100, description="Soil moisture percentage 0–100")
    plant_type: str     # succulent, leafy, flowering, herb
    sunlight: str       # low, medium, high
    temperature_c: float
    pot_size: str       # small, medium, large
    season: str         # spring, summer, fall, winter

class RecommendResponse(BaseModel):
    should_water_today: bool
    recommended_volume_ml: int
    recommended_frequency_days: int
    tips: List[str]
    fired_rules: List[str]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/recommend", response_model=RecommendResponse)
def recommend(req: RecommendRequest):
    inputs = Inputs(
        soil_moisture=req.soil_moisture,
        plant_type=req.plant_type,
        sunlight=req.sunlight,
        temperature_c=req.temperature_c,
        pot_size=req.pot_size,
        season=req.season,
    )
    rec = evaluate(inputs)
    return RecommendResponse(
        should_water_today=rec.should_water_today,
        recommended_volume_ml=rec.recommended_volume_ml,
        recommended_frequency_days=rec.recommended_frequency_days,
        tips=rec.tips,
        fired_rules=rec.fired_rules,
    )
