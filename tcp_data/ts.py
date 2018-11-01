import struct

headerSize = 4
# 把数据存入缓冲区，类似于push数据
dataBuffer += data
def data_process(dataBuffer):
    while True:
        if len(dataBuffer) < headerSize:
            print("数据包（%s Byte）小于消息头部长度，跳出小循环" % len(dataBuffer))
            break

        # 读取包头
        # struct中:!代表Network order，3I代表3个unsigned int数据
        headPack = struct.unpack('!I', dataBuffer[:headerSize])
        bodySize = headPack[0]

        # 分包情况处理，跳出函数继续接收数据
        if len(dataBuffer) < headerSize+bodySize :
            print("数据包（%s Byte）不完整（总共%s Byte），跳出小循环" % (len(dataBuffer), headerSize+bodySize))
            break
        # 读取消息正文的内容
        body = dataBuffer[headerSize:headerSize+bodySize]

        # 数据处理
        dataHandle(headPack, body)

        # 粘包情况的处理
        dataBuffer = dataBuffer[headerSize+bodySize:] # 获取下一个数据包，类似于把数据pop出