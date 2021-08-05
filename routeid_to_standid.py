route=[]
def routes_txt(route_short_name):
    infile = open('routes.txt')
    data = infile.readline() #for reading first line of the file 
    #print("Here are all the route ids ...")
    while data :   #loop for reading each data in the file 
        data = infile.readline() 
        l1=list(data.split(",")) #for storing the string file to list for single line of data 
        if(len(l1)==1) : #for ignoring the last line of file 
            break
        if route_short_name in l1[1] :#comparing if the give shot name is in the given data 
            print('========================================================')
            print(l1[1])
            trip_txt(l1[3])
            #route.append(l1[3])   #storing the route_id for further traversal 
           # print(l1[1],l1[4],'Route_id =',l1[3]) # this line is for printing bus no. and route id for the given bus no. 

def trip_txt(route_id):
    infile = open('trips.txt')
    data = infile.readline()
    count =0
    while data and count<1:
        data = infile.readline()
        l2=list(data.split(","))
        if(len(l2)==1):
            break 
        if route_id in l2[0]:
            print('trip_id is ',l2[2])
            #print('**************************************8')
            count +=1
            stop_times(l2[2])


def stop_times(trip_id):
    infile = open('stop_times.txt')
    data = infile.readline()
    while data :
        data = infile.readline()
        l3=list(data.split(","))
        if(len(l3)==1):
            break 
        if trip_id == l3[0]:
           # print(l3[3])
            stop_txt(l3[3])


def stop_txt(stop_id):
    infile = open('stops.txt')
    data = infile.readline()
    while data :
        data = infile.readline()
        l4=list(data.split(","))
        if(len(l4)==1):
            break 
        if stop_id == l4[0]:
            print(l4[1],l4[2])


route_short_name = input("Enter route short name\n")
routes_txt(route_short_name)