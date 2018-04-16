import nep

node = nep.node("sub")
conf = node.conf_sub(network = "direct")
sub = node.new_sub("test", conf)
while True:
    s, msg = sub.listen_string()
    if s:
        print (msg)

