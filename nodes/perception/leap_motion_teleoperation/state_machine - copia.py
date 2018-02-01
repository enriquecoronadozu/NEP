from transitions import Machine

def defineStateMachine():
    class Mode(object):
        def move(self):
            print "Going for Navigation"
        def arm(self):
            print "Going for Arm Control"
        def rest(self):
            print "Going for a Rest"
        def reset_head(self):
            print "Going to Reset Head"
        def stand(self):
            try:
                motionProxy = ALProxy("ALMotion", robotIP, PORT)
                postureProxy.goToPosture("Stand", 0.5)
                time.sleep(1)
            except Exception,e:
                print "Could not create proxy to ALMotion"
                print "Error was: ",e

                
    lump=Mode()
        
    states = ['arm','move','grab','shoulder'
            #State(name='arm',on_enter=['arm']),
            #State(name='move',on_enter=['move'])
            ]
            
    transitions = [
            ['LGrab','move','arm'],
            ['LGrab','arm','move'],
            ['RGrab','arm','shoulder'],
            ['RGrab','shoulder','arm']
            #['Pinch','arm','grab'],
            #['Pinch','grab','arm'],                    
        ]
        
    machine = Machine(model=lump,states=states,transitions=transitions,ignore_invalid_triggers=True)
    return machine, lump
