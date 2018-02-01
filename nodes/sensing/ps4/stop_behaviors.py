# -*- encoding: UTF-8 -*-
import time
from nep import*

        
r = interaction()

r.do_parallel_actions(["stop_behaviors","none"], {},["nao"])
r.do_parallel_actions(["wake_up","none"], {},["nao"])
