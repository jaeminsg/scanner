#! python
# -*- coding: utf-8 -*-
# PortScanProgram with nmap Library

import nmap
import time
import datetime
import os.path
import os

startTime = time.time()                # 시작 시간 기록
nm = nmap.PortScanner()                # nmap 객체 생성
hostList = ['192.168.0.5','127.0.0.1']    # 호스트 리스트 작성
portList = '1-440'                # 포트 리스트 작성
myArg = '-sS -sV -O'                # 옵션 설정
fileList = []                    # 파일 이름 저장할 리스트 생성
dirName = 'scan_result'                # 폴더 이름 지정

# 폴더 생성
if not os.path.exists('./' + dirName):        # 폴더 없을 시 폴더 생성
        os.system('mkdir ' + dirName)
        print (dirName + " directory is made\n")
else:                        # 폴더 존재 시 폴더 생성 안함
        print (dirName + " directory exists already\n")

if not os.path.isdir(dirName):            # 해당 파일이 폴더가 아닐 경우 오류 발생
        print ("Err: Same name file exists with directory name")
        exit()

# 스캔 시작
for host in hostList:
        print("scan %s ..."% host)
        result = nm.scan(host, portList, myArg)            # 스캔 수행

        ntime = str(datetime.datetime.now()).replace(':','_')    # 날짜 기록
        ntime = ntime.replace(' ','_')
        filename=ntime+'_'+host+'_result.csv'             # 파일 이름 생성

        csvFile = open('./'+dirName+'/'+filename,'w')        # 파일 열기
        try:                            # OS 정보 쓰기
                csvFile.write("os info : " +
(result['scan'][host]['osmatch'][0]['name']) + '\n')
        except:
                csvFile.write('OS : unknown\n')
        csvFile.write(nm.csv().replace(';',','))    # ms-csv형식으로 쓰기
        csvFile.close()
        fileList.append(filename)            # 파일 리스트에 목록 추가

# 결과 출력 : [2) python-nmap 체험하기]에서 사용한 코드를 그대로 사용하였다.
        for host in nm.all_hosts():
                print('\n\n------------------------result-------------------------')
                print('Host : %s ( %s)' %(host, nm[host].hostname()))
                print('State : %s' % nm[host].state())
                try:                            # OS 정보 출력
                        print('OS : '+ result['scan'][host]['osmatch'][0]['name'] + '\n')
                except:
                        print('OS : unknown\n')
                proto = 'tcp'
                print('--------')
                print('Protocol : %s' %proto)
                lport = nm[host][proto].keys()
                lport.sort()
                for port in lport:
                        print ('port : %s\tstate : %s' % (port,
                                str(nm[host][proto][port]['state'])))
                print("\n\n----------------------------------------------------------")

print("It's Finished!!")

endTime = time.time()                           # 종료 시간 기록

print("\n\n----------------------------------------------------------")
print("executed Time : " + str(endTime - startTime))     # 실행 시간 출력

print("\n\n>>>>>>>>>>> please check your result files")
print("This is your path:\n\t" + os.path.realpath(dirName) + '\n')
for fileName in fileList:                             # 생성한 파일 목록 출력
    print(fileName)
