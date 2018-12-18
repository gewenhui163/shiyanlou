#!/usr/bin/env python3

import sys

salary = sys.argv[1]

try:
	money = int(salary)
	over_money = money - 3500
except:
	print("Parameters Error")

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
print("{:.2f}".format(cal))	
