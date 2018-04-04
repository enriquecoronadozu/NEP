#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

# Luis Enrique Coronado Zuniga

# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.


import nep
import nep_nao
import sys

nao_port = "9559"
robot_name = "nao"
nao_ip = '127.0.0.1'


try:
    robot_name = sys.argv[1]
except:
    pass
try:
    nao_ip = sys.argv[2]
except:
    pass
try:
    nao_port = sys.argv[3]
except:
    pass

print ("Robot IP to connect:" + str(nao_ip))
print ("Robot PORT to connect:" + str(nao_port))
print ("Robot name:" + str(robot_name))
    

robot = nep.robot(robot_name, "pubsub")
nao = nep_nao.nao(nao_ip, nao_port)

robot_actions = {
            'say':nao.say_contextual,
            'rest':nao.rest,
            'say_contextual': nao.say_contextual,
            'wake_up': nao.wake_up,
            'animation': nao.animation,
            'imitation': nao.imitation,
            'stop_behaviors':nao.stop_behaviors,
            'posture':nao.posture,
            'play_sound':nao.play_sound,
            'open_hand': nao.open_hand,
            'close_hand': nao.close_hand,
            'move':nao.move_to_position,
            'change_joint_value':nao.change_joint_value,
            'save_motion':nao.save_motion,
            }

robot.set_robot_actions(robot_actions)
robot.run()



            
