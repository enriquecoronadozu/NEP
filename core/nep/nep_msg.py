#!/usr/bin/env python

# ------------------------ NEP types --------------------------------
# Description: Basic types definition for NEP
# --------------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga


from nep import*


def point(x = 0, y = 0, z = 0):
    p = {'x': x, 'y' : y, 'z' : z, 'type' : "point"}
    return p

def vector(x = 0, y = 0, z = 0):
    v = {'x' : x, 'y' : y, 'z' : z, 'type' : "vector"}
    return v
 
def quaternion(x = 0, y = 0, z = 0, w = 0):
    q = {'x' : x, 'y' : y, 'z' : z, 'w' : 0,  'type' : "quaternion"}
    return q

def velocity(linear = vector() , angular = vector()):
    v = {'linear' : linear , 'angular': angular, 'type' : "velocity"}
    return v

def accel(linear = vector() , angular = vector()):
    a = {'linear' : linear , 'angular' : angular, 'type' : "accel"}
    return a

def wrench(force = vector() , torque = vector()):
    w = {'force' : force , 'torque' : torque, 'type' : "wrench"}
    return w

def pose(position = vector() , orientation = quaternion()):
    pose = {'position' : position , 'orientation' : orientation, 'type' : "pose" }
    return pose
                                    
if __name__ == "__main__":
    import doctest
    doctest.testmod()

                                
