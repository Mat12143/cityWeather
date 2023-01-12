# --------------------------------------------------------------------------------------------------------------------------------------------#
# City Temperature Tracker
# by Mat12143
# --------------------------------------------------------------------------------------------------------------------------------------------#

# --------------------------------------------------------------------------------------------------------------------------------------------#
# Import Modules
# --------------------------------------------------------------------------------------------------------------------------------------------#

from dataclasses import dataclass
from distutils.log import error
from bs4 import BeautifulSoup
import requests, json
from datetime import datetime
import traceback
import time

# --------------------------------------------------------------------------------------------------------------------------------------------#
# Variables
# --------------------------------------------------------------------------------------------------------------------------------------------#

# I colori del terminale
ERROR_COLOR = "\033[1;37;41m"
RESET_COLOR = "\033[0;0m"
DONE_COLOR = "\033[1;37;42m"

# Ora minima in cui fa la registrazione per quel momento della giornata
startMorningTime = "08:00"
startAfternoonTime = "14:00"
startEveningTime = "20:00"

# Ora massima in cui fa la registrazione per quel momento della giornata
stopMorningTime = "09:00"
stopAfternoonTime = "15:00"
stopEveningTime = "21:00"

# Dopo quanto ricontrolla l'ora
checkAfterSeconds = 600

# The city where you wanto to check the temperature
CITY = 'Parigi'

# --------------------------------------------------------------------------------------------------------------------------------------------#
# Functions
# --------------------------------------------------------------------------------------------------------------------------------------------#

# Opens the JSON file
def openJSON() -> dict:
    with open("./website/records.json", "r") as f:
        data = json.load(f)
        f.close()
    return data

# Writes the JSON
def saveJSON(newData) -> any:
    with open("./website/records.json", "w") as f:
        json.dump(newData, f)
        f.close()

# Checks if there is a record for the moment of the day
def alreadyRegistred(dayMoment) -> bool:
    today = datetime.today().strftime('%d-%m-%Y')

    data = openJSON()
    if (today in data.keys()):
        if (dayMoment in data[today]):
            return True
        else:
            return False
    else:
        return False

# Retrieve the weather data from Google
def getWeatherData():
    weather = None
    hourOfRecord = None
    temperature = None

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    res = requests.get(
        f'https://www.google.com/search?q={CITY} meteo&oq={CITY} meteo&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    try:
        # Web scraping moment
        hourOfRecord = soup.select('#wob_dts')[0].getText().strip()
        temperature = soup.select('#wob_tm')[0].getText().strip()
    except Exception as e:
        errorLog(str(traceback.format_exc()))
    else:
        return {"hourOfRecord" : hourOfRecord, "temperature": temperature}

def getDateTime():
    today = datetime.today()
    return {"date": today.strftime('%d-%m-%Y'), "hour": today.strftime("%H:%M"), "full": today.strftime("%d-%m-%Y %H:%M")}

def errorLog(errorText):

    with open("./website/errors.json", "r") as f:
        data = json.load(f)
        f.close()

    fullDate = getDateTime()["full"]

    data[fullDate] = errorText

    with open("./website/errors.json", "w") as f:
        json.dump(data, f)
        f.close()

    print(f"{ERROR_COLOR}[{fullDate}] ERROR! Check the logs{RESET_COLOR}")

def registerRecord(dayMoment):
    weatherData = getWeatherData()
    dateTime = getDateTime()

    try:
        temperature = weatherData["temperature"]

        date = dateTime["date"]

        recordData = openJSON()

        if date in recordData.keys():
            recordData[date][dayMoment] = {
                "temperature": temperature
            }
        else:
            recordData[date] = {}
            recordData[date][dayMoment] = {
                "temperature": temperature
            }
        
        saveJSON(recordData)

        full = dateTime["full"]

        print(f"{DONE_COLOR}[{full}] Record saved!{RESET_COLOR}")

        with open("./website/lastRecord.txt", "w") as f:
            f.write(full)
            f.close()

    except Exception as e:
        errorLog(str(traceback.format_exc()))

def isTheRightMoment(dayMoment):
    hour = getDateTime()["hour"]

    if dayMoment == "Morning":
        if (hour > startMorningTime and hour < stopMorningTime): return True

    if dayMoment == "Afternoon":
        if (hour > startAfternoonTime and hour < stopAfternoonTime): return True

    if dayMoment == "Evening":
        if (hour > startEveningTime and hour < stopEveningTime): return True
    
    return False
    


# --------------------------------------------------------------------------------------------------------------------------------------------#
# Main
# --------------------------------------------------------------------------------------------------------------------------------------------#

while True:

    
    if not alreadyRegistred("Morning") and isTheRightMoment("Morning"):
        registerRecord("Morning")

    if not alreadyRegistred("Afternoon") and isTheRightMoment("Afternoon"):
        registerRecord("Afternoon")

    if not alreadyRegistred("Evening") and isTheRightMoment("Evening"):
        registerRecord("Evening")
    
    time.sleep(checkAfterSeconds)