from mapper.mapper import mapper
from Reducer.Reducer import Reducer
from Partitioner.partitioner import partitioner
from EDFS.EDFS_client.EDFSClient import EDFSClient
import pandas as pd


e = EDFSClient("/Users/abhilashbss/Desktop/repositories/DSCI_551_project/EDFS/EDFS_client/namenode_config.conf")
# e.WriteFile("a/b/crime_rate_csv","/Users/abhilashbss/Desktop/repositories/DSCI_551_project/dataset/CrimeRate.csv",
#             "csv", 4 )
e.setup_datanode("firebase")
partitions = e.ReadFileRetainPartition("a/b/literacy_rate_csv")

#Find the country with the highest literacy rate

def MapFn2(key, partition_data):
    # print(partition_data["partition_content"])
    df = pd.DataFrame(partition_data["partition_content"])
    df1=df.sort_values(by=['Literacy rates (World Bank, CIA World Factbook, and other sources)'], ascending=False)
    res=df1[['Entity','Literacy rates (World Bank, CIA World Factbook, and other sources)']].iloc[0]
    t=[(1,[res['Entity'],res['Literacy rates (World Bank, CIA World Factbook, and other sources)']])]
    return t


m = mapper(MapFn2)
mapped_partitions = m.map(partitions)

# print(mapped_partitions)




def func_for_reduce(value_list, output):
    value_list.sort(key=lambda x: -1*float(x[1]))
    top = value_list[0]
    output.append(top)    #return statement


r = Reducer(func_for_reduce)
reduced_output = r.reduce(m.partitioned_data)
print("reduced_output")
print(reduced_output)

# Output
# defaultdict(<class 'list'>, {1: defaultdict(<class 'list'>, {1: [['North Korea', '99.999237']]})})
#

