import nep
import time

import nep  # Import nep library
client = nep.client('127.0.0.1', '8010') # Create a new client instance

while True:
    msg = {"message":"hello server"}
    client.send_info(msg)   # Send request
    print client.listen_info() # Wait for server response
    time.sleep(.001)
