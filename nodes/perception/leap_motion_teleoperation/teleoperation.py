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

    #motionProxy.setWalkArmsEnabled(True, True)
    if l.Pinch == 1 or l.PalmPos[2] >= 150:
        x = 0.0
        y = 0.0
        theta = 0.0
        frequency = 0.0
        
        if l.PalmPos[1] < 60 :
            motionProxy.rest()
            time.sleep(5)
        else:
            pass
    elif l.Pinch ==1 and l.PalmPos[1] >= 150:
        motionProxy.wakeUp()      
    elif l.Pitch <-5 and l.Pitch > -30:
        x = 1
        y = 0.0
        theta = 0.0
        frequency = 0.5                
    elif l.Pitch <= -30:
        x = 1
        y = 0.0
        theta = 0.0
        frequency = 1.0                
    elif l.Pitch > 30:
        x = -1
        y = 0.0
        theta = 0.0
        frequency = 0.5                
    elif l.Roll >= 40:
        x = 0.0
        y = 0.5
        theta = 0.0
        frequency = 0.5                
##                elif PalmPos[0] <= -175: 
##                    x = 0.0
##                    y = 0.5
##                    theta = 0.0
##                    frequency = 1.0                
    elif l.Roll <= -20:  
        x = 0.0
        y = -0.5
        theta = 0.0
        frequency = 0.5                
##                elif PalmPos[0] >= -30:
##                    x = 0.0
##                    y = -0.5
##                    theta = 0.0
##                    frequency = 1.0            
    elif l.Yaw <= -10:
        x = 0.0
        y = 0.0
        theta = 1.0
        frequency = 0.5                
    elif l.Yaw >= 30 :
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


    global P_angle
    global Y_angle

    if r.Pitch <= -40 or r.Pitch >=40 :
        if r.Pitch <= -40 and P_angle < 29.5:
            P_angle = 0.5
        elif r.Pitch >= 40 and P_angle > -38.5:
            P_angle = -0.5
        else :                
            P_angle = 0
    elif r.Roll >= 25 or r.Roll <= -50:
        if r.Roll >= 25 and Y_angle < 119.5:
            Y_angle = 0.5
        elif r.Roll < -50 or Y_angle > -119.5:
            Y_angle = -0.5
        else:
            Y_angle = 0
    elif r.Grab == 1:
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
           
    name = ["LElbowYaw","LElbowRoll","LShoulderPitch","LWristYaw"]
    angle = [-l.AngleYaw ,\
            round((-200*r.Direction[2]-200)*almath.TO_RAD,1),\
            round((-0.4*l.Wrist[1]+120)*almath.TO_RAD,1),\
            round((-1.25*l.Roll+75)*almath.TO_RAD,1)]
    speed = 0.3
    motionProxy.post.setAngles(name,angle,speed)                    
    time.sleep(0.0001)    
            
                                                                          
    name = ["RElbowYaw","RElbowRoll","RShoulderPitch","RWristYaw"]
    angle = [-r.AngleYaw+3.14 ,\
            round((200*r.Direction[2]+200)*almath.TO_RAD,1),\
            round((-0.4*r.Wrist[1]+120)*almath.TO_RAD,1),\
            round((-1.25*r.Roll-75)*almath.TO_RAD,1)]
    speed = 0.3
    motionProxy.post.setAngles(name,angle,speed)
    time.sleep(.0001)
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

    name = "LShoulderRoll"
    angle = round((-0.4*l.PalmPos[0]-75)*almath.TO_RAD)
    speed = 0.3
    motionProxy.post.setAngles(name,angle,speed)
    time.sleep(0.0001)
          
    name = "RShoulderRoll"
    angle = round((-0.4*r.PalmPos[0]+75)*almath.TO_RAD)                
    speed = 0.3
    motionProxy.post.setAngles(name,angle,speed)
    time.sleep(0.0001)


