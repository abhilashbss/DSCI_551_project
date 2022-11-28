from threading import Thread
from Combiner.combiner import Combiner
from Partitioner.partitioner import partitioner

class mapper:
    def __init__(self, mapper_func, combine_func=None):
        self.mapper_func = mapper_func
        self.combine_func = combine_func
        self.partitioned_data = None

    def mapPartition(self, key, value, output_kv_list, partitioned_data ):
        output_pairs = self.mapper_func(key, value)
        if self.combine_func:
            c = Combiner(self.combine_func)
            output_kv_list += c.combine_map(output_pairs)
        else:
            output_kv_list += output_pairs

        p = partitioner()
        partitioned_data.append(p.partition(output_kv_list))

    def map(self, partitions):
        output_key_value_list = [[] for i in range(len(partitions))]
        self.partitioned_data = [[] for i in range(len(partitions))]
        threads = []
        output_pairs = []
        for i in range(len(partitions)):
            thread = Thread(target=self.mapPartition, args=("",partitions[i], output_key_value_list[i], self.partitioned_data[i]))
            threads.append(thread)
            thread.start()

        for i in range(len(threads)):
            threads[i].join()
            output_pairs.append(output_key_value_list[i])


        return output_pairs


def func_for_map(key, arr_of_dict):
    output_pairs = []
    for i in range(len(arr_of_dict)):
        output_pairs.append((arr_of_dict[i]["1960"], arr_of_dict[i]["1960"]%2))
    return output_pairs

# m = mapper(func_for_map)
# partitions = [  [{"1960":1},{"1960":2}],
#                 [{"1960":3},{"1960":4}]]
#
# print(m.map(partitions))
#



