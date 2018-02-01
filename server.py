#!/usr/bin/python
#
# Flask server, woo!
#

import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()
from flask import Flask, request, redirect, url_for, send_from_directory, Response
import platform
import os
import re
import subprocess
import thread
import time
import nep
import simplejson
import requests





def onDeviceLaunch(params):
    """Launch a sensory device node"""
    print "Device execution request"
    list_devices = params.split(",")

    if ("smartwatch_gestures" in list_devices):
        
        device = "smartwatch"
        perception = "smartwatch_gestures"
        lan.nep_launch("sensing", device)
        lan.nep_launch("perception", perception)


#TODO: improve this approach
def onRunCode(data):
    code = data['input']

    print 
    print "***Code execution request***"
    try:
        print code
    except: 
        print "The visualization of some characters are not soported in for operating system, or are not installed"

    print os.getcwd()
    file = open("cognitive_node.py","w") 
    file.write(code.encode("UTF-8")) 
    file.close() 
    time.sleep(.5)
    lan.launch("cognitive_node.py") 


def onRobotLaunch(node_name,robot_name, robot_ip):
    """Action engine execution request"""
    
    print "connecting with the action engine: " +  node_name
    lan.nep_launch("action", node_name, robot_name, robot_ip)


def onCodeStop():
    
    dic = {'action': "stop"}
    pub_exit.send_info(dic)
    print "kill sended"


def onSaveFiles(data):
    
    
    project_name = data['name']
    how = data['how']
    path = os.getcwd()

    #Create the projects folder if was delated
    path_projects = path + "/static/projects"
    if not os.path.exists(path_projects):
        os.makedirs(path_projects)

    #Create a new project of not exists
    path_projects = path_projects + "/"
    print path_projects
    if not os.path.exists(path_projects + project_name):
        os.makedirs(path_projects + project_name)
        print ("New project created")
    else:
        print ("Error creating a new project: the name of the project already exists")

    try:
        path_projects = path + "/static/projects/"
        code = data['code']
        xml = data['xml']

        name_file = "blocks.xml"
        if how == "auto":
            name_file = "recover_blocks.xml"

        xml_file = open(path_projects + project_name +  "/" +  name_file , "w")
        py_file = open(path_projects + project_name + "/code.py", "w")
        print xml
        xml_file.write(xml)
        py_file.write(code)
        xml_file.close()
        py_file.close()
        print ("Code and XML saved for project: " +  project_name)
    except:
        pass
    finally:
        os.chdir(global_path)




# Setup Flask app.
app = Flask(__name__)
#app.debug = True

# Routes
@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)


@app.route('/new_action', methods=['GET', 'POST'])  # Changed SET to POST here
def new_action():
    print ("*********************")
    if request.method == 'POST':
        print ("New HTTP POST request")
        content = request.get_json(silent=True)
        data =  content
        print "New data: " + str(data)

        # Split the action to do and the parameters
        action_to_do = data['action']

        #TODO improve this part
        print "action to do: " + action_to_do
        if (action_to_do == "stop"):
            onCodeStop()
        if (action_to_do == "run"):
            thread.start_new_thread ( onRunCode, (data,)) #Here the parameter is the code to run
        if (action_to_do == "launch_action"):
            node_name = data['node_name']
            robot_name = data['robot_name']
            robot_ip = data['robot_ip']
            thread.start_new_thread ( onRobotLaunch, (node_name,robot_name,robot_ip))
        if (action_to_do == "launch_nodes"):
            nodes = data['nodes_to_launch']
            thread.start_new_thread ( onDeviceLaunch, (nodes,))
        if (action_to_do == "save"):
            thread.start_new_thread ( onSaveFiles, (data,))

        if (action_to_do == "load"):
            # Send a list of project in the static/projects path
            list_projects = os.listdir("static/projects")
            print "Projects"
            print list_projects

            result = {'projects': list_projects}
            return simplejson.dumps(result)


        
        return "POST request wet it!"

    elif request.method == 'GET':
        print ("New HTTP GET request")

        return "GET request wet it!"
    return "The request is not defined in the server"

def event_stream():
    
    while True:
        gevent.sleep(1)
        success, state =  status_sub.listen_info(False)
        if success:
            node_type = str(state['node_type'])
            node_status = str(state['node_status'])
            if node_type == 'action':
                robot_name = state['robot_name']
                message  = {'node_type':node_type, 'node_status':node_status, 'robot_name':robot_name}
                message = simplejson.dumps(message)
                yield 'data: %s \n\n' %message

            if node_type == 'main_code':
                message  = {'node_type':node_type, 'node_status':node_status}
                message = simplejson.dumps(message)
                yield 'data: %s \n\n' %message

            
        else: 
            yield 'data: null\n\n'

@app.route('/my_event_source')
def sse_request():
    return Response(
            event_stream(),
            mimetype='text/event-stream')



lan = nep.launcher()
print ("Starting NEP Master...")
lan.launch("NEP_master.py")
time.sleep(3)
print ("Starting Server ...")
import webbrowser
url = "http://127.0.0.1:5000/"
global_path = os.getcwd()

node = nep.node("RIZE_server")
sub_config = node.conf_sub(mode = "many2one")
status_sub  = node.new_sub("/node_status", sub_config)

pub_config = node.conf_pub(mode = "one2many")
pub_exit  = node.new_pub("/program_execution", pub_config)

webbrowser.open(url, new=2)
app.run(threaded=True)
