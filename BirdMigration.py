import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import cartopy.crs as ccrs
import cartopy.feature as cfeature

birddata = pd.read_csv("bird_tracking.csv")
plt.figure(figsize = (10,10))
bird = pd.unique(birddata.bird_name)
for name in bird:
    ix = birddata.bird_name == name
    x, y = birddata.longitude[ix], birddata.latitude[ix]
    plt.plot(x, y, ".", label = name)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend(loc = "lower right")
plt.savefig("3bird.pdf")

'''
plt.figure(figsize = (8,4))
speed = birddata.speed_2d[birddata.bird_name == 'Eric']
ind = np.isnan(speed)
plt.hist(speed[~ind], bins = np.linspace(0,30,20), normed = True) 
plt.xlabel("2d speed (m/s)")                  
plt.ylabel("Frequency")
plt.savefig("hist.pdf")

# for data which are non numeric --> np.isnan(speed) it gives out the list 
# of data in the specific portion about the non numeric if any present
'''
'''Even Pandas can be used to plot the graph and it does not require a 
line of code to ccheck for the nan . check below'''

birddata.speed_2d.plot(kind = 'hist', range = [0,30] )
plt.xlabel("2d speed (m/s)")                  
plt.ylabel("Frequency")
plt.savefig("pdhist.pdf")

timestamp = []
for k in range(len(birddata.date_time)):
    timestamp.append(datetime.datetime.strptime\
                     (birddata.date_time.iloc[k][:-3],"%Y-%m-%d %H:%M:%S"))

birddata["Timestamp"] = pd.Series(timestamp, index = birddata.index)

times = birddata.Timestamp[birddata.bird_name == "Eric"]
elapsedtime = [time - times[0] for time in times]
elapseddays = np.array(elapsedtime) / datetime.timedelta(days = 1)
plt.plot(np.array(elapsedtime) / datetime.timedelta(days = 1))
plt.xlabel("Observation")
plt.ylabel("Elapsed time in days")
plt.savefig("timeplot.pdf")

data = birddata[birddata.bird_name == "Eric"]
nextday = 1
dailymean_speed = []
inds = []
for (i,t) in enumerate(elapseddays):
    if t < nextday:
        inds.append(i)
    else:
        dailymean_speed.append(np.mean(data.speed_2d[inds]))
        inds = []
        nextday += 1
        
plt.figure(figsize = (7,7))
plt.plot(dailymean_speed)
plt.xlabel("Day")
plt.ylabel("Mean speed m/s")
plt.savefig("dms.pdf")
    
'''projection on a map called as cartography'''
proj = ccrs.Mercator()
plt.figure(figsize = (10,10))
ax = plt.axes(projection = proj)
ax.set_extent((-25.0, 20.0, 52.0, 10.0))
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS , linestyle = ':')
for name in bird:
    ix = birddata['bird_name'] == name
    x, y = birddata.longitude[ix], birddata.latitude[ix]
    ax.plot(x, y, ".", transform = ccrs.Geodetic(), label = name)
plt.legend(loc = "upper right")
plt.savefig("map.pdf")
