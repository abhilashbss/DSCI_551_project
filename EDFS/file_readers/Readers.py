import csv

class Reader:
    def read(self):
        pass

    def write(self, local_file_path):
        pass


class JsonReader(Reader):
    def __init__(self, file_name):
        pass

    def read(self):
        pass

    def write(self, local_file_path):
        pass



class CsvReader(Reader):
    def __init__(self):
        pass

    def read(self, file_name):
        with open(file_name, 'r') as file:
            data = []
            for line in csv.DictReader(file):
                data.append(line)
            return data

    def write(self, local_file_path):
        pass

