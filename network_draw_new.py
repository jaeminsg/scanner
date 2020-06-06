# -*- encoding:utf8 -*-
import os
#from os import getpid
import math
import shutil
import webbrowser

path = os.getcwd()

# networkIP = {'myip': '192.168.0.5', 'gwip': '192.168.0.1', 'pubip': '211.221.184.224', 'ttlchai': 0, 'discoverip': [{'dc_ip': '', 'dc_mac': '', 'dc_vendor': '', 'dc_os': '', 'dc_name': '', 'mynet': 'y'}, {'dc_ip': '192.168.0.1', 'dc_mac': '88:36:6C:6A:96:AC', 'dc_vendor': 'EFM Networks', 'dc_os': '', 'dc_name': '', 'mynet': 'y'}, {'dc_ip': '192.168.0.10', 'dc_mac': '10:F1:F2:0C:ED:C3', 'dc_vendor': 'LG (Mobile)', 'dc_os': '', 'dc_name': '', 'mynet': 'y'}, {'dc_ip': '192.168.0.111', 'dc_mac': '', 'dc_vendor': '', 'dc_os': '', 'dc_name': '', 'mynet': 'y'}, {'dc_ip': '192.168.0.12', 'dc_mac': '90:8D:6C:23:BA:DB', 'dc_vendor': 'Apple', 'dc_os': '', 'dc_name': '', 'mynet': 'y'}, {'dc_ip': '192.168.0.13', 'dc_mac': 'C6:25:E9:35:07:D5', 'dc_vendor': 'unknown', 'dc_os': '', 'dc_name': '', 'mynet': 'y'}, {'dc_ip': '192.168.0.14', 'dc_mac': 'C2:25:E9:E2:68:E9', 'dc_vendor': 'unknown', 'dc_os': '', 'dc_name': '', 'mynet': 'y'}, {'dc_ip': '192.168.0.5', 'dc_mac': '', 'dc_vendor': '', 'dc_os': '', 'dc_name': '', 'mynet': 'y'}, {'dc_ip': '192.168.0.8', 'dc_mac': '64:C2:DE:78:34:26', 'dc_vendor': 'LG (Mobile)', 'dc_os': '', 'dc_name': '', 'mynet': 'y'}], 'anotherip': [{'ac_ip': '', 'ac_os': '', 'ac_name': '', 'mynet': 'n'}, {'ac_ip': '192.168.33.1', 'ac_os': '', 'ac_name': '', 'mynet': 'n'}, {'ac_ip': '192.168.56.1', 'ac_os': '', 'ac_name': '', 'mynet': 'n'}]}


another_list = []

# html로 망도 그리기

def html_node_write(n_id, n_label, n_image, n_size):        # 노드 생성
    with open("./output/network.html", "a") as f_network:
        text = "      nodes.push({id: " + str(n_id) + ", label: '" + str(n_label) + "', image: DIR + '" + n_image + "', size: " + str(n_size) + ", shape: 'image' });\r\n"
        print(text)
        f_network.write(text)

def html_edge_write(start_id, end_id, edge_length):                      # 연결선(edge) 생성
    with open("./output/network.html", "a") as f_network:
        f_network.write("      edges.push({from: " + "{0}, to: {1}, length: {2}".format(start_id, end_id, edge_length) + " });\r\n")

def device_check(vendor):
    if vendor in ('Apple', 'LG (Mobile)'):
        n_image = 'mobile.png'
        return(n_image)
    elif vendor in ('EFM Networks', 'EFM'):
        n_image = 'homeRouter.png'
        return(n_image)
    else:
        n_image = 'pc.png'
        return(n_image)

def network_draw(networkIP):
    print("=======network drawing==========")

    # html head 부분은 공통이므로 미리 만든 network_before.txt 화일 copy
    shutil.copy(path + "/conf/network_before.txt", path + "/output/network.html")
    # network_before copy한 화일 - network.html 화일을 열어서 내용을 추가 한다.
    with open("./output/network.html", "a") as f_network:

#       # 각 노드에는 번호를 붙인다. 1000번대 (1001:GW, 1002: 외부공인, 1003: 내 pc, 이후는 찾은 결과 )
        n_id = 0
        html_node_write(n_id, 'intranet', 'internet.png', 15)       # (id 0) 인터넷(구름 모양) 노드 그리기

