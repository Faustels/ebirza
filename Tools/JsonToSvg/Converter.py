import json

fileName = "polygons.html"

def ReadFile(fileName):
    f = open("districts.json", encoding="utf-8")
    data = json.load(f)
    f.close()
    ans = []
    for i in range(len(data['features'])):
        ans.append([])
        for i2 in data['features'][i]['geometry']['coordinates']:
            for i3 in i2:
                ans[-1].append(i3)
    return ans

def FindMinMax(data):
    X = [100, 0]
    Y = [100, 0]
    for i in data:
        for i2 in i:
            for i3 in i2:
                if i3[0] < X[0]:
                    X[0] = i3[0]
                if i3[0] > X[1]:
                    X[1] = i3[0]

                if i3[1] < Y[0]:
                    Y[0] = i3[1]
                if i3[1] > Y[1]:
                    Y[1] = i3[1]
    return [X, Y]

def ToRange(data, minMax, trueMax):
    xRange = minMax[0][1] - minMax[0][0]
    yRange = minMax[1][1] - minMax[1][0]

    xMax = trueMax
    yMax = yRange / xRange * trueMax * 1.75
    ans = []
    for i in data:
        ans.append([])
        for i2 in i:
            ans[-1].append([])
            for i3 in i2:
                ans[-1][-1].append([ (i3[0] - minMax[0][0]) / ( minMax[0][1] - minMax[0][0]) * xMax, (i3[1] - minMax[1][0]) / ( minMax[1][1] - minMax[1][0]) * yMax])
    return ans, [xMax, yMax]

def Invert(data, max):
    ans = []
    for i in data:
        ans.append([])
        for i2 in i:
            ans[-1].append([])
            for i3 in i2:
                ans[-1][-1].append([i3[0], max - i3[1]])
    return ans


def ToSVG(data):
    i = 0
    ans = "<svg height=\"100%\" width=\"100%\">\n"

    for i in data:
        ans += "\t <g class=\"mapG\" onmouseover=\"toFront(this)\">\n"
        for i2 in i:
            ans += "\t\t <polygon points=\""
            for i3 in i2:
                ans += str(i3[0]) + "," + str(i3[1]) + " "
            ans += "\" />\n"
        ans += "\t</g>\n"
    ans += "</svg>"
    return ans

def ToFile(ans, fileName):
    f = open(fileName, "w")
    f.write(ans)
    f.close()

data = ReadFile(fileName)
coords, maxRange = ToRange(data, FindMinMax(data), 1000)
coords = Invert(coords, maxRange[1])
ToFile(ToSVG(coords), fileName)
