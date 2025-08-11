
# 🌿 Plant Watering Advisor — Rule-based Expert System

A beginner-friendly final project that checks all assignment boxes:
- **Expert system** (rule-based rules with explanations)
- **Backend API** using FastAPI (`/recommend`)
- **Frontend** using Streamlit (simple interactive UI)
- **Clear block diagram & pipeline** (see `docs/report.md`)
- **Easy to run locally**

---

## 🧩 Project Structure

```
plant-watering-expert-system/
├─ backend/
│  ├─ app.py          # FastAPI backend (POST /recommend)
│  └─ engine.py       # Rule-based expert system core
├─ frontend/
│  └─ streamlit_app.py  # Streamlit UI
├─ docs/
│  └─ report.md       # Short report template with block diagram
├─ requirements.txt
└─ README.md
```

---

## 🔧 Quickstart (Local)

> **Prereq**: Python 3.9+ recommended.

```bash
# 1) Create & activate a virtual environment (recommended)
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2) Install deps
pip install -r requirements.txt

# 3) Run the backend (terminal 1)
uvicorn backend.app:app --reload --port 8000

# 4) Run the frontend (terminal 2)
streamlit run frontend/streamlit_app.py
```

Open the Streamlit URL it prints (usually `http://localhost:8501`), make sure the **Backend URL** field is `http://127.0.0.1:8000`, and click **Get Recommendation**.

---

## 🔬 Test quickly with `curl`

```bash
curl -X POST "http://127.0.0.1:8000/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "soil_moisture": 22,
    "plant_type": "leafy",
    "sunlight": "high",
    "temperature_c": 29.5,
    "pot_size": "medium",
    "season": "summer"
  }'
```

Expected: JSON with `should_water_today`, `recommended_volume_ml`, `recommended_frequency_days`, `tips`, and `fired_rules`.

---

## 🧠 How the Expert System Works (Short)

- We start with a **base profile** per plant type (succulent/leafy/flowering/herb): default watering frequency (days) and volume (ml).
- We apply **if–then rules** to adjust the base recommendations based on:
  - Soil moisture (dry vs. wet)
  - Sunlight (low/medium/high)
  - Temperature (°C)
  - Pot size (small/medium/large)
  - Season (spring/summer/fall/winter)
- The engine returns the final recommendation **+ list of rules fired** as an explanation.

See `backend/engine.py` for readable rule logic.

---

## 🎥 10‑Minute Video Outline (Investor Pitch Style)

1. **Hook & Problem (1 min)**  
   - Many beginners overwater or underwater houseplants. It’s confusing to balance plant type, moisture, sunlight, and season.

2. **Solution (1 min)**  
   - A lightweight **expert system** that explains **why** it recommends watering or waiting — transparent, cheap, and fast.

3. **Live Demo (3 min)**  
   - Change inputs in Streamlit, show backend JSON, point out “Rules fired” explanations.

4. **How It Works (2–3 min)**  
   - Rule base: base profiles + adjustments.  
   - API: FastAPI endpoint `/recommend`.  
   - Frontend: Streamlit form -> calls API -> displays results.

5. **Performance & Validation (1–2 min)**  
   - Show 3–5 test scenarios (dry succulent in summer vs. wet herb in winter, etc.).  
   - Emphasize consistency and interpretability.

6. **Wrap (1 min)**  
   - Roadmap: add soil sensor input, log history, reminders, and a tiny RAG module to fetch care tips from trusted sources.

---

## ⚠️ Disclaimer
This is a **learning demo**. For real plants, cross-check with care guides.
