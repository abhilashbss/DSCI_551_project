from EDFS.EDFS_client.EDFSClient import EDFSClient
import json
import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)



def parse_json(data):
    return json.loads(json_util.dumps(data))

class edfs_client_processor:
    def __init__(self, db_type):
        self.e = EDFSClient("/Users/abhilashbss/Desktop/repositories/DSCI_551_project/EDFS/EDFS_client/namenode_config.conf")
        self.e.setup_datanode(db_type)

    def process_edfs_command(self, command):
        e = self.e
        args = command.split(" ")[1:]
        comm = command.split(" ")[0]

        if comm == "mkdir":
            return e.Mkdir(args[0], args[1])
        elif comm == "ls":
            ls = e.Ls(args[0])
            return ls
        elif comm == "cat":
            file_data = JSONEncoder().encode(e.ReadFile(args[0]))
            # file_data = json.dumps(e.ReadFile(args[0]), indent=2)
            return file_data
        elif comm == "rm":
            return e.Rm(args[0])
        elif comm == "put":
            if e.WriteFile(args[0], args[1], args[2], int(args[3])):
                return "File written succesfully"
            else:
                return "File write failed"
        elif comm == "getPartitionLocations":
            return json.dumps(e.GetPartitionLocations(args[0]), indent=2)
        elif comm == "readPartition":
            return json.dumps(e.ReadFilePartition(args[0],args[1]), indent=2)
        else:
            return "Invalid command. Try again!!"

    def get_directory_contents(self, fs_path):
        e = self.e
        return e.getChildNodes(fs_path)