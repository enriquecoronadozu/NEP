#!/usr/bin/python
# -*- coding: utf-8 -*-


#TODO improve for n parameters

import os
from subprocess import Popen, call

if os.environ.get('OS','') == 'Windows_NT':
    from subprocess import CREATE_NEW_CONSOLE

from sys import executable
#TODO documentation

class launcher():
    """
    This class is used to launch nodes inside the node folder
    """

    def __init__(self):
        self.initial_path = os.getcwd()


    def _return_initial_path(self):
        os.chdir(self.initial_path)
        

    def launch(self, script):
        """
            Launch a python program

            Parameters
            ----------
            script : string
                script name + extension. Example: "script.py" 

        """
        print "To run: " + script
        if os.environ.get('OS','') == 'Windows_NT':

            print "Windows launcher in new console ......."
            Popen("python " + script, creationflags=CREATE_NEW_CONSOLE)
        else: 
            print "MAC/Linux launcher ......."
            import applescript

            inst = "cd "
            path = os.getcwd()
            set_path = inst+path
            to_run = inst+path + "\n" + "python " + script
            tell = 'tell application "Terminal" to do script '
            complete = tell + '"' +  to_run + '"'

            applescript.AppleScript(complete).run()
            self._return_initial_path()



    #TODO: put in a class that save the initial path to avoid problems with os.chdir("../../..")
    def nep_launch(self, node_type, input_, options_=""):
        """ Launch a node. We need to specify the type of node and the node name
                
            Parameters
            ----------
            node_type : string
                Type of node (name of the folder inside the node folder)
            input_: string
                name of the node to launch
            options_: dictionary or "none"
                parameters or arguments to launch the node
                
        """

        node_name = input_
        parameters = ""

        if node_type == "robots":
             name = options_['robot_name'].encode("UTF-8")
             ip = options_['robot_ip'].encode("UTF-8")
             port = options_['robot_port'].encode("UTF-8")
             parameters = " " + name + " " + ip +  " " + port
            
        self._return_initial_path()
        

        # Define the folder if the node
        folder = "nodes/"+ node_type + "/" + node_name
       

        # Define the script + arguments
        script =  node_name + ".py" +  parameters
        os.chdir(folder)
        cw_path = os.getcwd()

        print "Launching node in path:" + cw_path + "/" + node_name +  ".py"
        print "Parameters of the node: " +  parameters
        
        self.launch(script)
        self._return_initial_path()
        


        



