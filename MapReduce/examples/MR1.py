from mapper.mapper import mapper
from Reducer.Reducer import Reducer
from Partitioner.partitioner import partitioner
from EDFS.EDFS_client.EDFSClient import EDFSClient
import pandas as pd


e = EDFSClient("/Users/abhilashbss/Desktop/repositories/DSCI_551_project/EDFS/EDFS_client/namenode_config.conf")
e.setup_datanode("firebase")
# e.WriteFile("a/b/crime_rate_csv","/Users/abhilashbss/Desktop/repositories/DSCI_551_project/dataset/CrimeRate.csv",
#             "csv", 4 )
partitions = e.ReadFileRetainPartition("a/b/crime_rate_csv")

#Graph to show how the crime index is distributed across different countries

def MapFn1(key, partition_data):
    df = pd.DataFrame(partition_data["partition_content"])
    df.sort_values(by=['crimeIndex'], ascending=False)
    res=df[['country', 'crimeIndex']].head()
    l=[]
    for k, row in res.iterrows():
        l.append((1,[row["country"],row["crimeIndex"]]))
    return l


m = mapper(MapFn1)
mapped_partitions = m.map(partitions)


def func_for_reduce(value_list, output):
    value_list.sort(key=lambda x: -1*float(x[1]))
    top_5 = value_list[:5]
    output.append(top_5)    #return statement


r = Reducer(func_for_reduce)
reduced_output = r.reduce(m.partitioned_data)
print("reduced_output")
print(reduced_output)



