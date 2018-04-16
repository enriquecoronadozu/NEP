import sys
import time
import motion
import almath
from transitions import Machine
from naoqi import ALProxy
import threading
import nep
from state_machine import*

node = nep.node("subs")
sub = node.new_sub("leap_hand")
sensing_started = False

HandType = 0
PalmPos = 0
Pitch = 0
Roll = 0
Grab = 0
Yaw = 0
Direction = 0
AngleYaw = 0
Elbow = 0
ElbowPitch = 0
ElbowRoll = 0
Wrist = 0
Pinch = 0



def Walk():                                                                     
    print "Navigation"                                                
    if HandType == 0 :                
        #motionProxy.setWalkArmsEnabled(True, True)
        if Pinch == 1 or PalmPos[2] >= 150:
            x = 0.0
            y = 0.0
            theta = 0.0
            frequency = 0.0
            
            if PalmPos[1] < 60 :
                motionProxy.rest()
                time.sleep(5)
            else:
                pass
        elif Pinch ==1 and PalmPos[1] >= 150:
            motionProxy.wakeUp()      
        elif Pitch <-5 and Pitch > -30:
            x = 1
            y = 0.0
            theta = 0.0
            frequency = 0.5                
        elif Pitch <= -30:
            x = 1
            y = 0.0
            theta = 0.0
            frequency = 1.0                
        elif Pitch > 30:
            x = -1
            y = 0.0
            theta = 0.0
            frequency = 0.5                
        elif Roll >= 40:
            x = 0.0
            y = 0.5
            theta = 0.0
            frequency = 0.5                
##                elif PalmPos[0] <= -175: 
##                    x = 0.0
##                    y = 0.5
##                    theta = 0.0
##                    frequency = 1.0                
        elif Roll <= -20:  
            x = 0.0
            y = -0.5
            theta = 0.0
            frequency = 0.5                
##                elif PalmPos[0] >= -30:
##                    x = 0.0
##                    y = -0.5
##                    theta = 0.0
##                    frequency = 1.0            
        elif Yaw <= -10:
            x = 0.0
            y = 0.0
            theta = 1.0
            frequency = 0.5                
        elif Yaw >= 30 :
            x = 0.0
            y = 0.0
            theta = -1.0
            frequency = 0.5                
        else:
            x = 0.0
            y = 0.0
            theta = 0.0
            frequency = 0.0
        motionProxy.setWalkTargetVelocity(x,y,theta,frequency)
        time.sleep(0.0001)

    
    else :
        global P_angle
        global Y_angle
    
        if Pitch <= -40 or Pitch >=40 :
            if Pitch <= -40 and P_angle < 29.5:
                P_angle = 0.5
            elif Pitch >= 40 and P_angle > -38.5:
                P_angle = -0.5
            else :                
                P_angle = 0
        elif Roll >= 25 or Roll <= -50:
            if Roll >= 25 and Y_angle < 119.5:
                Y_angle = 0.5
            elif Roll < -50 or Y_angle > -119.5:
                Y_angle = -0.5
            else:
                Y_angle = 0
        elif Grab == 1:
            motionProxy.angleInterpolationWithSpeed("Head",[0,0],0.5)
            #postureProxy.goToPosture("StandInit", 1.0)
            time.sleep(1)
        else :
            P_angle = 0
            Y_angle = 0
    
        change = [Y_angle,P_angle]
        fraction = 0.1
        motionProxy.changeAngles("Head", change, fraction)
        time.sleep(0.0001)
                                    

def Arm(): 
    print "Arm Control"                                 
    if HandType == 0 :        
        name = ["LElbowYaw","LElbowRoll","LShoulderPitch","LWristYaw"]
        angle = [-AngleYaw ,\
                round((-200*Direction[2]-200)*almath.TO_RAD,1),\
                round((-0.4*Wrist[1]+120)*almath.TO_RAD,1),\
                round((-1.25*Roll+75)*almath.TO_RAD,1)]
        speed = 0.3
        motionProxy.post.setAngles(name,angle,speed)                    
        time.sleep(0.0001)    
            
    else:                                                                           
        name = ["RElbowYaw","RElbowRoll","RShoulderPitch","RWristYaw"]
        angle = [-AngleYaw+3.14 ,\
                round((200*Direction[2]+200)*almath.TO_RAD,1),\
                round((-0.4*Wrist[1]+120)*almath.TO_RAD,1),\
                round((-1.25*Roll-75)*almath.TO_RAD,1)]
        speed = 0.3
        motionProxy.post.setAngles(name,angle,speed)
        time.sleep(0.0001)
