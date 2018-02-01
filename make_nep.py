import os
import subprocess
from sys import executable
import time

# Description: This script as a auto building of the NEP framework


print "Building ***** NEP core *******"
setup_path = "core"


os.chdir(setup_path)

try:
    run_code = ("rmdir /Q /S build")
    print subprocess.check_output(run_code,  shell=True)
except:
    pass

run_code = ("python setup.py install")
print subprocess.check_output(run_code,  shell=True)
os.chdir("..")
time.sleep(3)

#raw_input("Press enter to continue...")


