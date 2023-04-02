import requests
from Services.Database.database import MySQLGet

def GetForecast(county):
    coords = MySQLGet("Select latitude, longitude from county where name = %s", (county,))
    arguments = {"latitude" : coords[0]["latitude"], "longitude": coords[0]["longitude"],
                 "hourly": ["temperature_2m","relativehumidity_2m","precipitation","surface_pressure",
                            "cloudcover,windspeed_10m","winddirection_10m","windgusts_10m","shortwave_radiation",
                            "direct_radiation","diffuse_radiation","direct_normal_irradiance"]}
    r = requests.get("https://api.open-meteo.com/v1/forecast", params = arguments)
    responseArray = r.json()
    ans = [{} for i in range(len(responseArray["hourly"]["time"]))]
    for key in responseArray["hourly"]:
        for currentPoz in range(len(responseArray["hourly"][key])):
            ans[currentPoz][key] = responseArray["hourly"][key][currentPoz]
    return ans