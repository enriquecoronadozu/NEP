#!/usr/bin/env python

# ------------------------ Robot bahavior class --------------------------------
# Description: This node obtain data inertial data from a android based smarwatch
# For this it is necessary run the Nep WearAmi Smartwatch/Smartphone application
# Intructions of how to install and run this apps are in:  
# --------------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga


import nep
import sys
import zmq
import time
import signal
import socket   
import select
import Queue
import time

class smartwatch_server():

        def decode(self,line):
                """Acceleration decodification
                :param line: string with a sample of the inertial data: accelerometer or gyroscope
                :return: 
                        - success: The function return True in this parameter if the string sended has the correct format
                        - option: if option == 0 then the line contain acceleration data, if option == 1 then the line contain gyroscope data
                        - value1: x acceleration or velocity (gyroscope) component
                        - value2: y acceleration or velocity (gyroscope) component
                        - value3: z acceleration or velocity (gyroscope) component

                The format used for Nep WearAmi programs:

                - <index>;number;x_value;y_value:z_value
                
                where <index> can be "a" for (acceleration) or "y" for (gyroscope) data. 

                """
                self.delimiter = ";"
                line_list = line.split(self.delimiter)
                if(line_list[0] == 'a'):
                        if(len(line_list)==5 and line_list[4] != '' and line_list[4] != '-'):
                                x = line_list[2]
                                y = line_list[3]
                                z = line_list[4]
                                return True,0,x,y,z
                if(line_list[0] == 'y'):
                        if(len(line_list)==5 and line_list[4] != '' and line_list[4] != '-'):
                                x = line_list[2]
                                y = line_list[3]
                                z = line_list[4]
                                return True,1,x,y,z
                return False,0,0,0,0



        def run_server(self):
                """This function is used to run the server and obtain the data from the Nep WearAmi programs.
                The data is obtained from the port 8080 using a normal socket (please don't use this port in other processes to avoid errors). A client server pattern is used.
                Then the data is published using a ZeroMQ socket using publisher/subscriber pattern
                """

                signal.signal(signal.SIGINT, self.signal_handler)
                
                #A server must perform the sequence socket(), bind(), listen(), accept()
                HOST = socket.gethostname()   # Get local machine name
                PORT = 8080                # Reserve a port for your service.

                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.setblocking(0)
                t0 = time.time()
                cont = 0
                suma = 0
                prom = 0

                #Running an example several times with too small delay between executions, could lead to this error:
                #socket.error: [Errno 98] Address already in use
                # There is a socket flag to set, in order to prevent this, socket.SO_REUSEADDR:
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.bind(('', PORT))

                # Listen for incoming connections
                server.listen(5)

                # Sockets from which we expect to read
                inputs = [ server ]

                # Sockets to which we expect to write
                outputs = [ ]

                # Outgoing message queues (socket:Queue)
                message_queues = {}
                #i = 0


                print "\n"
                print("********* Smartwatch sensing node ***********")
                print("Press Ctrl+C to exit of this program")
                print("Socket get data from smartphone connected to the host:" +  str(HOST) + ", in port:" + str(PORT))
                

                #New ZQM soket to publish the datas

                
                node = nep.node("smartwatch")
                pub_config = node.config_pub()
                pub  = node.new_pub("/smart_accel", pub_config)
                
                while True:

                        # Wait for at least one of the sockets to be ready for processing
                        readable, writable, exceptional = select.select(inputs, outputs, inputs)

                        # Handle inputs
                        for s in readable:
                                if s is server:
                                    # A "readable" server socket is ready to accept a connection
                                    connection, client_address = s.accept()
                                    print >>sys.stderr, 'new connection from', client_address
                                    connection.setblocking(0)
                                    inputs.append(connection)

                                    # Give the connection a queue for data we want to send
                                    message_queues[connection] = Queue.Queue()

                                else:
                                        data = s.recv(1024)
                                        if data:
                                                # A readable client socket has data
                                                list_data = data.split("\n")
                                                #read each line
                                                for line in list_data:
                                                        condition, option, x,y,z = self.decode(line)
                                                        message = str(x) + "," + str(y) + "," + str(z)
                                                        if(condition == True and option == 0):
                                                                # Here we publish the acceleration data in the topic  "/smart_accel"
                                                                self.pub.send_string(message)
                                                        #TODO not implemented
                                                        if(condition == True and option == 1):
                                                                # Here we publish the gyroscope data in the topic  "/smart_gyro"
                                                                self.pub.send_string(message) #change topic

                                                        message_queues[s].put(data)
                                                        # Add output channel for response
                                                        if s not in outputs:
                                                            outputs.append(s)
                                                t1 = time.time()
                                                tm =  t1 - t0
                                                suma  = suma + tm
                                                cont = cont + 1
                                                if (cont == 50):
                                                        prom = suma/50
                                                        suma = 0
                                                        cont = 0
                                                        print >>sys.stderr, "freq ", 1/prom
                                                t0 = t1


                                        else:
                                                # Interpret empty result as closed connection
                                                print >>sys.stderr, 'closing', client_address, 'after reading no data'
                                                # Stop listening for input on the connection
                                                if s in outputs:
                                                    outputs.remove(s)
                                                inputs.remove(s)
                                                s.close()

                                                # Remove message queue
                                                del message_queues[s]

        def signal_handler(self, signal, frame):
                """Signal handler used to close the app"""
                print('Signal Handler, you pressed Ctrl+C!')
                print('Server will be closed')
                self.pub.close()
                time.sleep(1)
                sys.exit(0)


server = smartwatch_server()
server.run_server()







