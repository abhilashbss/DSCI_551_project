import mysql
import pymongo
import requests
import json


# This is for datanode connector
class db_connector:
    def __init__(self):
        self.connector = None

    '''
    {
        'db_type':
        'db_connection':
        'db_user':
        'db_pass':
    }
    '''
    def get_connector(self, conf):
        if conf["db_type"] == "mongoDB":
            self.connector = mongo_connector(conf["db_url"])
        if conf["db_type"] == "firebase":
            self.connector = firebase_connector(conf["db_url"])

        return self.connector

'''
import pymongo
'''
class mongo_connector():

    def __init__(self, datanode_db_url):
        print(datanode_db_url)
        myclient = pymongo.MongoClient(datanode_db_url)
        self.mydb = myclient["Datanode"]

    def read(self, partition_table ):
        mycol = self.mydb[partition_table]
        data = []
        for x in mycol.find({}):
            data.append(x)
        return data

    def write(self, partition_table , partitioned_data_array):
        print(partitioned_data_array["file_content"])
        mycol = self.mydb[partition_table]
        mycol.insert_many(partitioned_data_array["file_content"])

'''
url = "https://dsci-551-19f64-default-rtdb.firebaseio.com/"

'''


class firebase_connector():
    def __init__(self, url):
        self.url = url

    def read(self, partition_table):
        response = requests.get(self.url+ "/"+ partition_table+".json")
        return response.json()


    def write(self, partition_table, partition_data):
        response = requests.put(self.url+ "/" + partition_table + ".json", json.dumps(partition_data["file_content"], ensure_ascii=True))
        print("firebase_response")
        print(response.json())

# f = firebase_connector("https://dsci-551-19f64-default-rtdb.firebaseio.com/")
# f.write("a_b_0",[{"a":"b"},{"a":"c"}])
# print(f.read("a_b_0"))