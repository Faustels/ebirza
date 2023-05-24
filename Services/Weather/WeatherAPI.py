from Services.Database.database import MySQLGet
from Services.Weather.NeuralNetwork import NeuralNetwork
from datetime import datetime, timedelta
import requests
import json
import numpy as np

weatherStations = []
network = None
historicalWeather = {}
predictedWeather = {}
predictions = {}
inputMinMax = [[-20.37222222222222, 33.06111111111111],
               [0.011111111111111112, 10.13888888888889],
               [0.18333333333333332, 19.572222222222223],
               [10.555555555555555, 349.3333333333333],
               [0.0, 100.0],
               [974.3055555555555, 1047.5944444444444],
               [19.944444444444443, 98.83333333333333],
               [0.0, 3.7111111111111104]]
resultMinMax = [[0.0, 59.83]]

def SetNetwork():
    global network
    network = NeuralNetwork.LoadNetwork("Services/Weather/network.json")
    
def PrepareWeatherAPI():
    global weatherStations
    with open("Services/Weather/stations.json") as file:
        weatherStations = json.loads(file.read())
    SetNetwork()

def UpdateData():
    global historicalWeather
    global predictedWeather
    date = datetime.now()
    day = timedelta(days=1)
    currentDate = date.strftime("%Y-%m-%d")
    date -= day
    previousDate = date.strftime("%Y-%m-%d")
    tempHistoricalWeather = {}
    tempPredictedWeather = {}

    for station in weatherStations:
        newHistorical = []
        response = requests.get("https://api.meteo.lt/v1/stations/" + station["name"] + "/observations/" + previousDate).json()
        newHistorical.extend(response["observations"])
        response = requests.get("https://api.meteo.lt/v1/stations/" + station["name"] + "/observations/" + currentDate).json()
        newHistorical.extend(response["observations"])
        tempHistoricalWeather[station["name"]] = newHistorical

        response = requests.get("https://api.meteo.lt/v1/places/" + station["cityName"] + "/forecasts/long-term").json()
        tempPredictedWeather[station["name"]] = response["forecastTimestamps"]


    historicalWeather = tempHistoricalWeather
    predictedWeather = tempPredictedWeather

def GetPrediction(latitude, longitude):
    closestStation = GetClosestStation(latitude, longitude)

def GeneratePredictions(date):
    inputs = {}
    hours12 = timedelta(hours = 12)
    hour1 = timedelta(hours=1)
    date -= hours12

    for station in weatherStations:
        inputs[station["name"]] = []

    for i in range(48):
        currentDate = ToDateStr(date)
        for station in weatherStations:
            foundData = False
            for old in historicalWeather[station["name"]]:
                if old["observationTimeUtc"] == currentDate:
                    foundData = True
                    inputs[station["name"]].append(old)
                    break
                if not foundData:
                    for new in predictedWeather[station["name"]]:
                        if new["forecastTimeUtc"] == currentDate:
                            inputs[station["name"]].append(new)
        date += hour1
    data = OrderData(inputs)
    for key in data:
        data[key] = Normalize(data[key], inputMinMax)
    data = ToParts(data)
    Predict(data)
    print(data["birzu-ams"][0])


def OrderData(data):
    order = ["airTemperature", "windSpeed", "windGust",
             "windDirection", "cloudCover", "seaLevelPressure",
             "relativeHumidity", "precipitation"]

    for key in data:
        newData = []
        for element in data[key]:
            tempElement = []
            for orderKey in order:
                if orderKey not in element:
                    tempElement.append(element["totalPrecipitation"])
                else:
                    tempElement.append(element[orderKey])
            newData.append(tempElement)
        data[key] = newData
    return data

def ToParts(data):
    for key in data:
        newData = []
        for pos in range(len(data[key]) - 12):
            tempNewData = []
            for newDataPos in range(13):
                tempNewData.extend(data[key][pos + newDataPos])
            newData.append(tempNewData)

        data[key] = np.array(newData)
    return data

def Predict(data):
    global predictions
    for key in data:
        outputs = network.Input(data[key])[-1]
        outputs = Unnormalize(outputs, resultMinMax)
        predictions[key] = outputs

def Normalize(inputs, normalizer):
    ans = []
    rowLength = len(normalizer)
    for row in inputs:
        newRow = []
        for pos in range(rowLength):
            element = row[pos]
            if element is None:
                element = 0
            newRow.append((element - normalizer[pos][0]) / (normalizer[pos][1] - normalizer[pos][0]))
        ans.append(newRow)
    return np.array(ans)
def Unnormalize(inputs, normalizer):
    ans = []
    rowLength = len(normalizer)
    for row in inputs:
        newRow = []
        for pos in range(rowLength):
            element = row[pos]
            newRow.append(element *
                (normalizer[pos][1] - normalizer[pos][0])
                + normalizer[pos][0])
        ans.append(newRow)
    return ans

def ToDateStr(date):
    return date.strftime("%Y-%m-%d %H") + ":00:00"

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
