import requests
from Services.Database.database import MySQLGet

weatherStations = []

def GetWeather(latitude, longitude):
    if len(weatherStations) == 0:
        PrepareWeatherAPI()
    
def PrepareWeatherAPI():
    global weatherStations
    weatherStations = MySQLGet("Select * from station", (0,))
    print(weatherStations)

def Distance(x1, y1, x2, y2):
    return (((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5
def GetClosestStation(latitude, longitude):
    closestStation = weatherStations[0]["id"]
    closestDistance = Distance(weatherStations[0]["latitude"], weatherStations[0]["longitude"], latitude, longitude)
    for station in weatherStations:
        currentDistance = Distance(station["latitude"], station["longitude"], latitude, longitude)
        if currentDistance < closestDistance:
            closestStation = station["id"]
            closestDistance = currentDistance
    return closestStation
