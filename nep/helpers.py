# coding = utf-8
#!/usr/bin/env python

# ------------------------------ Helper functions ---------------------------------
# Description: Some useful functions used in NEP core
# --------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga


from os import listdir
from os.path import isfile, join
import simplejson
import nep
import time
import sys, os
from subprocess import Popen, call


def nepmaster(version="2", param =""):
    """
        Launch master in NEP_WS

        Parameters
        ----------
        version : string
            Python version, 0 for default, 2 for Python 2 and 3 for Python 3

        param : string
            Can be "local", or "network"
    """

    if os.environ.get('OS','') == 'Windows_NT':
        from subprocess import CREATE_NEW_CONSOLE

    nep_ws = nep.getNEPpath()
    script = "master"
    command = "python " + nep_ws + "/" + script + ".py"+ " " + param

    if os.environ.get('OS','') == 'Windows_NT':

        if version == "2": #If more that one python version, specify Python 2
            print ("Running in Python 2")
            command = "py -2 " + nep_ws + "/" + module + "/" + script + ".py"+ " " + parameters
        elif version == "3": #If more that one python version, specify Python 3
            print ("Running in Python 3")
            command = "py -3 " + nep_ws + "/" + module + "/" + script + ".py"+ " " + parameters

        print ("Windows launcher in new console .......")
        Popen(command, creationflags=CREATE_NEW_CONSOLE)
    else: 
        print ("OSX launcher .......")

        if version == "2": #If more that one python version, specify Python 2
            print ("Running in Python 2")
            command = "python2 " + nep_ws + "/" + module + "/" + script + ".py"+ " " + parameters
        elif version == "3": #If more that one python version, specify Python 3
            print ("Running in Python 3")
            command = "python3 " + nep_ws + "/" + module + "/" + script + ".py"+ " " + parameters

        import applescript

        tell = 'tell application "Terminal" to do script '
        complete = tell + '"' +  command + '"'

        applescript.AppleScript(complete).run()


def neprun(module, script, parameters, version="2"):

    """
        Launch a python script in NEP_WS

        Parameters
        ----------
        module : string
            Module name

        script : string
            Script name

        script : parameters
            Additional command line parameters

        version : string
            Python version, 0 for default, 2 for Python 2 and 3 for Python 3

    """
    try:

        if os.environ.get('OS','') == 'Windows_NT':
            from subprocess import CREATE_NEW_CONSOLE

        nep_ws = nep.getNEPpath() 
        command = "python " + nep_ws + "/" + module + "/" + script + ".py"+ " " + parameters
    


        print ("To run: " + command)
        if os.environ.get('OS','') == 'Windows_NT':

            if version == "2": #If more that one python version, specify Python 2
                print ("Running in Python 2")
                command = "py -2 " + nep_ws + "/" + module + "/" + script + ".py"+ " " + parameters
            elif version == "3": #If more that one python version, specify Python 3
                print ("Running in Python 3")
                command = "py -3 " + nep_ws + "/" + module + "/" + script + ".py"+ " " + parameters

            print ("Windows launcher in new console .......")
            Popen(command, creationflags=CREATE_NEW_CONSOLE)
        else: 
            print ("OSX launcher .......")

            if version == "2": #If more that one python version, specify Python 2
                print ("Running in Python 2")
                command = "python2 " + nep_ws + "/" + module + "/" + script + ".py"+ " " + parameters
            elif version == "3": #If more that one python version, specify Python 3
                print ("Running in Python 3")
                command = "python3 " + nep_ws + "/" + module + "/" + script + ".py"+ " " + parameters

            import applescript

            tell = 'tell application "Terminal" to do script '
            complete = tell + '"' +  command + '"'

            applescript.AppleScript(complete).run()

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        time.sleep(3)
        return False
 

