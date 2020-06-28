import pandas as pd
import numpy as np
import json
# Here we determine exactly when did the exponential growth in each
# Country started , along with when did it flatten the curve if they did

data = pd.read_csv("dataset-covid.csv", sep=";", header=0, index_col=0)
pd.set_option('display.max_rows', data.shape[0]+1)
print()
allCountries = []
for country in data.index:
    countryInfo = {}
    countryInfo["name"] = country
    #We get the log value of the total cases per day in this data series
    #We chose the log value because it helps to determine where the graph went exponential ( when the log values are incrementing by a value greater than one)
    #As well as to determine where the graph flattened , where the log value floored ( floor(1.3) = 1 )will be always the same , hence determining that the curve is flattenned
    data.loc[country] = data.loc[country].apply(np.log)
    i = 0
    firstExpon = ""
    startFlat = ""
    totalCases = ""
    countryData = data.loc[country]
    # Calculation for the Day that the exponential growth started in
    while i < (countryData.size - 5):
        compPoint = countryData[i]
        if(compPoint != float('-inf')):
            flooredLog = np.floor(compPoint)
            logIncrement = 0
            j = i+1
            while j < i+5:
                if(np.floor(countryData[j])-flooredLog > 0):
                    flooredLog = np.floor(countryData[j])
                    logIncrement = logIncrement+1
                j = j+1
            if(logIncrement > 1 and firstExpon == ""):
                firstExpon = data.columns[i]
        i = i+1

    i = 0
    # Calculation for the Day that the curve started flattening if it did
    while i < (countryData.size):
        compPoint = countryData[i]
        if(compPoint != float('-inf')):
            flooredLog = np.floor(compPoint)
            j = i+1
            isStartOfFlatCurve = True
            while j < countryData.size:
                if(np.floor(countryData[j]-flooredLog) >= 1):
                    isStartOfFlatCurve = False
                    break

                j = j+1
            if isStartOfFlatCurve and countryData.size - i > 30:
                startFlat = data.columns[i]
                break
            if isStartOfFlatCurve and not countryData.size - i > 30:
                startFlat = "Not Flattened"

        i = i+1
    countryInfo["name"] = country
    countryInfo["firstExponential"] = firstExpon
    countryInfo["StartedFlattening"] = startFlat
    countryInfo["Total Cases"] = countryData[countryData.size-1]
    allCountries.append(countryInfo)

    print("Country : {} , First : {} , startFlat : {}".format(
        country, firstExpon, startFlat))

with open("output.json", "w") as data_file:
    json.dump(allCountries, data_file, indent=4, sort_keys=True)
