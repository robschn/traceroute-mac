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
deviceName = input("\nPlease enter the IP of the switch you would like to search: ")

# SSH login
while True:
    try:
        myDevice = {
        'host': deviceName,
        'username': '', #type your user name here!
        'password': getpass(),
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

print ('\nSearching MAC address...\n')
#check to see if the MAC is on the switch
while True:
    #issue show mac add add %USER MAC%
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

while True:
    tracerouteMAC = net_connect.send_command('traceroute mac ' +userMAC+ ' ' + userMAC)
    if 'Layer 2 trace completed' in tracerouteMAC:
        
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
        break
    #if traceroute is an error, the MAC is on the 4500 itself or not a valid MAC
    else:
        userMAC = input("\nPlease try again. MAC must be HHHH.HHHH.HHHH format: ")
        continue

#make everything look pretty
print ("MAC HAS BEEN FOUND!\n\nSwitch: " +switchName+ " (" +switchIP+ ")" "\nInterface: " +switchInt+ "\nVLAN: " +switchVLAN+ "\n")