from flask import Flask, request
import googlemaps
import numpy as np
import pytz
import os
from datetime import datetime, timedelta
import requests
import africastalking
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 


app = Flask(__name__)

# Replace with your actual API key
api_key = os.getenv("GOOGLE_MAPS_API_KEY")
gmaps_client = googlemaps.Client(api_key)
USERNAME = "semishonian@gmail.com"
API_KEY  = os.getenv("AFRICA_TALKING_KEY")
africastalking.initialize(USERNAME, API_KEY)
ussd = africastalking.USSD

destinations = ["4 Abule Oja, Yaba", "5 Oniru, Victoria Island, Lagos", "27 Ojota, Lagos", "10 Obanikoro, Lagos"]
mode = "driving"

# Utilities from your previous code


def get_lon_lat(address,gmaps_client):
    loc = gmaps_client.geocode(address)
    coords = (loc[0]['geometry']['location']["lat"], loc[0]['geometry']['location']["lng"])
    return coords 
def get_distances(destinations,origin,gmaps_client,mode):
    results  = []
    distances = gmaps_client.distance_matrix(
        origins = [origin],
        destinations = destinations,
        mode = mode
    )

    # check if valid reponses were sent:
    for i, data in enumerate(distances["rows"][0]['elements']):
        if data["status"] == "OK":
            rec = {"distance":data["distance"]["value"], "ETA":data["duration"]["text"]}
            results.append(rec)
           # do some shit
        else:
            results.append(None) 
    return results

def get_custom_forecast(
    latitude: float,
    longitude: float,
    timezone: str = "Africa/Lagos",
) -> list[dict]:
    """
    Gets a tailored weather forecast:
      • If current time ≤ 20:00 → forecast for now+3h (Today) + 7AM, 12PM, 3PM (Tomorrow)
      • Else → just 7AM, 12PM, 3PM (Tomorrow)
    
    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        timezone (str): Timezone string, e.g. 'Africa/Lagos'.
    
    Returns:
        list[dict]: Weather forecast entries.
    """
    # Get current time in local timezone
    tz = pytz.timezone(timezone)
    now = datetime.now(tz)

    # Fetch weather data
    resp = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "temperature_2m,precipitation",
            "forecast_days": 2,
            "timezone": timezone
        }
    ).json()

    times = resp["hourly"]["time"]
    temps = resp["hourly"]["temperature_2m"]
    precs = resp["hourly"]["precipitation"]

    # Build lookup for (date, hour) → index
    lookup = {
        (datetime.fromisoformat(t).date(), datetime.fromisoformat(t).hour): i
        for i, t in enumerate(times)
    }

    results = []

    # Include 3 hours ahead only if current time is ≤ 20:00
    if now.hour <= 20:
        future_time = now + timedelta(hours=3)
        key = (future_time.date(), future_time.hour)
        if key in lookup:
            idx = lookup[key]
            results.append({
                "day": "Today",
                "time": future_time.strftime("%I %p").lstrip("0"),
                "temperature": temps[idx],
                "precipitation": precs[idx],
                "timezone": timezone
            })

    # Always include 7 AM, 12 PM, and 3 PM of tomorrow
    tomorrow = (now + timedelta(days=1)).date()
    for hr in (7, 12, 15):
        key = (tomorrow, hr)
        if key in lookup:
            idx = lookup[key]
            dt = datetime.fromisoformat(times[idx])
            results.append({
                "day": "Tomorrow",
                "time": dt.strftime("%I %p").lstrip("0"),
                "temperature": temps[idx],
                "precipitation": precs[idx],
                "timezone": timezone
            })

    return results

def get_closest_storage_fac(data,destinations):
    distances = []
    for index, store_dat in enumerate(data):
        if store_dat!=None:
            distances.append(store_dat["distance"])
        else:
            distances.append(np.inf)
    
    closest_index = np.argmin(distances)
    return(destinations[closest_index],round(distances[closest_index]/1000,2),data[closest_index]["ETA"]) #closest storage facility , distance in km, ETA





# USSD API Endpoint
@app.route('/ussd', methods=['POST'])
def ussd_callback():
    session_id = request.form.get("sessionId")
    phone_number = request.form.get("phoneNumber")
    text = request.values.get("text", "default")


    parts = text.split("*")
    level = len(parts)

    if text == "":
        return "CON Welcome to Cyber Farm.\nEnter your location:"
    
    elif level == 1:
        return "CON What do you want to do?\n1. Get Weather Forecast\n2. Find Nearest Storage"

    elif level == 2:
        address = parts[0]
        option = parts[1]

        try:
            origin_coords = get_lon_lat(address, gmaps_client)
        except Exception:
            return "END Could not find your location. Please try again."

        timestamp = datetime.now().timestamp()
        timezone_info = gmaps_client.timezone(location=origin_coords, timestamp=timestamp)
        timezone_id = timezone_info['timeZoneId']

        if option == "1":
            forecast = get_custom_forecast(origin_coords[0], origin_coords[1], timezone=timezone_id)
            if forecast!= None:
                forecast_text = "\n".join([f"{f['day']} {f['time']}: {f['temperature']}°C, {f['precipitation']}mm" for f in forecast[:3]])
                return f"END Weather Forecast:\n{forecast_text}"
            else:
                return "END An error Occured. Please try again."

        
        elif option == "2":
            distances = get_distances(destinations, origin_coords, gmaps_client, mode)
            closest, dist_km, eta = get_closest_storage_fac(distances, destinations)
            if closest!=None and dist_km!=None and eta!=None:
                return f"END Nearest Storage:\n{closest}\nDistance: {dist_km} km\nETA: {eta} by driving"
            else:
                return "END An error Occured. Please try again."

        else:
            return "END Invalid option. Please try again."

    else:
        return "END Invalid input."

