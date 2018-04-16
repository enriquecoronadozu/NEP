import nep

node = nep.node("pubs")
conf = node.conf_sub( mode= "many2many")
sub = node.new_sub("/leap_motion", conf )

print "start"
while True:
    s, msg = sub.listen_info()
    
    if s:
        print msg
        
