# coding = utf-8
#!/usr/bin/env python

# ------------------------------- Respondent -------------------------------
# Description: Low-level Responsent class
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

class respondent():
        
        def __init__(self, topic, node_name = "default", debug = False):
            
            """ Nanomsg surveyor class
            
            Parameters
            ----------

            topic : string
                Topic to exchange info

            debug: bool
                If True some additional information of the subscriber is shown

            """
            self.topic = topic
            print("RESP: " + self.topic + " waiting for NEP master ...")

            self.pid = os.getpid()
            success, port, ip  = nep.masterRegister(node_name, self.topic, master_ip = '127.0.0.1', master_port = 7000, socket = "respondent", pid = self.pid, data_type = "json")
            print("RESP: " + self.topic + " socket ready")
            self.debug = debug
           
            if success:

                self.NN_installed = False
                try:
                    import nanomsg
                    self.NN_installed = True
                except ImportError:
                    print ("NEP ERROR: Nanomsg not installed")
                    self.NN_installed = False

                if self.NN_installed == False:
                    msg = "Unable to use surveyor pattern due that Nanomsg is not installed "
                    raise ValueError(msg)

                
                self.sock = nanomsg.Socket(nanomsg.RESPONDENT)
                endpoint = "tcp://" + ip + ":" + str(port)
                self.sock.connect(endpoint)
                time.sleep(1)
                if self.debug:
                    print ("respondednt started in: " + str(endpoint))
        
              
        def __dumps(self,o, **kwargs):
            """Serialize object to JSON bytes (utf-8).
                
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
                    Message to be send, topic + message 
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
            """Load object from JSON bytes (utf-8). See jsonapi.jsonmod.loads for details on kwargs.
            """

            if sys.version_info[0] == 2:
                if str is unicode and isinstance(s, bytes):
                    s = s.decode('utf8')
        
            return simplejson.loads(s, **kwargs)


    
        #Status: OK
        def __deserialization(self, info):
            """ JSON deserialization function
                    
                Parameters
                ----------
                info : string
                    message received

                Returns
                -------
                info : dictionary
                    Message as python dictionary
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
        def listen_json(self, block_mode = False):
            """ Listen for a json message
                        
                Returns
                -------

                info : dictionary
                    Message obtained
            """
          
            if block_mode:#TODO, change s, data= ....
                info = self.__deserialization(self.sock.recv())
                return  True, info
            else:
                try:
                     info = self.__deserialization(self.sock.recv(flags=nanomsg.DONTWAIT))
                     return True, info
                except nanomsg.NanoMsgAPIError:
                    return  False, {}


         
        
        def close(self):
            """Close socket """
            self.sock.close()
                

if __name__ == "__main__":
    import doctest
    doctest.testmod()
