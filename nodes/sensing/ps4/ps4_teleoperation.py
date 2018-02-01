
import time
import nep
import threading



LY = 0
LX = 0
triangle = False
circle = False
share = False
option = False


r = nep.interaction()
def onUpdateData():
    global LY, triangle, LX, circle, share, option
    print ("Waiting data...")
    msg = {'action':'remote', 'input': "velocity", 'params':{'x':0, 'y':0, 'theta':0 }}
    while True :
        s, data = sub.listen_info()
        if s == True:
            LY = data["axis"]["LY"]
            LX = data["axis"]["LX"]
            triangle = data["button"]["triangle"]
            circle = data["button"]["circle"]
            share = data["button"]["share"]
            option = data["button"]["option"]
        
            

node = nep.node("animation_maker")
c = node.conf_sub()
sub = node.new_sub("ps4", c)
c = node.conf_pub(mode = "many2many")
pub = node.new_pub("/action_request", c)


sense = threading.Thread(target = onUpdateData)
# Used to finish the background thread when the main thread finish
sense.daemon = True
# Start new thread 
sense.start()
print ("Thread launched")


while True:

    if share == True:

            r.do_parallel_actions(["rest","none"], { },["nao"])
            print "rest"

    if option == True:

            r.do_parallel_actions(["wake_up","none"], { },["nao"])
            print "wake_up"

    if triangle == True:
        action = {'action':'move_to_position', 'input': "velocity", 'parameters':{'x':0, 'y':0, 'theta':0 }}
        msg = {"actions":[action]}
        print "triangle"
        print LY

            
        if LY < - .7 and triangle == True:

            r.do_parallel_actions(["move_to_position","velocity"], {'x':.2, 'y':0, 'theta':0, 'frequency': 0.5 },["nao"])

        elif LY > .7  and triangle == True:

         
            r.do_parallel_actions(["move_to_position","velocity"], {'x':-.2, 'y':0, 'theta':0, 'frequency': 0.5 },["nao"])

        elif LX > .7  and triangle == True:

         
            r.do_parallel_actions(["move_to_position","velocity"], {'x':0, 'y':0, 'theta':0.2, 'frequency': 0.5 },["nao"])

        elif LX < -.7  and triangle == True:
          
            r.do_parallel_actions(["move_to_position","velocity"], {'x':0, 'y':0, 'theta':-0.2, 'frequency': 0.5 },["nao"])
            

        else:

            action['parameters']['x'] = 0
            action['parameters']['y'] = 0
            action['parameters']['theta'] = 0
            action['parameters']['frequency'] = 0.0
            r.do_parallel_actions(["move_to_position","velocity"], {'x':0, 'y':0, 'theta':0, 'frequency': 0 },["nao"])


    if circle == True:
        action = {'action':'change_joint_value', 'input': "HeadPitch", 'parameters':{'value':0 }}
        msg = {"actions":[action]}
        if LY < - .7 and circle == True:

            action['parameters']['value'] = 3
            r.do_parallel_actions(["move_to_position","velocity"], {'x':.2, 'y':0, 'theta':0.5, 'frequency': 0.5},["nao"])

        elif LY >  .7 and circle == True:

            action['parameters']['value'] = -3
            r.do_parallel_actions(["move_to_position","velocity"], {'x':.2, 'y':0, 'theta':0.5, 'frequency': 0.5 },["nao"])

        else:
            pass
        

    time.sleep(.05)
        
        
    
