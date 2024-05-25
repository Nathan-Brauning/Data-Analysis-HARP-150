import pandas as pd
import matplotlib.pyplot as plt
#Datetime library used to calculate the total ride time by subtracting start_times from end_times
#https://docs.python.org/3/library/datetime.html
import datetime as dt
#https://saturncloud.io/blog/how-to-add-a-regression-line-in-python-using-matplotlib/
import numpy as np

citi_bike_df = pd.read_csv("Data Sets/JC-202403-citibike-tripdata.csv")   
citi_bike_df.drop('ride_id', axis = 1, inplace = True)


index1 = 0
dropped_index_list = []
for i in citi_bike_df['ended_at']:
    if str(i[6]) == '4':
        citi_bike_df.drop(index1, axis = 'index', inplace = True)
        dropped_index_list.append(index1)
    index1 += 1

    
all_start_times = {}
start_scatter_list = []
duration_scatter_list = []
station_counts = {}
weekday_counts = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0, 'Sunday': 0}
index2 = 0
for i in citi_bike_df['started_at']:
    day_and_start_time = str(i)
    start_length = len(day_and_start_time)
    start_time = day_and_start_time[start_length-8: start_length]
    if start_time[0:2] not in all_start_times:
        all_start_times[start_time[0:2]] = 1
    else:
        all_start_times[start_time[0:2]] += 1
    day_and_end_time = str(citi_bike_df.loc[index2, 'ended_at'])
    end_length = len(day_and_end_time)
    end_time = day_and_end_time[end_length-8: end_length]
    
    #https://www.geeksforgeeks.org/how-to-add-time-onto-a-datetime-object-in-python/
    ride_duration = str(dt.timedelta(days = int(day_and_end_time[8:10]) - int(day_and_start_time[8:10]), hours = int(end_time[0:2]) - int(start_time[0:2]), minutes = int(end_time[3:5]) - int(start_time[3:5]), seconds = int(end_time[6:8]) - int(start_time[6:8])))
    
    start_scatter = (int(start_time[0:2])) + (int(start_time[3:5])/60) + (int(start_time[6:8])/(60*60))
    start_scatter = round(start_scatter, 2)
    start_scatter_list.append(start_scatter)
    
    if len(ride_duration) < 8:
        ride_duration = '0' + ride_duration
    if ride_duration[2:5] == 'day':
        duration_scatter = (int(ride_duration[0])*24*60) + (int(ride_duration[7:8])*60) + (int(ride_duration[9:11])) + (int(ride_duration[12:14])/60)
    else:
        duration_scatter = (int(ride_duration[0:2])*60) + (int(ride_duration[3:5])) + (int(ride_duration[6:8])/60)
    
    duration_scatter = round(duration_scatter, 2)
    duration_scatter_list.append(duration_scatter)
    
    start_station = citi_bike_df.loc[index2, 'start_station_name']
    end_station = citi_bike_df.loc[index2, 'end_station_name']
    
    if start_station not in station_counts:
        station_counts[start_station] = 1
    else:
        station_counts[start_station] += 1
    if end_station not in station_counts:
        station_counts[end_station] = 1
    else:
        station_counts[end_station] += 1
        
    time = dt.datetime(int(i[0:4]), int(i[5:7]), int(i[8:10]), int(i[11:13]), int(i[14:16]), int(i[17:19]))
    day_of_week = time.weekday()
    if day_of_week == 0:
        day_of_week = 'Monday'
    if day_of_week == 1:
        day_of_week = 'Tuesday'
    if day_of_week == 2:
        day_of_week = 'Wednesday'
    if day_of_week == 3:
        day_of_week = 'Thursday'
    if day_of_week == 4:
        day_of_week = 'Friday'
    if day_of_week == 5:
        day_of_week = 'Saturday'
    if day_of_week == 6:
        day_of_week = 'Sunday'

    weekday_counts[day_of_week] += 1
    
    
    index2 += 1
    while True:
        if index2 in range(len(citi_bike_df)):
            try:
                filler = citi_bike_df.loc[index2, 'started_at']
                break
            except:
                index2 += 1
        else:
            break    

ride_type_counts = citi_bike_df['rideable_type'].value_counts()
member_type_counts = citi_bike_df['member_casual'].value_counts()

#sorted taken from Kolade Chris to sort in descending order
#https://www.freecodecamp.org/news/sort-dictionary-by-value-in-python/
station_counts = sorted(station_counts.items(), key=lambda x:x[1], reverse = True) 

station_counts_dictionary = {}
index3 = 0
for i in station_counts:
    if index3 <= 9:
        station_counts_dictionary[i[0]] = i[1]
    index3 += 1

all_start_times = sorted(all_start_times.items())

#Line graph of start times
plt.title("Starting ride times of Citi Bikes in March")
plt.xlabel("Hour")
plt.ylabel("Number of rides")
plt.plot(list(dict(all_start_times).keys()), list(dict(all_start_times).values()))
plt.show()


#Stat plot of start vs duration    
plt.title("Ride start times vs. ride duration")
plt.xlabel("Start time (hour)")
plt.ylabel("Duration (minutes)")
plt.xlim(0,24)
plt.scatter(start_scatter_list, duration_scatter_list, 0.8)
plt.show()



#Pie chart of ride types
plt.title("Do more people ride electric bikes or classic bikes?")
plt.pie(ride_type_counts, labels = ['Electric Bike', 'Classic Bike'], autopct = '%1.2f%%', startangle = 90, explode = [.1,0], shadow = True)
plt.legend(title = 'Ride Types')
plt.show()



#10 most popular stations
plt.barh(list(dict(station_counts_dictionary).keys()), list(dict(station_counts_dictionary).values()), height = 0.5, align = 'center')
plt.xlabel('Amount of bikes in and out of station')
plt.ylabel('Station name')
plt.title('Top 10 Most Popular Stations')
plt.show()



#Casual vs member rides
plt.title("How Many Riders Are Members With Citibike Vs. Casual Riders?")
plt.pie(member_type_counts, labels = ['Member', 'Casual'], autopct = '%1.2f%%', startangle = 0, explode = [.1,0], shadow = True)
plt.legend(title = 'Member Types')
plt.show()



print(weekday_counts)
plt.bar(list(dict(weekday_counts).keys()), list(dict(weekday_counts).values()), width = 0.5, align = 'center')
plt.xlabel('Day of the week')
plt.ylabel('Number of rides')
plt.title('What Is The Most Popular Day Of The Week To Go For A Bike Ride?')
plt.show()