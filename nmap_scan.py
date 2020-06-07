#! python
# -*- coding: utf-8 -*-
# PortScanProgram with nmap Library

import nmap
import time
import datetime
import os.path
import os

def arping(IP, discoverIP_list, networkIP):
    print('== arp scan start ==')
    # 스캔 시작
    # print("scan %s"% IP_range)
    startTime = time.time()                # 시작 시간 기록
    ntime = str(datetime.datetime.now()).replace(':','_')    # 날짜 기록
    ntime = ntime.replace(' ','_')

    path = os.getcwd()

    nm = nmap.PortScanner()                # nmap 객체 생성
    result = nm.scan(hosts=IP, arguments='-sn')            # 스캔 수행


    # print(ntime, result)
    with open(path + "\scan_result\\result.txt", "a") as f:
        for host in nm.all_hosts():
            discoverIP_arp = nm[host]['addresses']['ipv4']
            if nm[host]['vendor'] != {}:
                discoverMAC_arp = list(nm[host]['vendor'].keys())[0]
                discoverVendor_arp = list(nm[host]['vendor'].values())[0]
                discoverVendor_arp = discoverVendor_arp.replace(" Communications", "")
                discoverVendor_arp = discoverVendor_arp.replace(" Electronics", "")
            elif len(list(nm[host]['addresses'])) == 1:
                    discoverMAC_arp = ''
                    discoverVendor_arp = ''
            else:
                discoverMAC_arp = list(nm[host]['addresses'].values())[1]
                discoverVendor_arp = 'unknown'
            print( discoverIP_arp + '\t' + discoverMAC_arp + '\t' + discoverVendor_arp)
            f.write( 'discoverIP :\t' + discoverIP_arp + '\t' + discoverMAC_arp + '\t' + \
                discoverVendor_arp + '\r\n'  )
            discoverIP_list.append({'dc_ip':discoverIP_arp, 'dc_mac':discoverMAC_arp, \
                'dc_vendor':discoverVendor_arp, 'dc_os':'', 'dc_name':'', 'mynet':'y'})
            networkIP['discoverip'] = discoverIP_list
