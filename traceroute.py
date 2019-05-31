#requires Python 3 and Netmiko

#imports
from __future__ import print_function, unicode_literals
from netmiko import Netmiko
from getpass import getpass

import string
import socket


#Ask for user input "What's your MAC?"
userMAC = input("\nPlease enter the MAC address you would like to search. Must be HHHH.HHHH.HHHH format: ")

# Ask user what IP would they like to connect to
deviceName = input("Please enter the IP of the switch you would like to search: ")

username = input("\nUsername: ")
password = getpass()

# SSH login
while True:
    try:
        myDevice = {
        'host': deviceName,
        'username': username,
        'password': password,
        'device_type': 'cisco_ios',
        }
        print ('\nLogging in now...')
        #connect to device
        net_connect = Netmiko(**myDevice)
        net_connect.enable()
        break
    except:
        print ('\nLogin failed. Please try again.')
        continue

print ('Searching MAC address...')
#check to see if the MAC is on the switch
while True:
    #issue show mac add add USER MAC
    showMAC =  net_connect.send_command('show mac add add ' +userMAC)
    #checks to see if we get an output
    if 'Unicast Entries' in showMAC:
        #splits output into strings
        MAClst = [];
        for char in showMAC:
            MAClst.append(char)
        MACvarsplit = (''.join(MAClst).split('\n'))

        #grabs only the part of output that contains VLAN
        MACint = MACvarsplit[3]

        #grabs VLAN number
        switchVLAN = MACint.split()[0]
        break
    else:
        #if no results, tell the user MAC not found, check MAC
        print ('\n*****ERROR: MAC NOT FOUND****\n')
        #offer for them to change MAC and try again or change MAC
        userMAC = input("\nPlease try again. MAC must be HHHH.HHHH.HHHH format: ")
        continue

print('Running traceroute. This may take up one minute...')

while True:
    tracerouteMAC = net_connect.send_command('traceroute mac ' +userMAC+ ' ' + userMAC)
    if 'Layer 2 trace completed' in tracerouteMAC:
        break

    else:
        #there is a phone in the middle of the switch and device

        #grab phoneIP from output
        PHONElst = [];
        for char in tracerouteMAC:
            PHONElst.append(char)
        PHONEvarsplit = (''.join(PHONElst).split('\n'))
        PHONEint = PHONEvarsplit[0]
        outputPhoneIP = PHONEint.split()[-3]
        phoneIP = outputPhoneIP.strip(string.punctuation) #removes . from output
        #issue sh ip arp phoneIP
        phoneARP = net_connect.send_command('sh ip arp ' + phoneIP)

        #grab phoneMAC
        phoneMAClst = [];
        for char in phoneARP:
            phoneMAClst.append(char)
        phoneMACvarsplit = (''.join(phoneMAClst).split('\n'))

        phoneMACint = phoneMACvarsplit[1]
        phoneMAC = phoneMACint.split()[3]

        #issue traceroute mac phoneMAC phoneMAC
        tracerouteMAC = net_connect.send_command('traceroute mac ' + phoneMAC + ' ' + phoneMAC)
        break

#makes output into seperate strings
TRACElst = [];
for char in tracerouteMAC:
    TRACElst.append(char)
TRACEvarsplit = (''.join(TRACElst).split('\n'))

#grabs only the part of the output that contains IP and interface of MAC
TRACEint = TRACEvarsplit[1]

#grabs switch name
switchName = TRACEint.split()[1]

#grabs switch interface
switchInt = TRACEint.split()[-1]

#grabs switch IP
outputSwitchIP = TRACEint.split()[2]
switchIP = outputSwitchIP.strip(string.punctuation) #removes () from output

#make everything look pretty
print ("\nMAC FOUND!\n\nSwitch: " +switchName+ " (" +switchIP+ ")" "\nInterface: " +switchInt+ "\nVLAN: " +switchVLAN+ "\n")
