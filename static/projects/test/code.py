# -*- encoding: UTF-8 -*-
import time
from nep import*

r = interaction()
r.new_action([{"primitive":"animation","input":"","options":{"velocity":"50","flip":False,"reverse":false}}, {"primitive":"animation","input":"","options":{"velocity":"50","flip":false,"reverse":false}}],"nao")
r.new_action({"primitive":"say","input":"edit","options":edit},)