def masterRegister(node, topic, master_ip = '127.0.0.1', master_port = 7000, socket = "subscriber", mode = "many2many", pid = "none"):
    """ Register topic in master node
            
    Parameters
    ----------

    node: string
        Node name

    topic : string
        Topic to register

    master_ip : string 
        IP of the master node service

    master_port : int
        Port of the master node service

    socket: string
        Socket type. Example "surveyor", "publisher", "subscriber", "respondent", "client", "server"

    mode: string
        Parameter only for Publish/Subscriber pattern. Options are "one2many", "many2one" and "many2many".

    Returns
    ----------

    result : bool
        Only if True socket can be connected

    port : string
        Port used to connect the socket

    ip : string
        IP used to connect the socket
    
    """
    topic = topic
    client = nep.client( master_ip, master_port, transport = "ZMQ", debug = False)
    time.sleep(.01)
    message = {
            'node':node,
            'topic':topic,
            'mode':mode,
            'socket':socket,
            'pid':pid
              }
    
    client.send_info(message)
    response = client.listen_info()
    try:
        topic_id = response['topic']

        if(topic_id == topic):
            port = response['port']
            if "ip" in response:
                ip = response['ip']
            else:
                ip = '127.0.0.1'
            state = response['state']
            if state == "success":
                return True, port, ip
            else:
                print ("NEP ERROR: wrong socket configuration")
                return False, port, ip
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print ("NEP ERROR: wrong response from master")
        return False, "none", "none"

    print ("NEP ERROR: wrong topic from master")
    return False, "none", "none"

def getNEPpath():
    """ Get path to NEP Workspace

    Returns
    ----------

    path : string
        Current workspace path

    """
    import os
    return os.environ['NEP_WS']

def getPath():
    return os.getcwd()


def setNEPpath(new_path):
    """ Set path to NEP Workspace

    Parameters
    ----------

    new_path: string
        New path for NEP workspace

    """
    import os

    if os.environ.get('OS','') == 'Windows_NT':
        from subprocess import CREATE_NEW_CONSOLE
        command = 'setx NEP_WS "' + new_path + '"'
        Popen(command, creationflags=CREATE_NEW_CONSOLE)
        
    os.environ["NEP_WS"] = new_path


def getMyIP():
    """ Get current IP address of the PC

    Returns
    ----------

    ip : string
        Current IP

    """
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    cw_ip = s.getsockname()[0]
    s.close()
    return str(cw_ip)

def json2dict(s, **kwargs):
    """Convert JSON to python dictionary. See jsonapi.jsonmod.loads for details on kwargs.
     
        Parameters
        ----------
        s: string
            string with the content of the json data

        Returns:
        ----------
        dict: dictionary
            dictionary with the content of the json data
    """

    if sys.version_info[0] == 3:
        return simplejson.loads(s, **kwargs)

    else:
        if str is unicode and isinstance(s, bytes):
            s = s.decode('utf8')
    
    return simplejson.loads(s, **kwargs)

def dict2json(o, **kwargs ):
    """ Load object from JSON bytes (utf-8). See jsonapi.jsonmod.dumps for details on kwargs.
     
        Parameters
        ----------
        o: dictionary
            dictionary to convert
            

        Returns:
        ----------
        s: string
            string in json format

    """
        
    if 'separators' not in kwargs:
        kwargs['separators'] = (',', ':')
        
    s = simplejson.dumps(o, **kwargs)

    import sys
    if sys.version_info[0] == 3:
        if isinstance(s, str):
            s = s.encode('utf8')

    else:
        if isinstance(s, unicode):
            s = s.encode('utf8')
        
    return s

def read_json(json_file):
    """ Read a json file and return a string 
        
        Parameters
        ----------
        json file:string
            Path +  name + extension of the json file

        Returns:
        ----------
        json_data: string
            string with the content of the json data

    """
    json_data = open (json_file).read()
    return json_data

def getFiles(path):
    """ Get a list of files that are inside a folder
        
        Parameters
        ----------
        path: string
            path of the folder

        Returns:
        ----------
        onlyfiles: list 
            list of strings with the name of the files in the folder

    """
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    print ("Available primitives:" +  str(onlyfiles))
    return onlyfiles
