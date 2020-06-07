# -*- encoding:utf8 -*-
import os
import multiprocessing
import subprocess
from select import select
from os import getpid
from struct import pack,unpack
from socket import AF_INET
from socket import SOCK_RAW
from socket import socket
from socket import htons
import netaddr
import re
import shutil
from icmpscan import icmpscan, ttl_check
from nmap_scan import arping
from network_draw_new import network_draw

path = os.getcwd()
# myIP = ''
regex_ip= re.compile('^(1|2)?\d?\d([.](1|2)?\d?\d){3}')

#discoverIP_list =
discoverIP_dic ={'dc_ip':'', 'dc_mac':'', 'dc_vendor':'', 'dc_os':'', 'dc_name':'', 'mynet':'y'}
anotherip_dic ={'ac_ip':'', 'ac_ttl':'', 'ac_os':'', 'ac_name':'', 'mynet':'n'}
discoverIP_list = [discoverIP_dic]
anotherip_list = [anotherip_dic]
networkIP = {'myip':'', 'gwip':'', 'pubip':'', 'ttlchai':0, 'discoverip':discoverIP_list, 'anotherip':anotherip_list }

# 외부 프로그램을 실행 시키기 위함
def subProcess(cmd):
    fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
    data = fd_popen.read().strip()
    fd_popen.close()
    return data

def search_vendor(ipconfig_mac):
    with open('d:/dev/scanner/conf/mac.txt', 'r') as f_mac:
        for mac_txt in f_mac:
            mac_txt = mac_txt.strip().split('\t')
            if mac_txt[0] == ipconfig_mac:
                return mac_txt[1].split(' ')[0]
                print('test : ',mac_txt[0], "-", mac_txt[1].split(' ')[0])

def main():
    # print(path)
## 1 현재 사용중인 IP -----------------------------------------
##    netstat -n 명령어 활용
    cmd = ['netstat', '-n']
    myIP_strs = str(subProcess(cmd))
    myIP_lines = myIP_strs.split("\\r\\n")

    no_lines = 0
    myIP_list = []

    for myIP_line in myIP_lines:
        if no_lines < 3:
            pass
        else:
            myIP_net = myIP_line.split(':')[0].split()[1]
            if myIP_net == '127.0.0.1':
                print('pass : ', myIP_net)
            else:
                myIP_list.append(myIP_net)
        no_lines += 1
    myIP_list_set = list(set(myIP_list))        # myIP_list_set : 중복제거

##   ipconfig로 mac 가져오기
    cmd = ['ipconfig','/all']
    myIP_mac_strs = str(subProcess(cmd)).split(myIP_list_set[0])[0].split(':')[-4]

    myIP_mac = myIP_mac_strs.split(' ')[1].replace('\\r\\n','')
    myIP_vendor = search_vendor(myIP_mac.replace("-","")[0:6])

## write(myIP_vendor)
    with open(path + "\scan_result\\result.txt", "w") as f:
        for myIP_el in myIP_list_set:           # myIP_el : 여러개일 경우 각각 IP
            f.write('My IP :\t' + myIP_el + '\t' + myIP_mac + '\t' + myIP_vendor + '\t' + '\r\n')
    print('My IP  : ' + myIP_el)
    print('vendor : ' + myIP_vendor)
    networkIP['myip'] = myIP_el

# ## 2 현재 IP 대역 ---------------------------------------------------
    myIP_netId = myIP_el.split('.')
    myIP_range3 = myIP_netId[0] + '.' + myIP_netId[1] + '.' + myIP_netId[2]
    myIP_range4 = myIP_range3 + '.0/24'
#
# ## 3 gateway IP -----------------------------------------------------
#        ipconfig 를 사용
    myIP_el_str = str(myIP_el)
    cmd = ['ipconfig']
    gatewayIP_strs = str(subProcess(cmd))
    gatewayIP = gatewayIP_strs.split(myIP_el_str)[1].split(':')[2].split('\\r\\n')[0]
    gatewayIP = gatewayIP.replace(' ', '')
    with open(path + "\scan_result\\result.txt", "a") as f:
        f.write('GW IP :\t' + gatewayIP + '\t\t\r\n')
    print('GW IP : ' + gatewayIP)
    networkIP['gwip'] = gatewayIP

#
# ## 4 외부 공인 IPgatewayIP --------------------------------------------
    cmd = ['curl', '-4', 'icanhazip.com']
    try:
        publicIP_byte = subProcess(cmd)
        publicIP_str = publicIP_byte.decode()
        with open(path + "\scan_result\\result.txt", "a") as f:
            f.write('PubIP :\t' + publicIP_str + '\t\t\r\n')
        print('PubIP :\t' + publicIP_str)
        networkIP['pubip'] = publicIP_str
    except Exception as e:
        print(str(e))

# ## 4-1  외부 공인 까지 ttl 확인
    ttl_public = ttl_check(publicIP_str)
    print('Pub ttl : ' + ttl_public)
    with open(path + "\scan_result\\result.txt", "a") as f:
        f.write('Pub ttl :\t' + ttl_public + '\t\t\r\n')

# ## 4-2  GW IP 까지 ttl 확인
    ttl_gateway = ttl_check(gatewayIP)
    print('GW ttl  : ' + ttl_gateway)
    with open(path + "\scan_result\\result.txt", "a") as f:
        f.write('GW ttl :\t' + ttl_gateway + '\t\t\r\n')

# ## 4-3 TTL 차이
    ttl_chai = int(ttl_public) - int(ttl_gateway)
    networkIP['ttlchai'] = ttl_chai

## ## 5 nmap arp scan
    arping(myIP_range4, discoverIP_list, networkIP)

## 6 사설 IP scan
    icmpscan(myIP_range3, anotherip_list, networkIP)

## 7 네트워크 그리기
    network_draw(networkIP)


if __name__ == '__main__':
    main()
