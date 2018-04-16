import nep

node = nep.node("pubs")
conf = node.conf_sub( mode= "one2many")
sub = node.new_sub("/kinect_human", conf )
conf = node.conf_pub( mode= "many2many")
pub = node.new_pub("/human_state", conf)

print "start"
while True:
    s, msg = sub.listen_info()
    if s:
        x =  msg['shoulder_rot']

        if x > -.5 and x < .5:
           print "center"
           pub.send_info({"type_state":"hand_position", "state":"center"})
        elif x < -.5 :
           print "left"
           pub.send_info({"type_state":"hand_position", "state":"left"})
        elif x > .5:
           print "right"
           pub.send_info({"type_state":"hand_position", "state":"right"})        
