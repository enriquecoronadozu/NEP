import time
import nep

def random_selector(children, memory=False):
    # Used to define a sequence node using behavior trees
    json_ = {"node":"random_selector","children":children, "state":"active", "memory":False, "n":0}
    return json_

def until_success(children, n_max = 5, memory=False):
    # Used to define a sequence node using behavior trees
    json_ = {"node":"until_success","children":children, "state":"active", "memory":False, "n":0, "max":n_max}
    return json_
    

def always_failure(children, memory=False):
    # Used to define a sequence node using behavior trees
    json_ = {"node":"always_failure","children":children, "state":"active", "memory":False, "n":0}
    return json_
 

def action(primitives, robots):
    # Function used to specify an action from a primitive or a list of primitives.
    # The user also specify the robots where execute these asction
    if type(primitives) is list:
        message = {"node":"action", "primitives":primitives, "robots":robots, "state":"active", "memory":False, "n":0}
    else:
        message = {"node":"action", "primitives":[primitives], "robots":robots, "state":"active", "memory":False, "n":0}
    return message

def sequence(children, memory=False):
    # Used to define a sequence node using behavior trees
    json_ = {"node":"sequence","children":children, "state":"active", "memory":False, "n":0}
    return json_

def selector(children, memory=False):
    # Used to define a sequence node using behavior trees
    json_ = {"node":"selector","children":children, "state":"active", "memory":False, "n":0}
    return json_

#TODO: change in working memory and related all the type_state to primitve, and state to input
def condition(primitive,state):
    # Used to define a sequence node using behavior trees
    json_ = {"node":"condition","primitive":primitive, "input":state,"state":"active", "memory":False, "n":0}
    return json_

