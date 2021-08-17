from os import name
import pandas as pd 
import numpy as np 

def routes_txt(route_sname):
    # print(route_sname)

    # #####print(route_sname)
    # df1=pd.read_csv('routes.txt',delimiter=",",dtype={'route_short_name':'float64','route_long_name':'object','route':'int','agency_id':'object'})
    # print(df1)
    
    if route_sname in routes_df.values:
        routeid=routes_df[(routes_df['route_long_name'] == route_sname) & (routes_df['agency_id']=='DTC')]['route_id'].item()
        trip_txt(routeid,route_sname)
    # else :
    #     # list1.append(route_sname)
    #     # print('-->>',route_sname)
            

def trip_txt(routeid,route_sname):
    # df2 = pd.read_csv('trips.txt', delimiter = ",",dtype = {'route_id': 'int64', 'service_id': 'int64', 'trip_id': 'O', 'shape_id': 'float64'})
    # print(df2)
    route_sname=route_sname
    tripid = trips_df.loc[(trips_df['route_id']==routeid),'trip_id'].unique()[0]
    # ###print('trip id is ==',tripid)
    stop_time_txt(tripid,route_sname)


def stop_time_txt(tripid,route_sname):
    # df3 = pd.read_csv('stop_times.txt',delimiter = ",",dtype = {'trip_id': 'O', 'arrival_time': 'O', 'departure_time': 'O', 'stop_id': 'O', 'stop_sequence': 'int'})
    # print(df3)
    route_sname=route_sname
    stopid = stop_time_df.loc[stop_time_df['trip_id']==tripid,'stop_id'].tolist()
    # print(stopid)
    print('===========')
    stop_txt(stopid,route_sname)
  
def stop_txt(stopid,route_sname):
    all_stands=[]
    # df4 = pd.read_csv('stops.txt', delimiter=",",dtype={'stop_id':'object','stop_code':'object','stop_name':'O','stop_lat':'float64','stop_lon':'float64'})
    route_sname=route_sname
    previous_stop_name="**"
    previous_stopid="**"
    save_route_in_file(route_sname)
    
    for i in stopid:
        next_stop_name=stops_df.loc[stops_df['stop_id']==i,'stop_name'].tolist()
        # stop_code=df4.loc[df4['stop_id']==i,'stop_code']
        if(previous_stop_name == next_stop_name[0]) :
            # save_route_in_file(route_sname)
            all_stands.append(previous_stopid)
            all_stands.append(previous_stop_name)
            all_stands.append(i)
            all_stands.append(next_stop_name[0])
            # print(previous_stopid,'---',previous_stop_name,'->',i,'---',next_stop_name[0])
            # save_stand_in_file(previous_stopid,previous_stop_name,i,next_stop_name[0])
            # print('---------------------')
            if len(all_stands)==4:
                # print('----------------')
                data_formate(all_stands)
                stand_in_file(all_stands)
                all_stands=[]
        previous_stop_name=next_stop_name[0]
        previous_stopid=i
    # data_formate(all_stands)
    # print(all_stands)
    
def stand_in_file(all_stands):
    string_data= str(all_stands)
    stand_name =open('consecutive.txt',"a")
    stand_name.write('#')
    stand_name.write(string_data)
    

#function to write file in list order and sequal 
def save_stand_in_file(previous_stopid,previous_stop_name,i,next_stop_name):
    consecutive =open('conc.txt',"a")
    consecutive.write(previous_stopid)
    consecutive.write("  ")
    consecutive.write(previous_stop_name)
    consecutive.write("    ")
    consecutive.write(i)
    consecutive.write("  ")
    consecutive.write(next_stop_name)
    consecutive.write("\n")

def data_formate(stand_list):
    print(stand_list)

def save_route_in_file(route):
    route_name =open('consecutive.txt',"a")
    route_name.write("\n")
    route_name.write(route)
    

def read_files() :
    with open('DTC_NewData.txt') as f:
        for filename in f  :
            filename=filename.strip()+"_DTC"
            routes_txt(filename)



global routes_df,trips_df,stop_time_df,stops_df
routes_df = pd.read_csv('routes.txt',delimiter=",",dtype={'route_short_name':'float64','route_long_name':'object','route':'int','agency_id':'object'})
trips_df = pd.read_csv('trips.txt', delimiter = ",",dtype = {'route_id': 'int64', 'service_id': 'int64', 'trip_id': 'O', 'shape_id': 'float64'})
stop_time_df = pd.read_csv('stop_times.txt',delimiter = ",",dtype = {'trip_id': 'O', 'arrival_time': 'O', 'departure_time': 'O', 'stop_id': 'O', 'stop_sequence': 'int'})
stops_df = pd.read_csv('stops.txt', delimiter=",",dtype={'stop_id':'object','stop_code':'object','stop_name':'O','stop_lat':'float64','stop_lon':'float64'})
read_files()
# global list1
# list1=[]
# print(list1)
# route_lname = input("route  ")
# routes_txt(route_lname)