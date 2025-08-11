
"""
Plant Watering Advisor - Rule-based Expert System
-------------------------------------------------
Inputs:
- soil_moisture: int (0-100 %) — current soil moisture
- plant_type: one of ["succulent", "leafy", "flowering", "herb"]
- sunlight: one of ["low", "medium", "high"]
- temperature_c: float (°C)
- pot_size: one of ["small", "medium", "large"]
- season: one of ["spring", "summer", "fall", "winter"]

Outputs (recommendation):
- should_water_today: bool
- recommended_volume_ml: int
- recommended_frequency_days: int
- tips: list[str]
- fired_rules: list[str]  (explanations)
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class Inputs:
    soil_moisture: int
    plant_type: str       # succulent, leafy, flowering, herb
    sunlight: str         # low, medium, high
    temperature_c: float
    pot_size: str         # small, medium, large
    season: str           # spring, summer, fall, winter

@dataclass
class Recommendation:
    should_water_today: bool
    recommended_volume_ml: int
    recommended_frequency_days: int
    tips: List[str]
    fired_rules: List[str]

ALLOWED = {
    "plant_type": {"succulent", "leafy", "flowering", "herb"},
    "sunlight": {"low", "medium", "high"},
    "pot_size": {"small", "medium", "large"},
    "season": {"spring", "summer", "fall", "winter"},
}

def clamp(val: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, val))

def base_by_plant(plant_type: str) -> Tuple[int, int, List[str]]:
    """Return (base_freq_days, base_volume_ml, fired_rule)"""
    if plant_type == "succulent":
        return 10, 120, ["Base: succulents need infrequent, small watering"]
    if plant_type == "leafy":
        return 4, 250, ["Base: leafy plants need moderate watering"]
    if plant_type == "flowering":
        return 3, 300, ["Base: flowering plants need more frequent watering"]
    if plant_type == "herb":
        return 2, 220, ["Base: herbs need frequent, moderate watering"]
    # fallback
    return 5, 200, ["Base: default profile"]

def evaluate(inputs: Inputs) -> Recommendation:
    # Validate categorical
    for k in ["plant_type", "sunlight", "pot_size", "season"]:
        val = getattr(inputs, k)
        if val not in ALLOWED[k]:
            raise ValueError(f"Invalid {k}: {val}. Allowed: {sorted(ALLOWED[k])}")
    if not (0 <= inputs.soil_moisture <= 100):
        raise ValueError("soil_moisture must be 0..100")

    fired = []
    tips = []

    freq_days, vol_ml, base_rule = base_by_plant(inputs.plant_type)
    fired.extend(base_rule)

    # Soil moisture based urgency
    # <15% => urgent, 15-30 => soon, 30-60 => moderate, >60 => low
    if inputs.soil_moisture < 15:
        fired.append("Moisture <15% => Very dry: decrease interval, increase volume")
        freq_days -= 2
        vol_ml += 100
    elif inputs.soil_moisture < 30:
        fired.append("Moisture 15–29% => Dry: decrease interval, slight volume boost")
        freq_days -= 1
        vol_ml += 50
    elif inputs.soil_moisture > 60:
        fired.append("Moisture >60% => Wet: increase interval, reduce volume")
        freq_days += 2
        vol_ml -= 50
        tips.append("Soil is already quite moist — ensure pot has proper drainage.")

    # Sunlight
    if inputs.sunlight == "high":
        fired.append("High sunlight => plants transpire more: water a bit more, sooner")
        freq_days -= 1
        vol_ml += 50
    elif inputs.sunlight == "low":
        fired.append("Low sunlight => slower evaporation: water less, less often")
        freq_days += 1
        vol_ml -= 30

    # Temperature
    if inputs.temperature_c > 28:
        fired.append("Hot (>28°C) => increase water and decrease interval")
        freq_days -= 1
        vol_ml += 60
    elif inputs.temperature_c < 15:
        fired.append("Cool (<15°C) => reduce water and increase interval")
        freq_days += 1
        vol_ml -= 40

    # Pot size
    if inputs.pot_size == "large":
        fired.append("Large pot => holds more water: increase volume, slightly longer interval")
        vol_ml += 80
        freq_days += 1
    elif inputs.pot_size == "small":
        fired.append("Small pot => dries faster: decrease interval, slightly reduce volume")
        freq_days -= 1
        vol_ml -= 30

    # Season
    if inputs.season == "summer":
        fired.append("Summer => higher evapotranspiration: water a bit more, sooner")
        freq_days -= 1
        vol_ml += 40
    elif inputs.season == "winter":
        fired.append("Winter => plant growth slows: water less, less often")
        freq_days += 2
        vol_ml -= 60

    # Clamp sensible bounds
    freq_days = clamp(freq_days, 1, 14)
    vol_ml = clamp(vol_ml, 50, 600)

    # Decision: should water today?
    # Water today if soil is pretty dry OR conditions are harsh and not too wet.
    should_water_today = (inputs.soil_moisture < 30) or (
        inputs.soil_moisture < 50 and inputs.sunlight == "high" and inputs.temperature_c > 28
    )
    if not should_water_today and inputs.soil_moisture > 60:
        tips.append("Skip watering for now. Recheck moisture in a few days.")

    # Generic tips
    tips.append("Always water until excess drains out; never leave roots sitting in water.")
    tips.append("Recheck soil moisture with your finger 2–3 cm below the surface before watering.")

    return Recommendation(
        should_water_today=bool(should_water_today),
        recommended_volume_ml=int(vol_ml),
        recommended_frequency_days=int(freq_days),
        tips=tips,
        fired_rules=fired
    )

if __name__ == "__main__":
    # Quick manual test
    demo = Inputs(
        soil_moisture=22,
        plant_type="leafy",
        sunlight="high",
        temperature_c=29.5,
        pot_size="medium",
        season="summer",
    )
    rec = evaluate(demo)
    print(rec)
