#!/usr/bin/env python3

import sys

def calc(workId, salary):
    try:
        money = int(salary)
    except:
        print("Parameters Error")
    get_money = money * 0.835
    over_money = get_money - 3500
    if over_money <= 0:
        cal = 0
    elif over_money <= 1500:
        cal = over_money * 0.03
    elif over_money <= 4500:
        cal = over_money * 0.1 - 105
    elif over_money <= 9000:
        cal = over_money * 0.2 - 555
    elif over_money <= 35000:
        cal = over_money * 0.25 - 1005
    elif over_money <= 50000:
        cal = over_money * 0.3 -2775
    elif over_money <= 80000:
        cal = over_money * 0.35 - 5505
    else:
        cal = over_money * 0.45 - 13505

    get_money -= cal
    print("{}:{:.2f}".format(workId, get_money))

if __name__ == '__main__':
    params = sys.argv[1:]
    for param in params:
        paramlist = param.split(":")
        calc(paramlist[0], paramlist[1])
