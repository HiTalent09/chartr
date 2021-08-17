import pandas as pd
data = pd.read_csv("result_filter.txt",delimiter = '#')
print(data)
data.to_csv('consecutive.csv',index = None)
