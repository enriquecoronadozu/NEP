# coding = utf-8
#!/usr/bin/env python

# ------------------------------- Node -------------------------------
# Description: Low-level Node Class
# --------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga

import time
import os
import sys
import signal
import threading
import simplejson
import nep
import zmq
import atexit
from zmq.eventloop import ioloop, zmqstream



#TODO: bug sending strings there is a space + message in publish-subscriber with ZMQ
#TODO: unregister topic when closed


try:
    if sys.version_info[0] == 2:
        import nanomsg
except ImportError:
    pass

try:
    if sys.version_info[0] == 3:
        import rclpy
except ImportError:
    pass   

class node:

    # ----------------------- __signal_handler  ------------------------------
    def __signal_handler(self, signal, frame):
        """ Exit node with Ctrl+C """
        import os
        print('Signal Handler, you pressed Ctrl+C! to close the node')
        if not os.environ.get('OS','') == 'Windows_NT': # Windows
            time.sleep(.5)
            os.system('kill %d' % os.getpid())
            sys.exit(0)
        else:
            """Signal handler used to close when user press Ctrl+C"""
            time.sleep(.5)
            import os
            pid = os.getpid()
            import subprocess as s
            s.Popen('taskkill /F /PID {0}'.format(pid), shell=True)
            sys.exit(0)
        
    # ----------------------- __wait_kill ------------------------------
    def __wait_kill(self):
        """Listen for close the current node from an extrenal message on the topic \nep_node"""
        exit = False
        time.sleep(.1)
        conf = self.direct("127.0.0.1", "12345", "one2many") 
        exit_sub  = self.new_sub("/nep_node", "json", conf)
        time.sleep(.1)

        # Always wait in blocking mode for the kill message of the node 
        while not exit:
            # Wait for kill signal (Operation in blocking mode)
            s, data = exit_sub.listen_json(True) 
            # If new kill signal detected
            if s == True:
      
                try:
                    kill_proccess = False

                    if "node" in data:
                        node_ = data["node"]
                        if type(node_) is list:
                            for l in node_:
                                # If one of the names and the type of the request to kill is equal the name and type of this node, then kill the node
                                if l == self.node_name:
                                    kill_proccess = True
                        elif type(node_) is str: 
                            # If current name and type of the request to kill is equal the name and type of this node, then kill the node
                            if node_ == "all":
                                kill_proccess = True
                            if node_ == self.node_name:
                                kill_proccess = True

                    if kill_proccess:
                        self.__unregister()
                        print ("************* Node signal **************")
                        print (data)
                            
                        exit = True
                        import os

                        if not os.environ.get('OS','') == 'Windows_NT': # Windows
                            os.system('kill %d' % os.getpid())
                            sys.exit(0)
                        else:
                            pid = os.getpid()
                            print (pid)
                            import subprocess as s
                            s.Popen('taskkill /F /PID {0}'.format(pid), shell=True)
                except:
                    print ("NEP ERROR: processing node signal")
                    pass

    def __unregister(self):
        # TODO send pub message to manster to unregister topics
        print ("Closing NEP node")
        time.sleep(3)
        pass
        
    
    def __init__(self, node_name, transport = "ZMQ", exit_thread = True):
        """
        Class used to define a new node using the publisher-subscriber pattern. This class is compatible with ZeroMQ, Nanomsg and ROS.

        Parameters
        ----------

        node_name : string 
            Name of the node
        
        transport : string
            Define the transport layer of the node, can be 'ROS' to use ROS, 'ZMQ' to use ZeroMQ and 'NN' or 'nanomsg' to use nanomsg.

        exit_thread : bool
            If True then the node can be killed sending a dictionary to the "/nep_node" topic with the info of {'node': <node-name-to-kill>} or {"type":<node-type-to-kill>}. Where  <node-name-to-kill> and  <node-type-to-kill> can be string or list of strings.

        """
        atexit.register(self.__unregister)
        self.NN_installed = False
        try:
            import nanomsg
            self.NN_installed = True
        except ImportError:
            self.NN_installed = False
            
        # Enable to kill the node using Ctrl + C
        signal.signal(signal.SIGINT, self.__signal_handler)
        
        self.node_name = node_name
        self.transport  = transport
        self.pid = os.getpid()

        print ("NODE: " + self.node_name + ", pid: " + str(self.pid))

        if self.transport == "ZMQ" or self.transport == "NN" or self.transport == "nanomsg":
            if exit_thread: # Enable this node to be killed from an external signal
                
                # ------------------------- Kill thread ------------------------------------
                # thread that can de used to stop the program
                self.exit = threading.Thread(target = self.__wait_kill)
                # Used to finish the background thread when the main thread finish
                self.exit.daemon = True
                # start new thread 
                self.exit.start()
        
        # Import ROS libraries and create new ROS enviroment

        if self.transport  == 'ROS':
            try:
                import rospy		
                rospy.init_node(node_name, anonymous=True)
                print ("ROS node started")
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

                print ("NEP ERROR: rospy not found, possible causes:")
                print ("- Are you using Ubuntu or another Linux distribution complatible with ROS?")
                print ("- Have you installed ROS in your PC?")
                print ("- Is ROS installed correctly ?")
                print ("- Are you using Python 2.7")
                
                if sys.version_info < (3.0):
                    y = raw_input("Press ENTER to continue and exit")
                else:
                    time.sleep(5)
                sys.exit(1)

        elif self.transport  == 'ROS2':
            try:
                import rclpy		
                rclpy.init()
                self.node_ros2 = rclpy.create_node(node_name)
                print ("NODE: ROS2 started")

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

                print ("NEP ERROR: rclpy not found, possible causes:")
                print ("- Have you installed ROS 2.0 in your PC?")
                print ("- Is ROS 2.0 installed correctly?")
                print ("- Are you using Python 3")
                
                if sys.version_info < (3.0):
                    y = raw_input("Press ENTER to continue and exit")
                else:
                    time.sleep(5)
                sys.exit(1)



    def hybrid(self, master_ip = "127.0.0.1", mode = "many2many", transport = "ZMQ"):
        """ 
        Publisher-Subscriber Hybrid P2P configuration
       
        Parameters
        ----------

        master_ip : string
           IP of master    

        mode : string
            Only for ZeroMQ and Nanomsg. It can be "one2many" (one publisher and many subscribers in a topic), "many2one" (one publisher and many subscribers in a topic), "many2many" (many publishers and many subscribers in a topic).    

        Returns
        ----------

        conf: dictionary
            Dictionary with the specifications of the publisher

        """
        conf = {'transport': transport, 'network': "broker", 'mode':mode, 'master_ip': master_ip}
        return conf


    def direct(self, ip = "127.0.0.1", port = "9000", mode = "one2many", transport = ""):

        """
        Publisher-Subscriber direct network configuration

        Parameters
        ----------

        port : string 
            Value of the port to perform the socket connection (only for ZeroMQ and Nanomsg in a "direct" network)

        ip : string 
            Value of the ip to perform the socket connection (only for ZeroMQ and Nanomsg in a "direct" network)

        mode : string
            Only for ZeroMQ and Nanomsg. It can be "one2many" (one publisher and many subscribers in a topic) or "many2one" (one publisher and many subscribers in a topic).

        Returns
        ----------

        conf: dictionary
            Dictionary with the specifications of the publisher

        """
        if transport == "":
            transport = "ZMQ"
        else:
            transport = self.transport
        conf = {'transport': transport, 'network': "direct", 'port': port, 'ip': ip, 'mode':mode}
        return conf

    def new_client(self, topic):
        """
        Function used to generate a new client by specifying a topic

        Parameters
        ----------
        topic : string 
            Name of the topic

        Returns
        ----------

        client : nep.client
            Client instance

        """

        print("CLIENT: " + topic + ", waiting NEP master ...")
        s, port, ip  = nep.masterRegister(self.node_name, topic, master_ip = '127.0.0.1', master_port = 7000, socket = "client", pid = self.pid, data_type="json")

        if s:
            print ("CLIENT: " + topic + ", in " + ip + ":" + str(port))
            client = nep.client(ip, port, debug = False)
            print("CLIENT: " + topic + ", socket ready")
            return client
        else:
            print ("NEP ERROR: " + topic + ", client socket not connected")

    def new_server(self, topic):
        """
        Function used to generate a new server by specifying a topic

        Parameters
        ----------
        topic : string 
            Name of the topic

        Returns
        ----------

        server : nep.server
            Server instance

        """

        print("SERVER: " + topic + ", waiting NEP master ...")
        s, port, ip  = nep.masterRegister(self.node_name, topic, master_ip = '127.0.0.1', master_port = 7000, socket = "server", pid = self.pid, data_type="json")
        if s:
            print ("SERVER: " + topic + ", in " + ip + ":" + str(port))
            server = nep.server(ip,port, debug = False) #Create a new server instance
            print("SERVER: " + topic + ", socket ready")
            return server
        else:
            print ("NEP ERROR: " + topic + ", server socket not connected")
 

    def new_pub(self,topic, msg_type = "json", configuration =  {'transport': "ZMQ", 'network': "broker", 'mode':"many2many", "master_ip":"127.0.0.1" }):
        """
        Function used to generate a new publisher in the current node

        Parameters
        ----------
        topic : string 
            Name of the topic

        configuration : dictionary 
            Configuration of the publisher


        Returns
        ----------

        pub : nep.publisher
            Publisher instance

        """
        if self.transport == 'ROS2':
            configuration =  {'transport': "ROS2", 'network': "broker", 'mode':"many2many"}
            pub = nep.publisher(topic, self.node_ros2, msg_type,configuration )
            return pub

        if self.transport == 'ROS':
            configuration =  {'transport': "ROS", 'network': "broker", 'mode':"many2many"}
            
        #TODO: launch error if you dont put msg_type or conf
        pub = nep.publisher(topic, self.node_name, msg_type, configuration)
        return pub

    def new_callback(self, topic , msg_type , callback, conf = {'transport': 'ZMQ', 'network': "broker", 'mode':"many2many", "master_ip":"127.0.0.1"}):
        """
        Function used to generate a new subscriber callback. Only for ZMQ and ROS.

        Parameters
        ----------
        topic : string 
            Name of the topic

        msg_type : string
            Message type: "string", "json" for ZMQ and nanomsg, some ROS geometry messages are also supported 

        callback: function
            Function that will be executed

        """

        if self.transport == 'ROS2':
            conf = {'transport': "ROS2", 'network': "broker", 'mode':"many2many"}
            self.sub = nep.subscriber(topic, self.node_ros2, msg_type, conf, callback)

        elif self.transport  == 'ROS':
            conf = {'transport': "ROS", 'network': "broker", 'mode':"many2many"}
            self.sub = nep.subscriber(topic, self.node_name, msg_type, conf, callback)

        elif self.transport  == 'ZMQ':
            self.sub = nep.subscriber(topic, self.node_name, msg_type, conf)
            self.sub_socket = self.sub.sock
            self.sub_callback = callback
            self.sub_msg_type = msg_type
        else:
            print("NEP ERROR: middleware " + self.transport + " do not support callback subscribers")

        return self.sub

    def __process_message(self,msg):

        if self.sub_msg_type == 'string':
            info = msg[0]
            index = info.find(' ')
            topic = info[0:index].strip()
            message = info[index+1:]
            self.sub_callback(message)
        
        else:
            s, message = self.__deserialization(msg[0])
            if s:
                self.sub_callback(message)


    def __loads(self, s, **kwargs):
        """Load object from JSON bytes (utf-8). See jsonapi.jsonmod.loads for details on kwargs.
        """
        if sys.version_info[0] == 2:
            if str is unicode and isinstance(s, bytes):
                s = s.decode('utf8')
        return simplejson.loads(s, **kwargs)
        
    def __deserialization(self, info):
        """ Separate the topic and the json message from the data received from the ZeroMQ socket. If the deserialization was successful and the message as a python dictionary
            
            Parameters
            ----------
            info : string
                topic + message received by the ZQM socket 

            Returns
            -------
            msg : string
                String message as a python dictionary
        """
        try:
            json0 = info.find('{')
            topic = info[0:json0].strip()
            msg = self.__loads(info[json0:])
            success = True
        except:
            print("NEP Serialization Error: \n" + str(info) + "\n" + "Is not JSON serializable")
            msg = {}
            success = False
        return success, msg


    def spin(self):
        """ Start event loop"""
        if self.transport  == 'ZMQ':
            # Event Loop calback option
            if self.sub_callback != None:
                stream_sub = zmqstream.ZMQStream(self.sub_socket)
                stream_sub.on_recv(self.__process_message)
                ioloop.IOLoop.instance().start()
        elif self.transport  == 'ROS':
            import rospy
            """Function used to spin ROS subscriber"""
            rospy.spin()

        elif  self.transport  == 'ROS2':
            import rclpy
            while rclpy.ok():
                rclpy.spin_once(self.node_ros2)
            # Destroy the node explicitly
            # (optional - otherwise it will be done automatically
            # when the garbage collector destroys the node object)
            self.node_ros2.destroy_node()
            rclpy.shutdown()


    def new_surveyor(self, topic, timeout = 1000):
        """
        Function used to generate a new subscriber in the current node

        Parameters
        ----------
        topic : string 
            Name of the topic

        timeout : int
            Maximun miliseconds waiting for response

        Returns
        ----------

        sub : nep.surveyor 
            subscriber instance
        """
        sur = nep.surveyor(topic, timeout, self.node_name)
        return sur

    def new_respondent(self, topic, msg_type = "json"):
        """
        Function used to generate a new subscriber in the current node

        Parameters
        ----------
        topic : string 
            Name of the topic

        msg_type : Type of message
            Name of the topic


        Returns
        ----------

        sub : nep.respondent 
            subscriber instance
        """
        res = nep.respondent(topic, self.node_name)
        return res


    def new_sub(self, topic, msg_type = "json", configuration =  {'transport': "ZMQ", 'network': "broker", 'mode':"many2many", "master_ip":"127.0.0.1" }):

        """
        Function used to generate a new subscriber in the current node

        Parameters
        ----------
        topic : string 
            Name of the topic

        msg_type : Type of message
            Name of the topic

        configuration : dictionary  
            Configuration of the subscriber

        Returns
        ----------

        sub : nep.subscriber 
            subscriber instance
        """

        sub = nep.subscriber(topic, self.node_name, msg_type, configuration)
        return sub


# TODO: sock.close() and context.destroy() must be set when a process ends
# In some cases socket handles won't be freed until you destroy the context.
# When you exit the program, close your sockets and then call zmq_ctx_destroy(). This destroys the context.
# In a language with automatic object destruction, sockets and contexts 
# will be destroyed as you leave the scope. If you use exceptions you'll have to
#  do the clean-up in something like a "final" block, the same as for any resource.


if __name__ == "__main__":
    import doctest
    doctest.testmod()
