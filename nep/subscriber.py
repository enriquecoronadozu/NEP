# coding = utf-8
#!/usr/bin/env python

# ------------------------------ Subscriber --------------------------------
# Description: Low-level Subscriber Class
# --------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga


import time
import os
import zmq
import simplejson
import sys
import nep
import base64


try:
    import numpy as np
except ImportError:
    pass

try:
    import nanomsg
except ImportError:
    pass

try:
    import cv2
except ImportError:
    pass

class subscriber:
    """ Subscriber class used for inter-process comunication between nodes. Supports ZeroMQ, nanomsg and ROS publishers. 

        Parameters
        ----------

        topic : string 
            topic name to publish the messages

        node : string or ROS node
            Name of the node or ROS 2.0 instance

        msg_type : string
            Message type: "string", "json" for ZMQ and nanomsg, some ROS geometry messages are also supported 

        conf : dictionary
            Configuration of the publisher.

        callback : function
            Callback function (Only ROS).

        debug: bool
            If True some additional information of the subscriber is shown

    """
    def __init__(self, topic, node = "default", msg_type = "dict", conf =  {'transport': "ZMQ", 'network': "broker", 'mode':"many2many", "master_ip":"127.0.0.1"}, callback = "", debug = False):

        self.callback = callback
        self.topic = topic
        self.node = node
        self.conf = conf
        self.network = self.conf['network']
        self.transport =  self.conf['transport']
        self.msg_type = msg_type
        self.ip = ""
        self.port = ""
        self.debug = debug

        self.master_ip = "127.0.0.1"

        try:
            self.master_ip = conf["master_ip"]
            if self.master_ip == "127.0.0.1":
                print ("SUB: " + topic + " in local-host")
            else:
                print ("SUB: " + topic + " in " +  str(self.master_ip))
        except:
            pass

        if self.transport ==  "ROS":
            print ("SUB: " + topic + " using ROS 1.0")                                        #Use ROS
            self.__create_ROS_subscriber()
        elif self.transport ==  "ROS2":                                       #Use ROS 2.0
            print ("SUB: " + topic + " using ROS 2.0")
            self.__create_ROS2_subscriber()
        elif self.transport ==  "ZMQ":                                      #Use ZeroMQ
            if self.topic != "/nep_node":
                print ("SUB: " + topic + ", using ZMQ " + self.network)
            self.mode = "many2many" #many2many is the default value
            if "mode" in self.conf:
                self.mode = self.conf['mode']
            self.__create_ZMQ_subscriber()

        if self.transport ==  "NN" or self.transport ==  "nanomsg":          #Use nanomsg
            if self.topic != "/nep_node": 
                print ("SUB: " + topic + " using nanomsg " + self.network)
            self.mode = "many2many" #many2many is the default value #TODO: XPUB XSUB nn_device
            if "mode" in self.conf:
                self.mode = self.conf['mode']
            self.__create_NN_subscriber()
        

    def __network_selection(self):
        """ Get IP and port of this socket

        Returns
        ----------

        success : bool
            Only if True socket can be connected

        port : string
            Port used to connect the socket

        ip : string
            IP used to connect the socket
        """
        success = False
        ip = "127.0.0.1"
        port = "7000"
        self.pid = os.getpid()
        if self.network == "direct":
            # Set the port and ip selected by the user
            port = self.conf["port"]
            ip = self.conf['ip']
            success =  True
        elif self.network == "broker":
            if self.topic != "/nep_node":
                print("SUB: " + self.topic + " waiting NEP master ...")
            # Register the topic in the NEP Master and get the port and ip
            success, port, ip  = nep.masterRegister(self.node, self.topic, master_ip = self.master_ip, master_port = 7000, socket = "subscriber", mode = self.mode, pid = self.pid, data_type = self.msg_type)
            if self.topic != "/nep_node":
                print("SUB: " + self.topic + " socket ready")
        return success, port, ip

    # ---------------------------------- ROS ----------------------------------------
    def __create_ROS_subscriber(self):
        """Function used to create a ROS subscriber"""

        import rospy

        from std_msgs.msg import String
        rospy.Subscriber(self.topic, String, self.__process_ROS_callback)
    
        rospy.init_node(self.node, anonymous = True)



    # ---------------------------------- ROS 2.0 ----------------------------------------
    def __create_ROS2_subscriber(self):
        """Function used to create a ROS subscriber"""

        from std_msgs.msg import String
        self.ros_sub = self.node.create_subscription(String, self.topic, self.__process_ROS_callback)


    def __process_ROS_callback(self,data):
        if self.msg_type == "string":
            message = data.data
            self.callback(message)
        elif self.msg_type == "json":
            msg = data.data
            message = self.__loads(msg)
            self.callback(message)
        


    # ---------------------------------- ZMQ ----------------------------------------
    def __create_ZMQ_subscriber(self):
        """Function used to create a ZeroMQ subscriber"""
        success, self.port, self.ip = self.__network_selection()
        if success:
            try:        
                # ZeroMQ Context
                self.context = zmq.Context()
                # Define the type of context, in this case a subcriber
                self.sock = self.context.socket(zmq.SUB)
                # Define subscription and the messages with prefix to accept.
                # setsockopt obtain the data which message starts with the second argument
                # Then we obtain data from the topic with that starts with self.topic value
                if sys.version_info[0] == 2:
                    self.sock.setsockopt(zmq.SUBSCRIBE, self.topic)
                    self.sock.setsockopt(zmq.CONFLATE, 1) # Only keeps last mesange in queue
                else:
                    self.sock.setsockopt_string(zmq.SUBSCRIBE, self.topic)
                
                self.__connect_ZMQ_socket()
            except:
                print ("NEP ERROR: socket already in use")
        else:
            print("NEP ERROR: Socket unable to be connected")


    def __connect_ZMQ_socket(self):
        """ Connect ZMQ socket in base it configuration
        """

        if self.mode == "many2one":
            endpoint = "tcp://" + self.ip + ":" + str(self.port)
            self.sock.bind(endpoint)
            if self.debug or self.network == "direct":
                if not self.topic == "/nep_node":
                     print("SUB: " + self.topic + " endpoint " + endpoint +  " bind")
        elif self.mode == "one2many":

            endpoint = "tcp://" + self.ip + ":" + str(self.port)
            self.sock.connect(endpoint)
            if self.debug or self.network == "direct":
                if not self.topic == "/nep_node":
                    print("SUB: " + self.topic + " endpoint " + endpoint +  " connect")

        elif self.mode == "many2many":
            endpoint = "tcp://" +  self.ip + ":" + str( self.port+1)
            self.sock.connect(endpoint)
            if self.debug or self.network == "direct":
                if not self.topic == "/nep_node":
                    print("SUB: " + self.topic + " endpoint " + endpoint +  " connect")

        else:
            msg = "NEP ERROR: mode value " +  self.mode + "is not valid"
            raise ValueError(msg)

    def close_ZMQ_subscriber(self):
        """ This function closes the socket"""
        self.sock.close()
        self.context.destroy()
        time.sleep(1)

    # ---------------------------------- Nanomsg ----------------------------------------
    def __create_NN_subscriber(self):
        """Function used to create a NN publisher"""
        try:
            import nanomsg
            self.NN_installed = True
        except ImportError:
            print ("NEP WARNING: Nanomsg not installed")
            self.NN_installed = False

        if self.NN_installed == False:
            msg = "Unable to use surveyor pattern due that Nanomsg is not installed "
            raise ValueError(msg)
        else:
            success, self.port, self.ip = self.__network_selection()
            if success: 
                try:  
                    self.sock = nanomsg.Socket(nanomsg.SUB)
                    self.sock.set_string_option(nanomsg.SUB, nanomsg.SUB_SUBSCRIBE, self.topic)
                    #TODO: zmq.CONFLATE in nanomsg # Only keeps last mesange in queue
                    self.__connect_NN_socket()
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)


    def __connect_NN_socket(self):
        """Function used to create a Nanomsg publisher"""

        if self.mode == "many2one":
            if self.ip == '127.0.0.1':
                 self.ip = "*"
            endpoint = "tcp://" + self.ip + ":" + str(self.port)
            self.sock.bind(endpoint)
            #if self.debug or self.network == "direct":
                #print ("subscriber " + endpoint +  " bind")
        elif self.mode == "one2many":
            if self.ip == '127.0.0.1':
                self.ip = "localhost"
            endpoint = "tcp://" + self.ip + ":" + str(self.port)
            self.sock.connect(endpoint)
            #if self.debug or self.network == "direct":
                #print ("subscriber " + endpoint +  " connect")
        elif  self.mode == "many2many":
            if self.ip == '127.0.0.1':
                self.ip = "localhost"
            endpoint = "tcp://" + self.ip + ":" + str(self.port+1)
            self.sock.connect(endpoint)
            #if self.debug or self.network == "direct":
                #print ("subcriber " + endpoint +  " connect")

        else:
            msg = "NEP ERROR: mode value " +  self.mode + "is not valid"
            raise ValueError(msg)

    def __dumps(self,o, **kwargs):
        """Serialize object to JSON bytes (utf-8). See jsonapi.jsonmod.dumps for details on kwargs.

        Returns
        -------
        message : string
            Encoded string 

        """

        if 'separators' not in kwargs:
            kwargs['separators'] = (',', ':')
        
        s = simplejson.dumps(o, **kwargs)
        

        if sys.version_info[0] == 2: #Python 2
            if isinstance(s, unicode):
                s = s.encode('utf8')
        return s


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

    def listen(self,block_mode = False):
        """ Listen data from publishers
            
            Returns
            -------
            message : string or dict
                Return message, must be the same type that msg_type
        """

        if self.msg_type == "string":
            return self.listen_string(block_mode)
        elif self.msg_type == "json":
            return self.listen_json(block_mode)
        elif self.msg_type == "image":
            return self.listen_image(block_mode)
        else:
            msg = "NEP ERROR: msg_type selected '" + str(self.msg_type) + "' non compatible"
            raise ValueError(msg)

    def listen_image(self, block_mode = False):
        """ Function used to read string data from the sokect. The operation is by default in non blocking mode

            Parameters
            ----------
            block_mode : bool
                If True, the socket will set in blocking mode, otherwise the socket will be in non blocking mode
                
            Returns
            -------
            success : bool
                If True the information was obtained inside the timeline in non blocking mode  

            message : image 
                OpenCV Image.      
        """

        s, imageraw = self.listen_string(False)
        if s:
            jpg = base64.b64decode(imageraw)
            jpg = np.frombuffer(jpg, dtype=np.uint8)
            img = cv2.imdecode(jpg, 1)
            return s, img
        return s, imageraw


    def listen_string(self, block_mode = False):
        """ Function used to read string data from the sokect. The operation is by default in non blocking mode

            Parameters
            ----------
            block_mode : bool
                If True, the socket will set in blocking mode, otherwise the socket will be in non blocking mode
                
            Returns
            -------
            success : bool
                If True the information was obtained inside the timeline in non blocking mode  

            message : string 
                String obtained in the socket.      
        """

        message = ""
        try:
            #Blocking mode
            if block_mode:
                # Get the message
                if sys.version_info[0] == 2:
                    info = self.sock.recv()
                else:
                    info = self.sock.recv_string()
                # Split the message

                index = info.find(' ')
                topic = info[0:index].strip()
                message = info[index+1:]
                success = True
            #Non blocking mode
            else:
                if self.transport ==  "ZMQ":
                    if sys.version_info[0] == 2:
                        info = self.sock.recv(flags = zmq.NOBLOCK)
                    else:
                        info = self.sock.recv_string(flags = zmq.NOBLOCK)
                elif self.transport ==  "NN" or self.transport ==  "nanomsg":
                    info = self.sock.recv(flags=nanomsg.DONTWAIT)
                      
                # Split the message
                index = info.find(' ')
                topic = info[0:index].strip()
                message = info[index+1:]

                success = True
        #Exeption for non blocking mode timeout
        except zmq.Again as e:
            #Nothing to read
            success = False
            pass

        #Exeption for non blocking mode timeout
        except nanomsg.NanoMsgAPIError:
            #Nothing to read
            success = False
            pass

        return  success, message
        
    def listen_json(self, block_mode =  False):
        """ Listen for a json message. The operation is by default in non blocking mode
            
            Parameters
            ----------

            block_mode : bool
                If True, the socket will set in blocking mode, otherwise the socket will be in non blocking mode
                
            Returns
            -------

            success : bool
                If True the information was obtained inside the timeline in non blocking mode  

            info : dictionary
                Message obtained
        """
         
        success = False
        info = {}
        try:
            #Blocking mode
            if block_mode:
                if sys.version_info[0] == 2:
                    success, info = self.__deserialization(self.sock.recv())
                else:
                    success,info = self.__deserialization(self.sock.recv_string())

                #time.sleep(.001)
            #Non blocking mode
            else:
                if self.transport ==  "ZMQ":
                    if sys.version_info[0] == 2:
                        success, info = self.__deserialization(self.sock.recv(flags = zmq.NOBLOCK))
                    else:
                        success,info = self.__deserialization(self.sock.recv_string(flags = zmq.NOBLOCK))

                elif self.transport ==  "NN" or self.transport ==  "nanomsg":
                    success, info = self.__deserialization(self.sock.recv(flags=nanomsg.DONTWAIT))

                #time.sleep(.001)
        #Exeption for non blocking mode timeout
        except zmq.Again as e:
            #Nothing to read
            success = False
            pass

        #Exeption for non blocking mode timeout
        except nanomsg.NanoMsgAPIError:
            #Nothing to read
            success = False
            pass

        return  success, info


if __name__ == "__main__":
    import doctest
    doctest.testmod()
