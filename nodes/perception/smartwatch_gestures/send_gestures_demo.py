#!/usr/bin/env python

# Luis Enrique Coronado Zuniga
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.

# Descrption: ---------------------------------
# Code used to publish some fake gesture recognition task to test the platform
# ---------------------------------------------
#%%
from numpy import*
from hmpy import*
import os
from nep import*
import time

ip = "127.0.0.1"
port = 5002
topic = "/arm_gesture"

pub = publisher(ip, port, topic)
message = {}
while True:

        message = {'human_action': 'hand_up'}
        pub.send_info(message)
        print message
        time.sleep(5)

        message = {'human_action': 'hand_up'}
        pub.send_info(message)
        print message
        time.sleep(5)

        message = {'human_action': 'hand_up'}
        pub.send_info(message)
        print message
        time.sleep(5)

        message = {'human_action': 'hand_up'}
        pub.send_info(message)
        print message
        time.sleep(5)


        message = {'human_action': 'press_button'}
        pub.send_info(message)
        print message
        time.sleep(1)

