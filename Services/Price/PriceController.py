import subprocess
import datetime
CREATE_NO_WINDOW = 0x08000000

def CreateData():
    subprocess.call("Rscript Price.R", stdout=subprocess.DEVNULL, creationflags=CREATE_NO_WINDOW)