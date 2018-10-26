# poker_frame.py

from multiprocessing import Process
from socket import *
# import sys
# import signal
import pymysql
from poker_desk import *
from port import *


def main():
    db = pymysql.connect('localhost', 'root', '123456', 'poker')
    for num in range(10):
        p = Process(target=desk, args=(num, db))
        p.start()


def desk(num, db):
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    port = d_port[str(num)]
    sockfd.bind(('127.0.0.1', port))
    sockfd.listen(8)
    rlist = [sockfd]
    pdk = PokerDesk(sockfd, db, rlist, num)
    while True:
        r, w, e = select.select(rlist, [], [])
        for temp in r:
            if temp is sockfd:
                pdk.new_coming(temp)
            else:
                data = temp.recv(256).decode()
                if data == '':
                    if pdk.start == 0:
                        pdk.do_out(temp)
                    else:
                        pdk.do_playingout(temp) 
                elif data[0] == 'Q':
                    if pak.start == 0:
                        pdk.do_out(temp)
                    else:
                        temp.send('# 游戏中不允许退出'.encode())
                elif data[0] == 'S' and pdk.fd_name[temp] == pdk.master:
                    if pdk.start == 1:
                        temp.send('# 游戏进行中'.encode())
                        continue
                    if len(rlist) < 4:
                        temp.send('# 人数少于三人'.encode())
                        continue
                    pdk.do_start()
                elif data[0] == 'C' and pdk.start == 1:
                    pdk.do_betmessage(data, temp)
                else:
                    msg = '# %s说%s' % (pdk.fd_name[temp], data)
                    pdk.do_tel(msg)


if __name__ == '__main__':
    main()
















