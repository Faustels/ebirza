import subprocess

CREATE_NO_WINDOW = 0x08000000

currentHour = 0
sellArray = []
buyArray = []


def CreateData():
    subprocess.call("Rscript Price.R", stdout=subprocess.DEVNULL, creationflags=CREATE_NO_WINDOW)


def SetHour(h):
    global currentHour
    currentHour = h


def GetHour():
    return currentHour


def CombineArrays(array1, array2):
    ans = []
    for i in range(len(array1)):
        temp = []
        temp.append(array1[i])
        temp.append(array2[i])
        ans.append(temp)
    return ans


def SetData():
    global sellArray
    global buyArray
    dataLocation = "Services/Price/Data/" + str(currentHour) + "/"

    file1 = open(dataLocation + "SellX.txt", "r")
    file2 = open(dataLocation + "SellY.txt", "r")
    newSellArray = CombineArrays([float(x) for x in file1.readline().split()],
                                 [float(x) for x in file2.readline().split()])
    file1.close()
    file2.close()

    file1 = open(dataLocation + "BuyX.txt", "r")
    file2 = open(dataLocation + "BuyY.txt", "r")
    newBuyArray = CombineArrays([float(x) for x in file1.readline().split()],
                                [float(x) for x in file2.readline().split()])
    file1.close()
    file2.close()

    sellArray = newSellArray
    buyArray = newBuyArray
