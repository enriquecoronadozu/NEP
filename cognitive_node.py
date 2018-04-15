# -*- encoding: UTF-8 -*-
import time
from nep import*

lan = launcher()
lan.nep_launch("devices", "leap_motion")
def launch_():
  lan.nep_launch("perception", "hand_position")

launch_()
