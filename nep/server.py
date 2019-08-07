# coding = utf-8
#!/usr/bin/env python

# ------------------------------- Server -----------------------------------
# Description: Low-level Server Class
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

class server:
    def __init__(self, IP, port, transport = "ZMQ", debug = True):
        """
        Creates a new server object

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
        self.connected = False

        if transport == "ZMQ":

            # ZMQ sockets
            context = zmq.Context()
                
            try:
                # Define the socket using the "Context"
                self.sock = context.socket(zmq.REP)
                self.sock.bind("tcp://" + IP + ":" + str(port))
                self.connected = True
                if debug:
                    print ("SERVER: ZMQ server in " + IP + ":" + str(port))
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print ('NEP ERROR: Failed in creating socket, already in use')
                self.sock.close()
                context.destroy()
                self.connected = False

        
        elif transport == "normal": 
            # Normal sockets
            try:
                #create an AF_INET, STREAM socket (TCP)
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #self.s.setblocking(0)
                self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            except:
                print ('NEP ERROR: Failed in creating socket, already in use')
                time.sleep(3)
                sys.exit()

            try:
                if IP == "localhost":
                #Same computer
                        IP = socket.gethostbyname( IP )
                        print ("local host in :", IP)
                
            except socket.gaierror:
                #could not resolve
                print ('Hostname could not be resolved. Exiting')
                sys.exit()
            #Connect to remote server
            self.s.bind(('' , int(port)))
            self.s.listen(5)
            print ("SERVER: POSIX server in " + IP + ":" + str(port))
            print ("SERVER: Waiting for connection")
            self.connection, client_address = self.s.accept()
            print ("SERVER: Connection ready")
            self.connected = True

    def __loads(self, s, **kwargs):
        """Load object from JSON bytes (utf-8). See jsonapi.jsonmod.loads for details on kwargs.
        """

        if sys.version_info[0] == 2:
            if str is unicode and isinstance(s, bytes):
                s = s.decode('utf8')
        
        return simplejson.loads(s, **kwargs)

    
    #Status: OK
    def __deserialization(self, info):
        """ JSON deserialization function  (string to dictionary)
            
            Parameters
            ----------
            info : string
                topic + message received by the ZQM socket 

            Returns
            -------
            info : dictionary
                Message as python dictionary
        """
        try:
            msg = self.__loads(info)
            success = True
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print ("NEP ERROR: msg in not a json value")
            msg = {}
            success = False
        return msg

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

            request : dictionary or string
                Message obtained
        """

        if self.transport == "ZMQ" and self.connected:
            #response = self.sock.recv_json()
            #return response
            request = self.sock.recv()
            return self.__deserialization(request)
            
        elif self.connected:
            # Wait for a connection
            try:
                request = self.connection.recv(16)
                return request
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print ("NEP WARNING: client connection lost, waiting for new client")
                self.connection.close()
                self.connection, client_address = self.s.accept()
                request = self.connection.recv(16)
                return request
        else:
            print ("NEP ERROR: socket in use, unable to read")
            if self.transport == "ZMQ":
                return {}
            else:
                return ""

    def send_info(self,response):
        """ Function used to send client response as a python dictionary  (if transport == "ZMQ") or as string (if transport == "normal")
            
            Parameters
            ----------

            response : dictionary or string
                    Python dictionary (ZMQ) or string (Python sockets) to be send

        """
        if self.connected:
            if self.transport == "ZMQ":
                #self.sock.send_json(response)
                if sys.version_info[0] == 2:
                    self.sock.send(self.__serialization(response))
                else:
                    self.sock.send_string(self.__serialization(response))
            else:
                try:
                    self.connection.sendall(response)
                
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print ("NEP WARNING: client connection lost, waiting for new client")
        else:
            print ("NEP ERROR: socket in use, data not sent")
            time.sleep(2)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
