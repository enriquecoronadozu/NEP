# coding = utf-8
#!/usr/bin/env python

# ------------------------------- Broker -----------------------_-----------
# Description: Low-level Broker class
# --------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga


import time
import os
import zmq
import sys
import nep


class broker():
    def __init__(self, IP, PORT_XPUB, PORT_XSUB, TOPIC = ""):
        """
        Creates a XPUB/XSUB broker for many2many publish-subcribe communication

        Parameters
        ----------

        IP : int 
            IP value of the broker

        PORT_XPUB : int 
            XPUB port. Which must be different that PORT_XSUB.

        PORT_XSUB : int 
            XSUB port. Which must be different that PORT_XPUB.

        """
        self.PORT_XPUB = PORT_XPUB
        self.PORT_XSUB = PORT_XSUB
        self.TOPIC =  TOPIC
        self.context = zmq.Context()
        self.frontend = self.context.socket(zmq.XSUB)
        self.frontend.bind("tcp://" + IP + ":" + str(PORT_XSUB))
        self.backend = self.context.socket(zmq.XPUB)
        self.backend.bind("tcp://" + IP + ":" + str(PORT_XPUB))

    def start(self):
        """ Start proxy
        """
        try:
            zmq.proxy(self.frontend, self.backend)
        except:
            if self.TOPIC == "":
                print ("Proxy in (" + str(self.PORT_XSUB) + "," + str(self.PORT_XPUB) + ") stopped")
            else:
                print ("Proxy **" + self.TOPIC + "** in (" + str(self.PORT_XSUB) + "," + str(self.PORT_XPUB) + ") stopped")

        
    def stop(self):
        """ Stop proxy
        """
        self.frontend.close()
        self.backend.close()
        self.context.term()

if __name__ == "__main__":
    import doctest
    doctest.testmod()