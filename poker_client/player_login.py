# player_login.py

import getpass
from menu import *
from socket import *
import select
import sys
import signal
from tcp_m import *


class Player_login(object):
    def __init__(self, s):
        self.s = s
        self.name_dict = {}
        self.bet_dict = {' ': 0}
        self.handcard = ''
        self.deskcard = ''
        self.beting = 0
        self.tm = TcpMessage()

    def user_login(self):
        '''用户登录'''
        name = input('User:')
        passwd = getpass.getpass()
        msg = 'L {} {}'.format(name, passwd)
        self.s.send(msg.encode())
        data = self.s.recv(128).decode()
        if data == 'ok':
            return name
        else:
            return

    def user_register(self):
        '''用户注册'''
        while True:
            name = input('User:')
            passwd = getpass.getpass()
            passwd1 = getpass.getpass('Aganin:')
            if (' ' in name) or (' ' in passwd):
                print('用户名密码不允许有空格')
                continue
            if passwd != passwd1:
                print('两次密码不一致')
                continue

            msg = 'R {} {}'.format(name, passwd)
            self.s.send(msg.encode())
            data = self.s.recv(128).decode()
            print(data)
            if data == 'ok':
                print('注册成功')
                return
            elif data == 'EXISTS':
                print('用户存在')
                return
            else:
                print('注册失败')
                return

    def do_join(self, sockfr, name, num):
        '''用户进房间'''
        self.sockfr = sockfr
        msg = 'J {} {}'.format(name, num)
        self.s.send(msg.encode())
        data = self.s.recv(128).decode()
        try:
            # self.sockfr.connect(('172.18.4.98', int(data)))
            self.sockfr.connect(('127.0.0.1', int(data)))
            return 'ok'
        except Exception as e:
            print(e)
            print('进入房间失败')

    def do_show(self, data):
        '更新桌面信息'
        if data[1] == 'h':
            self.handcard = ' '.join(data.split()[1:])
        elif data[1] == 'd':
            self.deskcard = ' '.join(data.split()[1:])
        elif data[1] == 'c':
            dic = ' '.join(data.split()[1:])
            for name in eval(dic):
                self.bet_dict[name] = eval(dic)[name]
        else:
            dic = ' '.join(data.split()[1:])
            # 将字符串转为表达式
            self.name_dict = eval(dic)
            for n in self.name_dict:
                self.bet_dict[self.name_dict[n]] = 0
        desk_print(self.name_dict, self.handcard, self.deskcard, self.bet_dict)

    def do_bet(self, data):
        if data[1] == 's':
            self.beting = 2
            print('y:同意发牌/开牌,ca+金额:加注,f:弃牌')
            print('倒计时30秒')
        else:
            self.beting = 1
            print("ca+金额:加注,r:跟注,ch:发牌/开牌,f:弃牌")
            print('倒计时30秒')

    def do_end(self):
        print('游戏结束')
        self.handcard = ''
        self.deskcard = ''
        for name in self.bet_dict:
            self.bet_dict[name] = 0

    def do_fold(self, sig, frame):
        self.sockfr.send(self.tm.send('Cf'))




    

















