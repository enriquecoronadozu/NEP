# coding = utf-8
#!/usr/bin/env python

# ------------------------------ Publisher ---------------------------------
# Description: Low-level Publisher Class
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
    import nanomsg
except ImportError:
    pass
    
try:
    import cv2
except ImportError:
    pass



class publisher:
    """ Publisher class used for inter-process comunication between nodes. Supports ZeroMQ, nanomsg and ROS publishers. 
        
        Parameters
        ----------

        topic : string 
            Topic name to publish the messages

        node : string or ROS node
            Name of the node or ROS 2.0 instance

        msg_type : string
            Message type: "string", "json" for ZMQ and nanomsg, some ROS geometry messages are also supported 

        conf : dictionary 
            Configuration of the publisher.

        debug: bool
            If True some additional information of the publisher is shown

    """

    def __init__(self, topic, node = "default", msg_type = "json", conf =  {'transport': "ZMQ", 'network': "broker", 'mode':"many2many", "master_ip":"127.0.01"}, debug = False):

        self.conf = conf
        self.network = self.conf['network']
        self.transport =  self.conf['transport']
        self.node = node
        self.topic = topic
        self.msg_type =  msg_type
        self.ip = ""
        self.port = ""
        self.connected = False
        self.debug = debug
        self.master_ip = "127.0.0.1"

        try:
            self.master_ip = conf["master_ip"]
            if self.master_ip == "127.0.0.1":
                print ("PUB: " + topic + " in local-host")
            else:
                print ("PUB: " + topic + " in " +  str(self.master_ip))
        except:
            pass

        if self.transport ==  "ROS":                                                    #Use ROS
            print ("PUB: " + self.topic + " using ROS 1.0")
            self.__create_ROS_publisher()

        elif self.transport ==  "ROS2":                                                   #Use ROS 2.0
            print ("PUB: " + self.topic + " using  ROS 2.0")
            self.__create_ROS2_publisher()

        elif self.transport ==  "ZMQ":                                                  #Use ZeroMQ
            print ("PUB: " + self.topic + " using ZMQ " + self.network)
            #many2many is the default value
            self.mode = "many2many"                                                     
            if "mode" in self.conf:
                self.mode = self.conf['mode']
            # Create a ZMQ socket
            self.__create_ZMQ_publisher()

        elif self.transport ==  "NN" or self.transport == "nanomsg":                    #Use nanomsg
            
            print ("PUB: " + self.topic + " nanomsg " + self.network)
            #many2many is the default value
            self.mode = "many2many" 
            if "mode" in self.conf:
                self.mode = self.conf['mode']
            self.__create_NN_publisher()
        else:
            msg = "NEP ERROR: Transport parameter " + self.transport + "is not supported, use instead 'ROS', 'ROS2', 'ZMQ' or 'nanomsg' "
            raise ValueError(msg)

    def __create_ROS2_publisher(self):

        from std_msgs.msg import String
        self.ros_pub = self.node.create_publisher(String, self.topic)
        self.connected = True



    #TODO:also define queue_size
    def __create_ROS_publisher(self):
        """Function used to create a ROS publisher"""
        import rospy
        
        from std_msgs.msg import String
        self.ros_pub = rospy.Publisher(self.topic, String, queue_size=10)

        rospy.init_node(self.node, anonymous = True)
        self.connected = True
        
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
        port = "8000"
        self.pid = os.getpid()
        if self.network == "direct":
            # Set the port and ip selected by the user
            port = self.conf["port"]
            ip = self.conf['ip']
            success =  True
        elif self.network == "broker":
            if self.topic != "/nep_node":
                print("PUB: " + self.topic + " waiting NEP master ...")
            # Register the topic in the NEP Master and get the port and ip
            success, port, ip  = nep.masterRegister(self.node, self.topic, master_ip = self.master_ip, master_port = 7000, socket = "publisher", mode = self.mode, pid = self.pid, data_type = self.msg_type)
            if self.topic != "/nep_node":
                print("PUB: " + self.topic + " socket ready")
                
        return success, port, ip

    def __create_ZMQ_publisher(self):
        """Function used to create a ZeroMQ publisher"""

        success, self.port, self.ip = self.__network_selection()
        if success:    
            # Create a new ZeroMQ context and a publisher socket
            try:
                context = zmq.Context()
                # Define the socket using the "Context"
                self.sock = context.socket(zmq.PUB)
                #Set the topic of the publisher and the end_point
                self.__connect_ZMQ_socket()
                self.connected = True
            except:
                print ("NEP ERROR: socket already in use")
            
            time.sleep(1)
            #This delay in important, whithout them the comunication is not effective
 
            # ZeroMQ note:
            # There is one more important thing to know about PUB-SUB sockets: 
            # you do not know precisely when a subscriber starts to get messages.
            # Even if you start a subscriber, wait a while, and then start the publisher, 
            # the subscriber will always miss the first messages that the publisher sends. 


            # In Chapter 2 - Sockets and Patterns we'll explain how to synchronize a 
            # publisher and subscribers so that you don't start to publish data until 
            # the subscribers really are connected and ready. There is a simple and 
            # stupid way to delay the publisher, which is to sleep. Don't do this in a
            #  real application, though, because it is extremely fragile as well as
            #  inelegant and slow. Use sleeps to prove to yourself what's happening, 
            # and then wait for 
            # Chapter 2 - Sockets and Patterns to see how to do this right

    def __create_NN_publisher(self):
        """Function used to create a Nanomsg publisher"""
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
                    self.sock = nanomsg.Socket(nanomsg.PUB)
                    self.__connect_NN_socket()
                    self.connected = True
                    time.sleep(1)
                except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
          

    def __connect_ZMQ_socket(self):
        """ Connect ZMQ socket in base it configuration
        """
        endpoint = "tcp://" + self.ip + ":" + str(self.port)
        if self.mode == "one2many":
        # This allows only use one publisher connected at the same endpoint
            self.sock.bind(endpoint)
            if self.debug or self.network == "direct":
                if not self.topic == "/nep_node":
                    print("PUB: " + self.topic + " endpoint: " + endpoint +  " bind")
        elif self.mode == "many2one":
            # This allows two use more that one publisher ate the same endpoint
            self.sock.connect(endpoint)
            if self.debug or self.network == "direct":
                if not self.topic == "/nep_node":
                    print("PUB: " + self.topic + " endpoint: " + endpoint +  " connect")
        elif  self.mode == "many2many":
            self.sock.connect(endpoint)
            if self.debug or self.network == "direct":
                print("PUB: " + self.topic + " endpoint: " + endpoint +  " connect")

    def __connect_NN_socket(self):
        """ Connect Nanomsg socket in base it configuration
        """
        if self.mode == "one2many":
            # This allows only use one publisher connected at the same endpoint
            if self.ip == '127.0.0.1':
                ip = "*"
            endpoint = "tcp://" + ip + ":" + str(self.port)
            self.sock.bind(endpoint)
            #if self.debug or self.network == "direct":
                #print ("publisher " + endpoint +  " bind")
        
        elif self.mode == "many2one":
            # This allows two use more that one publisher ate the same endpoint
            if self.ip == '127.0.0.1':
                ip = "localhost"
            endpoint = "tcp://" + ip + ":" + str(self.port)
            self.sock.connect(endpoint)
            #if self.debug or self.network == "direct":
                #print ("publisher " + endpoint +  " connect")
            
        elif  self.mode == "many2many":
            if self.ip == '127.0.0.1':
                ip = "localhost"
            endpoint = "tcp://" + ip + ":" + str(self.port)
            self.sock.connect(endpoint)
            #if self.debug or self.network == "direct":
                #print ("publisher " + endpoint +  " connect")
              
        

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


    def __serialization(self, message):
        """ Function used to serialize a python dictionary using json. In this function the message to be send is attached to the topic. 
            
            Parameters
            ----------
            message : dictionary
                Python dictionary to be send
            
            Returns
            -------
            message : string
                Message to be send: topic + message 
        """
        return self.topic + ' ' + self.__dumps(message)
            
    def publish(self, message):
        """ Send message to subscribers

        Parameters
        ----------
        message : obj 
            Message to be send, must have the same type that msg_type 

        """

        if self.msg_type == "string":
            self.send_string(message)
        elif self.msg_type == "json":
            self.send_json(message)
        elif self.msg_type == "image":
            self.send_image(message)
        else:
            msg = "NEP ERROR: msg_type selected '" + str(self.msg_type) + "' non compatible"
            raise ValueError(msg)

    def send_image(self,message):
        """ Publish a opencv image. 
            
            Parameters
            ----------
            message : image 
                Image to be sended 
        """

        ret, jpg = cv2.imencode('.jpg', message)
        encoded = base64.b64encode(jpg.tostring())
        if sys.version_info[0] == 2:
            self.sock.send(self.topic + ' ' + str(encoded))
        else:
            self.sock.send_string(self.topic + ' ' + encoded.decode("utf-8"))
            

        
    
    def send_string(self,message):
        """ Publish a string value. 
            
            Parameters
            ----------
            message : string 
                String to be sended 
        """
        if self.connected:

            if self.transport ==  "ZMQ":
                self.sock.send_string(self.topic + ' ' + message)
            
            elif self.transport ==  "NN" or self.transport ==  "nanomsg":
                self.sock.send(self.topic + ' ' + message)

            elif self.transport == "ROS":
                self.ros_pub.publish(message)

            elif self.transport == "ROS2":

                from std_msgs.msg import String
                msg = String()
                msg.data = message
                self.ros_pub.publish(msg)

        else:
            print ("NEP ERROR: socket already in use, message not sent")


    def send_json(self, message):
        """ Function used to publish a python dictionary. The message is serialized using json format and then published by the socket
            
            Parameters
            ----------
            message : dictionary 
                Python dictionary to be send

        """
        if self.connected:

            if self.transport ==  "ZMQ" or self.transport ==  "NN" or self.transport ==  "nanomsg":
                
                info = self.__serialization(message)

                if sys.version_info[0] == 2: #Python 2
                    self.sock.send(info)
                else: # Python 3
                    self.sock.send_string(info)

            elif self.transport == "ROS":
                message = self.__dumps(message)
                self.ros_pub.publish(message)

            elif self.transport == "ROS2":
                message = self.__dumps(message)
                from std_msgs.msg import String
                msg = String()
                msg.data = message
                self.ros_pub.publish(msg)

        else:
            print ("NEP ERROR: socket already in use, message not sent")
        

if __name__ == "__main__":
    import doctest
    doctest.testmod()