class LeftHand():
    def __init__(self):
        print "New left hand object"
        self.PalmPos = 0
        self.PalmPos =0
        self.Pitch = 0
        self.Roll = 0
        self.Grab = 0
        self.Yaw = 0
        self.Direction = 0
        self.AngleYaw = 0
        self.Elbow = 0
        self.ElbowPitch = 0
        self.ElbowRoll = 0
        self.Wrist = 0
        self.Pinch = 0

class RightHand():
    def __init__(self):
        print "New left hand object"
        self.PalmPos = 0
        self.PalmPos =0
        self.Pitch = 0
        self.Roll = 0
        self.Grab = 0
        self.Yaw = 0
        self.Direction = 0
        self.AngleYaw = 0
        self.Elbow = 0
        self.ElbowPitch = 0
        self.ElbowRoll = 0
        self.Wrist = 0
        self.Pinch = 0

r = RightHand()
l = LeftHand()

def onUpdateData():
    global sensing_started, HandType, PalmPos, Pitch, Roll,Grab,Yaw,Direction,AngleYaw
    global Elbow ,ElbowPitch,ElbowRoll,Wrist,Pinch
    global l, r 
    print ("Waiting data...")
    while True : 
        s, data = sub.listen_info()
        if s == True:
            if sensing_started == False:
                sensing_started = True
                print ("Reading data...")
            
            if  data["Hand Type"] == 0:
                l.Grab = float(data["Grab"])
                l.PalmPos = data["Palm Position"]
                l.Pitch = float(data["Pitch"])
                l.Roll = float(data["Roll"])
                l.Grab = float(data["Grab"])
                l.Yaw = float(data["Yaw"])
                l.Direction = data["Direction"]
                l.AngleYaw = data["Angle Yaw"]
                l.Elbow = data["Elbow Position"]
                l.ElbowPitch = data["Elbow Pitch"]
                l.ElbowRoll = data["Elbow Roll"]
                l.Wrist = data["Wrist"]
                l.Pinch = float(data["Pinch"])
            else:
                r.Grab = float(data["Grab"])
                r.PalmPos = data["Palm Position"]
                r.Pitch = float(data["Pitch"])
                r.Roll = float(data["Roll"])
                r.Grab = float(data["Grab"])
                r.Yaw = float(data["Yaw"])
                r.Direction = data["Direction"]
                r.AngleYaw = data["Angle Yaw"]
                r.Elbow = data["Elbow Position"]
                r.ElbowPitch = data["Elbow Pitch"]
                r.ElbowRoll = data["Elbow Roll"]
                r.Wrist = data["Wrist"]
                r.Pinch = float(data["Pinch"])
                


PORT = 9559
robotIP = "192.168.0.101"

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
machine.set_state('idle')

sense = threading.Thread(target = onUpdateData)
# Used to finish the background thread when the main thread finish
sense.daemon = True
# Start new thread 
sense.start()
print ("Thread launched")


def  getTrigger(HandType,Grab):
    
    Lopen = False
    Ropen = False
    trigger = "none"

    if l.Grab == 1  and r.Grab == 1:
        trigger  = "both_close"
    elif l.Grab == 1  and r.Grab == 0:
        trigger  = "L_open"
    elif l.Grab == 0  and r.Grab == 1:
        trigger  = "R_open"
    elif l.Grab == 0  and r.Grab == 0:
        trigger  = "both_open"

    return trigger
        
old_trigger = "none" 
exit_app = False    
while not exit_app: 

    if sensing_started:
        
        trigger = getTrigger(HandType,Grab)

        if trigger == "both_open":
            lump.Bopen()
        elif trigger == "L_open": 
            lump.Lopen()   
        elif trigger == "R_open": 
            lump.Ropen()  
        elif trigger == "both_close": 
            lump.Nopen()  
    

            

   
        
        if lump.state == 'move':
            Walk()
        elif lump.state == 'arm':
            motionProxy.stopMove()            
            Arm()            
        elif lump.state =='shoulder':
            motionProxy.stopMove()
            Shoulder()
        elif lump.state =='shoulder':
            motionProxy.stopMove()
            motionProxy.setWalkTargetVelocity(0,0,0,0)
            

    
        
