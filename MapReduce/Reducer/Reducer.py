
from collections import defaultdict
from threading import Thread
from shuffle.shuffle import shuffle
import collections


def flatten(l):
    return [item for sublist in l for item in sublist]


class Reducer:
    def __init__(self, reducer_func):
        self.reducer_func = reducer_func

    def reduce(self, partitioned_data):
        s = shuffle()
        partitions = s.shuffle(partitioned_data)
        output = defaultdict(list)
        for i in partitions.keys():
            output[i]=self.reducePartition({i:partitions[i]})
        return output

    def reducePartition(self, key_valuelist_dict):
        output_key_value_list = defaultdict(list)
        threads = []
        output_pairs = []
        for i in key_valuelist_dict.keys():
            thread = Thread(target=self.reducer_func, args=(flatten(key_valuelist_dict[i]), output_key_value_list[i]))
            threads.append(thread)
            thread.start()

        for i in range(len(threads)):
            threads[i].join()

        return output_key_value_list


# def func_for_reduce(value_list, output):
#     output.append(sum(value_list))
#
# r = Reducer(func_for_reduce)
# data = {"1":[1,2,3],"2":[3,4,5]}
# print(r.reduce(data))
