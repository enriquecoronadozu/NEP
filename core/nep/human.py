#!/usr/bin/env python

# ------------------------ Human representation class  --------------------------------
# Description: Set of classes used to describe the human states
# --------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga


class face_state:
  """ Class used to describe the face states of a human entity  """
  def __init__(self):
    self.face_happy = 'unknown'
    self.face_engaged = 'unknown'
    self.face_glasses = 'unknown'
    self.face_lefteyeclosed = 'unknown'
    self.face_righteyeclosed = 'unknown'
    self.face_mouthopen = 'unknown'
    self.face_mouthmoved = 'unknown'
    self.face_lookingaway = 'unknown'
  
class human_state:
  """ Class used to describe the state of a human entity  """
  def __init__(self):
    self.id_number = 0
    self.face  = face_state()
