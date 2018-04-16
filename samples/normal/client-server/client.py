import nep 
import time 

client = nep.client('127.0.0.1', 8010, 'normal') # Create a new client instance

while True:
    msg = "hello server" # Message to send as request
    client.send_info(msg)   # Send request
    print (client.listen_info()) # Wait for server response
    time.sleep(1) # Wait one second
