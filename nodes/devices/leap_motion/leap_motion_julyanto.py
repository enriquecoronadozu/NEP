import Leap, sys, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

            
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
        #controller.config.set("Gesture.KeyTap.MinDownVelocity", 40.0)
        #controller.config.set("Gesture.KeyTap.HistorySeconds", .2)
        #controller.config.set("Gesture.KeyTap.MinDistance", 1.0)
        #controller.config.save()

    def on_disconnect(self, controller):
        print"Motion Sensor Disconnected!"
    def on_exit(self, controller):
        print"Exitted"
    def on_frame(self, controller):
        frame = controller.frame()
       

        """print "Frame ID " + str(frame.id) + ", Timestamp :" + str(frame.timestamp)\
            + ", # of Hands " + str(len(frame.hands)) + ", # of FIngers " + \
            str(len(frame.fingers))   
        
        def differential_normalizer(self, leap_point, iBox, is_left, clamp):
            normalized = iBox.normalize_point(leap_point, True)
            offset = 0.25 if is_left else -0.25
            normalized.x = normalized.x + offset

            #clamp after offsetting
            normalized.x = 0 if (clamp and normalized.x < 0) else normalized.x
            normalized.x = 1 if (clamp and normalized.x > 1) else normalized.x
            normalized.y = 0 if (clamp and normalized.y < 0) else normalized.y
            normalized.y = 1 if (clamp and normalized.y > 1) else normalized.y

            return normalized
        """
        
        for hand in frame.hands:                    
            
            handType = 0 if hand.is_left else 1
            normal = hand.palm_normal
            direction = hand.direction            
            arm = hand.arm
            elbow_dir = arm.elbow_position
            wrist = hand.wrist_position
            #linear_hand_movement = hand.translation(controller.frame(1))               
                                                                        
            for finger in hand.fingers:
                
                #Length = finger.length
                #Width = finger.width
                #Tipp = finger.tip_position
                #Tipv = finger.tip_velocity
                FingerDir = finger.direction
                #Straight = finger.is_extended
                StabPos = finger.stabilized_tip_position
                angle_yaw = direction.angle_to(Leap.Vector.x_axis)
                angle_roll = normal.angle_to(Leap.Vector.x_axis)
                elbow_pitch = elbow_dir.angle_to(Leap.Vector.z_axis)
                elbow_roll = elbow_dir.angle_to(Leap.Vector.y_axis)
                print angle_yaw
                    
                time.sleep(0.008)
        """        
        for gesture in frame.gestures():
            if gesture.type is Leap.Gesture.TYPE_KEY_TAP:
                key_tap = Leap.KeyTapGesture(gesture)
                tap_direction = key_tap.direction
                #tapper = key_tap.pointable  
                tapper = str(gesture.state)
                
                #pub2.send_info({"Tapper":tapper,"TapDir":[tap_direction.x,tap_direction.y,tap_direction.z]})
        """     
                
        '''for hand in frame.hands:    
            handType = "Left Hand" if hand.is_left else "Right Hand"
                        
            print type(hand.palm_position)
            print  "Hand ID:"  + str(hand.id) +  "Palm Position :" \
                + str(hand.palm_position.x)
            while True :
                pub.send_info({"Hand Type":handType,"Hand ID":str(hand.id), \
                               "Palm Position":[hand.palm_position.x,hand.palm_position.y]})
        
            #calculation pitch, roll, and yaw
            normal = hand.palm_normal
            direction = hand.direction

            print "Pitch: " + str(direction.pitch * Leap.RAD_TO_DEG) + " Roll: "\
                + str(normal.roll * Leap.RAD_TO_DEG) + " Yaw: "\
                + str(direction.yaw * Leap.RAD_TO_DEG)'''
         
   

def main():
    listener = LeapMotionListener()
    controller = Leap.Controller()

    controller.add_listener(listener)

    print"Press enter to quit"
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)

if __name__ == "__main__":
    try:
        main()
    except:
        print "CONNECTION_ERRROR: leap motion not connected"
        print "closing node ... "
        time.sleep(3)
