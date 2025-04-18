from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request
import requests
import os
from werkzeug.middleware.dispatcher import DispatcherMiddleware

flask_app = Flask(__name__)
API_KEY = os.getenv("OPENWEATHER_API_KEY")

@flask_app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None

    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
            response = requests.get(url)
            if response.status_code == 200:
                weather_data = response.json()
            else:
                error = f"City '{city}' not found."

    return render_template('index.html', weather=weather_data, error=error)

# Mount the app at /api-assignment
app = DispatcherMiddleware(Flask('dummy_root'), {
    '/api-assignment': flask_app
})
