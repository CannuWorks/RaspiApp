import hashlib
import re
import subprocess
from pprint import pprint


def get_ip_addr():
    get_ip_addr = subprocess.run(['ip', '-4', 'address'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    cmd_result = get_ip_addr.stdout.decode('utf-8')

    ip_addr_result = []

    cmd_result0 = cmd_result.splitlines()
    for read_line in cmd_result0:
        if re.search('^\s*inet', read_line):
            read_line0 = read_line.lstrip(' ').rstrip('\n').split()
            ip_addr_result.append(read_line0)

    ip_addr_result2 = []

    for read_line in ip_addr_result:
        ip_addr_result2.append((read_line[-1], read_line[1]))

    result_dict = dict(ip_addr_result2)

    return result_dict

# pprint(get_ip_addr())


def get_socket():
    get_socket = subprocess.run(['ss', '-tu'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    cmd_result = get_socket.stdout.decode('utf-8')

    socket_list0 = []

    cmd_result0 = cmd_result.splitlines()
    for line in cmd_result0:
        line0 = [*line.split(), '']
        socket_list0.append(line0)

    socket_list1 = []

    for list_value in socket_list0:
        socket_list1.append(list_value)

        if 'Netid' in list_value:
            value0 = list_value[4] + '-' + list_value[5]
            value1 = list_value[6] + '-' + list_value[7]
            socket_list1[0].insert(4, value0)
            socket_list1[0].insert(5, value1)
            socket_list1[0].remove('Local')
            socket_list1[0].remove('Peer')
            socket_list1[0].remove('Address:Port')
            socket_list1[0].remove('Address:Port')
            del socket_list1[0][-1]

    return socket_list1

# pprint(get_socket())


def get_route():
    get_route = subprocess.run(['route'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    cmd_result = get_route.stdout.decode('utf-8')

    route_result = []

    cmd_result0 = cmd_result.splitlines()
    for read_line in cmd_result0:
        read_line0 = read_line.split()
        route_result.append(read_line0)
    
    del route_result[0]

    return route_result

# pprint(get_route())


def get_temp():
    get_temp = subprocess.run(['vcgencmd', 'measure_temp'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    value0 = get_temp.stdout.decode('utf-8')
    value1=value0.split('=')
    value2=value1[1][:-2]
    temp_result = f'RaspberryPi4 Temparature : {value2}°C \n'

    return temp_result

# print(get_temp())


def get_disk():

    #Get disk info via "lsblk" command
    get_block_dev = subprocess.run(['lsblk'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    lsblk_result = get_block_dev.stdout.decode('utf-8')

    result_list0 = []

    lsblk_result0 = lsblk_result.splitlines()
    for read_line in lsblk_result0:
        read_line0 = read_line.rstrip('\n').split()
        result_list0.append(read_line0)


    #Get disk info via "df -h" command
    get_disk_usage = subprocess.run(['df', '-h'],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
    df_result = get_disk_usage.stdout.decode('utf-8')

    result_list1 = []

    df_result0 = df_result.splitlines()
    for read_line in df_result0:
        read_line0 = read_line.rstrip('\n').split()
        result_list1.append(read_line0)

    result_list2 = []

    for read_line in result_list1:
        result_list2.append(read_line)

        if 'Filesystem' in read_line:
            h_list = read_line[5] + '-' + read_line[6]
            result_list2[0].insert(5, h_list)
            result_list2[0].remove('Mounted')
            result_list2[0].remove('on')

    return result_list0, result_list2

# pprint(get_disk())


def get_mem():
    get_socket = subprocess.run(['free', '--mega', '-w'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    cmd_result = get_socket.stdout.decode('utf-8')

    result_list = []

    cmd_result0 = cmd_result.splitlines()
    for line in cmd_result0:
        line0 = line.split()
        result_list.append(line0)

    result_list[0].insert(0, '')
    result_list[2].extend(['', '', '', ''])

    return result_list

# pprint(get_mem())


def get_vmstat():
    get_socket = subprocess.run(['vmsta'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    cmd_result = get_socket.stdout.decode('utf-8')

    result_list = []

    cmd_result0 = cmd_result.splitlines()
    for read_line in cmd_result0:
        read_line0 = read_line.split()
        result_list.append(read_line0)
    
    del result_list[0]

    return result_list

# pprint(get_vmstat())


def get_digest256(password):
    pwd = bytes(password, 'utf-8')
    diget = hashlib.sha256(pwd).hexdigest()
    return diget


def get_digest224(password):
    pwd = bytes(password, 'utf-8')
    diget = hashlib.sha224(pwd).hexdigest()
    return diget


ubuntumin_sha224 = get_digest224('ubuntumin')
ubuntumin_sha256 = get_digest256('Mk970101')

raspimin_sha224 = get_digest224('raspimin')
raspimin_sha256 = get_digest256('Mk970101')

print(f'Ubuntumin for Git : {ubuntumin_sha224}')
print(f'mashcannu for AWS : {ubuntumin_sha256}')
print(f'Raspimin for Git : {raspimin_sha224}')
print(f'mashcannu for Raspi : {raspimin_sha256}')
