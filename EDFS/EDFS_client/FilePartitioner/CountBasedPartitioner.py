import math
from file_readers.file_reader import GenericFileReader


class CountBasedPartitioner:
    def __init__(self, file, format):
        self.file = file
        self.format = format
        self.reader = GenericFileReader(format)
        self.file_content = self.reader.read(file)
        self.partitions = []
        self.partition_length = -1
        self.total_file_count = -1

    def partition(self, no_of_partitions):
        self.total_file_count = len(self.file_content)
        # print("record count in file: " + str(self.total_file_count))
        self.partition_length = math.floor(self.total_file_count/no_of_partitions)
        i = 0
        while (i+1)*self.partition_length <= self.total_file_count:
            self.partitions.append(self.file_content[i*self.partition_length: (i+1)*self.partition_length])
            i+=1
        if i*self.partition_length<self.total_file_count:
            self.partitions[-1] += self.file_content[i*self.partition_length: ]

    def get_partition(self, partition_no):
        return self.partitions[partition_no]

    def get_all_partitions(self):
        return self.partitions


# c = CountBasedPartitioner("./EDFS_client/sample_text.csv", "csv")
# c.partition(4)
# print(c.get_all_partitions()) # working

