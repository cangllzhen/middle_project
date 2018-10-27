# poker_link.py

from port import *


class PokerLink(object):
    '''服务器类　用于处理客户端　登录注册请求'''
    def __init__(self, c, db):
        self.c = c
        self.db = db
        self.cursor = self.db.cursor()

    def do_login(self, data):
        '''处理用户登录'''
        data_list = data.split(' ')
        name = data_list[1]
        passwd = data_list[2]
        sql = 'select * from player where name=%s \
               and password=%s'
        self.cursor.execute(sql, [name, passwd])
        r = self.cursor.fetchone()
        if r is None:
            self.c.send(b'FALL')
        else:
            self.c.send(b'ok')

    def do_register(self, data):
        '''处理用户注册'''
        data_list = data.split(' ')
        name = data_list[1]
        passwd = data_list[2]
        sql = 'select * from player where name=%s'
        self.cursor.execute(sql, [name])
        r = self.cursor.fetchone()
        if r is not None:
            self.c.send('EXISTS'.encode())
            return
        sql = 'insert into player (name,password,money) values (%s,%s,%s)'
        try:
            self.cursor.execute(sql, [name, passwd, 10000])
            self.db.commit()
            self.c.send(b'ok')
        except Exception as e:
            print(e)
            self.db.rollback()
            self.c.send(b'FALL')
        else:
            print("%s注册成功" % name)

    def do_join(self, data):
        '''处理用户进房间请求'''
        data_list = data.split(' ')
        port = d_port[data_list[2]]
        # name = data[1]
        self.c.send(str(port).encode())


if __name__ == '__main__':
    print(d_port)


