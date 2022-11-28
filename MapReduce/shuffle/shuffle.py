from collections import defaultdict

class shuffle:
    def __init__(self):
        pass

    def shuffle(self, partitioned_data):
        output = defaultdict(list)
        for i in range(len(partitioned_data)):
            for key in partitioned_data[i][0].keys():
                output[key].append(partitioned_data[i][0][key])

        return output