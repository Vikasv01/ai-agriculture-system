from fastapi import FastAPI
from ai_models.plant_health import plant_health
from ai_models.decision_engine import decide_irrigation
from simulation.sensor_simulator import get_sensor_data
from backend.weather_service import get_weather
from genai.explanation_engine import generate_explanation
from ai_models.prediction_model import predict_moisture

app = FastAPI()

@app.get("/status")
def status():

    weather = get_weather(12.97, 77.59)
    sensor = get_sensor_data(weather, irrigation=0) 

    predicted_moisture = predict_moisture(
    sensor["soil_moisture"],
    weather["temperature"],
    weather["humidity"]
)
     # store it in sensor
    sensor["predicted_moisture"] = predicted_moisture

    # STEP 1: define health FIRST
    health = plant_health(
        sensor["soil_moisture"],
        sensor["pH"],
        sensor["EC"],
        sensor["N"],
        sensor["P"],
        sensor["K"]
    )

    # STEP 2: then use it
    irrigation = decide_irrigation(sensor, weather, health)

    explanation = generate_explanation(sensor, weather, health, irrigation)

    # STEP 3: return
    return {
        "sensor": sensor,
        "weather": weather,
        "plant_health": health,
        "predicted_moisture": sensor.get("predicted_moisture"), 
        "irrigation": irrigation,
        "explanation": explanation 
    }