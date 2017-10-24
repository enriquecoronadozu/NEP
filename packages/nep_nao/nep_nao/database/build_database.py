# coding = utf-8
#!/usr/bin/env python

# ------------------------ Build database  --------------------------------
# Description: Create a databes from a list of txt files in the "animations" folder
# --------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga


from tinydb import TinyDB, Query
from os import listdir
from os.path import isfile, join
import re
import ast
import json

# Delete database
import os
import os.path

if (os.path.exists("nao_animation_db.json")):
  os.remove("nao_animation_db.json")
  print("***Database restarted!***")

# Get a list of files inside the animations folder
path = "animations"

onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
print ("Files to build database:" +  str(onlyfiles))

# Build database
print ("***Building database***")
db = TinyDB('nao_animation_db.json')
for file_ in onlyfiles:

  f = open(path  + "/" +  file_,"r")

  try:
    movement_name = file_.split(".txt")

    data =  f.read()
    names = list()
    times = list()
    keys = list()

    #Get animation elements from Choregraphe timeline/clipboard (simple mode)
    list_data =  data.split("\n\n")
    i = 0
    for parts in list_data:
        e = parts.split("\n")
        try:
          
          result = re.search('names.append\("(.*)"\)', e[0])
          name = str(result.group(1))
          result = re.search('times.append\((.*)\)', e[1])
          time = ast.literal_eval(result.group(1))
          result = re.search('keys.append\((.*)\)', e[2])
          key = ast.literal_eval(result.group(1))

          names.append(name)
          times.append(time)
          keys.append(key)
          
          
        except:
          pass
        
    # Save animation in the database
    db.insert({'animation': movement_name[0], 'names': names, 'times':times, 'keys':keys})
    print (str(movement_name[0]) + " ---> added")

  except:
    print ("Error reading file: " + str(file_))
    pass
      
print("***database build finished!***")

