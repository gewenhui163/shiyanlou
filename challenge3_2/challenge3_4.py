#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from datetime import datetime

def open_parser(filename):
    with open(filename) as logfile:
        pattern = (r''
                   r'(\d+.\d+.\d+.\d+)\s-\s-\s'  # IP 地址
                   r'\[(.+)\]\s'  # 时间
                   r'"GET\s(.+)\s\w+/.+"\s'  # 请求路径
                   r'(\d+)\s'  # 状态码
                   r'(\d+)\s'  # 数据大小
                   r'"(.+)"\s'  # 请求头
                   r'"(.+)"'  # 客户端信息
                   )
        parsers = re.findall(pattern, logfile.read())
    return parsers

def main():
    ips_dict = {}
    urls_dict = {}
    logs = open_parser('/home/gewenhui/Code/eviroment/challenge/Code/shiyanlou/challenge3_2/nginx.log')
    #print(logs[1])
    for log in logs:
        #print(log[1].split(':')[0])
        if log[1].split(':')[0] == '12/Jan/2017':
            if log[2] in ips_dict:
                ips_dict[log[2]] += 1
            else:
                ips_dict[log[2]] = 1

        if log[3] == '404':
            if log[2] in urls_dict:
                urls_dict[log[2]] += 1
            else:
                urls_dict[log[2]] = 1
    #print(urls_dict)

    ip_dict = sorted(ips_dict.items(), key=lambda item: item[1], reverse=True)[0]
    url_dict = sorted(urls_dict.items(), key=lambda item: item[1], reverse=True)[0]


    return ip_dict, url_dict


if __name__ == '__main__':
    ip_dict, url_dict = main()
    print(ip_dict, url_dict)