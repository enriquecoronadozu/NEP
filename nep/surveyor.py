# coding = utf-8
#!/usr/bin/env python

# ------------------------------- Server -----------------------------------
# Description: Low-level Server class
# --------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga


import time
import os
import simplejson
import sys
import nep

try:
    import nanomsg
except ImportError:
    pass

class surveyor():
    
        def __init__(self, topic, timeout = 1000, node_name = "default", debug = False):
            
            """ Nanomsg surveyor class
            
            Parameters
            ----------

            topic : string
                Surveyor topic

            timeout : int
                Maximun miliseconds waiting for response

            debug: bool
                If True some additional information of the subscriber is shown

            """
            self.topic = topic
            print("SURVEY: " + self.topic + " waiting for NEP master ...")
            self.pid = os.getpid()
            success, port, ip  = nep.masterRegister(node_name, self.topic, master_ip = '127.0.0.1', master_port = 7000, socket = "surveyor", pid = self.pid)
            print("SURVEY: " + self.topic + " socket ready")
            self.debug = debug
           


            if success:

                self.NN_installed = False
                try:
                    import nanomsg
                    self.NN_installed = True
                except ImportError:
                    print ("Nanomsg not installed")
                    self.NN_installed = False

                if self.NN_installed == False:
                    msg = "Unable to use surveyor pattern due that Nanomsg is not installed "
                    raise ValueError(msg)
                
                self.sock = nanomsg.Socket(nanomsg.SURVEYOR)
                endpoint = "tcp://" + ip + ":" + str(port)
                self.sock.bind(endpoint)
                self.sock.set_int_option(nanomsg.SURVEYOR, nanomsg.SURVEYOR_DEADLINE, timeout)
                time.sleep(1)
                if self.debug:
                    print ("surveyor started in: " + str(endpoint))

        

        def __dumps(self,o, **kwargs):
            """ Serialize object to JSON bytes (utf-8).
                
                See jsonapi.jsonmod.dumps for details on kwargs.
            """

            if 'separators' not in kwargs:
                kwargs['separators'] = (',', ':')
        
            s = simplejson.dumps(o, **kwargs)
            
            if sys.version_info[0] == 2: #Python 2
                if isinstance(s, unicode):
                    s = s.encode('utf8')
            return s

        #Status: OK
        def __serialization(self, message):
            """ Function used to serialize a python dictionary using json. 

                Parameters
                ----------
                message : dictionary
                    Python dictionary to be send
                    
                Returns
                -------
                message : string
                    Message to be send
            """
            return self.__dumps(message)
            
    

        def send_json(self, message):
            """ Function used to send a python dictionary.
                    
                Parameters
                ----------
                message : dictionary 
                    Python dictionary to be send

            """

            info = self.__serialization(message)
            self.sock.send(info)


        def __loads(self, s, **kwargs):
            """Load object from JSON bytes (utf-8).
                
            See jsonapi.jsonmod.loads for details on kwargs.
            """

            if sys.version_info[0] == 2:
                if str is unicode and isinstance(s, bytes):
                    s = s.decode('utf8')
        
            return simplejson.loads(s, **kwargs)
                

    
        #Status: OK
        def __deserialization(self, info):
            """ Deserialization string to dictionary

                Parameters
                ----------
                info : string
                        Message received 

                Returns
                -------
                msg : dictionary
                    String message as a python dictionary
            """
            try:
                json0 = info.find('{')
                topic = info[0:json0].strip()
                msg = self.__loads(info[json0:])
                success = True
            except:
                msg = ""
                success = False
            return msg

        #Status: OK
        def listen_json(self):
            """ Listen for a json message
                        
                Returns
                -------
                success: bool
                    True if a message arrives before the timeout, otherwise return false

                info : dictionary
                    Message obtained
            """
          
            while True:
                    try:
                            info = self.__deserialization(self.sock.recv())
                            return True, info

                    #Exeption for non blocking mode timeout
                    except nanomsg.NanoMsgAPIError:
                            return  False, {}

         
        
        def close(self):
            """Close socket """
            self.sock.close()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
