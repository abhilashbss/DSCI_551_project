import pymongo
import xmlrpc.client
import copy

class NameNodeManager:
    def __init__(self, db_type, db_url, default_datanode_type=None, default_datanode_url=None):
        if db_type == "mongoDB":
            self.myclient = pymongo.MongoClient(db_url)
            self.mydb = self.myclient["Namenode"]
            self.mycol = self.mydb["metadata"]
        self.default_datanode_type = default_datanode_type
        self.default_datanode_url = default_datanode_url

    #returned object should contain datanodedb url
    def GetPartitionLocations(self, file_path):
        file_path_query = {"file_path": file_path}
        mydoc = self.mycol.find(file_path_query)
        data = list(mydoc)
        assert len(data) == 1
        return {"datanode_db_url": data[0]["datanode_db_url"], "datanode_db_type": data[0]["datanode_db_type"], "partitions": data[0]["partition_locations"]}

    # create tables in datanode db and update metastore
    def CreateFilePartitions(self, file_name, file_type, number_of_partitions, datanode_type=None, datanode_url=None):
        # check if parent path is directory

        table_names = []

        if datanode_url == None:
            datanode_url = self.default_datanode_url
            datanode_type = self.default_datanode_type
        file_path_parent_query = {"file_path": "/".join(file_name.split("/")[:-1])}
        mydoc = self.mycol.find(file_path_parent_query)
        parent = list(mydoc)
        assert len(parent) == 1
        assert parent[0]["file_type"] == "directory"

        # file does not exist
        file_path_query = {"file_path": file_name}
        mydoc = self.mycol.find(file_path_query)
        file = list(mydoc)
        assert len(file) == 0

        #add the new file entry
        new_file = {"file_path": file_name,"file_type": file_type,"total_partitions": number_of_partitions,
                    "datanode_db_type": datanode_type,"datanode_db_url":datanode_url}
        partition_obj = {}
        file_name = file_name.replace("/","_")
        for i in range(number_of_partitions):
            partition_obj[str(i)] = {"table_name": file_name+"_"+str(i)}

        new_file["partition_locations"] = partition_obj
        res = copy.deepcopy(new_file)
        self.mycol.insert_one(new_file)
        return str(res)

    def Mkdir(self, parent_path, directory_name):
        file_path_parent_query = {"file_path": parent_path}
        mydoc = self.mycol.find(file_path_parent_query)
        parent = list(mydoc)
        assert len(parent) == 1
        assert parent[0]["file_type"] == "directory"

        # file does not exist
        directory_path_query = {"file_path": directory_name}
        mydoc = self.mycol.find(directory_path_query)
        dir = list(mydoc)
        assert len(dir) == 0

        new_file = {"file_path": parent_path + "/"+ directory_name, "file_type": "directory", "total_partitions": 0,
                    "datanode_db_type": "", "datanode_db_url": "", "partition_locations":""}
        self.mycol.insert_one(new_file)

    def Ls(self, path):
        file_path_query = {}
        mydoc = self.mycol.find(file_path_query)
        all_files = list(mydoc)
        children = []
        for i in range(len(all_files)):
            if "/".join(all_files[i]["file_path"].split("/")[:-1]) == path:
                children.append(all_files[i]["file_path"])
        return children

    def Rm(self, file_path):
        # check if this is a directory and check the respective flags
        file_path_query = {"file_path": file_path}
        mydoc = self.mycol.find(file_path_query)
        file = list(mydoc)

        if file[0]["file_type"] == "directory":
            file_path_query = {}
            mydoc = self.mycol.find(file_path_query)
            all_files = list(mydoc)
            children = []
            for i in range(len(all_files)):
                if all_files[i]["file_path"].startswith(file_path):
                    myquery = {"file_path": all_files[i]["file_path"]}
                    self.mycol.delete_one(myquery)
        else:
            self.mycol.delete_one(file_path_query)

    def GetDefaultDataNode(self):
        return {"db_type": self.default_datanode_type, "db_url": self.default_datanode_url}



n = NameNodeManager("mongoDB","mongodb+srv://dsci:dsci@dsci.tgtoaqs.mongodb.net/?retryWrites=true&w=majority")
# print(n.GetPartitionLocations("a/b/c"))
# print(n.CreateFilePartitions("a/b/d","non-directory", 5 ,"","")) #before parent directory creation should fail, getting error
# print(n.Mkdir("a/b", "new_dir" ))
# print(n.Ls("a/b"))
# print(n.Rm("a/b/c"))  # working
# print(n.Rm("a/b"))    # working




