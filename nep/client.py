# coding = utf-8
#!/usr/bin/env python

# -------------------------------- Client ---------------------------------
# Description: Low-level Client Class
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
import socket


class client:
    def __init__(self, IP, port, transport = "ZMQ", debug = True):
        """
        Creates a new client object

        Parameters
        ----------

        IP : string
            IP value of server

        port : string
            Port used to connect the socket
            
        transport : string
            Define the transport layer of the server, can be 'ZMQ' or "normal", to use ZeroMQ or TCP/IP python sockets

        debug: bool
            If True some additional information of the socket is shown

        """
        
        
        self.transport = transport
        if self.transport == "ZMQ":
            context = zmq.Context()
            # Define the socket using the "Context"
            self.sock = context.socket(zmq.REQ)
            self.sock.connect("tcp://" + IP + ":" + str(port))
            if debug:
                print ("CLIENT: connected in " + IP + ":" + str(port))

        elif transport == "normal":

            # Normal sockets
            print ("CLIENT: POSIX server in " + IP + ":" + str(port))
            try:
                #create an AF_INET, STREAM socket (TCP)
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error:
                print ('CLIENT: Failed creating socket')
                sys.exit()

            try:
                if IP == "localhost":
                #Same computer
                        IP = socket.gethostbyname( IP )
                        print ("CLIENT: local host in :", IP)
                
            except socket.gaierror:
                #could not resolve
                print ('Hostname could not be resolved. Exiting')
                sys.exit()
            #Connect to remote server
            max_v = 10
            i = 0
            connect=False
            while not connect:
                try: 
                    self.s.connect((IP , int(port)))
                    connect = True
                except:
                    print ("NEP WARNING: Server not found intent:" + str(i) + ", max = 10")
                    time.sleep(2)
                    i = i + 1
                    if i > max_v-1:
                        print ("NEP WARNING: Server not found after max number of intents")
                        time.sleep(4)
                        sys.exit()
            
            print ("CLIENT: connected in " + IP + ":" + str(port))



    def __loads(self, s, **kwargs):
        """Load object from JSON bytes (utf-8). See jsonapi.jsonmod.loads for details on kwargs.
        """
        
        if sys.version_info[0] == 2:
            if str is unicode and isinstance(s, bytes):
                s = s.decode('utf8')
        
        return simplejson.loads(s, **kwargs)

    
    #Status: OK
    def __deserialization(self, info):
        """ 
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
            msg = self.__loads(info)
        except:
            msg = ""
        return msg

    def __dumps(self,o, **kwargs):
        """ JSON deserialization function  (string to dictionary)
            
            Parameters
            ----------
            info : string
                Message received by the ZQM socket 

            Returns
            -------
            info : dictionary
                Message as python dictionary
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



    def listen_info(self):
        """ Listen for a json message
                        
            Returns
            -------

            response : dictionary or string
                Message obtained
        """
        
        if self.transport == "ZMQ":
            #response = self.sock.recv_json()
            #return response
            response = self.sock.recv()
            return self.__deserialization(response)
            
        else:
          response = self.s.recv(1024)
          return response
            

    def send_info(self,request):
        
        """ Function used to send client request as a python dictionary  (if transport == "ZMQ") or as string (if transport == "normal")
            
            Parameters
            ----------

            request : dictionary or string
                    Python dictionary (ZMQ) or string (Python sockets) to be send

        """

        if self.transport == "ZMQ":
            #self.sock.send_json(request)
            if sys.version_info[0] == 2:
                self.sock.send(self.__serialization(request))
            else:
                self.sock.send_string(self.__serialization(request))

        else:
            try:
                self.s.sendall(request)
            except:
                print ("ERROR: for normal socket messages must be string not dictionaries")
                sys.exit()

if __name__ == "__main__":
    import doctest
    doctest.testmod()