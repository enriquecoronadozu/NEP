import nep
import time

node = nep.node("pubs")
conf = node.conf_sub( mode= "one2many")
sub = node.new_sub("/kinect_human", conf )
conf = node.conf_pub( mode= "many2many")
pub = node.new_pub("/human_state", conf)

print "start"

start = time.time()
 
while True:
    s, msg = sub.listen_info()
    if s:
        x =  msg['Head'][2]
        start = time.time()
        print x

        if x > 1.5:
           print "human"
           pub.send_info({"type_state":"human_presence", "state":"human"})
           pub.send_info({"type_state":"human_close", "state":"no"})
        elif x < 1.5 :
           pub.send_info({"type_state":"human_presence", "state":"human"})
           pub.send_info({"type_state":"human_close", "state":"yes"})


    end = time.time()
    elapsed = end - start
    if (elapsed > 2): #
         start = time.time()
         pub.send_info({"type_state":"human_presence", "state":"no_human"})
         pub.send_info({"type_state":"human_close", "state":"no"})

            
