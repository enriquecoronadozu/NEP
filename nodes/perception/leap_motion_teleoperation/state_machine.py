from transitions import Machine


class Mode(object):
    def Move(self):
        print "Going for Navigation"
    def Arm(self):
        print "Going for Arm Control"
    def Shoulder(self):
        print "Going for shoulder"
    def Idle(self):
        print "Going to Idle"

def defineStateMachine():
          
    lump=Mode()
        
    states = ['arm','move','shoulder','idle'
            #State(name='arm',on_enter=['arm']),
            #State(name='move',on_enter=['move'])
            ]
            
    transitions = [
            { 'trigger': 'Bopen', 'source': 'idle', 'dest': 'move', 'before': 'Move'},
            { 'trigger': 'Bopen', 'source': 'arm', 'dest': 'move', 'before': 'Move'},  
            { 'trigger': 'Bopen', 'source': 'shoulder', 'dest': 'move', 'before': 'Move'}, 
            
            { 'trigger': 'Lopen', 'source': 'idle', 'dest': 'arm', 'before': 'Arm'},
            { 'trigger': 'Lopen', 'source': 'move', 'dest': 'arm', 'before': 'Arm'},  
            { 'trigger': 'Lopen', 'source': 'shoulder', 'dest': 'arm', 'before': 'Arm'},    

            { 'trigger': 'Ropen', 'source': 'idle', 'dest': 'shoulder', 'before': 'Shoulder'},
            { 'trigger': 'Ropen', 'source': 'move', 'dest': 'shoulder', 'before': 'Shoulder'},  
            { 'trigger': 'Ropen', 'source': 'arm', 'dest': 'shoulder', 'before': 'Shoulder'}, 

            { 'trigger': 'Nopen', 'source': 'shoulder', 'dest': 'idle', 'before': 'Idle'},
            { 'trigger': 'Nopen', 'source': 'move', 'dest': 'idle', 'before': 'Idle'},  
            { 'trigger': 'Nopen', 'source': 'arm', 'dest': 'idle', 'before': 'Idle'},            
        ]
        
    machine = Machine(model=lump,states=states,transitions=transitions,ignore_invalid_triggers=True)
    return machine, lump

