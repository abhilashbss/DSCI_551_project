import xmlrpc.client
import configparser
import json
class NameNodeInterface:
    def __init__(self, configFilePath):
        configParser = configparser.RawConfigParser()
        configParser.read(configFilePath)
        config_dict = dict(configParser.items('default'))
        self.server = xmlrpc.client.ServerProxy(config_dict["namenode_url"])

    def mkdir(self, file_path, directory_name):
        self.server.Mkdir(file_path, directory_name)

    def rm(self, file_path):
        self.server.Rm(file_path)

    def create_file_partitions(self, file_path, no_of_partitions):
        response = self.server.CreateFilePartitions(file_path, "non-directory",no_of_partitions)
        print("response: "+response)
        # print(json.loads(response.replace("\'",'\"'))["total_partitions"])
        return json.loads(response.replace("\'",'\"'))

    def get_file_partitions(self, file_path):
        return self.server.GetPartitionLocations(file_path)

    def ls(self, file_path):
        return self.server.Ls(file_path)

    def get_partition_table_name(self, file_path, partition_no):
        partition_locations = self.server.GetPartitionLocations(file_path)
        return partition_locations[str(partition_no)]
        
    def get_default_datanode_db(self):
        return self.server.GetDefaultDataNode()


# n = NameNodeInterface("./EDFS_client/namenode_config.conf")
# print(n.mkdir("a/b","dir"))  working
#   todo: test for rest
