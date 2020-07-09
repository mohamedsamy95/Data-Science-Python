import pandas as pd
import time
import os
import seaborn as sb
from matplotlib import pyplot as plt
import numpy as np
import math
##Hilfsfunktionen
def indexof(list,item):
    try:
        index_value = list.index(item)
    except ValueError:
        index_value = -1
    return index_value
    
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
#plot days to flatten the curve compared to lockdown length
def plot_lockdown_flatten(hyprid_df):
    plt.xticks(rotation=25)
    sb.set_context("paper")
    sb.set_style("darkgrid")
    sb.barplot(x="Country", y="Lockdown Length",hue="Days to flatten the curve",data=hyprid_df)
    plt.title("The length of the lockdown")
    plt.show()
    return



#path of the project folder
path="C:/Users/user/Desktop/Data-Science-Python"
##code...
#change the working directory
os.chdir(path)
print("Current Directory: "+os.getcwd())
#loading the lockdown dataset
lockdown = excel("Lockdown dataset/Lockdown.xlsx")
covid19=excel("Extracted Dates.xlsx")

#average
avg=get_average_lockdown(lockdown)
print("Average length: "+str(avg))
#variance
standard_deviation=np.std(lockdown["Length"])
print("Standard deviation: "+str(standard_deviation))
#plot lockdown
plot_lockdown(lockdown)

c0=covid19["Total Duration in Days"].to_list()
c1=covid19["Country"].to_list()
c2=lockdown["Country"].to_list()
c4=covid19["firstExponential"].tolist() ## Date of the first exp-growth in infections
c5=lockdown["Start of lockdown"].to_list() ## 

##countries with missing data
not_found_country=[]

for item in c1:
    original_index=indexof(c1,item)
    index_value=indexof(c2,item)
    if index_value<0 or math.isnan(c0[original_index]):
        not_found_country.append(item)
## print not found country
print("Not found countries"+str(not_found_country))


sorted_length_to_flatten_curve=[]
##collecting days needed to flatten the curve
for item in c2:
    # if country not in the list of missing data
    index_value=indexof(not_found_country,item)
    if index_value<0:
        sorted_length_to_flatten_curve.append(c0[indexof(c1,item)])
    else:
        sorted_length_to_flatten_curve.append(-1)

##create new dataframe with 
hy_df=pd.DataFrame(list(zip(lockdown["Length"], sorted_length_to_flatten_curve)),columns=["Lockdown Length","Days to flatten the curve"],index=c2)

## delete countries with missing data
for land in  hy_df.iterrows():
    if indexof(not_found_country,land[0])>0:
        hy_df.drop([land[0]], inplace=True)
## plot the new data frame
axes = hy_df.plot(kind='bar')
plt.show()

##calculate a factor
## we calculate average of (number of infections and length of lockdown for each country)
## the smaller the average the better the result of this country is

##calculate the factor
#hy_df['lockdown_flatten_factor'] = hy_df.apply (lambda row:(row["Lockdown Length"]+row["Days to flatten the curve"])/2 , axis=1)


## calculate the diffrence between the start of lockdown and the start of exp-growth
dates=[]
for land in  hy_df.iterrows():
    index_covid=indexof(c1,land[0])
    index_lockdown=indexof(c2,land[0])
    ##error correction
    ## if the country had no lockdown then drop
    if(land[1]["Lockdown Length"]==0):
        hy_df.drop([land[0]], inplace=True)
    else:
        dates.append(c5[index_lockdown]-c4[index_covid])
## add dates to the dataframe
hy_df["days_between_lockdown_first_exp_growth"]=dates
hy_df["days_between_lockdown_first_exp_growth"]=hy_df["days_between_lockdown_first_exp_growth"].dt.days.astype('int16')

print(hy_df)

axes = hy_df.plot(kind='bar')
plt.show()

###correlations
x=hy_df["days_between_lockdown_first_exp_growth"].corr(hy_df["Lockdown Length"])
print(x)


###read economical changes in the lockdown
#economey_path="Stock market data/"
#onlyfiles = [f for f in os.listdir(economey_path) if os.path.isfile(os.path.join(economey_path, f))]
#austeria=pd.read_csv(economey_path+onlyfiles[0])
#print(austeria)