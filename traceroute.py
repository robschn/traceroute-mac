#requires Python 3 and Netmiko

#imports
from __future__ import print_function, unicode_literals
from netmiko import Netmiko
from getpass import getpass
import string
import socket

userMAC = input("\nPlease enter the MAC address you would like to search. Must be HHHH.HHHH.HHHH format: ")
deviceName = input("Please enter the IP of the switch you would like to search: ")

# SSH login
while True:
    try:
        username = input("Username: ")
        password = getpass()
        myDevice = {
        'host': userSwitch,
        'username': username,
        'password': password,
        'device_type': 'cisco_ios',
        }
        print("Logging in now...")
        net_connect = Netmiko(**myDevice)
        net_connect.enable()
        break
    except:
        print("Login failed. Please try again.\n")
        continue

print ('Searching MAC address...')

# check to see if the MAC is valid
while True:
    # issue show mac add add userMAC
    showMAC = net_connect.send_command('show mac add add ' +userMAC)
    # checks to see if we get correct output
    if 'Unicast Entries' in showMAC:
        # splits output into strings
        MAClst = [];
        for char in showMAC:
            MAClst.append(char)
        MACvarsplit = (''.join(MAClst).split('\n'))

        MACint = MACvarsplit[3]

        # grabs VLAN
        switchVLAN = MACint.split()[0]

        # grabs current interface
        currentSwitchInt = MACint.split()[4]

        break
    else:
        # if no results, tell the user MAC not found, check MAC
        print ('\n*****ERROR: MAC NOT FOUND****\n')
        # offer for them to change MAC and try again or change MAC
        userMAC = input('\nMust be HHHH.HHHH.HHHH format. Please try again: ')
        continue
#run traceroute mac
print('Running traceroute. This may take up one minute...')
while True:
    tracerouteMAC = net_connect.send_command('traceroute mac ' +userMAC+ ' ' + userMAC)

    # MAC address found on a connected switch
    if 'Layer 2 trace completed' in tracerouteMAC:
        # makes output into seperate strings
        TRACElst = [];
        for char in tracerouteMAC:
            TRACElst.append(char)
        TRACEvarsplit = (''.join(TRACElst).split('\n'))

        # grabs only the part of the output that contains IP and interface of MAC
        TRACEint = TRACEvarsplit[1]

        # grabs switch name
        switchName = TRACEint.split()[1]

        # grabs switch interface
        switchInt = TRACEint.split()[-1]

        # grabs switch IP
        outputSwitchIP = TRACEint.split()[2]
        switchIP = outputSwitchIP.strip(string.punctuation) # removes () from output

        # tell the user MAC has been found and where it is
        print ('\nMAC ' +userMAC+ ' has been found! \n\nSwitch: ' +switchName+ ' (' +switchIP+ ')\nInterface: ' +switchInt+ '\nVLAN: ' +switchVLAN+ '\n')
        break

    # MAC address found on current switch.
    elif 'Source and Destination on same port and no nbr!' in tracerouteMAC:
	# tell the user the MAC has been found and is on the current switch
        print ('\nMAC ' +userMAC+ ' is on this switch! \n\nInterface: ' +currentSwitchInt+ '\nVLAN: ' +switchVLAN+ '\n')
        break

    # MAC address is behind a VoIP phone
    elif 'Unable to send a l2trace request' in tracerouteMAC:
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

        # makes output into seperate strings
        TRACElst = [];
        for char in tracerouteMAC:
            TRACElst.append(char)
        TRACEvarsplit = (''.join(TRACElst).split('\n'))

        # grabs only the part of the output that contains IP and interface of MAC
        TRACEint = TRACEvarsplit[1]

        # grabs switch name
        switchName = TRACEint.split()[1]

        # grabs switch interface
        switchInt = TRACEint.split()[-1]

        # grabs switch IP
        outputSwitchIP = TRACEint.split()[2]
        switchIP = outputSwitchIP.strip(string.punctuation) # removes () from output

        # tell the user MAC has been found and where it is
        print ('\nMAC ' +userMAC+ ' has been found! \n\nSwitch: ' +switchName+ ' (' +switchIP+ ')\nInterface: ' +switchInt+ '\nVLAN: ' +switchVLAN+ '\n')
        break
    else:
        print ('Error has occurred. Exit program...')
        break

exit()
