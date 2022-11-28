from mapper.mapper import mapper
from Reducer.Reducer import Reducer
from Partitioner.partitioner import partitioner

# output_pairs: [(1,0),(1,3)]
def func_for_partition(key, arr_of_dict):
    output_pairs = []
    for i in range(len(arr_of_dict)):
        output_pairs.append((arr_of_dict[i]["1960"]%3, 1))
    return output_pairs

def func_for_reduce(value_list, output):
    output.append(sum(value_list))

partitions = [[{"1960":1},{"1960":2}],
              [{"1960":3},{"1960":4}]]

# Map operation
m = mapper(func_for_partition)
mapped_partitions = m.map(partitions)

print("mapped_partitions")
print(mapped_partitions)
print("partitioned data")
print(m.partitioned_data)


# Reduce operation
r = Reducer(func_for_reduce)
reduced_output = r.reduce(m.partitioned_data)
print("reduced_output")
print(reduced_output)




def MapFn1(key, partition_data):
    df = pd.DataFrame(partition_data)
    df.sort_values(by=['crimeIndex'], ascending=False)
    res=df[['country', 'crimeIndex']].head()
    print(res)
    return res

m = mapper(MapFn1)
mapped_partitions = m.map(partitions)

print("mapped_partitions")
print(mapped_partitions)
print("partitioned data")
print(m.partitioned_data)
print(MapFn1(partition_data))