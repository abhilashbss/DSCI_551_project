from EDFS.EDFS_client.EDFSClient import EDFSClient
import json
class edfs_client_processor:
    def __init__(self, command):
        self.command = command

    def process_command(self):
        e = EDFSClient("/Users/abhilashbss/Desktop/repositories/DSCI_551_project/EDFS/EDFS_client/namenode_config.conf")
        args = self.command.split(" ")[1:]
        comm = self.command.split(" ")[0]

        if comm == "mkdir":
            return e.Mkdir(args[0], args[1])
        elif comm == "ls":
            ls = e.Ls(args[0])
            return ls
        elif comm == "cat":
            file_data = json.dumps(e.ReadFile(args[0]), indent=2)
            return file_data
        elif comm == "rm":
            return e.Rm(args[0])
        elif comm == "put":
            if e.WriteFile(args[0], args[1], args[2], int(args[3])):
                return "File written succesfully"
            else:
                return "File write failed"
        elif comm == "getPartitionLocations":
            return json.dumps(e.ReadFileRetainPartition(args[0]), indent=2)
        elif comm == "readPartition":
            return json.dumps(e.ReadFilePartition(args[0],args[1]), indent=2)
        else:
            return "Invalid command. Try again!!"
