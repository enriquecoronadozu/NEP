
# Here we add the leap motion libraries
import Leap, sys, time
import nep
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

# This library allows to create new thread (to do parallel tasks)
import threading

# -------- Here we start the communication with other nodes --------------

# Here we define a the name of the node
node = nep.node("leap_motion")
# Here we define the setting of the socket
conf = node.conf_sub( mode= "many2many")
# Here we define a new publisher with the topic "/leap_motion"
pub = node.new_pub("/leap_motion",conf)


#--------- Global variable that define the hand parameters -------------

#Hand id
left_id = 0
rigth_id = 0

#Palm position
leap_state_left = {"Palm Position": [0,0,0]}
leap_state_right = {"Palm Position": [0,0,0]}

        
# ------------------ Leap motion class ---------------------------
#Leap motion class used to connect, get frames, disconect the device
class LeapMotionListener(Leap.Listener):
    finger_names = ["Thumb","Index","Middle","Ring","Pinky"]
    bone_names = ["Metacarpal","Proximal","Intermediate","Distal"]
    state_names = ["STAE_INVALID","STATE_START", "STATE_UPDATE", "STATE_END"]

    def on_init(self, controller):
        print"Initialized"
    def on_connect(self, controller):
        print"Motion Sensor Connected!"

        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        print"Motion Sensor Disconnected!"
    def on_exit(self, controller):
        print"Exitted"

    # This is the important one.
    # This function is executed each time anew frame arrives
    def on_frame(self, controller):
        frame = controller.frame()
        
        global left_id, rigth_id
        for hand in frame.hands:
            
            normal = hand.palm_normal
            direction = hand.direction            
            arm = hand.arm
            elbow_dir = arm.elbow_position
            wrist = hand.wrist_position


            # Set the id for each hand
            if hand.is_left:
                left_id = hand.id
            elif hand.is_right:
                right_id = hand.id

            #Set palm position of left hand
            if left_id == hand.id:
                leap_state_left["Palm Position"] = [hand.palm_position.x,hand.palm_position.y,hand.palm_position.z]
            #Set palm position of rigth hand
            elif right_id == hand.id:
                leap_state_right["Palm Position"] = [hand.palm_position.x,hand.palm_position.y,hand.palm_position.z]
 
                                                                 
            for finger in hand.fingers:
                  
                FingerDir = finger.direction
                StabPos = finger.stabilized_tip_position
                angle_yaw = direction.angle_to(Leap.Vector.x_axis)
                angle_roll = normal.angle_to(Leap.Vector.x_axis)
                elbow_pitch = elbow_dir.angle_to(Leap.Vector.z_axis)
                elbow_roll = elbow_dir.angle_to(Leap.Vector.y_axis)

                #if hand.is_left: #Here we save the right hand info
                    #leap_state_right["Palm Position"] = [hand.palm_position.x,hand.palm_position.y,hand.palm_position.z]
                #else:  #Here we save the left hand info
                leap_state_left["Palm Position"] = [hand.palm_position.x,hand.palm_position.y,hand.palm_position.z]
    
##                pub.send_info({"Hand Type":handType,"Hand ID":str(hand.id),"Pinch": hand.pinch_strength,\
##                           "Palm Position":[hand.palm_position.x,hand.palm_position.y,hand.palm_position.z],\
##                           "Pitch":str(direction.pitch * Leap.RAD_TO_DEG),"Roll":str(normal.roll * Leap.RAD_TO_DEG),\
##                           "Yaw":str(direction.yaw * Leap.RAD_TO_DEG),"Grab":str(hand.grab_strength),\
##                           "Elbow Position":[arm.elbow_position.x,arm.elbow_position.y,arm.elbow_position.z],\
##                           "Direction":[hand.direction.x,hand.direction.y,hand.direction.z],\
##                           "StabPos":[StabPos.x,StabPos.y,StabPos.z],\
##                           "Angle Yaw":angle_yaw,"Angle Roll":angle_roll,"Elbow Pitch":elbow_pitch,\
##                           "Elbow Roll":elbow_roll,"Wrist":[wrist.x,wrist.y,wrist.z]})
                


#------------ In parallel -----------------
# This function will be executed in parallel with the main program
def pub_sense_info():
    while True:
        # Send the leap motion info each .1 seconds
        time.sleep(.1)
        print leap_state_left
        # Publish the leap motion data
        pub.send_info(leap_state_left)

# --------- In main thread ---------------   
# Here we define which function will be executed in parallel
sense_thread = threading.Thread(target = pub_sense_info)
# This avoid that the parallel task follows running after closing the main task
sense_thread.daemon = True
# Here we start the parallel task
sense_thread.start()

# -------- Main function -----------------
def main():

    # Start a new LeapMotionListener object
    listener = LeapMotionListener()
    # Start the connection with leap motion
    controller = Leap.Controller()
    # Start getting new frames from leap motion
    controller.add_listener(listener)

    print"Press enter to quit"
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)

# --------- Program start -----------
if __name__ == "__main__":
    try:
        main()
    except:
        print "CONNECTION_ERRROR: leap motion not connected"
        print "closing node ... "
        time.sleep(3)
