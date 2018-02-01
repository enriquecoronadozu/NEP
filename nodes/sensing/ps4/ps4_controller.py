#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file presents an interface for interacting with the Playstation 4 Controller
# in Python. Simply plug your PS4 controller into your computer using USB and run this
# script!
#
# NOTE: I assume in this script that the only joystick plugged in is the PS4 controller.
#       if this is not the case, you will need to change the class accordingly.
#
# Copyright © 2015 Clay L. McLeod <clay.l.mcleod@gmail.com>
#
# Distributed under terms of the MIT license.

import os
import pprint
import pygame
import time
import nep
import signal


def signal_handler(self, signal, frame):
        """Signal handler used to close the app"""
        print('Signal Handler, you pressed Ctrl+C!')
        print('Server will be closed')
        self.pub.close()
        time.sleep(1)
        sys.exit(0)

node = nep.node("ps4")
c = node.conf_pub()
pub = node.new_pub("ps4", c)
signal.signal(signal.SIGINT, signal_handler)

class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""
        
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def listen(self):
        """Listen for events to happen"""
        
        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        while True:
            for event in pygame.event.get():
                
                
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value,2)
                    print str(event.axis)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value


                # Insert your code on what you would like to happen for each event here!
                # In the current setup, I have the state simply printing out to the screen.

                 #print self.axis_data
                buttons = {
                'square': self.button_data[0],
                'x': self.button_data[1], 
                'circle': self.button_data[2],
                'triangle': self.button_data[3],
                'L1': self.button_data[4], 
                'R1': self.button_data[5],
                'L2': self.button_data[6], 
                'R2': self.button_data[7],
                'share': self.button_data[8],
                'option': self.button_data[9], 
                'l_analog': self.button_data[10],
                'r_analog': self.button_data[11],
                'ps4': self.button_data[12], 
                'touch': self.button_data[13]
                }
                
                try:
                    axis_data = {'LX': self.axis_data[0], 
                                'LY': self.axis_data[1], 
                                'RX': self.axis_data[2], 
                                'RY': self.axis_data[3],
                                'L2': self.axis_data[4],
                                'R2': self.axis_data[5],
                                }
                except:
                    axis_data = {'LX': 0, 'LY': 0, 'RX': 0, 'RY': 0, 'L2': 0, 'R2':0}

                try:
                    up = False
                    down = False
                    left = False
                    right = False
                    if  self.hat_data[0][0] == -1:
                        left = True
                    if self.hat_data[0][0] == 1:
                        right = True
                    if  self.hat_data[0][1] == 1:
                        up = True
                    if self.hat_data[0][1] == -1:
                        down = True
                        
                    hat_data = {'up': up, 
                                'down': down, 
                                'left': left, 
                                'right': right,
                                }
                except:
                    hat_data = {'up': 0, 'down': 0, 'left': 0, 'right': 0}

                
                ps4_info = {'button':buttons, 'axis':axis_data, 'hat': hat_data}
                pub.send_info(ps4_info)
                time.sleep(.1)
                #print(buttons)
                #pprint.pprint(self.axis_data)
                print hat_data
                #print(self.hat_data)



if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()
