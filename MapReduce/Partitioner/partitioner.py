from collections import defaultdict

class partitioner:
    def __init__(self):
        self.reducer = defaultdict(list)

    def partition(self, key_value_pairs_list):
        for i in range(len(key_value_pairs_list)):
            self.reducer[key_value_pairs_list[i][0]].append(key_value_pairs_list[i][1])

        return self.reducer
