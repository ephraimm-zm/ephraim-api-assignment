document.getElementById('weather-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const city = document.getElementById('city-input').value;
    
    fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`)
        .then(response => response.json())
        .then(data => {
            if (data.cod === "404") {
                showError(`City '${city}' not found.`);
            } else {
                showWeather(data);
            }
        })
        .catch(error => {
            showError('Failed to fetch weather data.');
        });
});
