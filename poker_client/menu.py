# menu.py


def menu0():
    '''登录界面'''
    print('+========================+')
    print('|                        |')
    print('|   1.登录               |')
    print('|    2.注册              |')
    print('|     3.退出             |')
    print('|                        |')
    print('+========================+')


def menu1():
    '''选桌界面'''
    print('=========================================')
    print('|                                       |')
    print('|  1.01桌      2.02桌      3.03桌       |')
    print('|  4.04桌      5.05桌      6.06桌       |')
    print('|  7.07桌      8.08桌      9.09桌       |')
    print('|  0.10桌                               |' )
    print('|                                       |')
    print('| 输入桌号,q退出                        |')
    print('=========================================')


def desk_print(dict, hand, desk, bet):
    '''游戏中界面'''
    for i in range(1, 9):
        if i not in dict:
            dict[i] = ' '
    print('=====================================================')
    print('玩家1:%-15s' % dict[1], '下注：%d' % bet[dict[1]])
    print('玩家2:%-15s' % dict[2], '下注：%d' % bet[dict[2]])
    print('玩家3:%-15s' % dict[3], '下注：%d' % bet[dict[3]])
    print('玩家4:%-15s' % dict[4], '下注：%d' % bet[dict[4]])
    print('玩家5:%-15s' % dict[5], '下注：%d' % bet[dict[5]])
    print('玩家6:%-15s' % dict[6], '下注：%d' % bet[dict[6]])
    print('玩家7:%-15s' % dict[7], '下注：%d' % bet[dict[7]])
    print('玩家8:%-15s' % dict[8], '下注：%d' % bet[dict[8]])
    print('桌牌:%s 手牌:%s' % (desk, hand))
    print('*exit退出*','*房主%s输入start开始游戏*' % dict['master'])
    print('=====================================================')


if __name__ == '__main__':
    menu0()
    menu1()








