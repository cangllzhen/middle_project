import struct
import json

def msg_process(msg):
    body = json.dumps(msg)
    headPack = struct.pack("!I", body.__len__())
    return headPack + body.encode()



