# poker_desk.py

from socket import *
import select
from port import *
from time import sleep
from poker_duch import *


class PokerDesk(object):
    '''桌子类 处理玩家进出 控制游戏流程'''
    def __init__(self, s, db, rlist, num):
        self.desknum = str(num)  # 桌号
        self.db = db
        self.cr = db.cursor()
        self.sockfd = s
        self.rlist = rlist
        self.player = {}  # 包含座号玩家名的字典
        self.chip = {}  # 包含玩家名筹码的字典
        self.fd_name = {}  # 包含套接字玩家名的字典
        self.master = ''  # 房主信息
        self.start = 0  # 游戏开始与否标志
        self.offline = []  # 游戏中掉线玩家

    def new_coming(self, temp):
        '''处理当有新玩家进入的情况'''
        client, addr = temp.accept()
        name = client.recv(128).decode()
        self.rlist.append(client)
        # 如果房间已满 不再允许进入
        if len(self.rlist) > 9 or self.start == 1:
            msg = 'F'+str(self.start)
            client.send(msg.encode())
            self.rlist.remove(client)
            client.close()
            return
        # 如果为第一人 直接定义为房主
        elif len(self.rlist) == 2:
            self.master = name
            self.player['master'] = '*' + name
        print(name, '进入')
        # 分配座位 更新字典
        for i in range(1, 9):
            if i not in self.player:
                self.player[i] = name
                break
        self.fd_name[client] = name
        nameDict = "R %s" % self.player
        self.do_tel(nameDict)
        sql = 'select money from player where name=%s'
        self.cr.execute(sql, [name])
        chip = self.cr.fetchone()[0]
        self.chip[name] = chip
        # 给其他玩家发送进房消息
        msg = '# %s进入了%s号桌,筹码%d' % (name, self.desknum, chip)
        self.do_tel(msg, client)

    def do_tel(self, msg, c=None):
        '''给所有玩家发送信息'''
        for r in self.rlist:
            if r is self.sockfd or r is c:
                continue
            r.send(msg.encode())
        sleep(0.1)

    def do_out(self, client, offline=False):
        '''处理玩家退出'''
        name = self.fd_name[client]
        # 在座位字典和套接字字典中清除
        for n in self.player:
            if self.player[n] == name:
                del self.player[n]
                break
        del self.fd_name[client]
        del self.chip[name]
        # 在IO事件列表中清除 如果为房主 轮换至下一人
        if not offline:
            index = self.rlist.index(client)
            self.rlist.remove(client)
            if len(self.rlist) == 1:
                self.start = 0
                self.master = ''
            elif name == self.master:
                self.master = self.fd_name[self.rlist[index]]
                self.player['master'] = '*' + self.master
        # 关闭该玩家收发套接字 给其他玩家发消息
        client.close()
        nameDict = "R %s" % self.player
        self.do_tel(nameDict)
        self.do_tel('# %s退出了房间' % name)

    def do_start(self):
        '''游戏开始 发牌'''
        self.handcard_dict = {}  # 手牌
        self.bet_dict = {}  # 游戏中玩家筹码
        self.fold_dict = {}  # 弃牌玩家筹码
        self.circle = 0  # 圈数，用于流程控制
        self.bet_client = ''  # 正在下注的玩家(套接字)
        self.playing_seat = list(self.player.keys())  # 现存玩家座号列表
        self.begin_seat = self.__key(self.master, self.player)
        # 游戏开始 将开始标志设为1 根据玩家人数发牌 压底注
        self.start = 1
        self.do_tel("Rc %s" % self.bet_dict)
        self.do_tel('# 游戏开始')
        player_num = len(self.fd_name)
        self.duch = Poker_duch(player_num)
        self.show_desk = self.duch.show_desk()
        h = iter(self.duch.player_deck)
        for client in self.fd_name:
            handcard = next(h)
            msg = 'Rh ' + ' &'.join(handcard)
            client.send(msg.encode())
            name = self.fd_name[client]
            self.handcard_dict[name] = handcard
            self.bet_dict[name] = 100
        sleep(0.1)
        self.do_play()

    def do_play(self):
        '''控制游戏流程'''
        print(self.bet_dict,self.circle)
        if self.circle == 0:
            self.do_bet(self.begin_seat)
        else:
            self.begin_seat = self.next_player(self.begin_seat)
            self.circle = 0
            self.bet_client = ''
            try:
                show_desk = next(self.show_desk)
            except StopIteration:
                self.do_win()
                return
            msg = 'Rd ' + ' &'.join(show_desk)
            self.do_tel(msg)
            self.do_bet(self.begin_seat)

    def do_bet(self, seat, check=False):
        '''根据座号发送下注信息'''
        name = self.player[seat]
        temp = self.__key(name, self.fd_name)
        self.bet_client = temp
        if temp in self.offline:
            self.do_fold(temp)
            return
        if not check:
            temp.send(b'B ')
        else:
            temp.send(b'Bs')

    def next_player(self, n=None):
        '''确定下一名下注玩家的座号'''
        if not n:
            name = self.fd_name[self.bet_client]
            next_seat = self.__key(name, self.player) + 1
        else:
            next_seat = n
        while True:
            if next_seat == 9:
                next_seat = 1
            if next_seat == self.begin_seat:
                self.circle += 1
            if next_seat in self.playing_seat:
                break
            next_seat += 1
        return next_seat

    def do_betmessage(self, data, client):
        '''处理玩家下注信息'''
        player_name = self.fd_name[client]
        # 处理加注
        if data[1] == 'a':
            try:
                money = int(data[2:].strip())
            except:
                client.send('# 金额输入有误'.encode())
                return
            money_all = money + self.bet_dict[player_name]
            if money_all < max(self.bet_dict.values()):
                client.send('# 金额低于上一个玩家,请重新输入'.encode())
                return
            msg = '# %s加注%d' % (player_name, money)
            self.do_tel(msg, client)
            self.bet_dict[player_name] = money_all
            self.do_tel("Rc %s" % self.bet_dict)
            print(self.bet_dict,self.circle)
            client.send(b'O')
            sleep(0.1)
            next_player = self.next_player()
            if len(set(self.bet_dict.values())) == 1 and self.circle > 0:
                self.do_play()
            else:
                self.do_bet(next_player)
        # 处理跟注
        elif data[1] == 'r':
            if self.bet_dict[player_name] == max(self.bet_dict.values()):
                client.send('# 您无法选择跟注,请重新输入'.encode())
                return
            money = max(self.bet_dict.values()) - self.bet_dict[player_name]
            msg = '# %s跟注%d' % (player_name, money)
            self.do_tel(msg, client)
            self.bet_dict[player_name] += money
            self.do_tel("Rc %s" % self.bet_dict)
            print(self.bet_dict,self.circle)
            client.send(b'O')
            sleep(0.1)
            next_player = self.next_player()
            if len(set(self.bet_dict.values())) == 1 and self.circle > 0:
                self.do_play()
            else:
                self.do_bet(next_player)
        # 处理看牌
        elif data[1] == 'h':
            if player_name != self.player[self.begin_seat] and self.circle ==0:
                client.send('# 您无法选择看牌,请重新选择'.encode())
                return
            self.do_bet(self.next_player(), True)
        elif data[1] == 'y':
            self.do_tel('# %s同意看牌' % player_name)
            client.send(b'O')
            sleep(0.1)
            next_player = self.next_player()
            if len(set(self.bet_dict.values())) == 1 and self.circle > 0:
                self.do_play()
            else:
                self.do_bet(next_player, 1)
        # 处理弃牌
        elif data[1] == 'f':
            self.do_fold(client)

    def do_fold(self, client):
        '''处理弃牌'''
        player_name = self.fd_name[client]
        self.fold_dict[player_name] = self.bet_dict[player_name]
        del self.bet_dict[player_name]
        player_seat = self.__key(player_name, self.player)
        self.playing_seat.remove(player_seat)
        self.do_tel('# %s选择了弃牌' % player_name)
        if client not in self.offline:
            client.send(b'O')
        if len(self.playing_seat) == 2:
            self.do_win()
            return
        sleep(0.1)
        next_player = self.next_player()
        if player_seat == self.begin_seat:
            self.begin_seat = next_player
        if len(set(self.bet_dict.values())) == 1 and self.circle > 0:
            self.do_play()
        else:
            self.do_bet(next_player)
        print('弃牌')

    def do_playingout(self, client):
        '''处理玩家游戏中掉线'''
        name = self.fd_name[client]
        index = self.rlist.index(client)
        self.rlist.remove(client)
        if name == self.master:
            self.master = self.fd_name[self.rlist[index]]
            self.player['master'] = '*' + self.master
        self.offline.append(client)
        self.do_tel('# %s离线' % name)
        if client == self.bet_client:
            self.do_fold(client)

    def do_win(self):
        hand_dict = {}
        for name in self.bet_dict:
           hand_dict[name] = self.handcard_dict[name]
        win_list = self.duch.max_hand(hand_dict)
        self.do_tel('# %s是赢家' % ' '.join(win_list))
        all_money = sum(self.bet_dict.values()) + sum(self.fold_dict.values())
        self.do_end()

    def do_end(self):
        del self.handcard_dict  # 手牌
        del self.bet_dict  # 游戏中玩家筹码
        del self.fold_dict  # 弃牌玩家筹码
        del self.circle  # 圈数，用于流程控制
        del self.bet_client  # 正在下注的玩家(套接字)
        del self.playing_seat  # 现存玩家座号列表
        del self.begin_seat
        self.do_tel('E ')
        self.start = 0
        for client in self.offline:
            self.do_out(client, True)
        self.offline = []

    def __key(self, value, dict):
        '''通过字典的值取键 须确保值的唯一性'''
        for n in dict:
            if dict[n] == value:
                return n


        

        
        
            



    










