import os, subprocess, time
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

def closest(lst, K):
    	return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]

# Sensor to Query
data_mode	= "temperature"
data_file	= "./data/wx_data.csv"

# Indoors
#data_tower	= "Acurite-Tower-2235"
#data_tower     = "Acurite-Tower-6694"

# Outdoors
data_tower	= "Acurite-6045M-90"
#data_tower	= "Acurite-Tower-13772"
#data_tower	= "Acurite-609TXC-210"

# Do the boring stuff, be creative with bash
time_now 	= int(time.time())
time_hrs	= 6
time_min	= time_now - 3600*time_hrs #hrs of data
time_max	= time_now

time_string	= subprocess.check_output("grep -i '"+ data_tower +"' " + data_file + " | cut -d ',' -f 2", shell=True, universal_newlines=True)
time_list	= time_string.splitlines()
time_list 	= list(map(int, time_list))

data_time 	= subprocess.check_output("grep -i '"+ data_tower +"' " + data_file + " | sed -n '/"+ str(closest(time_list, time_min)) +"/,/"+ str(closest(time_list, time_max)) +"/p' | cut -d ',' -f 2", shell=True, universal_newlines=True)
data_temp       = subprocess.check_output("grep -i '"+ data_tower +"' " + data_file + " | sed -n '/"+ str(closest(time_list, time_min)) +"/,/"+ str(closest(time_list, time_max)) +"/p' | cut -d ',' -f 3", shell=True, universal_newlines=True)
data_dewp       = subprocess.check_output("grep -i '"+ data_tower +"' " + data_file + " | sed -n '/"+ str(closest(time_list, time_min)) +"/,/"+ str(closest(time_list, time_max)) +"/p' | cut -d ',' -f 4", shell=True, universal_newlines=True)
data_humi       = subprocess.check_output("grep -i '"+ data_tower +"' " + data_file + " | sed -n '/"+ str(closest(time_list, time_min)) +"/,/"+ str(closest(time_list, time_max)) +"/p' | cut -d ',' -f 5", shell=True, universal_newlines=True)
data_bolt       = subprocess.check_output("grep -i '"+ data_tower +"' " + data_file + " | sed -n '/"+ str(closest(time_list, time_min)) +"/,/"+ str(closest(time_list, time_max)) +"/p' | cut -d ',' -f 7", shell=True, universal_newlines=True)
data_mile       = subprocess.check_output("grep -i '"+ data_tower +"' " + data_file + " | sed -n '/"+ str(closest(time_list, time_min)) +"/,/"+ str(closest(time_list, time_max)) +"/p' | cut -d ',' -f 8", shell=True, universal_newlines=True)

wx_time		= data_time.replace("\n", ",").split(",")
wx_temp		= data_temp.replace("\n", ",").split(",")
wx_dewp         = data_dewp.replace("\n", ",").split(",")
wx_humi         = data_humi.replace("\n", ",").split(",")
wx_bolt         = data_bolt.replace("\n", ",").split(",")
wx_mile         = data_mile.replace("\n", ",").split(",")

while("" in wx_time) :
    wx_time.remove("")

while("" in wx_temp) :
    wx_temp.remove("")

while("" in wx_dewp) :
    wx_dewp.remove("")

while("" in wx_humi) :
    wx_humi.remove("")

while("" in wx_bolt) :
    wx_bolt.remove("")

while("" in wx_mile) :
    wx_mile.remove("")



dmap_time = map(float, wx_time)
data_time = list(dmap_time)

dmap_temp = map(float, wx_temp)
data_temp = list(dmap_temp)

dmap_dewp = map(float, wx_dewp)
data_dewp = list(dmap_dewp)

dmap_humi = map(float, wx_humi)
data_humi = list(dmap_humi)

dmap_bolt = map(int, wx_bolt)
data_bolt = list(dmap_bolt)

dmap_mile = map(float, wx_mile)
data_mile = list(dmap_mile)



# Do the cool stuff
x = np.array(data_time)
if "humidity" in data_mode:
	y = np.array(data_humi)
	data_title = "Humidity"
elif "dew" in data_mode:
	y = np.array(data_dewp)
	data_title = "Dew Point"
elif "strike" in data_mode:
	data_title = "Lightning"
	y = np.array(data_bolt)
elif "distance" in data_mode:
	data_title = "Storm Distance"
	y = np.array(data_mile)
else:
	y = np.array(data_temp)
	data_title = "Temperature"


cubic_interploation_model = interp1d(x, y, kind = "cubic")

# Plotting the Graph
X_=np.linspace(x.min(), x.max(), 500)
Y_=cubic_interploation_model(X_)

plt.plot(X_, Y_)
#plt.gca().invert_yaxis()
plt.title(data_tower)
plt.xlabel(data_title + " -  " + str(time.ctime(int(time_min)))+ " +"+ str(time_hrs)  +"hr")
if "humidity" in data_mode:
        plt.ylabel("Humidity (%)")
elif "dew" in data_mode:
        plt.ylabel("Dew Point (F)")
elif "strike" in data_mode:
        plt.ylabel("Strikes")
elif "distance" in data_mode:
        plt.ylabel("Distance (M)")
else:
        plt.ylabel("Temp (F)")
ax = plt.gca()
ax.axes.xaxis.set_ticklabels([])


plt.savefig("./images/wx_"+ data_tower.lower()  +"-"+ str(time_now).rstrip('.')  +".png")
plt.show()
