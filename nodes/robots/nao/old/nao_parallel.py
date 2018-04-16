#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

# Luis Enrique Coronado Zuniga

# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.


# TODO: cambiar a nueva nimevlaturea ---- action por primitive, 

import nep
import nep_nao
import time
import atexit
import sys
import signal
import numpy as np
import json
import threading


node = nep.node("NAO")

def signal_handler(signal, frame):
    """Signal handler used to close the app"""
    print('Signal Handler, you pressed Ctrl+C!')
    time.sleep(1)
    sys.exit(0)


    


class nao_action():

    def __init__(self, nao_ip, nao_port, robot_name):
        

        # New nao instance
        self.robot = nep_nao.nao(nao_ip, nao_port)
        print self.robot.set_angles()
        y = raw_input("click")

        i = 0
        while i < 100:
            i = i + 1
            self.robot.get_angles_from_motions()
            time.sleep(.1)
            print i

        with open('data.txt', 'w') as outfile:
            json.dump(self.robot.data2save, outfile)



        
                        
def main(nao_ip,nao_port,robot_name):

    print "****** NAO Robot IP: " + nao_ip
    nao = nao_action(nao_ip, nao_port, robot_name )


if __name__ == "__main__":

    nao_port = "9559"
    robot_name = "nao"
    nao_ip = '192.168.0.100'

    main(nao_ip,int(nao_port),robot_name)



            
