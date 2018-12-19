#!/usr/bin/env python3

import getopt, sys
import csv
import queue
from multiprocessing import Process, Queue
from configparser import ConfigParser
from datetime import datetime

#数据通讯
qu1 = Queue()

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
        self.userobj = userobj
        self.rate = 0
        #self.rate = float(configobj.get_config('YangLao'))+float(configobj.get_config('YiLiao'))+float(configobj.get_config('ShiYe'))+float(configobj.get_config('GongShang'))+float(configobj.get_config('ShengYu'))+float(configobj.get_config('GongJiJin'))
        #print("rate:{}".format(self.rate))
        for i in configobj:
            if 'jishul' in i or 'jishuh' in i:
                continue
            self.rate += float(i[1])
        print("rate:{}".format(self.rate))
    def calu(self,sal,rately):

        if sal <= 2193:
            shebao = 2193 * rately
        elif sal <= 16446:
            shebao = sal * rately
        else:
            shebao = 16446 * rately
        #print(shebao)
        r_sal = sal - shebao - 3500
        if r_sal <= 0:
            geshui = 0
        elif r_sal <= 1500:
            geshui = r_sal * 0.03
        elif r_sal <= 4500:
            geshui = r_sal * 0.1 - 105
        elif r_sal <= 9000:
            geshui = r_sal * 0.2 - 555
        elif r_sal <= 35000:
            geshui = r_sal * 0.25 - 1005
        elif r_sal <= 55000:
            geshui = r_sal * 0.3 - 2775
        elif r_sal <= 80000:
            geshui = r_sal * 0.35 - 5505
        else:
            geshui = r_sal * 0.45 - 13505
        on_sal = sal - shebao - geshui
        saltime = datetime.now()
        saltimestr = saltime.strftime('%Y-%m-%d %H:%M:%S')
        return ['{:.2f}'.format(shebao), '{:.2f}'.format(geshui), '{:.2f}'.format(on_sal), saltimestr]

    def result(self):
        res = []
        for i in self.userobj:
            i.extend(self.calu(float(i[1]),self.rate))
            res.append(tuple(i))
        return res

    def outfile(self,outfile):
        data = self.result()
        #print(data)
        with open(outfile,'w') as f:
            csv.writer(f).writerows(data)

class Args:
    def __init__(self):
        #self.args = sys.argv[1:]
        self.opts, self.args = getopt.getopt(sys.argv[1:], "hC:c:d:o:", ["help"])
        print(self.opts)

    def get_filename(self):
        hflag = 0
        if len(self.opts) == 3 or len(self.opts) == 4 or len(self.opts) == 5:
            cityname = 'DEFAULT'
            for optparam in self.opts:
                if '-C' in optparam:
                    cityname = optparam[1].upper()
                if '-c' in optparam:
                    configfilename = optparam[1]
                if '-d' in optparam:
                    userfilename = optparam[1]
                if '-o' in optparam:
                    outfilename = optparam[1]
                if ('-h' in optparam or '--help' in optparam):
                    hflag = 'exist'
            return [cityname,configfilename, userfilename, outfilename, hflag]
        else:
            print("Parameter Error")

def q1(userfile):
    user = UserData(userfile).userdata
    qu1.put(user)
    #print('user_in:')
    #print(user)
def q2(configfile, cityname='DEFAULT'):
    while True:
        try:
            userdata = qu1.get(False)
        except queue.Empty:
            break
    print('user_out:')
    config_user = ConfigParser()
    config_user.read(configfile,encoding='UTF-8')
    print(config_user.sections())
    configdata = config_user.items(cityname)
    print(cityname)
    print(configdata)
    newdata = Result(configdata,userdata).result()
    qu1.put(newdata)
    print('newdata_in:')
    print(newdata)
def q3(outfile):
    while True:
        try:
            newdata1 = qu1.get(False)
        except queue.Empty:
            break
    print('newdata_in:')
    print(newdata1)
    with open(outfile,'w') as f:
        csv.writer(f).writerows(newdata1)

def main(file1,file2,file3,file4):
    p1 = Process(target=q1,args=(file1,))
    p2 = Process(target=q2,args=(file2,file3))
    p3 = Process(target=q3,args=(file4,))

    p1.start()
    p1.join()
    p2.start()
    p2.join()
    p3.start()
    p3.join()

if __name__ == '__main__':
    args = Args()
    files = args.get_filename()
    print('-----')
    print(files)
    main(files[2],files[1],files[0],files[3])
