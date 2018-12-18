#!/usr/bin/env python3

import sys
import csv
from multiprocessing import Process, Queue

#数据通讯
queue = Queue()

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
        self.rate = float(configobj.get_config('YangLao'))+float(configobj.get_config('YiLiao'))+float(configobj.get_config('ShiYe'))+float(configobj.get_config('GongShang'))+float(configobj.get_config('ShengYu'))+float(configobj.get_config('GongJiJin'))
        #print("rate:{}".format(self.rate))
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
        return ['{:.2f}'.format(shebao), '{:.2f}'.format(geshui), '{:.2f}'.format(on_sal)]

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
        self.args = sys.argv[1:]

    def get_filename(self):
        if len(self.args) == 6:
            cindex = self.args.index('-c')
            configfilename = self.args[cindex+1]
            dindex = self.args.index('-d')
            userfilename = self.args[dindex+1]
            oindex = self.args.index('-o')
            outfilename = self.args[oindex+1]
            return [configfilename, userfilename, outfilename]
        else:
            print("Parameter Error")

def q1(userfile):
    user = UserData(userfile)
    queue.put(user)
    print('user_in:')
    print(user)
def q2(configfile):
    userdata = queue.get([False,3])
    print('user_out:')
    print(userdata)
    config = Config(configfile)
    newdata = Result(config,userdata).result()
    queue.put(newdata)
    print('newdata_in:')
    print(newdata)
def q3(outfile):
    newdata1 = queue.get([False,3])
    print('newdata_in:')
    print(newdata)
    with open(outfile,'w') as f:
            csv.writer(f).writerows(newdata1)

def main(file1,file2,file3):
    p1 = Process(target=q1,args=(file1,))
    p2 = Process(target=q2,args=(file2,))
    p3 = Process(target=q3,args=(file3,))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

if __name__ == '__main__':
    args = Args()
    files = args.get_filename()
    #print(files)
    main(files[1],files[0],files[2])
