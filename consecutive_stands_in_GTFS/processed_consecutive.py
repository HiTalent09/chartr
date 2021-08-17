def write_in_filter(data):
    route_name =open('result_filter.txt',"a")
    route_name.write("\n")
    route_name.write(data)



infile = open('consecutive.txt')
data = infile.readline()
print(data)
while data :
    data = infile.readline()
    if '#' in data:
        data.strip('\n')
        print(data)
        write_in_filter(data)