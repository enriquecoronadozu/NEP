.. NEP documentation master file, created by
   sphinx-quickstart on Tue Apr 18 09:58:21 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to NEP's documentation!
===============================

Node primitives (NEP) is an open source experimental platform which allows the creation and design of social interactions with robots. 
This platform have the next main features:

* Supports Linux, Windows and OSX.
* “Easy to install”, “easy to use” and “easy to develop”.
* Uses an abstract transport layer, compatible with ROS, ZeroMQ and nanomsg (soon)
* Supports a Google blockly based enviroment for end-user programming.
* Mainly written in Python
* Robot independent


Installation
==================

This section describe how to install the platform in diferent operating systems.

Main requirements
**********************

* Python 2 for expert robot programming 

.. warning:: The NAO and Pepper SDK does not work in Python 3

* A modern web browser (Chrome, Firefox or Safari) for end-user programming

.. warning:: Internet explorer (IE) is not fully supported


Windows
**********************

* Download and install Python(x,y) from: https://python-xy.github.io/

* Download the most recent version of the NEP social robot programming platform from: https://github.com/enriquecoronadozu/NEP

* Unzip the folder and run the **install.bat** script (with double click) 


The platform have been tested in Windows 8.1 and Windows 10 and using Visual Studio Community 2013 and 2017 for the Kinect and Wii Balance Board devices.

Linux
**********************

* Download the most recent version of the NEP social robot programming platform from:

https://github.com/enriquecoronadozu/NEP

* Open the linux console and run the **install.sh** script

.. note:: Did you have problems running the script in Linux, then use the next commands:

.. code-block:: ruby

   chmod +x install.sh
   ./install.sh


Mac
**********************

* If you want use a NAO or Papper robot, then install Python the newest version of 2.7 from: https://www.python.org/downloads/

.. warning::  In Mac the NAO and Pepper SDK does not work with the default Python installation or with Anaconda


* Download the most recent version of the NEP social robot programming platform from: https://github.com/enriquecoronadozu/NEP
* Unzip the folder and with Mac Terminal run the install.sh script

.. note:: Did you have problems running the script in Mac, then use the next commands:

.. code-block:: ruby

   chmod +x install.sh
   ./install.sh


Getting started (Developer)
==================

The NEP plataform is composed by four main parts, the **core** API, the RIZE **interface**, **packages** and **nodes**

Core API
**********************

The **core** API contains a set of python methods and classes used to:

* Perform inter-procces comunications using ROS, ZeroMQ and nanomsg publish/subcriber pattern. This is done using the **comunication** class.
* Define the human and robot high level social programming primitives, which are used for design social interactions with robots. This is done using the **robot** class.
* Define the robot advanced and dynamic control programming primitives. This is done using the **robot_behaviors** class.

RIZE Interface
**********************

A Google Blocky **interface** that provide a visual programming tool in which novice and expert user can design and program robot social interactions. This is done using the JavaScript based Google Blocky API which generate python code. The generated python code uses the **robot** class (social primitives) to create and execute the interaction with robots. 


Packages
**********************

Set of third-party and user python libraries used to create nodes (basic robot functionalities or procceses). 


Nodes
**********************

Basic robot functionalities or procceses regulaly organized in a information processing based cognitive model. Most cognitive architectures have distinct modules or processor, but they regularly present the described below:


* **Sensory nodes:** Gives to the robots the ability of sense the enviroment. They are the input modalities of the robot. Examples are vision (using cameras or kinect), and audio (using kinect).
* **Perceptual nodes:** Gives to the robots the ability of understand the human actions in based to the sensory information. Examples are gesture, emotion and speech reconition.
* **Cognitive node** Gives the capacity of perform intelligent behaviors from the perceptual information obtained. Examples are decision making, dialog management, reactive and deliberative behaviors.
* **Action nodes:** Gives to the robots the ability of react to the human actions. They are the outputs of the robot. Examples are robot speech, walking, robot gestures, face expresion, among others.

These nodes or modules are necesary for the understading of the human actions and the execution of the robot behaviors. 

The sensory, perceptual and action modules can be written in python (Linux, OSX and Windows compatible) or C# (only Windows compatible). 

Robots supported (action module)
**********************

* NAO: 
* Papper  

Sensory devices supported
**********************
* Kinect V2
* Wii Balance Board (soon)
* IMU from Android smartwatches/smartphones


Methods and class index
==================
* :ref:`genindex`

Module index
==================

* :ref:`modindex`


