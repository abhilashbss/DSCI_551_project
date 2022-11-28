from file_readers.Readers import CsvReader, JsonReader


class GenericFileReader:
    def __init__(self, format):
        self.reader = None
        if format == 'csv':
            self.reader = CsvReader()
        else:
            self.reader = JsonReader()

    # all formats can be converted to json while returning the content
    def read(self, file_path):
        content = self.reader.read(file_path)
        return content