#       # 발견된 같은 네트워크 IP 노드 표시하기
        discover_no = 1004
        for discover_list in networkIP['discoverip']:
            discoverIP = discover_list.get('dc_ip')
            if discoverIP == networkIP['myip']:                  # (id 1003) 내 pc
                n_id = 1003
                n_label = discoverIP + "\\r\\n" + "My PC"
                n_image = 'pc.png'
                n_size = 15
                print(n_id)
                html_node_write(n_id, n_label, n_image, n_size)
            elif discoverIP == networkIP['gwip']:                # (id 1001) GW
                if networkIP.get('ttlchai') == 0:                # (id 1001) GW 와 공인 IP가 같은 장비 일 경우
                    n_id = 1001
                    # n_label = discoverIP + "\\r\\n" + "Gateway" + "\\r\\n" + discover_list.get('dc_vendor')
                    n_label = discoverIP + "\\r\\n" + "Gateway" + "\\r\\n" + "(Public: " + networkIP['pubip'] + ")" + "\\r\\n" + discover_list.get('dc_vendor')
                    n_image = device_check(discover_list.get('dc_vendor'))
                    n_size = 15
                    print(n_id)
                    html_node_write(n_id, n_label, n_image, n_size)
                else:                                            # (id 1001, 1002) GW 와 공인 IP가 다른 장비 일 경우
                    n_id = 1001
                    n_label = discoverIP + "\\r\\n" + "Gateway"
                    n_image = 'router.png'
                    n_size = 15
                    print(n_id)
                    html_node_write(n_id, n_label, n_image, n_size)
                    n_id = 1002
                    n_label = discoverIP + "\\r\\n" + "(Public: " + networkIP['pubip'] + ")"
                    n_image = 'router.png'
                    n_size = 15
                    print(n_id)
                    html_node_write(n_id, n_label, n_image, n_size)
            elif discoverIP != '':                              # ( id 1004~ []인터넷,GW,my PC]를 제외한 모든 발견된 시스템)
                n_id = discover_no
                n_label = discoverIP + "\\r\\n" + discover_list.get('dc_vendor')
                n_image = device_check(discover_list.get('dc_vendor'))
                n_size = 15
                html_node_write(n_id, n_label, n_image, n_size)
                discover_no += 1

#       다른 대역 ip (anoter network IP) 노드 표시하기
        another_no = 3001                                       # id 2001 ~  다른 대역 id
        print(networkIP['anotherip'])
        for anotherip_list in networkIP['anotherip']:
            anotherIP = anotherip_list.get('ac_ip')
            anotherTTL = anotherip_list.get('ac_ttl')
            if anotherIP == '':
                print('vacancy anotherIP : ', anotherIP)
            elif anotherIP == '192.168.56.1' and anotherTTL == 0:
                print('my virtual IP : ', anotherIP, anotherTTL)
            elif anotherIP == '192.168.33.1' and anotherTTL == 0:
                print('my virtual IP : ', anotherIP, anotherTTL)
            else:
                if anotherTTL =='' or anotherTTL == 0:
                    n_id = another_no
                    n_label = anotherIP
                    n_image = 'router.png'
                    n_size = 15
                    html_node_write(n_id, n_label, n_image, n_size)
                    another_list.append(another_no)
                    print('if..: ', another_list)
                    another_no += 1
                elif anotherTTL >= 1 and anotherTTL < 4:
                    for i in range(1, anotherTTL+1):
                        n_id = another_no
                        if i == anotherTTL:
                            n_label = anotherIP + ' ' + str(n_id)
                        else:
                            n_label = str(n_id)
                        n_image = 'router.png'
                        n_size = 15
                        html_node_write(n_id, n_label, n_image, n_size)
                        another_list.append(another_no)
                        print('elif.. : ', another_list)
                        another_no += 1
                else:
                    print("strange : ", anotherIP, ' ', anotherTTL)
                print('another_no : ' ,another_no)
                another_sosu = another_no /100
                another_no = math.trunc(another_no /100) * 100 + 101
                print('another_no : ' ,another_no)

#       # 같은 대역 - 노드간 연결선 만들기

        for edge_no in range(1001, discover_no):
            if edge_no == 1001:
                if networkIP.get('ttlchai') == 0:
                    start_id =  0
                    end_id = 1001
                    edge_length = 'EDGE_LENGTH_MAIN'
                    html_edge_write(start_id, end_id, edge_length)
                else:
                    start_id =  1001
                    end_id = 1002
                    edge_length = 'EDGE_LENGTH_SUB'
                    html_edge_write(start_id, end_id, edge_length)
                    start_id =  0
                    end_id = 1002
                    edge_length = 'EDGE_LENGTH_SUB'
                    html_edge_write(start_id, end_id, edge_length)
            elif edge_no != 1002:
                start_id =  edge_no
                end_id = 1001
                edge_length = 'EDGE_LENGTH_SUB'
                html_edge_write(start_id, end_id, edge_length)

#       # 다른 대역 - 노드간 연결선 만들기
        edge_no_before = 3000
        for edge_no in another_list:
            print('edge_no : ', edge_no)
            if edge_no_before == 3000:
                print('edge_no_before = 3000.. edge_no :', edge_no)
                start_id =  edge_no
                end_id = 1001
                edge_length = 'EDGE_LENGTH_SUB'
                html_edge_write(start_id, end_id, edge_length)
                edge_no_before = edge_no
            elif edge_no - edge_no_before == 1:
                print('edge_no - edge_no_before == 1.. edge_no :', edge_no)
                start_id =  edge_no
                end_id = edge_no_before
                edge_length = 'EDGE_LENGTH_SUB'
                html_edge_write(start_id, end_id, edge_length)
                edge_no_before = edge_no
            else:
                print('another range : ', edge_no)
                start_id =  edge_no
                end_id = 1001
                edge_length = 'EDGE_LENGTH_SUB'
                html_edge_write(start_id, end_id, edge_length)
                edge_no_before = edge_no


#       # html 마무리 처리
        with open(path + "/conf/network_after.txt", "r") as f_network_after:
            lines_result_after = f_network_after.readlines()
            for line_result in lines_result_after:
                f_network.write(line_result)

        url = path + "/output/network.html"
        # 브라우저 띠우기
        webbrowser.open(url)
        return()

# if __name__ == '__main__':
#     network_draw()
