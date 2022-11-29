from mapper.mapper import mapper
from Reducer.Reducer import Reducer
from Partitioner.partitioner import partitioner
from EDFS.EDFS_client.EDFSClient import EDFSClient
import pandas as pd
import matplotlib.pyplot as plt


e = EDFSClient("/Users/abhilashbss/Desktop/repositories/DSCI_551_project/EDFS/EDFS_client/namenode_config.conf")
e.setup_datanode("firebase")

# e.WriteFile("a/b/crime_rate_csv","/Users/abhilashbss/Desktop/repositories/DSCI_551_project/dataset/CrimeRate.csv",
#             "csv", 4 )
partitions = e.ReadFileRetainPartition("a/b/crime_rate_csv")
#Find top 5 countries which have the highest crime index

# Random Test
# c=0
# for i in range(len(partitions)):
#     p = partitions[i]["partition_content"]
#     for j in range(len(p)):
#         if float(p[j]["crimeIndex"]) > 20 and float(p[j]["crimeIndex"])  <40 :
#             c+=1
# print("manual count 20-40: "+str(c))

def MapAnalytics1(key, partition_data):

    # print(partition_data)
    df = pd.DataFrame(partition_data["partition_content"])
    print(df.head(5))
    l=[]
    for k, row in df.iterrows():
        if float(row['crimeIndex'])>0 and float(row['crimeIndex'])<=20:
            key='0-20'
        elif float(row['crimeIndex'])>20 and float(row['crimeIndex'])<=40:
            key='20-40'
        elif float(row['crimeIndex'])>40 and float(row['crimeIndex'])<=60:
            key='40-60'
        elif float(row['crimeIndex'])>60 and float(row['crimeIndex'])<=80:
            key='60-80'
        elif float(row['crimeIndex'])>80 and float(row['crimeIndex'])<=100:
            key='80-100'
        l.append((key, 1))
        
    return l


m = mapper(MapAnalytics1)
mapped_partitions = m.map(partitions)
print("mapped partitions")
print(mapped_partitions)
print("partitioned data")
print(m.partitioned_data)


def func_for_reduce(value_list, output):
    output.append(sum(value_list))


r = Reducer(func_for_reduce)
reduced_output = r.reduce(m.partitioned_data)
print("reduced_output")
print(reduced_output)

# fig = plt.figure(figsize = (10, 5))
# plt.bar(x, y, color ='maroon', width = 0.4)
# plt.show()

# Output
#
# defaultdict(<class 'list'>, {'80-100': defaultdict(<class 'list'>, {'80-100': [2]}), '60-80': defaultdict(<class 'list'>, {'60-80': [21]}), '40-60': defaultdict(<class 'list'>, {'40-60': [62]}), '20-40': defaultdict(<class 'list'>, {'20-40': [47]}), '0-20': defaultdict(<class 'list'>, {'0-20': [4]})})
#

