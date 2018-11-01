# playpoker_main.py

from socket import *
import signal
import sys
from menu import *
from player_login import *


def main():
    '''用户登录注册界面'''
    sockfd = socket()
    try:
        sockfd.connect(('172.18.4.98', 8888))
    except Exception as e:
        print(e)
        return
    pln = Player_login(sockfd)
    while True:
        menu0()
        try:
            cmd = int(input('请输入选项'))
        except Exception as e:
            print('命令错误')
            continue
        if cmd not in [1, 2, 3]:
            print('请输入正确选项')
            sys.stdin.flush()
            continue
        elif cmd == 1:
            name = pln.user_login()
            if name:
                print('登录成功')
                desk_choose(name, pln)
            else:
                print('用户名或密码不正确')
        elif cmd == 2:
            pln.user_register()
        elif cmd == 3:
            sockfd.send(b'Q')
            sys.exit('谢谢使用')


def desk_choose(name, pln):
    '''选择桌号界面'''
    while True:
        # 未完成
        menu1(['1', '1', '1', '1', '1', '1', '1', '1', '1', '1'])
        try:
            cmd = input('请选择桌号(q退出)')
            dnum = int(cmd)
        except Exception as e:
            if cmd == 'q':
                return
            print(e)
            print('命令错误')
            continue
        if dnum not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]:
            print('请输入正确选项')
            sys.stdin.flush()
            continue
        else:
            sockfr = socket()
            m = pln.do_join(sockfr, name, cmd)
            if m:
                desk_run(sockfr, pln, name, cmd)
            else:
                sockfr.close()


def desk_run(sockfr, pln, name, num):
        '''开始游戏'''
        sockfr.send(name.encode())
        print('欢迎进入%s桌' % num)
        rlist = [sockfr, sys.stdin]
        while True:
            r, w, e = select.select(rlist, [], [])
            for s in r:
                if s is sys.stdin:
                    msg = sys.stdin.readline().strip()
                    if msg == 'exit':
                        sockfr.send(b'Q ')
                    elif msg == 'start':
                        sockfr.send(b'S ')
                    # elif msg == 'ff':
                    #     desk_print(name_dict)
                    elif msg[:2] == 'ca' and pln.beting in [1, 2]:
                        sockfr.send(('Ca' + msg[2:]).encode())
                    elif msg == 'r' and pln.beting == 1:
                        sockfr.send(b'Cr')
                    elif msg == 'ch' and pln.beting == 1:
                        sockfr.send(b'Ch')
                    elif msg == 'f' and pln.beting == 1:
                        sockfr.send(b'Cf')
                    elif msg == 'y' and pln.beting ==2:
                        sockfr.send(b'Cy')
                    else:
                        sockfr.send((': ' + msg).encode())
                else:
                    data = s.recv(1024).decode()
                    # try:
                    if data == '':
                        print("服务器错误")
                        sockfr.close()
                        pln.beting = 0
                        return
                    elif data[0] == '#':
                        print(data)
                    elif data[0] == 'B':
                        signal.alarm(30)
                        signal.signal(signal.SIGALRM, pln.do_fold)
                        pln.do_bet(data)
                    elif data[0] == 'O':
                        pln.beting = 0
                        print('ok')
                        signal.signal(signal.SIGALRM, signal.SIG_IGN)
                    elif data[0] == 'R':
                        pln.do_show(data)
                    elif data[0] == 'E':
                        pln.do_end()
                    elif data[0] == 'Q':
                        sockfr.close()
                        return
                    elif data[0] == 'F':
                        if data[1] == 0:
                            print('房间已满')
                        else:
                            print('游戏中')
                        return
                    # except Exception as e:
                    #     print(e)


if __name__ == '__main__':
    main()











