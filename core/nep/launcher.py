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

    Example
    ----------

    Launch a node

    .. code-block:: python

        import nep
        lan = nep.launcher()
        lan.nep_launch("action", "nao_action_processor")

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
    #Improve, more paremeters
    def nep_launch(self, node_type = "action", node_name = "nao_action_engine", param1 = "Akari", param2 = "192.168.11.2"):
        """ Launch a node. We need to specify the type of node and the node name
                
            Parameters
            ----------
            node_type : string
                Type of node. Example: sensing, perception, action.
            node_name: string
                name of the node to open
            param1: string
                first parameter for launch the node
            param2: string
                second parameter for launch the node
                
                
            Returns
            -------
            node_name : string
                Name of the node without .py
        """
                
        params = ""
        self._return_initial_path()
        if(node_type == "action"):
            params = " " + str(param2) + " " + str(param1)
        if(node_type == "perception"):
            params = " " + str(param1) + " " + str(param1)

            
        setup = "nodes/"+ node_type + "/" + node_name
        print "Running " + setup + "/" + node_name +  ".py" 

        #python script to be excuted +  parameters
        script =  node_name + ".py" +  params
        print script
        os.chdir(setup)
        print "Current:" + os.getcwd()
        self.launch(script)
        self._return_initial_path()
        


        



