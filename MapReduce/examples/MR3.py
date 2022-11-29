from mapper.mapper import mapper
from Reducer.Reducer import Reducer
from Partitioner.partitioner import partitioner
from EDFS.EDFS_client.EDFSClient import EDFSClient
import pandas as pd


e = EDFSClient("/Users/abhilashbss/Desktop/repositories/DSCI_551_project/EDFS/EDFS_client/namenode_config.conf")
# e.WriteFile("a/b/crime_rate_csv","/Users/abhilashbss/Desktop/repositories/DSCI_551_project/dataset/CrimeRate.csv",
#             "csv", 4 )
e.setup_datanode("mongodb")
partitions = e.ReadFileRetainPartition("a/b/life_expectency")

#Find the countries which have life expectancy greater than 88

def MapFn3(key, partition_data):
    df = pd.DataFrame(partition_data["partition_content"])
    filter = df['Life expectancy '] != ''
    df1 = df[filter]
    df2=df1[df1['Life expectancy '].astype(float)>88]
    res=df2[['Life expectancy ','Country']]
    l=[]
    for k, row in res.iterrows():
        l.append((1,[row['Life expectancy '],row['Country']]))
    return l

m = mapper(MapFn3)
mapped_partitions = m.map(partitions)
print(m.partitioned_data)

def func_for_reduce(value_list, output):
    value_list.sort(key=lambda x: -1*float(x[0]))
    output.append(value_list)    #return statement


r = Reducer(func_for_reduce)
reduced_output = r.reduce(m.partitioned_data)
print("reduced_output")
print(reduced_output)
#
# Output
#
# defaultdict(<class 'list'>, {1: defaultdict(<class 'list'>, {1: [[['89', 'Belgium'], ['89', 'Finland'], ['89', 'France'], ['89', 'France'], ['89', 'Germany'], ['89', 'Italy'], ['89', 'New Zealand'], ['89', 'Norway'], ['89', 'Portugal'], ['89', 'Spain'], ['89', 'Sweden']]]})})

