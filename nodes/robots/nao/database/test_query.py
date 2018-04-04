from tinydb import TinyDB, Query
import re
import ast
import json

# Search inn database 
def animation_query(name_animation):
    db = TinyDB('nao_animation_db.json')
    q = Query()
    try:
        s = db.search(q.animation == name_animation)
        names = [x.encode('UTF8') for x in s[0]['names']]
        times =  s[0]['times']
        keys =  s[0]['keys']

        print ("names: \n" + str(names))
        print
        print ("times: \n" + str(times))
        print 
        print ("keys: \n" + str(keys))
        
    except:
        print "Animation not found in database"


name_animation = raw_input("Write the name of an animation to search \n:")
animation_query(name_animation)
