from django.shortcuts import render
from django.http import JsonResponse
import requests
import datetime

API_KEY = "fdc698257ddd41ab530c2053b282bd54"


# 🌤 MAIN VIEW
def home(request):
    city = "Delhi"
    lat = None
    lon = None

    current = None
    daily = []
    exception_occurred = False

    # 📥 If POST → use user input
    if request.method == "POST":
        city = request.POST.get("city")
        lat = request.POST.get("lat")
        lon = request.POST.get("lon")

    try:
        # 🔍 Always fetch lat/lon (even on GET)
        if not lat or not lon:
            geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={'fdc698257ddd41ab530c2053b282bd54'}"
            geo_data = requests.get(geo_url).json()

            if not geo_data:
                raise Exception("City not found")

            lat = geo_data[0]["lat"]
            lon = geo_data[0]["lon"]

        # 🌤 CURRENT WEATHER
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={'fdc698257ddd41ab530c2053b282bd54'}&units=metric"
        weather_data = requests.get(weather_url).json()

        print("WEATHER:", weather_data)  # 👈 DEBUG

        if weather_data.get("cod") != 200:
            raise Exception("Weather error")

        current = weather_data

        # 📅 FORECAST
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={'fdc698257ddd41ab530c2053b282bd54'}&units=metric"
        forecast_data = requests.get(forecast_url).json()

        print("FORECAST:", forecast_data)  # 👈 DEBUG

        daily = forecast_data['list'][::8]

    except Exception as e:
        print("ERROR:", e)
        exception_occurred = True

    day = datetime.date.today()

    return render(request, "weatherapp/index.html", {
        "city": city,
        "current": current,
        "daily": daily,
        "day": day,
        "exception_occurred": exception_occurred
    })


# 🔽 DROPDOWN API
def get_cities(request):
    query = request.GET.get("q")

    if not query:
        return JsonResponse([], safe=False)

    url = f"https://api.openweathermap.org/geo/1.0/direct?q={query}&limit=5&appid={'fdc698257ddd41ab530c2053b282bd54'}"

    try:
        response = requests.get(url)
        data = response.json()

        result = []
        for city in data:
            result.append({
                "name": city.get("name"),
                "state": city.get("state"),
                "country": city.get("country"),
                "lat": city.get("lat"),
                "lon": city.get("lon"),
            })

        return JsonResponse(result, safe=False)

    except Exception as e:
        print("City API error:", e)
        return JsonResponse([], safe=False)