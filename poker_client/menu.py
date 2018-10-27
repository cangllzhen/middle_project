# menu.py


def menu0():
    print('+========================+')
    print('|                        |')
    print('|   1.登录               |')
    print('|    2.注册              |')
    print('|     3.退出             |')
    print('|                        |')
    print('+========================+')


def menu1(L):
    print('=========================================')
    print('|                                       |')
    print('|  1.01桌(%s/8) 2.02桌(%s/8) 3.03桌(%s/8)  |' % (L[0], L[1], L[2]))
    print('|  4.04桌(%s/8) 5.05桌(%s/8) 6.06桌(%s/8)  |' % (L[3], L[4], L[5]))
    print('|  7.07桌(%s/8) 8.08桌(%s/8) 9.09桌(%s/8)  |' % (L[6], L[7], L[8]))
    print('|  0.10桌(%s/8)                          |' % L[9])
    print('|                                       |')
    print('| 输入桌号,q退出,ff刷新                 |')
    print('=========================================')


def desk_print(dict, hand, desk):
    for i in range(1, 9):
        if i not in dict:
            dict[i]=' '
    print('=====================================================')
    print('玩家1:%-15s' % dict[1], '下注：')
    print('玩家2:%-15s' % dict[2], '下注：')
    print('玩家3:%-15s' % dict[3], '下注：')
    print('玩家4:%-15s' % dict[4], '下注：')
    print('玩家5:%-15s' % dict[5], '下注：')
    print('玩家6:%-15s' % dict[6], '下注：')
    print('玩家7:%-15s' % dict[7], '下注：')
    print('玩家8:%-15s' % dict[8], '下注：')
    print('桌牌:%s 手牌:%s' % (desk, hand))
    print('*exit退出*','*ff刷新*','*房主%s输入start开始游戏*' % dict['master'])
    print('=====================================================')


if __name__ == '__main__':
    menu0()
    menu1()
    desk_print(['zhangsan', 'lisi'])







