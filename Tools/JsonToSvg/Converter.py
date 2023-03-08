import json

fileName = "polygons.html"

def ReadFile(fileName):
    f = open("districts.json", encoding="utf-8")
    data = json.load(f)
    f.close()
    ans = []
    for i in range(len(data['features'])):
        if i != 2:
            ans.append(data['features'][i]['geometry']['coordinates'][0][0])
        else:
            ans.append(data['features'][i]['geometry']['coordinates'][1][0])
            ans.append(data['features'][i]['geometry']['coordinates'][3][0])
    return ans

def FindMinMax(data):
    X = [100, 0]
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

def ToRange(data, minMax, trueMax):
    xRange = minMax[0][1] - minMax[0][0]
    yRange = minMax[1][1] - minMax[1][0]

    xMax = trueMax
    yMax = yRange / xRange * trueMax * 1.75
    ans = []
    for i in range(len(data)):
        ans.append([])
        for i2 in data[i]:
            ans[i].append([ (i2[0] - minMax[0][0]) / ( minMax[0][1] - minMax[0][0]) * xMax, (i2[1] - minMax[1][0]) / ( minMax[1][1] - minMax[1][0]) * yMax])
    return ans, [xMax, yMax]

def Invert(data, max):
    ans = []
    for i in data:
        temp = []
        for i2 in i:
            temp.append([i2[0], max - i2[1]])
        ans.append(temp)
    return ans


def ToSVG(data):
    ans = "<svg height=\"100%\" width=\"100%\">\n"

    for i in range(len(data)):
        ans += "\t <g style=\"stroke:purple;stroke-width:3;fill:none\">\n"
        if i != 2:

            ans += "\t\t <polygon points=\""
            for i2 in data[i]:
                ans += str(i2[0]) + "," + str(i2[1]) + " "
            ans += "\" />\n"
        else:
            for temp in range(2):
                ans += "\t\t <polygon points=\""
                for i2 in data[i + temp]:
                    ans += str(i2[0]) + "," + str(i2[1]) + " "
                ans += "\" />\n"
            i += 1
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
