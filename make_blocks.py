import os
import subprocess
from sys import executable
import time

print "Building ***** NEP interface *******"
setup_path = "static/web_libraries/blockly"
os.chdir(setup_path)
run_code = "python build.py"
print subprocess.check_output(run_code)
os.chdir("../..")
time.sleep(3)
#raw_input("Press enter to continue...")
