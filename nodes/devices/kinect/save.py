import nep
import json
    
node = nep.node("kinect_human") # Create a new node
conf = node.conf_sub() # Select the configuration of the subscriber
sub = node.new_sub("/kinect_human", conf) # Set the topic and the configuration of the subscriber

data={"ShoulderLeft":[], "ShoulderRight":[], "SpineBase":[]}

# Read the information published in the topic registered

i = 0
while i < 100:
    s, msg = sub.listen_info()
    if s:
        print msg["face_yaw"]



##
##
##with open('data.txt', 'w') as outfile:
##    json.dump(data, outfile)
##        
##
####"SpineMid"
####"SpineShoulder"
####"WristLeft"
####"WristRight"
####"ElbowLeft"
####"ElbowRight"
####"HipLeft"
####"HipRight"
####"Neck"
####"Head"
####"face_yaw"
####"face_pitch"
####"face_roll"
##

