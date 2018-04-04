import nep
import sys
import signal
import sys
import time

class feedback():

    def __init__(self,status_pub, node_name):
        """ Class used to help in the creation of an action node with NEP framework (ZeroMQ and NanoMsg) """
        self.node_name = node_name
        self.status_pub = status_pub
            
    def connection_starting(self):
        """Send connection_starting message"""
        status_message = {'node':self.node_name, 'input':"connection_starting"}
        self.status_pub.send_info(status_message)

    def connection_ready(self):
        """Send connection_ready message"""
        status_message = {'node':self.node_name, 'input':"connection_ready"}
        self.status_pub.send_info(status_message)
            
    def connection_error(self):
        """Send connection_error message"""
        status_message = {'node':self.node_name, 'input':"connection_error"}
        self.status_pub.send_info(status_message)

    def connection_closed(self):
        """Send connection_closed message"""
        status_message = {'node':self.node_name, 'input':"connection_closed"}
        self.status_pub.send_info(status_message)

    def execution_busy(self):
        """Send execution_busy message"""
        status_message = {'node':self.node_name, 'input':"execution_busy"}
        self.status_pub.send_info(status_message)

            
if __name__ == "__main__":
    import doctest
    doctest.testmod()


