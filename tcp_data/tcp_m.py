import struct
import json


class TcpMessage(object):
    def __init__():
        self.headerSize = 4
        # 把数据存入缓冲区，类似于push数据
        self.dataBuffer = bytes()

    def send(self, msg):
        body = json.dumps(msg)
        headPack = struct.pack("!I", body.__len__())
        return headPack + body.encode()

    def recv(self, data):
        self.dataBuffer += data
        while True:
            if len(self.dataBuffer) < self.headerSize:
                # print("数据包（%s Byte）小于消息头部长度，跳出小循环" % len(dataBuffer))
                break
            # 读取包头
            # struct中:!代表Network order，3I代表3个unsigned int数据
            headPack = struct.unpack('!I', dataBuffer[:headerSize])
            bodySize = headPack[0]
            # 分包情况处理，跳出函数继续接收数据
            if len(dataBuffer) < headerSize+bodySize :
                # print("数据包（%s Byte）不完整（总共%s Byte），跳出小循环" % (len(dataBuffer), headerSize+bodySize))
                break
            # 读取消息正文的内容
            body = dataBuffer[headerSize:headerSize+bodySize]
            # 粘包情况的处理
            self.dataBuffer = self.dataBuffer[headerSize+bodySize:] # 获取下一个数据包，类似于把数据pop出
            return body.decode()

