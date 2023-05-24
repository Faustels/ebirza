import subprocess
import shutil
import requests
from datetime import datetime

CREATE_NO_WINDOW = 0x08000000

currentHour = 0
data = []

def DownloadData():
    date = datetime.now();
    link = "https://www.nordpoolgroup.com/49b771/globalassets/download-center-market-data/mcp_data_report_" + date.strftime("%d-%m-%Y")+ "-00_00_00.xlsx"
    response = requests.get(link, stream=True)
    with open("Services/Price/duom.xlsx", "wb") as out_file:
        shutil.copyfileobj(response.raw, out_file)

def CreateData():
    subprocess.Popen("Rscript Price.R", cwd ="Services/Price", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=CREATE_NO_WINDOW)

def SetupNewData():
    DownloadData()
    CreateData()
    SetHour()

def SetHour():
    global currentHour
    currentHour = datetime.now().hour
    SetData()


def GetHour():
    return currentHour


def CombineArrays(array1, array2):
    ans = []
    for i in range(len(array1)):
        temp = [array1[i], array2[i]]
        ans.append(temp)
    return ans


def SetData():
    global data
    dataLocation = "Services/Price/Data/" + str(currentHour) + "/"

    file1 = open(dataLocation + "SellX.txt", "r")
    file2 = open(dataLocation + "SellY.txt", "r")
    sellArray = CombineArrays([float(x) for x in file1.readline().split()],
                                 [float(x) for x in file2.readline().split()])
    file1.close()
    file2.close()

    file1 = open(dataLocation + "BuyX.txt", "r")
    file2 = open(dataLocation + "BuyY.txt", "r")
    buyArray = CombineArrays([float(x) for x in file1.readline().split()],
                                [float(x) for x in file2.readline().split()])
    file1.close()
    file2.close()

    buyPos = 0
    sellPos = 0

    data = []


    while buyPos < len(buyArray) and sellPos < len(sellArray):
        temp = [None, None, None]
        buyPosIncrease = False
        sellPosIncrease = False
        if buyArray[buyPos][1] <= sellArray[sellPos][1]:
            temp[0] = buyArray[buyPos][1]
            temp[1] = buyArray[buyPos][0]
            buyPosIncrease = True
        if sellArray[sellPos][1] <= buyArray[buyPos][1]:
            temp[0] = sellArray[sellPos][1]
            temp[2] = sellArray[sellPos][0]
            sellPosIncrease = True
        if buyPosIncrease:
            buyPos += 1
        if sellPosIncrease:
            sellPos += 1
        data.append(temp)

    for i in range(buyPos, len(buyArray)):
        temp = [buyArray[i][1], buyArray[i][0], None]
        data.append(temp)

    for i in range(sellPos, len(sellArray)):
        temp = [sellArray[i][1], None, sellArray[i][0]]
        data.append(temp)

def GetData(mWh):
    if mWh <= 0:
        return GetParts(data)
    else:
        newData = []
        for i in data:
            temp = [None, None, None]
            temp[0] = i[0]
            temp[1] = i[1]
            temp[2] = i[2]
            if temp[2] != None:
                temp[2] += mWh
            newData.append(temp)
        return GetParts(newData)

def GetParts(splitData):
    splitAmount = 50
    lastBuy = None
    lastSell = None
    currentPos = 0

    for i in splitData:
        if i[1] is not None:
            lastBuy = [i[0], i[1]]
        if i[2] is not None:
            lastSell = [i[0], i[2]]
        currentPos += 1
        if lastBuy is not None and lastSell is not None:
            break
    while currentPos < len(splitData):
        if splitData[currentPos][1] is not None:
            lastBuy = [splitData[currentPos][0], splitData[currentPos][1]]
        if splitData[currentPos][2] is not None:
            lastSell = [splitData[currentPos][0], splitData[currentPos][2]]
        if lastBuy[1] < lastSell[1]:
            break
        currentPos += 1

    prevBuy = None
    prevSell = None
    for i in range(currentPos - 1, 0, -1):
        if splitData[i][1] is not None and prevBuy is None and splitData[i][1] != lastBuy[1]:
            prevBuy = [splitData[i][0], splitData[i][1]]
        if splitData[i][2] is not None and prevSell is None and splitData[i][2] != lastSell[1]:
            prevSell = [splitData[i][0], splitData[i][2]]
        if prevBuy is not None and prevSell is not None:
            break

    price = GetCross([prevBuy, lastBuy], [prevSell, lastSell])

    if currentPos + splitAmount / 2 >= len(splitData):
        currentPos = len(splitData) - (splitAmount / 2)
    elif currentPos < splitAmount / 2:
        currentPos = splitAmount / 2

    return splitData[int(currentPos - splitAmount / 2): int(currentPos + splitAmount / 2)], price

def GetCross(line1, line2):
    line1Mult = (line1[1][1] - line1[0][1]) / (line1[1][0] - line1[0][0])
    line2Mult = (line2[1][1] - line2[0][1]) / (line2[1][0] - line2[0][0])

    line1Null = line1[0][1] - line1[0][0] * line1Mult
    line2Null = line2[0][1] - line2[0][0] * line2Mult

    price = (line1Null - line2Null) / (line2Mult - line1Mult)

    return price


