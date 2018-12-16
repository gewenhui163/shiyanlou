#!/usr/bin/env python3

import sys
import csv

class Config:
    def __init__(self, configfile):
        self._config = {}
        with open(configfile) as f:
            for i in f.readlines():
                filelist = i.split('=')
                self._config[filelist[0].strip()] = filelist[1].strip()
    def get_config(self,param):
        return self._config[param]

class UserData:
    def __init__(self,userfile):
        self.userdata = []
        with open(userfile) as uf:
            userlist = list(csv.reader(uf))
            for i in userlist:
                self.userdata.append([i[0].strip(), i[1].strip()])
class Result:
    def __init__(self, configobj, userobj):
        rate = configobj.get_config('JiShuL')+configobj.get_config('JiShuH')+configobj.get_config('YangLao')+configobj.get_config('YiLiao')+configobj.get_config('ShiYe')+configobj.get_config('GongShang')+configobj.get_config('ShengYu')+configobj.get_config('GongJiJin')
        def calu(sal,rately):
            if sal <= 2193:
                shebao = 2193 * rately
            elif sal <= 16446:
                shebao = sal * rately
            else:
                shebao = 16446 * rately
            print(shebao)
            re_sal = sal - shebao - 3500
            if r_sal <= 0:
                geshui = 0
            elif r_sal <= 1500:
                geshui = r_sal * 0.03
            elif r_sal <= 4500:
                geshui = r_sal * 0.1 + 105
            elif r_sal <= 9000:
                geshui = r_sal * 0.2 + 555
            elif r_sal <= 35000:
                geshui = r_sal * 0.25 + 1005
            elif r_sal <= 55000:
                geshui = r_sal * 0.3 + 2775
            elif r_sal <= 80000:
                geshui = r_sal * 0.35 + 5505
            else:
                geshui = r_sal * 0.45 + 13505
            on_sal = sal - shebao - geshui
            return [shebao, geshui, on_sal]

        for user in userobj:
            user.extend(calu(int(user[1]),rate))
            print(user)
                



if __name__ == '__main__':
    config = Config('/home/shiyanlou/test.cfg')
   # print(config.get_config('JiShuL'))
    user = UserData('/home/shiyanlou/user.csv')
    Result(config, user.userdata)
