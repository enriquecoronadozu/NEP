# coding = utf-8
#!/usr/bin/env python

# ------------------------------- Master -----------------------------------
# Description: Low-level Master class
# --------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga


import zmq
import time
import nep
import sys, os
import signal


if sys.version_info[0] == 3:
    import _thread as thread
else:
    import thread
    
# ---------------------------------- Static ports ------------------------------------ :
# master port 7000

# ----------------------------------- Topic format ----------------------------------- :
# topic_name: [port,mode,ip] 

class master:

    def __signal_handler(self, signal, frame):
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
            print (pid)
            import subprocess as s
            s.Popen('taskkill /F /PID {0}'.format(pid), shell=True)
            sys.exit(0)

    
    def __init__(self, IP = '127.0.0.1' , port = 7000, initial_port_number = 9000):

        """
        Creates a new master object for service discovery

        Parameters
        ----------

        IP : string
            IP value of server

        port : int
            Port used to connect the socket
            
        initial_port_number : int
            Port numbers will be registered starting from the value of this parameter

        """

        # Start master server
        try:
            self.nodes_register = {}
            self.server = nep.server(IP,port)
            self.IP = IP
            self.initial_port_number = initial_port_number

            # Ports configuration
            self.current_port = initial_port_number
            self.topic_register = {}
            self.threads_id = []
            self.brokers = []
            msg_type = "json"         # Message type to listen. "string" or "dict"
            node = nep.node("master_node")                                                                   # Create a new node
            pub_port = 7777
            conf = node.direct(ip = IP, port =  pub_port, mode ="one2many")                # Select the configuration of the publisher
            self.master_pub = node.new_pub("master",msg_type,conf)
            time.sleep(1)
            self.master_pub.publish(self.topic_register)
        except Exception as e:
            print("MASTER ALREADY OPEN")
            sys.exit(0)

    def __onNewTopic(self,node_request):
        """
        Register and return connection parameters for requested topics

        Parameters
        ----------

        node_request : dictionary
            Request parameters of the topic. This parameters are: topic (i.e the topic name), node (i.e. name of the module), socket (e.g. publisher, subscriber, server, client, surveyor, ...) and mode (only for publish and subscriber and can be many2one, one2many and many2many). 
        """

        topic = str(node_request['topic'])

        if node_request["socket"] == "publisher" or node_request["socket"] == "subscriber":
            if node_request["mode"] == "many2many":
                
                try:
                    proxy = nep.broker(self.IP, self.current_port+1, self.current_port)
                except:
                    print("NEP ERROR: ports " + str(self.current_port) + " and " + str(self.current_port+1) + " not avaliable")
                    print("NEP MESSAGE: Trying with: " + str(self.current_port+2) + " and " + str(self.current_port+3))
                    ti = 0
                    while ti < 10:
                        self.current_port = self.current_port + 2
                        try:
                            proxy = nep.broker(self.IP, self.current_port+1, self.current_port)
                            ports_ok = True
                            break
                        except:
                            print("NEP ERROR: ports" + str(self.current_port) + " and " + str(self.current_port+1) + " not avaliable ----")
                        ti = ti+2
                        
                        
                        
                    
                self.brokers.append(proxy)
                th = thread.start_new_thread (proxy.start, ())
                self.threads_id.append(th)
                time.sleep(.5)
            if "msg_type" in node_request:
                self.topic_register.update({topic:{"port":self.current_port,"socket":node_request["socket"], 'ip': self.IP, "mode":node_request["mode"], "msg_type":node_request["msg_type"] }})
            else:
                 self.topic_register.update({topic:{"port":self.current_port,"socket":node_request["socket"], 'ip': self.IP, "mode":node_request["mode"], "msg_type":"json" }})

            msg = {'topic':topic, 'port': self.current_port, 'mode':node_request["mode"],  'ip': self.IP, 'socket':node_request["socket"], "state":"success"}

        elif node_request["socket"] == "surveyor" or node_request["socket"] == "respondent":
            self.topic_register.update({topic:{"port":self.current_port,"socket":node_request["socket"], 'ip': self.IP}})
            msg = {'topic':topic, 'port': self.current_port,  'ip': self.IP, 'socket':node_request["socket"], "state":"success"}
            pass

        elif node_request["socket"] == "client" or node_request["socket"] == "server":
            self.topic_register.update({topic:{"port":self.current_port,"socket":node_request["socket"]}, 'ip': self.IP})
            msg = {'topic':topic, 'port': self.current_port,  'ip': self.IP, 'socket':node_request["socket"],"state":"success"}
            pass
        
        self.server.send_info(msg)
        self.topic_register[topic]["nodes"] = {node_request['node']:{'socket':node_request["socket"], 'pid':"n.a.",'ip': self.IP}}
        
        if "pid" in node_request:
            self.topic_register[topic]["nodes"][node_request['node']] = {'socket':node_request["socket"], 'pid':node_request["pid"], 'ip': self.IP}
            #data = {node_request['node']:{'socket':node_request["socket"], 'pid':node_request["pid"]}}
            #data =  {'node':node_request['node'],'socket':node_request["socket"], 'pid':node_request["pid"]}
        else:
            self.topic_register[topic]["nodes"][node_request['node']] = {'socket':node_request["socket"], 'pid':"n.a."}
            #data = {node_request['node']:{'socket':node_request["socket"], 'pid':"n.a."}}
            #data =  {'node':node_request['node'],'socket':node_request["socket"], 'pid':"n.a."} 
        #self.topic_register[topic]["nodes"][node_request['node']] = {'socket':node_request["socket"], 'pid':node_request["pid"]}}
        #self.topic_register[topic]["nodes"].append(data)
        self.current_port = self.current_port + 2
        self.master_pub.publish(self.topic_register)
        #print (self.topic_register)

    def __onRegisteredTopic(self,topic, node_request):
        """ 
        Send topic info to the node

        Parameters
        ----------

        topic : string
            Topic name

        node_request : dictionary
            Request parameters of the topic. This parameters are: topic (i.e the topic name), node (i.e. name of the module), socket (e.g. publisher, subscriber, server, client, surveyor, ...) and mode (only for publish and subscriber and can be many2one, one2many and many2many). 
        
        """
        
        try:
            port = self.topic_register[topic]["port"]
            socket_= self.topic_register[topic]["socket"]

            if "mode" in self.topic_register[topic]:
                mode = self.topic_register[topic]["mode"]
                msg = {'topic':topic, 'port': port, 'mode':mode, 'ip': self.IP, 'socket':socket_ , "state":"success"}
            else:
                msg = {'topic':topic, 'port': port, 'ip': self.IP, 'socket':socket_, "state":"success"}

            self.server.send_info(msg)

            if "pid" in node_request:
                self.topic_register[topic]["nodes"][node_request['node']] = {'socket':node_request["socket"], 'pid':node_request["pid"], 'ip': self.IP}
            else:
                self.topic_register[topic]["nodes"][node_request['node']] = {'socket':node_request["socket"], 'pid':"n.a", 'ip': self.IP}

            self.master_pub.publish(self.topic_register)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print ("Error in topic request")
        
        #print (self.topic_register)

    def __stop(self):
        for key, value in self.topic_register.iteritems():
            nodes = value["nodes"]
            for node in nodes:

                if not os.environ.get('OS','') == 'Windows_NT': # Windows
                    os.system('kill %d' % node["pid"])

                else:
                    """Signal handler used to close when user press Ctrl+C"""
                    import subprocess as s
                    s.Popen('taskkill /F /PID {0}'.format(node["pid"]), shell=True)
    
    def stopNode(self, node):


            print ("Kill")
            print (node)
            if not os.environ.get('OS','') == 'Windows_NT': # Windows
                os.system('kill %d' % node["pid"])

            else:
                import subprocess as s
                s.Popen('taskkill /F /PID {0}'.format(node["pid"]), shell=True)

            if node['kill'] in self.nodes_register:
                self.nodes_register.pop(node['kill'], None)

                for topics in self.topic_register:
                    self.topic_register[topics]["nodes"].pop(node['kill'], None)




    def run(self):
            """ Run master node until Ctrl+C is pressed
            """
            # Enable to kill the node using Ctrl + C
            signal.signal(signal.SIGINT, self.__signal_handler)


            while True:
                time.sleep(.01)
                node_request = self.server.listen_info()
                print ("Request: " + str(node_request))
                if 'node' in node_request:
                    if node_request['node'] in self.nodes_register:
                        current_pid = self.nodes_register[node_request['node']]
                        if node_request['pid'] == current_pid:
                            pass
                        else:
                            try:

                                print ("kill: " + str(current_pid))
                                os.kill(current_pid, signal.SIGTERM)
                                time.sleep(1)


                            except:
                                pass
                    
                    self.nodes_register[node_request['node']] = node_request['pid']

                    topic = str(node_request['topic'])
                    current_pid = node_request['pid']
                    
                    if topic in self.topic_register:
                        self.__onRegisteredTopic(topic, node_request)
                    else:
                        self.__onNewTopic(node_request)
                        

                # Get avaliable topic list
                elif 'topic_list' in node_request: 
                    msg = self.topic_register
                    self.server.send_info(msg)

                elif 'master' in node_request: 
                    action = node_request["master"]
                    if action == "node_kill":
                        self.stopNode(node_request)
                        self.server.send_info({"node":"close_node", "status":"success"})

                    elif action == "kill_all":
                        pass
                        
                    
                    else:
                        self.server.send_info({"node":"action", "status":"failure"})

                else:
                    self.server.send_info({"node":"action", "status":"failure"})


                    #action = node_request["master"]
                    #if action == "stop":
                    #    print ("Master stoping ...")
                    #    time.sleep(1)
                    #    for p in self.brokers:
                    #        p.stop()
                    #    self.server.send_info({"node":"stop", "status":"success"})
                    #    break
                    #elif action == "clean":
                    #    print ("Clean master")
                    #    
                    #    for p in self.brokers:
                    #        self.current_port = self.initial_port_number
                    #        p.stop()


                    #    self.__stop()
                    #    self.topic_register = {}

                        
                    #    self.server.send_info({"node":"clean", "status":"success"})
                    #else:
                    #    self.server.send_info({"node":action, "status":"failure"})
                
                print (self.topic_register)
                print (self.nodes_register)

                        
if __name__ == "__main__":
    import doctest
    doctest.testmod()
