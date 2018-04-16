import nep
import time

node = nep.node("pub")
conf = node.conf_pub(network = "direct")
pub = node.new_pub("test", conf)
while True:
    msg = "hello world"
    pub.send_string(msg)
    time.sleep(1)
