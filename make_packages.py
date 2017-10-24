import os
import subprocess
from sys import executable
import time

# Description: This script as a auto building of packages

list_packages = os.listdir("packages")
print "Packages:"
print list_packages
print

for package in list_packages:

    print ("Instaling ***** " + package + " *******")
    print ("Current:" + os.getcwd())

    try:
        setup_path = "packages/" + package  
        os.chdir(setup_path)
        #print "Current:" + os.getcwd()

        run_code = "python setup.py install"
        
        #TODO: check if there is not error in ubuntu and windows
        print subprocess.check_output(run_code,  shell=True)
        os.chdir("../..")
        time.sleep(1)
    except:
        print ("ERROR:" + package + " did not contain a python package or there is not a setup.py file")

#raw_input("Press enter to continue...")
