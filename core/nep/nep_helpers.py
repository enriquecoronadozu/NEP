import nep
import sys
import signal
import sys
import time


class action():

    def action_signal_handler(self, signal, frame):
        """Signal handler used to close the app"""
        print('Signal Handler, you pressed Ctrl+C! to close the node')
        self.connection_closed()
        sys.exit(0)
        
    """ Class used to help in the creation of an action node with NEP framework (ZeroMQ and NanoMsg) """
    def __init__(self,robot_name = "nao"):
        self.robot_name = robot_name
        self.node = nep.node("action_"+str(robot_name)) # Create a new node
        self.__init_status_communication()
        self.__init_request_response()
        self.__connection_starting()
        signal.signal(signal.SIGINT, self.action_signal_handler)

    def __exit_function():
        self.connection_closed()
        
    def __init_status_communication(self):
        conf_pub = self.node.conf_pub(mode='many2one')
        self.status_pub = self.node.new_pub("/node_status",conf_pub)

    def __init_request_response(self):
        conf = self.node.conf_pub(mode= "many2many")
        self.pub = self.node.new_pub("/action_response", conf)
        conf = self.node.conf_sub(mode= "many2many")
        self.sub = self.node.new_sub("/action_request", conf)
            
    def __connection_starting(self):
        status_message = {'node_type':"action", 'node_status':"connection_starting", 'robot_name':self.robot_name}
        self.status_pub.send_info(status_message)

    def connection_ready(self):
        status_message = {'node_type':"action", 'node_status':"connection_ready", 'robot_name':self.robot_name}
        self.status_pub.send_info(status_message)
            
    def connection_error(self):
        status_message = {'node_type':"action", 'node_status':"connection_error", 'robot_name':self.robot_name}
        self.status_pub.send_info(status_message)

    def connection_closed(self):
        status_message = {'node_type':"action", 'node_status':"connection_closed", 'robot_name':self.robot_name}
        self.status_pub.send_info(status_message)
            

    def response (self,state = "success"):
        """ Define an standart message to be sent to the sequencer """
        msg = {'robot_name': self.robot_name, 'execution_state': state}
        return msg


            
if __name__ == "__main__":
    import doctest
    doctest.testmod()


