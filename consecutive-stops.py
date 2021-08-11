from os import name
import pandas as pd 
import numpy as np 

def routes_txt(route_sname):

    # #####print(route_sname)
    # df1=pd.read_csv('routes.txt',delimiter=",",dtype={'route_short_name':'float64','route_long_name':'object','route':'int','agency_id':'object'})
    # print(df1)
    
    if route_sname in df1.values:
        routeid=df1[(df1['route_long_name'] == route_sname) & (df1['agency_id']=='DTC')]['route_id'].item()
        # #####print('route id is ==',routeid)
        trip_txt(routeid,route_sname)
    # else :
    #     list1.append(route_sname)
    #     print(route_sname)    

def trip_txt(routeid,route_sname):
    # df2 = pd.read_csv('trips.txt', delimiter = ",",dtype = {'route_id': 'int64', 'service_id': 'int64', 'trip_id': 'O', 'shape_id': 'float64'})
    # print(df2)
    tripid = df2.loc[(df2['route_id']==routeid),'trip_id'].unique()[0]
    # ###print('trip id is ==',tripid)
    stop_time_txt(tripid,route_sname)


def stop_time_txt(tripid,route_sname):
    # df3 = pd.read_csv('stop_times.txt',delimiter = ",",dtype = {'trip_id': 'O', 'arrival_time': 'O', 'departure_time': 'O', 'stop_id': 'O', 'stop_sequence': 'int'})
    # print(df3)
    stopid = df3.loc[df3['trip_id']==tripid,'stop_id'].unique()
    # print(stopid)
    stop_txt(stopid,route_sname)
  
def stop_txt(stopid,route_sname):
    # df4 = pd.read_csv('stops.txt', delimiter=",",dtype={'stop_id':'object','stop_code':'object','stop_name':'O','stop_lat':'float64','stop_lon':'float64'})
    stop_name2="**"
    for i in stopid:
        
        stop_name=df4.loc[df4['stop_id']==i,'stop_name'].unique()
        # stop_code=df4.loc[df4['stop_id']==i,'stop_code']
        # if(stop_name2 in stop_name[0]) :
        if(stop_name2==stop_name[0]) :
            print("Route Name : ",route_sname)
            print("Repeated Stop Name :",stop_name[0])
        stop_name2=stop_name[0]
    
    
    # print(df4)
    # stop_id,stop_code,stop_name,stop_lat,stop_lon
    # 92,DC5155,Chand Pur Village,28.75137,77.00975


def read_files() :
    count=0
    with open('DTC_NewData.txt') as f:
    
        for filename in f  :
            # filename = f.readline()
            filename=filename.strip()+"_DTC"
            # print(filename)
            ##### print("*************************")
            routes_txt(filename)
            

global filename
global df1,df2,df3,df4
df1=pd.read_csv('routes.txt',delimiter=",",dtype={'route_short_name':'float64','route_long_name':'object','route':'int','agency_id':'object'})
df2 = pd.read_csv('trips.txt', delimiter = ",",dtype = {'route_id': 'int64', 'service_id': 'int64', 'trip_id': 'O', 'shape_id': 'float64'})
df3 = pd.read_csv('stop_times.txt',delimiter = ",",dtype = {'trip_id': 'O', 'arrival_time': 'O', 'departure_time': 'O', 'stop_id': 'O', 'stop_sequence': 'int'})
df4 = pd.read_csv('stops.txt', delimiter=",",dtype={'stop_id':'object','stop_code':'object','stop_name':'O','stop_lat':'float64','stop_lon':'float64'})
global list1
list1=[]
read_files()
print(list1)
# route_lname = input("route  ")
# routes_txt(route_lname)