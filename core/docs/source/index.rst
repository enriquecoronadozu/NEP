.. NEP documentation master file, created by
   sphinx-quickstart on Tue Apr 18 09:58:21 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to NEP's documentation!
===============================

Node primitives (NEP) is an open source experimental platform which allows the creation and design of social interactions with robots. 
This platform have the next main features:

* Supports Linux, Windows and OSX.
* Designed to be "easy to install", "easy to use" and "easy to develop".
* Uses an abstract transport layer, compatible with ROS, ZeroMQ and nanomsg 
* Supports a Google blockly based enviroment for end-user programming.
* Mainly written in Python


Installation
==================

This section describe how to install the platform in diferent operating systems.

Main requirements
**********************

* Python (we recommend to install only one version of python, preferently python 2)

.. warning:: The NAO and Pepper SDK are not compatible with Python 3

* A modern web browser for end user programming (Chrome, Firefox or Safari) 

.. warning:: Internet explorer (IE) is not fully supported


Windows
**********************

* Download and install Python 2.7

.. note:: We recommend the Python (x,y) distribution:  https://python-xy.github.io/

* Download the most recent version of the NEP social robot programming platform from: https://github.com/enriquecoronadozu/NEP

* Unzip the folder and run the **install.bat** script (with double click) 

NEP have been tested in Windows 8.1 and Windows 10

Linux
**********************

* Download the most recent version of the NEP social robot programming platform from: https://github.com/enriquecoronadozu/NEP

* Open the linux console and run the **install.sh** script

.. note:: Did you have problems running the **install.sh** script in Linux, then use the next commands:

.. code-block:: ruby

   chmod +x install.sh
   ./install.sh


Mac
**********************

* If you want use a NAO or Papper robot, then install the newest version of Python 2.7 from: https://www.python.org/downloads/

.. warning::  In Mac the NAO and Pepper SDK does not work with the default Python installation or with Anaconda


* Download the most recent version of the NEP social robot programming platform from: https://github.com/enriquecoronadozu/NEP

* Unzip the folder and with Mac Terminal run the install.sh script

.. note:: Did you have problems running the **install.sh** in Mac, then use the next commands:

.. code-block:: ruby

   chmod +x install.sh
   ./install.sh


Getting started (Developer)
==================

The NEP platform is composed by four main parts, the **core** API, the RIZE **interface**, **packages** and **nodes**

Core API
**********************

The **core** API contains a set of python methods and classes used to:

* Perform inter-procces comunication mainly based in client/sever and publish/subcriber patterns. This is done using the **comunication** class.
* ...
* ...

More about middlewares and patterns supported: 

RIZE Interface
**********************

A Google Blocky based **interface** that provide a visual programming tool in which novice and expert user can design and program robot social interactions. 

More about the RIZE interface:


Packages
**********************

Set of third-party and user-defined python libraries used to create nodes (robot functionalities). 


Nodes
**********************

Basic robot functionalities or proccesesors organized in a information processing based cognitive model. Most cognitive architectures have distinct modules or processor, but they regularly present the described below:


* **Sensory nodes:** Gives to the robots the ability of sense the enviroment. They are the input modalities of the robot. Examples are vision (using cameras or kinect), and audio (using kinect).
* **Perceptual nodes:** Gives to the robots the ability of understand the human actions in based to the sensory information. Examples are gesture, emotion and speech reconition.
* **Cognitive node** Gives the capacity of perform intelligent behaviors from the perceptual information obtained. Examples are decision making, dialog management, reactive and deliberative behaviors.
* **Action nodes:** Gives to the robots the ability of react to the human actions. They are the outputs of the robot. Examplesof outputs are robot speech, walking, robot gestures, face expresion, among others.


The sensory, perceptual and action modules are written by expert programming users. Cognitive nodes can be defined by end-users to generate applications. 

Robots supported (action processors)
**********************

* NAO: 
* Papper  

Sensory devices supported
**********************
* Kinect V2
* IMU from Android smartwatches/smartphones
* Wii Balance Board (soon)


Methods and class index
==================
* :ref:`genindex`



