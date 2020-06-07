# -*- encoding:utf8 -*-

import multiprocessing
import subprocess
import os

path = os.getcwd()

def subProcess(cmd):
    fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
    data = fd_popen.read().strip()
    fd_popen.close()
    return data

def icmpscan(myIP_range3, anotherip_list, networkIP):
    print('==icmp scan start==')
    pool_size = 255

    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()

    pool = [ multiprocessing.Process(target=pinger, args=(jobs,results))
             for i in range(pool_size) ]

    for p in pool:
        p.start()

    for i in range(0,255):
        if '192.168.{0}'.format(i) != myIP_range3:
            jobs.put('192.168.{0}.254'.format(i))
            jobs.put('192.168.{0}.1'.format(i))
        else:
            print('my ip range = 192.168.{0}'.format(i))
    print('jobs.put = 192.168.(0~254)')

    for i in range(16,32):
        for j in range(0, 10):
            if '172.{0}.{1}' != myIP_range3:
                jobs.put('172.{0}.{1}.254'.format(i,j))
                jobs.put('172.{0}.{1}.1'.format(i,j))
                # print('jobs.put = 172.{0}.{1}'.format(i,j))
            else:
                print('my ip range = 172.{0}.{1}'.format(i,j))
    print('jobs.put = 172.(16~31).(0~9)')

    for i in range(16,32):
        for j in (10, 254, 10):
            if '172.{0}.{1}' != myIP_range3:
                jobs.put('172.{0}.{1}.254'.format(i,j))
                jobs.put('172.{0}.{1}.1'.format(i,j))
                # print('jobs.put = 172.{0}.{1}'.format(i,j))
            else:
                print('my ip range = 172.{0}.{1}'.format(i))
    print('jobs.put = 172.(16~31).(10,20,..250)')

    for i in range(0,10):
        for j in range(0,10):
            if '10.{0}.{1}' != myIP_range3:
                jobs.put('10.{0}.{1}.254'.format(i,j))
                jobs.put('10.{0}.{1}.1'.format(i,j))
                # print('jobs.put = 10.{0}.{1}'.format(i,j))
            else:
                print('my ip range = 10.{0}.{1}'.format(i))

        for j in range(10,254,10):
            if '10.{0}.{1}' != myIP_range3:
                jobs.put('10.{0}.{1}.254'.format(i,j))
                jobs.put('10.{0}.{1}.1'.format(i,j))
                # print('jobs.put = 10.{0}.{1}'.format(i,j))
            else:
                print('my ip range = 10.{0}.{1}'.format(i))
    print('jobs.put = 10.(0~9).(0~9, 10,20,...250)')

    for i in range(10,254,10):
        for j in range(0,10):
            if '10.{0}.{1}' != myIP_range3:
                jobs.put('10.{0}.{1}.254'.format(i,j))
                jobs.put('10.{0}.{1}.1'.format(i,j))
                # print('jobs.put = 10.{0}.{1}'.format(i,j))
            else:
                print('my ip range = 10.{0}.{1}'.format(i))

        for j in range(10,254,10):
            if '10.{0}.{1}' != myIP_range3:
                jobs.put('10.{0}.{1}.254'.format(i,j))
                jobs.put('10.{0}.{1}.1'.format(i,j))
                # print('jobs.put = 10.{0}.{1}'.format(i,j))
            else:
                print('my ip range = 10.{0}.{1}'.format(i))
    print('jobs.put = 10.(10,20,..250).(0~9, 10,20,...250)')

    for p in pool:
        jobs.put(None)
    print("job.put complete")

    for p in pool:
        p.join()
    print("p.join complete")

    while not results.empty():
        ip = results.get()
        print('Other net GW ip :\t' + ip )
        ac_ttl_str = ttl_check(ip)
        print('ac_ttl_str : ', ac_ttl_str)
        if ac_ttl_str == '' or ac_ttl_str is None:
            print('ac_ttl == "" : ', ac_ttl )
        else:
            print('ac_ttl_str : ', ac_ttl_str)
            ac_ttl = int(ac_ttl_str)
            if 32 - ac_ttl >= 0:
                ac_ttl_chai = 32 - ac_ttl
            elif 64 - ac_ttl >= 0:
                ac_ttl_chai = 64 - ac_ttl
            elif 128 - ac_ttl >= 0:
                ac_ttl_chai = 128 - ac_ttl
            elif 255 - ac_ttl >= 0:
                ac_ttl_chai = 255 - ac_ttl
            else:
                print('ac_ttl > 255 : ', ac_ttl )


        with open(path + "\scan_result\\result.txt", "a") as f:
            f.write('OtherNet :\t' + ip + '\t\t\r\n')

        anotherip_list.append({'ac_ip':ip, 'ac_ttl':ac_ttl_chai, 'ac_os':'', 'ac_name':'', 'mynet':'n'})
        networkIP['anotherip'] = anotherip_list


def pinger( job_q, results_q ):
    DEVNULL = open(os.devnull,'w')
    while True:
        ip = job_q.get()
        if ip is None: break

        try:
            subprocess.check_call(['ping',ip], stdout=DEVNULL)
            results_q.put(ip)
        except:
            pass

def ttl_check( ip ):
    cmd = ['ping', ip]
    try:
        result_ping = subProcess(cmd)
        result_ping_str = str(result_ping)
        ttl_value = result_ping_str.split('TTL=')[1].split('\\r\\n')[0]
        # print('ttl_value : ', ttl_value)
        return ttl_value
    except Exception as e:
        ttl_value = ''
        return ttl_value
        print(str(e))

def trace_check( ip ):
    cmd = ['tracert', ip]
    try:
        result_tracert = subProcess(cmd)
        result_tracert_str = str(result_tracert)
        trace_list = result_tracert_str.split('\\r\\n')
        for line in trace_list:
            print(line)

    except Exception as e:
        print(str(e))


# if __name__ == '__main__':
#     ttl_check('10.10.0.251')
