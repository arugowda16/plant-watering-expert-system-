
import streamlit as st
import requests

st.set_page_config(page_title="Plant Watering Advisor", page_icon="🌿", layout="centered")

st.title("🌿 Plant Watering Advisor (Expert System)")
st.write("Beginner-friendly demo of a **rule-based expert system** with a FastAPI backend and Streamlit frontend.")

with st.form("inputs"):
    col1, col2 = st.columns(2)
    with col1:
        soil_moisture = st.slider("Soil moisture (%)", 0, 100, 35)
        plant_type = st.selectbox("Plant type", ["succulent", "leafy", "flowering", "herb"])
        pot_size = st.selectbox("Pot size", ["small", "medium", "large"])
    with col2:
        sunlight = st.selectbox("Sunlight", ["low", "medium", "high"])
        temperature_c = st.number_input("Temperature (°C)", min_value=-10.0, max_value=45.0, value=24.0, step=0.5)
        season = st.selectbox("Season", ["spring", "summer", "fall", "winter"])

    backend_url = st.text_input("Backend URL", value="http://127.0.0.1:8000")
    submitted = st.form_submit_button("Get Recommendation")

if submitted:
    try:
        payload = {
            "soil_moisture": soil_moisture,
            "plant_type": plant_type,
            "sunlight": sunlight,
            "temperature_c": float(temperature_c),
            "pot_size": pot_size,
            "season": season,
        }
        resp = requests.post(f"{backend_url}/recommend", json=payload, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            st.success("Recommendation generated!")

            left, right = st.columns(2)
            with left:
                st.metric("Should water today?", "Yes" if data["should_water_today"] else "No")
                st.metric("Recommended volume (ml)", data["recommended_volume_ml"])
            with right:
                st.metric("Frequency (days)", data["recommended_frequency_days"])

            with st.expander("Why these recommendations? (Rules fired)"):
                for rule in data["fired_rules"]:
                    st.write("• " + rule)

            st.subheader("Tips")
            for t in data["tips"]:
                st.write("• " + t)

        else:
            st.error(f"Backend error {resp.status_code}: {resp.text}")
    except Exception as e:
        st.error(f"Failed to reach backend: {e}")

st.markdown("---")
st.caption("Disclaimer: This is a simple demo for learning purposes, not professional horticulture advice.")
