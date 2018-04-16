import nep
import time

node = nep.node("pub")
conf = node.conf_pub(network = "direct")
pub = node.new_pub("test", conf)
while True:
    msg = {"message":"hello world"}
    pub.send_info(msg)
    time.sleep(1)
