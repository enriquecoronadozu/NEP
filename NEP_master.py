#%%
import zmq
import time
import nep
import thread


class master:
    
    def __init__(self, IP = '127.0.0.1' , port = 7000, initial_port_number = 9000):

        # Start master server
        self.s = nep.server(IP,port)

        # Ports configuration
        self.current_port = initial_port_number
        self.topic_register = {}

    def onMany2Many(self,port):
        """
        Cretates a  many 2 many XPUB/XSUB broker in a new thread

        Parameters
        ----------

        port : int
            Number of the port to set the broker. Ther brokers is made using port and port + 1. Therefore use only pairs or only odd numbers in this parameter
            
        """
        b = nep.broker('127.0.0.1', port+1, port)

    def run(self):
        
        while True:
            time.sleep(.01)
            node_request = self.s.listen_info()
            
            print ("Request: " + str(node_request))

            if 'topic' in node_request:
                topic = str(node_request['topic'])
                
                if topic in self.topic_register:
                    print ("Topic already register")
                    port = self.topic_register[topic]
                    msg = {'topic':topic, 'port': port}
                    self.s.send_info(msg)
                    print self.topic_register
                    
                else:

                    if node_request["mode"] == "many2many":
                        thread.start_new_thread ( self.onMany2Many, (self.current_port,)) 
                        time.sleep(.5)
                    print ("New topic register")
                    self.topic_register.update({topic:self.current_port})
                    msg = {'topic':topic, 'port': self.current_port}
                    self.s.send_info(msg)
                    self.current_port = self.current_port + 2
                    print self.topic_register


server = master()      
server.run()
    
