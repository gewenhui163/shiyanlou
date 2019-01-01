#!/usr/bin/env python3

import sys, socket

def get_args():
    args = sys.argv[1:]
    try:
        host_index = args.index('--host')
        port_index = args.index('--port')
        host_val = args[host_index+1]
        port_val = args[port_index+1]

        if len(host_val.split('.')) != 4:
            raise ValueError
        else:
            host = host_val

        if '-' in port_val:
            port = port_val.split('-')
        else:
            port = [port_val, port_val]

        return host, [int(port[0]), int(port[1])]
    except (ValueError, IndexError):
        print('Paramter Error')
        sys.exit()

def scan():
    host, port = get_args()
    openlist = []
    for i in range(port[0], port[1]+1):
        s = socket.socket()
        s.settimeout(0.1)
        if s.connect_ex((host,i)) == 0:
            openlist.append(i)
            print(i, 'open')
        else:
            print(i, 'closed')

        s.close()
    #print('Computed scan. Opening ports at {openlist}')

if __name__ == '__main__':
    scan()
