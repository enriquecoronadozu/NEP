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