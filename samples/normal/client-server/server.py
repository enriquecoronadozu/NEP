import nep  
import time 

import nep  # Import nep library
server = nep.server('127.0.0.1', 8010, 'normal') #Create a new server instance

while True:
    msg = "hello client" # Message to send as response 
    request = server.listen_info() # Wait for client request
    print request 
    server.send_info(msg) # Send server response
