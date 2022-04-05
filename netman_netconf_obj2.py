"""#!/usr/bin/python3"""
from __future__ import print_function
import sys
try:
    from ncclient import manager
    from prettytable import PrettyTable
    from netaddr import IPAddress
    import pandas as pd
    import ipaddress
    import os
except Exception:
    print('Install all the necessary modules')
    sys.exit()

if __name__ == "__main__":
    TABLE = PrettyTable(['Router',
                         'Hostname',
                         'Loopback 99 IP',
                         'OSPF area',
                         'Advertised OSPF Networks'])
    FILE = 'info.csv'
    if not os.path.exists(FILE):
        print(f"FILE {FILE} not found, exiting")
        sys.exit()
    if os.stat(FILE).st_size == 0:
        print(f'FILE {FILE} is empty, exiting')
        sys.exit()
    READ_FILE = pd.read_csv('info.csv')
    ROUTERS = READ_FILE['Router'].to_list()
    MGM_IP = READ_FILE['Mgmt IP'].to_list()
    UNAME = READ_FILE['Username'].to_list()
    PWD = READ_FILE['Password'].to_list()
    HOST = READ_FILE['Hostname'].to_list()
    LO_NAME = READ_FILE['Loopback Name'].to_list()
    LO_IP = READ_FILE['Loopback IP'].to_list()
    MASK = READ_FILE['Loopback Subnet'].to_list()
    WILDCARD = READ_FILE['Wildcard'].to_list()
    NETWORKS = READ_FILE['Network'].to_list()
    AREA = READ_FILE['OSPF Area'].to_list()

    CFG = '''
	<config>
	<cli-config-data>
	<cmd> hostname %s </cmd>
	<cmd> int %s </cmd>
	<cmd> ip address %s %s </cmd>
	<cmd> router ospf 1 </cmd>
	<cmd> network %s %s area %s </cmd>
	<cmd> network 198.51.100.0 0.0.0.255 area 0 </cmd>
	</cli-config-data>
	</config>
	'''

    for i in range(0, 5):
        connection = manager.connect(host=MGM_IP[i],
                                     port=22,
                                     username=UNAME[i],
                                     password=PWD[i],
                                     hostkey_verify=False,
                                     device_params={'name': 'csr'},
                                     allow_agent=False,
                                     look_for_keys=False)
        print(f'Logging into router {ROUTERS[i]} and sending configurations')
        CFG1 = CFG % (HOST[i], LO_NAME[i], LO_IP[i], MASK[i],
                      NETWORKS[i], WILDCARD[i], AREA[i])
        edit_CFG = connection.edit_config(target='running', config=CFG1)

    print('\n------------------Configs to all routers is sent------------------\n')

    FETCH_INFO = '''
    		<filter>
    		<config-format-text-block>
    		<text-filter-spec> %s </text-filter-spec>
    		</config-format-text-block>
    		</filter>
    		'''

    for i in range(0, 5):
        connection = manager.connect(host=MGM_IP[i],
                                     port=22,
                                     username='lab',
                                     password='lab123',
                                     hostkey_verify=False,
                                     device_params={'name': 'csr'},
                                     allow_agent=False,
                                     look_for_keys=False)
        print(f'Pulling information from router {ROUTERS[i]} to display')

        FETCH_HOSTNAME = FETCH_INFO % ('| i hostname')
        output1 = connection.get_config('running', FETCH_HOSTNAME)
        split1 = str(output1).split()
        hostname = split1[6]

        FETCH_LO_INFO = FETCH_INFO % ('int Loopback99')
        output2 = connection.get_config('running', FETCH_LO_INFO)
        split2 = str(output2).split()
        lo_ip_mask = split2[9] + '/' + \
            str(IPAddress(split2[10]).netmask_bits())

        FETCH_OSPF_INFO = FETCH_INFO % ('| s ospf')
        output3 = connection.get_config('running', FETCH_OSPF_INFO)
        split3 = str(output3).split()
        LO_IP_PREFIX = str(
            ipaddress.ip_network(
                split3[9] + '/' + split3[10],
                strict=False) .prefixlen)
        MGM_IP_PREFIX = str(
            ipaddress.ip_network(
                split3[14] + '/' + split3[15],
                strict=False) .prefixlen)
        ospf_area = split3[12]
        ospf_networks = split3[9] + '/' + \
            LO_IP_PREFIX, split3[14] + '/' + MGM_IP_PREFIX

        TABLE.add_row(
            (ROUTERS[i],
             hostname,
             lo_ip_mask,
             ospf_area,
             ospf_networks))

    print('\n------------------Displaying the fetched information------------------\n')
    print(TABLE)
