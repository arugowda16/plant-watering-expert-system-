
# Plant Watering Advisor — Final Project Report

## 1) Problem Identification
New plant owners often underwater or overwater because care depends on **several interacting factors**: soil moisture, plant type, sunlight, temperature, pot size, and season. A simple, **explainable** expert system can guide correct watering while teaching the reasoning behind it.

**Why important?**  
- Prevents plant stress and root rot  
- Saves water  
- Builds user confidence with transparent advice (rules shown to the user)

**Why expert system?**  
- The task maps naturally to **if–then rules** used by human experts.  
- Logic is **interpretable** and runs locally without expensive models.

---

## 2) System Pipeline & Block Diagram

**Pipeline:**  
User input → Frontend (Streamlit) → Backend API (FastAPI) → Rule Engine → Recommendation + Explanations → Frontend displays results

**Block Diagram (ASCII)**

```
+-------------+        HTTP JSON        +-------------------+
|  Frontend   |  POST /recommend -----> |   FastAPI Backend |
| (Streamlit) |                          |   (app.py)        |
+------+------+                          +----+--------------+
       |                                       |
       | calls                                 | imports
       v                                       v
+------+------------------+          +---------+--------------+
|  User Inputs (UI form)  |          |  Rule Engine (engine) |
|  moisture, plant, etc.  |          |  - base profile       |
+-------------------------+          |  - adjustment rules   |
                                     |  - explanation list   |
                                     +-----------+----------+
                                                 |
                                                 v
                                      +----------+-----------+
                                      | JSON Recommendation  |
                                      | water_today, volume, |
                                      | frequency, tips,     |
                                      | fired_rules          |
                                      +----------------------+
```

---

## 3) Front-end Application
- Built with **Streamlit** (simple form + metrics + expandable “Rules fired”).  
- User can adjust inputs and press “Get Recommendation”.  
- Backend URL is configurable (default `http://127.0.0.1:8000`).

---

## 4) Code Explanation (Technical Highlights)
- `backend/engine.py`:  
  - Starts with a **base** watering plan per `plant_type`.  
  - Applies **if–then rules** for soil moisture, sunlight, temperature, pot size, and season.  
  - **Clamps** outputs to reasonable ranges and returns **explanations** for transparency.
- `backend/app.py` (FastAPI):  
  - Defines input schema & output schema using **Pydantic**.  
  - POST `/recommend` builds `Inputs` object and calls `evaluate()`.
- `frontend/streamlit_app.py`:  
  - Collects inputs, calls the API with `requests`, and displays metrics + explanations.

---

## 5) Performance (Sample Scenarios)
1. **Succulent, very dry, summer, high sun, hot**  
   - Expect: **Yes, water today**; medium volume; short interval (e.g., 3–5 days).
2. **Herb, wet soil, winter, low sun, cool**  
   - Expect: **No, skip today**; low volume; longer interval (e.g., 7–12 days).
3. **Leafy, moderate moisture, spring, medium sun**  
   - Expect: Balanced volume; moderate interval.

These illustrate **rule consistency** and **sensible outputs** across edge cases.

---

## 6) Future Work
- Add “days since last watering” and plant age to refine decisions.
- Log user actions and outcomes to **learn** better thresholds.
- Optional **RAG**: retrieve care tips from reputable sources for the selected plant type.

---

## 7) How to Run
See root `README.md` for step‑by‑step instructions.
