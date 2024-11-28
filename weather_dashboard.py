from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "486fc37c40612d0599d9f137d887b227"  # Replace with your actual API key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city", "")  # Get city from user input
    if not city:
        return render_template("index.html", error="Please enter a city.")

    # Fetch weather data from the OpenWeatherMap API
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    
    # Print the API response status code and content for debugging
    print(f"API Response Status Code: {response.status_code}")
    print(f"API Response Text: {response.text}")

    data = response.json()

    # Check if the API returned a successful response
    if response.status_code != 200:
        error_message = data.get("message", "Something went wrong, please try again.")
        return render_template("index.html", error=f"City '{city}' not found! Error: {error_message}")

    # Extract weather data from the API response
    weather = {
        "city": city,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"]
    }

    # Render the weather data on the HTML page
    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run(debug=True)




