import nep
import time

import nep  # Import nep library
server = nep.server('127.0.0.1', '5000') #Create a new client instance

while True:
    msg = "server response"
    request = server.listen_info() # Wait for client request
    print request 
    server.send_info(msg) # Send server response
