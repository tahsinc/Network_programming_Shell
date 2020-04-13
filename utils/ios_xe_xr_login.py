import socket

import netmiko
from netmiko import ConnectHandler
import ipaddress
import getpass
import sys
import re
import time

# Show user's computer
print("\n**** Running this script from {}'s computer **** \n".format(getpass.getuser().upper()))

# Show user's environment
print("Python Enviroment of the system: {}\n".format(sys.version))

"""
raw_input: used in python version 2.x.x(generally comes by default in mac OS)
input: used in python version 3.x.x (generally the latest versions compatible both in windows and mac OS)
-Also tested in Ubuntu 18.x ( python 3.x.x: use python3 while running the script )
"""
pyVersion = int(sys.version[0])

if int(pyVersion) < 3:
    input_from_keyboard = raw_input
else:
    input_from_keyboard = input

# user defined function:
# name: ip_input_format(string_tag)
# input: string_tag: string_tag for ip address input
# function: returns Host IP address after checking the correct format
def ip_input_format(string_tag):
    while (True):
        ip_address = input_from_keyboard(string_tag)
        if pyVersion < 3:  # requires to decode the key_board input for ip
            ip_address = ip_address.decode('utf-8')  # applicable to "ipaddress" library for Python 2.x.x
        try:
            ipaddress.ip_address(ip_address)
            # socket.inet_aton(ip_address)
            # printl(ip_address)
            break
        except Exception as e:
            print(str(e))
            print("{}: Invalid IP Input. ---Try Again---'".format(ip_address))
            # exit(-1)
    return ip_address


"""
# User defined function:
# name: get_device
# input: device_type, remote_host, username, password, enablepassword
# function: returns devcice instance
"""


def get_device(device_type, remote_host, username, password, enablepassword):
    dev = {}
    dev['device_type'] = device_type
    dev['ip'] = remote_host
    dev['username'] = username
    dev['password'] = password
    dev['secret'] = enablepassword
    dev['timeout'] = 120

    return dev


"""
# User defined function:
# name: login_into_device
# input: remote_host, username, password, enablepassword
# function: after checking the device credential is correct,
            returns device handler and device connectivity (telnet or ssh) type 
"""


def login_into_device(remote_host, username, password, enablepassword, iter, telnet_port=23, ssh_port=22 ):
    device = {}
    net_connect = {}
    socketM = {}
    dev_type = ''
    socketM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CONNECT_FLAG = 1
    CONNECT_SUCCESS = 0
    if socketM.connect_ex((remote_host, telnet_port)) == 0:
        print('Connection established via TELNET')
        # device = get_device('cisco_ios_telnet', remote_host, input("Enter username: "), input("Enter password: "),
        #                     input("Enter enable password: "))
        device = get_device('cisco_ios_telnet', remote_host, username, password, enablepassword)
        # print(device)
        dev_type = 'cisco_ios_telnet'
        try:
            net_connect = ConnectHandler(**device)
            CONNECT_FLAG = 0
            CONNECT_SUCCESS = 1
        except Exception as e:
            print(str(e))
            print("Could not connect to the node with TELNET \n Trying with SSH\n")
            CONNECT_FLAG = 1
            device.clear()
            socketM.close()
            socketM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if (CONNECT_FLAG == 1) and (socketM.connect_ex((remote_host, ssh_port)) == 0):
        print('Connection established via SSH')
        # device = get_device('cisco_ios_ssh', remote_host, input("Enter username: "), input("Enter password: "),
        #                     input("Enter enable password: "))
        device = get_device('cisco_ios_ssh', remote_host, username, password, enablepassword)
        # print(device)
        dev_type = 'cisco_ios_ssh'
        try:
            net_connect = ConnectHandler(**device)
            CONNECT_SUCCESS = 1
        except Exception as e:
            print(str(e))
            print("Problem Occured with SSH Login")
            CONNECT_SUCCESS = 0

    if CONNECT_SUCCESS == 0:
        print('Unable to connect')
        socketM.close()
        device.clear()
        # exit(-1)
        # net_connect.disconnect()
    if CONNECT_SUCCESS == 1:
        # net_connect.set_terminal_width(0)
        if (net_connect.check_enable_mode() == False):
            try:
                net_connect.enable()
                if (net_connect.check_enable_mode() == True):
                    print("############### Credential verified for device {} ##################".format(iter + 1))
            except Exception as e:
                print(str(e))
                print("----Error in Enable Password---Try Again")
                net_connect = {}

        # print("############### Credential verified for device {} ##################".format(i + 1))

    return net_connect, dev_type


"""
# User defined function:
# name: deploy_command
# input: network_device, command_to_deploy, READY_TO_DEPLOY (by default = 1, 0 if uses does not want to deploy
# function: deploy the the command and return the network_device with the current changes 
"""


def deploy_command(network_device, command_to_deploy, READY_TO_DEPLOY=1):
    print(command_to_deploy)
    if (READY_TO_DEPLOY == 1):
        print(network_device.config_mode())
        deploy = network_device.send_config_set(command_to_deploy)
        print(deploy)
        print(network_device.exit_config_mode())

    return network_device


# ===========================================
""" Add user defined Function """

"""
# User defined function:
# name: find_text
# input: from_text, starting_at, ending_at_excluded
# output: extracted_text
# function: parse specific portion of text from a large text 
"""

def find_text(from_text, starting_at, ending_at_excluded):
    print_flag = 0
    extracted_text = ''
    for line in from_text.strip().split('\n'):
        if line.upper().strip() == starting_at.upper().strip():
            print_flag = 1
        if line.upper().strip() == ending_at_excluded.upper().strip():
            print_flag = 0
            break;

        if print_flag == 1:
            extracted_text = extracted_text + line + '\n'
            #print(line)

    return extracted_text

# ===========================================

"""
# User defined function:
# name: verify_device_login
# input: nNunmberOfDevice (default is 1, user can change to as many as they need)
# output: boxes
# function: return number of network devices or boxes ( 1 or more depending on input) 
"""

def verify_device_login(nNunmberOfDevice=1):
    boxes = list()
    for i in range(0, nNunmberOfDevice):
        box = dict()
        while (True):

            box['ip'] = ip_input_format("Enter the HOST-{} IP: ".format(i + 1))
            box['username'] = input_from_keyboard("Enter the HOST-{} Username: ".format(i + 1))
            #box['password'] = input_from_keyboard("Enter the HOST-{} Password: ".format(i + 1))
            #box['secret'] = input_from_keyboard("Enter the HOST-{} Enable Password: ".format(i + 1))
            box['password'] = getpass.getpass("Enter the HOST-{} Password: ".format(i + 1))
            box['secret'] = getpass.getpass("Enter the HOST-{} Enable Password: ".format(i + 1))
            # box['port'] = input_from_keyboard("Enter the HOST-{} Login Port: ".format(i+1))

            network_device, type = login_into_device(box['ip'], box['username'], box['password'], box['secret'], i)
            print(network_device)
            print(type)
            box['device_type'] = type
            if network_device == {} or type == '':
                continue
            else:
                break

        boxes = boxes + [box.copy()]

        ###=============================================================================

        """Add any extra input you need ....."""

        ###=============================================================================

    return boxes
