

const WEATHER_CODES = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing Rime Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Dense Drizzle",
    56: "Light Freezing Drizzle",
    57: "Dense Freezing Drizzle",
    61: "Slight Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    66: "Light Freezing Rain",
    67: "Heavy Freezing Rain",
    71: "Slight Snow Fall",
    73: "Moderate Snow Fall",
    75: "Heavy Snow Fall",
    77: "Snow Grains",
    80: "Slight Rain Showers",
    81: "Moderate Rain Showers",
    82: "Violent Rain Showers",
    85: "Slight Snow Showers",
    86: "Heavy Snow Showers",
    95: "Thunderstorm",
    96: "Thunderstorm with Slight Hail",
    99: "Thunderstorm with Heavy Hail",
}

fetch('../weather.json?t=' + Date.now())
    .then(response => response.json())
    .then(w => {
        // const hour = new Date().getHours();
        const weatherCode = w.current.weather_code;
        const weatherTemp = Math.round(w.current.temperature_2m);
        document.querySelector(".Title").textContent = WEATHER_CODES[weatherCode];
        document.querySelector(".Temperature").textContent = weatherTemp + "°F";
        document.querySelector(".City-name").textContent = w.city_name;
        document.querySelector(".time-text").textContent = w.current.time;
    });



