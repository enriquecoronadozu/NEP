#%%
import zmq
import time


class master:

    
    def __init__(self, IP = '127.0.0.1' , port = 7000):
        context = zmq.Context()
        self.sock = context.socket(zmq.REP)
        self.sock.bind("tcp://" + IP + ":" + str(port))

        # Ports configuration
        self.current_port = 9000
        self.topic_register = {}

    def run(self):
        while True:
            time.sleep(.01)
            node_request = self.sock.recv_json()
            print ("Request: " + str(node_request))
            if 'topic' in node_request:
                topic = str(node_request['topic'])
                if topic in self.topic_register:
                    print ("Topic already register")
                    port = self.topic_register[topic]
                    msg = {'topic':topic, 'port': port}
                    self.sock.send_json(msg)
                    print self.topic_register
                else:
                    print ("New topic register")
                    self.topic_register.update({topic:self.current_port})
                    msg = {'topic':topic, 'port': self.current_port}
                    self.sock.send_json(msg)
                    self.current_port = self.current_port + 1
                    print self.topic_register


server = master()      
server.run()
    
