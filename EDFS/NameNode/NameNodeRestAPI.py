
import configparser
# from db_connectors.db_connector import db_connector
from NameNodeManager import NameNodeManager
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import Binary



def get_name_node_manager():
    configParser = configparser.ConfigParser()
    configFilePath = r'/Users/abhilashbss/Desktop/repositories/DSCI_551_project/EDFS/NameNode/namenode.ini'
    configParser.read(configFilePath)
    print(configParser.sections())
    config_dict = dict(configParser.items('default'))
    firebase_config_dict = dict(configParser.items('firebase'))
    namenode_manager = NameNodeManager(config_dict["metastore_db_type"],
                                       config_dict["metastore_db_url"],
                                       config_dict["default_datanode_type"],
                                       config_dict["default_datanode_url"])
    return namenode_manager


if __name__ == '__main__':
    server = SimpleXMLRPCServer(('localhost', 9000),
                                logRequests=True,
                                allow_none=True)
    server.register_introspection_functions()
    server.register_multicall_functions()
    server.register_instance(get_name_node_manager())

    try:
        print('Use Control-C to exit')
        server.serve_forever()
    except KeyboardInterrupt:
        print('Exiting')
