class DatanodeInterface:
    def __init__(self, datanode_connector):
        self.datanode_connector = datanode_connector

    def ReadFilePartition(self, file_path, partition_table_name):
        partition_content = self.datanode_connector.read(partition_table_name)
        return partition_content

    def WriteFilePartition(self, file_path, file_partition_content, partition_table):
        self.datanode_connector.write(partition_table, {"file_path": file_path, "file_content": file_partition_content})


