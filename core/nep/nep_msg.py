#!/usr/bin/env python

# ------------------------ Robot bahavior class --------------------------------
# Description: Set of robot bahavior clases
# --------------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga


from nep import*

class nep_msg():

    def point(self, x = 0, y = 0, z = 0):
        p = {'x' = x, 'y' = y, 'z' = z, 'type' = "point"}
        return p

    def vector(self, x = 0, y = 0, z = 0):
        v = {'x' = x, 'y' = y, 'z' = z, 'type' = "vector"}
        return v
 
    def quaternion(self, x = 0, y = 0, z = 0, w = 0, 'type' = "quaternion"):
        q = {'x' = x, 'y' = y, 'z' = z, 'w' = 0}
        return q

    def velocity(self, linear = self.vector() , angular = self.vector(), 'type' = "velocity"):
        v = {'linear' = linear , 'angular' = angular}
        return v

    def accel(self, linear = self.vector() , angular = self.vector(), 'type' = "accel"):
        a = {'linear' = linear , 'angular' = angular}
        return a

    def wrench(self, force = self.vector() , torque = self.vector(), 'type' = "wrench"):
        w = {'force' = force , 'torque' = torque}
        return w

    def pose(self, position = self.vector() , orientation = self.quaternion(), 'type' = "pose" ):
        pose = {'position' = position , 'orientation' = orientation}
        return pose

                                    
if __name__ == "__main__":
    import doctest
    doctest.testmod()

                                