'''   
def Grab():
    print "Grabbing"
    if HandType == 0:
        if round(Pitch,1) >= 0.5:
            motionProxy.closeHand('LHand')
            time.sleep(0.0001)
        else:
            motionProxy.openHand('LHand')
            time.sleep(0.0001)
        
    else:
        if round(Pitch,1) >= 0.5:
            motionProxy.closeHand('RHand')
            time.sleep(0.0001)
        else:
            motionProxy.openHand('RHand')
            time.sleep(0.0001)
'''

def Shoulder():
    print "Shoulder Control"
    if HandType == 0 :
        name = "LShoulderRoll"
        angle = round((-0.4*PalmPos[0]-75)*almath.TO_RAD)
        speed = 0.3
        motionProxy.post.setAngles(name,angle,speed)
        time.sleep(0.0001)
    else :                
        name = "RShoulderRoll"
        angle = round((-0.4*PalmPos[0]+75)*almath.TO_RAD)                
        speed = 0.3
        motionProxy.post.setAngles(name,angle,speed)
        time.sleep(0.0001)



def onUpdateData():
    global sensing_started, HandType, PalmPos, Pitch, Roll,Grab,Yaw,Direction,AngleYaw
    global Elbow ,ElbowPitch,ElbowRoll,Wrist,Pinch 
    print ("Waiting data...")
    while True : 
        s, data = sub.listen_info()
        if s == True:
            if sensing_started == False:
                sensing_started = True
                print ("Reading data...")

            HandType = data["Hand Type"]
            PalmPos = data["Palm Position"]
            Pitch = float(data["Pitch"])
            Roll = float(data["Roll"])
            Grab = float(data["Grab"])
            Yaw = float(data["Yaw"])
            Direction = data["Direction"]
            AngleYaw = data["Angle Yaw"]
            Elbow = data["Elbow Position"]
            ElbowPitch = data["Elbow Pitch"]
            ElbowRoll = data["Elbow Roll"]
            Wrist = data["Wrist"]
            Pinch = float(data["Pinch"])



PORT = 9559
robotIP = "127.0.0.1"

try:
    motionProxy = ALProxy("ALMotion", robotIP, PORT)
except Exception,e:
    print "Could not create proxy to ALMotion"
    print "Error was: ",e
    
try:
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
except Exception, e:
    print "Could not create proxy to ALRobotPosture"
    print "Error was: ", e

postureProxy.goToPosture("StandInit", 0.5)
#StiffnessOn(motionProxy)

motionProxy.killAll()
print "All tasks reset."

P_angle = 0
Y_angle = 0
change = False
change_hand = False
change_shoulder = False
change_grab = False
LeftGrab = 0
RightGrab = 0
RightPinch = 0

#Get  state machine definition
machine, lump = defineStateMachine()
  
#Initial state
machine.set_state('move')

sense = threading.Thread(target = onUpdateData)
# Used to finish the background thread when the main thread finish
sense.daemon = True
# Start new thread 
sense.start()
print ("Thread launched")

exit_app = False    
while not exit_app : 

    if sensing_started:
        # Changing variable LeftGrab for Navigation-ArmControl Mode
        if HandType == 0 and Grab == 1:
            LeftGrab = 1
        elif HandType == 0 and Grab == 0:
            LeftGrab = 0

        # Changing variable LeftGrab for ArmControl-Shoulder Mode    
        if HandType == 1 and Grab == 1:
            RightGrab = 1
        elif HandType == 1 and Grab == 0:
            RightGrab = 0
        
        
        if LeftGrab == 1 and change_hand == False:            
            change_hand = True            
            lump.LGrab()        
        if RightGrab == 1 and change_shoulder == False:            
            change_shoulder = True
            lump.RGrab()        
        if LeftGrab == 0 :
            change_hand = False
        if RightGrab == 0:
            change_shoulder = False
            #change_grab == False
                
        
        if lump.state == 'move':
            Walk()
        elif lump.state == 'arm':
            motionProxy.stopMove()            
            Arm()            
        elif lump.state =='shoulder':
            motionProxy.stopMove()
            Shoulder()
    
        
