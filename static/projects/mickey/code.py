# -*- encoding: UTF-8 -*-
import time
from nep import*

r = interaction()
  r.new_action({"primitive":"animation","input":"greeting","options":{"velocity":"50"}},"pepper",run=False)
  r.new_action({"primitive":"say","input":"hello","options":{"velocity":"50","language":"English"}},"nao",run=False)
r.at_same_time([msg1,msg2])
time.sleep (1)
r.new_action(["rest","none"],"nao")
