import nep
import time

node = nep.node("subscriber_node") # Create a new node
conf = node.conf_sub() # Select the configuration of the subscriber
conf = {'msg_type':"dict", 'transport':"ZMQ" , 'network':"P2P", 'port': "9000", 'ip': "127.0.0.1", 'mode': "many2many" }
sub_emotion = node.new_sub("/robot_emotion", conf) # Set the topic and the configuration of the subscriber
import threading

def updateEmotion(r):
        r.do_parallel_actions(["wake_up","none"], {},["nao"])
        while True:
                if emotion == "neutral":
                        r.do_parallel_actions(["animation","em_neutral"], {},["nao"])
                        time.sleep(5)
                elif emotion == "happy":
                        r.do_parallel_actions(["animation","em_happy"], {},["nao"])
                        time.sleep(5)
                elif emotion == "angry":
                        r.do_parallel_actions(["animation","em_angry"], {},["nao"])
                        time.sleep(5)
                elif emotion == "sad":
                        r.do_parallel_actions(["animation","em_sad"], {},["nao"])
                        time.sleep(5)
                elif emotion == "protected":
                        r.do_parallel_actions(["animation","em_protected"], {},["nao"])
                        time.sleep(5)

r  = nep.interaction()
emotion = "neutral"
emo = threading.Thread(target = updateEmotion, args = (r,))
# Used to finish the background thread when the main thread finish
emo.daemon = True
# Start new thread 
emo.start()

while True:
        s, data = sub_emotion.listen_info(True)
        print data
        if s == True:
                emotion = data["emotion"]
                print emotion
        
