import nep

node = nep.node("subscriber_node") # Create a new node
conf = node.conf_sub(transport ="ZMQ", mode = "many2many") # Select the configuration of the subscriber
sub = node.new_sub("many2may_test", conf) # Set the topic and the configuration of the subscriber

# Read the information published in the topic registered
while True:
    s, msg = sub.listen_string()
    if s:
        print msg

