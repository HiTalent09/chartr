import pandas as pd
import numpy as np
import itertools 
from fuzzywuzzy import fuzz

#dataframes to traverse on txt files
global df1,df2,df3,df4
Path = "/home/anjali/Desktop/DTC_CHANGES"
df1 = pd.read_csv(f'{Path}/routes.txt',delimiter = ",",dtype={'route_short_name':'float64','route_long_name':'object','route_type':'int','route_id':'int','agency_id':'object'})
df2 = pd.read_csv(f'{Path}/trips.txt', delimiter = ",",dtype = {'route_id': 'int64', 'service_id': 'int64', 'trip_id': 'O', 'shape_id': 'float64'})
df3 = pd.read_csv(f'{Path}/stop_times.txt',delimiter = ",",dtype = {'trip_id': 'O', 'arrival_time': 'O', 'departure_time': 'O', 'stop_id': 'O', 'stop_sequence': 'int'})
df4 = pd.read_csv(f'{Path}/stops.txt', delimiter=",",dtype={'stop_id':'object','stop_code':'object','stop_name':'O','stop_lat':'float64','stop_lon':'float64'})

#function to match 2 given string using fuzzywuzzy library
def checkString(str1,str2):
    #token_set_ratio ignores upper and lower case letters , token_sort_ratio ignore order of letters
    #if(fuzz.token_set_ratio(str1,str2) > 80):
    #WRatio handles lower and upper cases and some other parameters too
    if(fuzz.WRatio(str1,str2) > 80 or fuzz.token_set_ratio(str1,str2) > 80 or fuzz.token_sort_ratio(str1,str2) > 80):
        return True
    else:
        return False

#function to WRtaio % by fuzzywuzzy
def findperc1(str1,str2):
    return fuzz.WRatio(str1,str2)

#function to token_sort_ratio % by fuzzywuzzy
def findperc2(str1,str2):
    return fuzz.token_sort_ratio(str1,str2)

    
#function to match 2 given strings (ignoring whitespace,special characters,upper&lower case)
def Stringcheck(str1,str2):
    disallowed_characters = [".",'',"!","-"," ","@",""]
    m = str1.lower()
    n = str2.lower()
    for character in disallowed_characters:
        m = m.replace(character, "")
        n = n.replace(character, "")
    if m ==n:
        return True
    else:
        return False

        
#traversing routes.txt file to get route_id corresponding to the route name
def routes_txt(route_lname):
    t  = route_lname+"_DTC"
    if t in df1.values:
        routeid = df1[(df1['route_long_name'] == t) & (df1['agency_id']=='DTC')]['route_id'].item()
        k = trip_txt(routeid)
        return k
    else:
        return []

#traversing trip.txt file to fing trip id corresponding to the route_id
def trip_txt(routeid):
    tripid = df2.loc[(df2['route_id']==routeid),'trip_id'].unique()[0]
    z = stop_times_txt(tripid)
    return z

#traversing stop_times.txt file to find count all stop counts correspoding to the trip_id
def stop_times_txt(tripid):
    old_stops = []
    stopid = df3.loc[df3['trip_id']==tripid,'stop_id'].tolist()
    for x in stopid:
        p = stop_txt(x)
        old_stops.append(p)      
    return old_stops

#traversing stop.txt file to find all stop names correspoding to the trip_id
def stop_txt(stopid):
    stopname = df4.loc[df4['stop_id']== stopid,'stop_name'].tolist()
    return stopname[0]
    

#function to match all stops sequences in old and new data for all routes
def MatchDataSequence():
    
    #extracting names of all routes in New DTC Data from DTC_NewData txt file
    df = pd.read_csv('/home/anjali/Desktop/DTC_CHANGES/DTC_NewData.txt', delimiter = ",")
    for ind in df.index:
            filenames = df['DTC_routes'][ind]
            fileName , separator , extension = filenames.partition('.')
            
            #passing the route name to routes_txt , storing old data stops in a list old_data
            old_data = routes_txt(fileName)#list of old stops
            
            #reading new dtc data from .csv files
            dataf = pd.read_csv(f'/home/anjali/Desktop/NewDTCdata/{filenames}',delimiter = ",")
            
            if('Stops_up' in dataf.columns):
                new_data = dataf['Stops_up'].tolist()#list of new stops
            else:
                new_data = dataf['Stops_down'].tolist()#list of new stops
            
            #string matching for old and new stops
            print(f"Route : {fileName}")
            print(f"Total stops in old data : {len(old_data)}")
            print(f"Total stops in new data : {len(new_data)}")
            
            #traversing old_data list of old DTC stops and finding corresponding stops in new_data list 
            new = [] #list to store final output of sequence matching
            if(len(old_data) and len(new_data)):
                i = 0
                #traversing complete list 1
                while(i < len(old_data)):
                    str1 = old_data[i]
                    str2 = ""
                    if( i < len(new_data)):
                        str2 = new_data[i]
                        
                    #if strings did matched for same index , store in output list
                    if (str1 == str2):
                         new.append("Match")
                    
                    #checking str1 and str2 by fuzzywuzzy string matching
                    elif (Stringcheck(str1,str2) == True):
                        new.append("Match")

                    elif (checkString(str1,str2) == True):
                        
                        if(findperc1(str1,str2) > 90 and findperc2(str1,str2) > 70):
                            new.append("Match")
                            
                        elif (findperc1(str1,str2) > 80 and findperc2(str1,str2) > 50):
                            new.append("Slightly match")
                            
                        else:
                            new.append("Not matched")
                
                    #when strings did not match for same index ,checking for all other indexes in new_data list
                    else:
                        j = 0
                        flag = True
                        while( j < len(new_data) and flag==True):
                            if (Stringcheck(str1,new_data[j]) == True):
                                new.append(f'Match at {j+1} in new_data list')
                                flag = False
                                break
                            else:
                                j += 1
                        if(flag == True and j == len(new_data)):
                            new.append("Not matched")
                    i += 1
                
                #creating a dataframe with the final output list
                a = {'OLD_STOPS':old_data, 'NEW_STOPS':new_data, 'OUTPUT':new}
               

            #if old_data list or new_data list is empty , return 0 stops for correspoding route
            else:
                if len(old_data) == 0:
                    print("No stops in Old data")
                    list1 = [None] * len(new_data)
                    a = {'OLD_STOPS':list1, 'NEW_STOPS':new_data}

                    
                else:
                    print("No stops in New data")
                    list1 = [None] * len(old_data)
                    a = {'OLD_STOPS':old_data, 'NEW_STOPS':list1}
            
            dframe = pd.DataFrame.from_dict(a, orient='index').T
            dframe.index = np.arange(1, len(dframe) + 1)
            #print(dframe.to_string())
                
            #stroring the dataframe in a .csv file for all routes
            dframe.to_csv(f'/home/anjali/Desktop/SequenceMatching/{filenames}')

            
#calling the function for sequence matching        
MatchDataSequence()