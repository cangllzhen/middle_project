import struct
# import json


class TcpMessage(object):
    def __init__(self):
        self.headerSize = 4
        # 把数据存入缓冲区，类似于push数据
        self.dataBuffer = bytes()

    def send(self, msg):
        body = msg.encode()
        headPack = struct.pack("!I", len(body))
        return headPack + body

    def recv(self, data):
        if not data:
            return
        self.dataBuffer += data
        while True:
            if len(self.dataBuffer) < self.headerSize:
                # print("数据包（%s Byte）小于消息头部长度，跳出小循环" % len(dataBuffer))
                break
            # 读取包头
            # struct中:!代表Network order，I代表１个unsigned int数据
            headPack = struct.unpack('!I', self.dataBuffer[:self.headerSize])
            bodySize = headPack[0]
            # 分包情况处理，跳出函数继续接收数据
            if len(self.dataBuffer) < self.headerSize+bodySize :
                # print("数据包（%s Byte）不完整（总共%s Byte），跳出小循环" % (len(dataBuffer), headerSize+bodySize))
                break
            # 读取消息正文的内容
            body = self.dataBuffer[self.headerSize:self.headerSize+bodySize]
            # 粘包情况的处理
            self.dataBuffer = self.dataBuffer[self.headerSize+bodySize:] # 获取下一个数据包，类似于把数据pop出
            return body.decode()

