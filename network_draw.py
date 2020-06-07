# -*- encoding:utf8 -*-
import os
from os import getpid
import re
import shutil
import webbrowser

path = os.getcwd()
discoverIP_list = []

#html로 망도 그리기
def network_draw(networkIP):
    print("=======network drawing==========")
    print(networkIP)
    # html head 부분은 공통이므로 미리 만든 network_before.txt 화일 copy
    shutil.copy(path + "/conf/network_before.txt", path + "/output/network.html")
    # network_before copy한 화일 - network.html 화일을 열어서 내용을 추가 한다.
    with open("./output/network.html", "a") as f_network:
        # ip scan 결과화일인 result.txt 화일을 열어서 읽는다.
        with open(path + "/scan_result/result.txt", "r") as f_result:
            line_result = f_result.readlines()
            # 각 노드에는 번호를 붙인다. 1000번대 (1001:GW, 1002:my pc, 1003:외부공인, 히후는 찾은 결과 )
            discover_no = 1003
            # 인터넷(구름 모양) 노드 그리기
            f_network.write("      nodes.push({id: 0, label: '" + "internet" + "', image: DIR + 'internet.png', size: 15, shape: 'image'});\r\n")
            # scan 결과 화일을 한줄 씩 읽는다.

            for node_result in line_result:
                list_result = node_result.split('\t')
                # GW IP일 경우 discoverIP_list 에 GW 정보 추가

                if list_result[0] == 'GW IP :':
                    My_GatewayIP = list_result[1].replace("\r\n","")
                    discoverIP_list.append(My_GatewayIP)
                # Scan 하고 있는 현재 내 pc인 경우 discoverIP_list 에 내 IP 정보 추가
                elif list_result[0] == 'My IP :':
                    My_IP = list_result[1].replace("\r\n", "")
                    discoverIP_list.append(My_IP)
                    My_DiscoverInfo = My_IP + "\\r\\n My PC"
                    f_network.write("      nodes.push({id: 1002, label: '" + "{}".format(My_DiscoverInfo) + "', image: DIR + 'pc.png', size: 15, shape: 'image'});\r\n")
                # 외부 공인 IP 정보 추가
                elif list_result[0] == 'PubIP :':
                    if networkIP.get('ttlchai') == 0:
                        Public_IP = list_result[1].replace("\r\n", "")
                    else:
                        Public_IP = list_result[1].replace("\r\n", "")
                        discoverIP_list.append(Public_IP)
                        My_DiscoverInfo = Public_IP + "\\r\\n out Public IP"
                        f_network.write("      nodes.push({id: 1003, label: '" + "{}".format(My_DiscoverInfo) + "', image: DIR + 'router.png', size: 15, shape: 'image'});\r\n")
                # Scan 해서 찾은 IP 정보 추가
                elif list_result[0] == 'discoverIP :':
                    My_DiscoverIP = list_result[1].replace("\r\n", "")
                    # Scan 해서 찾은 IP가 GW IP 일 경우 노드 추가 (중복일 경우 처리하는 것임)
                    if My_DiscoverIP == My_GatewayIP:
                        if networkIP.get('ttlchai') == 0:
                            My_DiscoverInfo = My_DiscoverIP + "\\r\\n" + "(Public :" + Public_IP + ")" + "\\r\\n" + list_result[3].replace("\n","")
                        else:
                            My_DiscoverInfo = My_DiscoverIP + "\\r\\n" + list_result[3].replace("\n","")
                        f_network.write("      nodes.push({id: 1001, label: '" + "{}".format(My_DiscoverInfo) + "', image: DIR + 'homeRouter.png', size: 15, shape: 'image'});\r\n")
                    else:
                        My_DiscoverInfo = My_DiscoverIP + "\\r\\n" + list_result[3].replace("\n", "")
                        if My_DiscoverIP not in discoverIP_list:
                            discover_no += 1
                            f_network.write("      nodes.push({id: " + str(discover_no) + ", label: '" + "{}".format(My_DiscoverInfo) + "', image: DIR + 'pc.png', size: 15, shape: 'image'});\r\n")
                            discoverIP_list.append(My_IP)
            # 노드간 연결선 만들기
            for edge_no in range(1002, discover_no+1):
                f_network.write("      edges.push({from: " + "{}".format(edge_no) + ", to: 1001, length: EDGE_LENGTH_SUB});\r\n")
            # 외부 공인 IP가 gw와 같을 경우/다를 경우 처리
            if networkIP.get('ttlchai') == 0:
                f_network.write("      edges.push({from: 0, to: 1001, length: EDGE_LENGTH_SUB});\r\n")
            else:
                f_network.write("      edges.push({from: 0, to: 1003, length: EDGE_LENGTH_SUB});\r\n")
        # html 마무리 처리
        with open(path + "/conf/network_after.txt", "r") as f_network_after:
            lines_result_after = f_network_after.readlines()
            for line_result in lines_result_after:
                f_network.write(line_result)

        url = path + "/output/network.html"
        # 브라우저 띠우기 - chrome은 불가
        webbrowser.open(url)
        return()
