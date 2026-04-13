import requests

API_KEY = "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"  


def generate_explanation(data):
    prompt = f"""
You are an AI agriculture assistant.

Given the following data:
Soil Moisture: {data['soil_moisture']}
Temperature: {data['temperature']}
Water Applied: {data['water']}
Plant Health: {data['plant_health']}
Nutrient Status: {data['nutrient_status']}

Explain the situation and suggest actions in simple human language.
"""

    try:
        print("Calling GenAI...")

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost",
                "X-Title": "AI Agriculture System"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )

        print("Status Code:", response.status_code)
        print("Response:", response.text)

        result = response.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"]

        else:
            print("API ERROR:", result)

            return (
                f"Soil moisture is {data['soil_moisture']}%. "
                f"Plant is {data['plant_health']}. "
                f"Basic system fallback explanation."
            )

    except Exception as e:
        print("EXCEPTION:", e)

        return (
            f"System fallback: Soil {data['soil_moisture']}%, "
            f"Plant {data['plant_health']}."
        )
    
def generate_explanation(sensor, weather, plant_health, irrigation):

    reasons = []

    # 💧 moisture
    if sensor["soil_moisture"] < 0.3:
        reasons.append("low soil moisture")

    # 🌡️ temperature
    if weather["temperature"] > 30:
        reasons.append("high temperature")

    # 🌱 plant health
    if plant_health < 60:
        reasons.append("poor plant health")

    # 🌧️ rain
    if weather["rain"] > 0:
        reasons.append("rain detected (reduced irrigation)")

    if not reasons:
        return "Conditions are stable. Moderate irrigation applied."

    explanation = " + ".join(reasons)

    return f"{explanation} → irrigation adjusted to {irrigation}"