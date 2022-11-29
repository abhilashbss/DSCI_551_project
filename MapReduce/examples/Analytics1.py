from mapper.mapper import mapper
from Reducer.Reducer import Reducer
from Partitioner.partitioner import partitioner
from EDFS.EDFS_client.EDFSClient import EDFSClient
import pandas as pd
import matplotlib.pyplot as plt


e = EDFSClient("/Users/abhilashbss/Desktop/repositories/DSCI_551_project/EDFS/EDFS_client/namenode_config.conf")
# e.WriteFile("a/b/crime_rate_csv","/Users/abhilashbss/Desktop/repositories/DSCI_551_project/dataset/CrimeRate.csv",
#             "csv", 4 )
partitions = e.ReadFileRetainPartition("a/b/CrimeRate.csv")

#Find top 5 countries which have the highest crime index

def MapAnalytics1(key, partition_data):
    df = pd.DataFrame(partition_data)
    l=[]
    for k, row in df.iterrows():
        if row['crimeIndex'].astype(float)>0 and row['crimeIndex'].astype(float)<=20:
            key='0-20'
        elif row['crimeIndex'].astype(float)>20 and row['crimeIndex'].astype(float)<=40:
            key='20-40'
        elif row['crimeIndex'].astype(float)>40 and row['crimeIndex'].astype(float)<=60:
            key='40-60'
        elif row['crimeIndex'].astype(float)>60 and row['crimeIndex'].astype(float)<=80:
            key='60-80'
        elif row['crimeIndex'].astype(float)>80 and row['crimeIndex'].astype(float)<=100:
            key='80-100'
        l.append((key, 1))
        
    return l


m = mapper(MapAnalytics1)
mapped_partitions = m.map(partitions)


def func_for_reduce(value_list, output):
    output.append(sum(value_list))


r = Reducer(func_for_reduce)
reduced_output = r.reduce(m.partitioned_data)
print("reduced_output")
print(reduced_output)

#fig = plt.figure(figsize = (10, 5))
#plt.bar(x, y, color ='maroon', width = 0.4)
#plt.show()