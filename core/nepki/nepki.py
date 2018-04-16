import nep
from random import randint

class nepki():
    def __init__(self):
        print ("New BT class created")
        self.exit = True
        self.next = False
        self.r = interaction()

    def tick(self,node, activate = False):
        node_type = node["node"]
        
        if activate: #If next nodes need to be actived
            start = time.time()
            node["state"] = "active"
            if node_type == "until_success":
                node["n"] = 0
            if "children" in node:
                children = node["children"]
                for child in children:
                    self.tick(child,activate)
            return "success"
            end = time.time()
            elapsed = end - start
            print ("Nodes actived in :" + str(elapsed) + " seconds")

        if not node["state"] == "inactive":
        #if node["state"] == "active" or node["state"] == "running" or node["state"] == "loop":
            
            if node_type == "sequence":
                return self.run_sequence(node,activate)

            elif node_type == "selector":
                return self.run_selector(node,activate)

            elif node_type == "action":
                return self.run_action(node)

            elif node_type == "condition":
                return self.run_condition(node)

            elif node_type == "random_selector":
                return self.run_random_selector(node,activate)

            elif node_type == "always_failure":
                return self.run_always_failure(node,activate)

            elif node_type == "until_success":
                return self.run_until_success(node,activate)


    def run_until_success(self,node,activate):
        children = node["children"]
        if activate == True:
            node["n"] = 0
        child = children[0]
        n_max = node["max"]
        n_times = node["n"]
        if (n_times < n_max):
            if node["state"] == "loop":
                print ("loop")
                print (n_times)
                self.tick(child,True) #Activation

            response = self.tick(child,False) #Execution
            print ("until success response " + str(response))
            if response == "failure":
                node["n"] = node["n"] + 1
                self.set_node_running(node) #TODO: Esta y la siguiente linea casuo confusion
                node["state"] = "loop" # TODO: Loop simpre debe ir luego de un ser node state, mejor has un set loop
                return "running"
            elif response == "running":
                self.set_node_running(node)
                return "running"
            elif response == "success":
                self.set_node_success(node)
                return "success"
            print (child)
            
        else:
            self.set_node_success(node)
            return "success"

    def run_always_failure(self,node,activate):
        children = node["children"]
        child = children[0]
        response = self.tick(child, activate)
      
        if response == "running":
            self.set_node_running(node)
            return response
        else:
            self.set_node_failure(node)
            return "failure"
        return "error"

    def run_random_selector(self,node,activate):
        children = node["children"]
        if node["n"] == "none":
            n_child = len(children)
            n_selected = randint(0, n_child-1)
            node["n"] = n_selected 
        response = self.tick(children[node["n"]],activate)
        if response == "running":
            self.set_node_running(node)
            return response
        elif response == "success":
            self.set_node_success(node)
            node["n"] = "none"
            return response
        elif response == "failure":
            self.set_node_failure(node)
            node["n"] = "none"
            return response 

    def run_condition(self,node):
        response = self.r.check_condition(node)
        print (node)
        print ("condition response: " + response) 
        if response == "failure":
            self.set_node_failure(node)
        elif response == "success":
            self.set_node_success(node)
        return response

    def run_action(self,node):
        print ("-------- Action ---------")
        response = self.r.research(node)
        if response == "running":
            self.set_node_running(node)
        elif response == "failure":
            self.set_node_failure(node)
        elif response == "success":
            self.set_node_success(node)
            print (node)
        elif response == "error":
            self.set_node_error(node)
        return response
        

    def set_node_running(self,node):
        # Set the node with running state
        node["state"] = "running"
        node["status"] = "running"

    def set_node_success(self,node,memory=False):
        # Set the node with succeess state
        if memory:
            node["state"] = "active"
        else:
            node["state"] = "inactive"
        node["status"] = "success"

    def set_node_failure(self,node,memory=False):
        # Set the node with succeess state
        if memory:
            node["state"] = "active"
        else:
            node["state"] = "inactive"
        node["status"] = "failure"

    def set_node_error(self,node,memory=False):
        # Set the node with error state
        print ("ERROR: in")
        print (node)
        if memory:
            node["state"] = "active"
        else:
            node["state"] = "inactive"
        node["status"] = "error"


    def run_sequence(self,node,activate):
        children = node["children"]
        memory = False
        
        for child in children:
            if "memory" in children:
                memory = child["memory"] # Memory can have True or False values
                if memory: #If child (sub-BT) need to be always checked (has memory?)
                    self.tick(child,True) # Reset sub-BT
            response = self.tick(child,activate) # Get response from child

            if response == "success":
                pass
            elif response == "running":
                self.set_node_running(node) #Set parent in "running"
                return response # Return exit and "running" state
            elif response == "failure":
                self.set_node_failure(node,memory)
                return  response
            elif response == "error":
                self.set_node_error(node,memory)
                return response
        self.set_node_success(node,memory)
        return "success"

    def run_selector(self,node,activate):
        children = node["children"]
        memory = False
        for child in children:
            if "memory" in children:
                memory = child["memory"] # Memory can have True or False values
                if memory: #If child (sub-BT) need to be always checked (has memory?)
                    self.tick(child,True) # Reset sub-BT
            response = self.tick(child,activate) # Get response from child

            if response == "success":
                self.set_node_success(node,memory) 
                return  response
            elif response == "running":
                self.set_node_running(node) #Set parent in "running"
                return response # Return exit and "running" state
            elif response == "failure":
                pass
            elif response == "error":
                self.set_node_error(node,memory)
                return response
        self.set_node_failure(node,memory)
        return "failure"
