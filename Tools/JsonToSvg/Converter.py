import json

fileName = "polygons.txt"

def readFile(fileName):
    f = open("districts.json", encoding="utf-8")
    data = json.load(f)
    f.close()
    ans = []
    for i in range(len(data['features'])):
        ans.append(data['features'][i]['geometry']['coordinates'][0][0])
    return ans

def findMinMax(data):
    X = [100,0]
    Y = [100, 0]
    for i in data:
        for i2 in i:
            if i2[0] < X[0]:
                X[0] = i2[0]
            if i2[0] > X[1]:
                X[1] = i2[0]

            if i2[1] < Y[0]:
                Y[0] = i2[1]
            if i2[1] > Y[1]:
                Y[1] = i2[1]
    return [X, Y]

def toRange(data, minMax, trueMax):
    xRange = minMax[0][1] - minMax[0][0]
    yRange = minMax[1][1] - minMax[1][0]

    if xRange > yRange:
        yMax = trueMax * yRange / xRange
        xMax = trueMax
    else:
        xMax = trueMax * xRange / yRange
        yMax = trueMax
    ans = []
    for i in range(len(data)):
        ans.append([])
        for i2 in data[i]:
            ans[i].append([ (i2[0] - minMax[0][0]) / ( minMax[0][1] - minMax[0][0]) * xMax, (i2[1] - minMax[1][0]) / ( minMax[1][1] - minMax[1][0]) * yMax])
    return ans

data = readFile(fileName)
print(toRange(data, findMinMax(data), 1000))
