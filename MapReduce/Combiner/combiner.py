
from collections import defaultdict

class Combiner:
    def __init__(self, combiner_func):
        self.combiner_func = combiner_func

    def combine_map(self, key_value_list):
        output_key_vlist = defaultdict(list)
        for i in range(len(key_value_list)):
            output_key_vlist[key_value_list[i][0]].append(key_value_list[i][1])

        for i in output_key_vlist.keys():
            output_key_vlist[i] = self.combiner_func(output_key_vlist[i])

        return output_key_vlist