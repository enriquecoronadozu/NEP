import nep
import time

import nep  # Import nep library
server = nep.server('127.0.0.1', '8010') #Create a new client instance

while True:
    msg = {"message":"hello client"}
    request = server.listen_info() # Wait for client request
    print "Request"
    print str(request) 
    server.send_info(msg) # Send server response
    time.sleep(.01)
