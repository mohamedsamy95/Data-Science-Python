import pandas as pd
import time
import os
import seaborn as sb
from matplotlib import pyplot as plt
import numpy as np
##Hilfsfunktionen
#read excel dataset
def excel(pfad):
    return pd.read_excel(pfad)

#get average lockdown length
def get_average_lockdown(lockdown):
    return lockdown["AVG(length)"][0]

#plot lockdown length
def plot_lockdown(lockdown):
    plt.xticks(rotation=25)
    sb.set_context("paper")
    sb.set_style("darkgrid")
    sb.barplot(x="Country", y="Length",data=lockdown)
    plt.title("The length of the lockdown")
    plt.show()
    return




#path of the project folder
path="C:/Users/user/Desktop/COVID-19 Project"
##code...
#change the working directory
os.chdir(path)
print("Current Directory: "+os.getcwd())
#loading the lockdown dataset
lockdown = excel("Lockdown dataset/Lockdown.xlsx")

#average
avg=get_average_lockdown(lockdown)
print("Average length: "+str(avg))
#variance
standard_deviation=np.std(lockdown["Length"])
print("Standard deviation: "+str(standard_deviation))
#plot lockdown
plot_lockdown(lockdown)




###read economical changes in the lockdown
economey_path="Stock market data/"
onlyfiles = [f for f in os.listdir(economey_path) if os.path.isfile(os.path.join(economey_path, f))]
austeria=pd.read_csv(economey_path+onlyfiles[0])
print(austeria)



