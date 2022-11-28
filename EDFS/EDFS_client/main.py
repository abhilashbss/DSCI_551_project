from EDFSClient import EDFSClient

e = EDFSClient("./EDFS_client/namenode_config.conf")
# e.WriteFile("a/b/csv","./EDFS_client/sample_text.csv",
#             "csv", 4 )
# print(e.ReadFile("a/b/csv"))
# print(e.ReadFilePartition("a/b/csv",2))
print(e.ReadFileRetainPartition("a/b/csv"))
# e.Mkdir("a/b","new_dir")
# e.Rm("a/b/new_dir")
#
# e.Mkdir("a/b", "new_dir")
# print(e.Ls("a/b"))
#
# print(e.GetPartitionLocations("a/b/csv"))


