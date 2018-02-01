#!/usr/bin/env python

# ------------------------ Behavior class --------------------------------
# Description: Main behavioral class
# --------------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga




import nep
import time
import threading

            

class behavior():

    def __init__(self, name):
        self.behavior = {"name": str(name), "sub_behaviors":[]}
        
    def add_action(self,action, inputs, robots):
        sub_behaviors = self.behavior["sub_behaviors"]
        new_action = [{"action":action, "inputs": inputs, "robots": robots}]
        sub_behaviors.append(new_action)
        self.behavior["sub_behaviors"] = sub_behaviors

    def add_parallel_action(self,action, inputs, robots):
        sub_behaviors = self.behavior["sub_behaviors"]
        parallel_action = {"action":action, "inputs": inputs, "robots": robots}
        if sub_behaviors is not None:
            last_action = sub_behaviors.pop()
            last_action.append(parallel_action)
            sub_behaviors.append(last_action)
            self.behavior["sub_behaviors"] = sub_behaviors
            
    def add_sequence(self, sequence):
        sub_behaviors = self.behavior["sub_behaviors"]
        sub_behaviors.append(sequence.sequence)
        self.behavior["sub_behaviors"] = sub_behaviors


    def add_simultaneos(self, sequence_list):
        sub_behaviors = self.behavior["sub_behaviors"]

        seq_list=[]
        for seq in sequence_list:
            seq_list.append(seq.sequence)
        simultaneo = {"type": "simultaneo", "sequences": seq_list}
        sub_behaviors.append(simultaneo)
        self.behavior["sub_behaviors"] = sub_behaviors


            
