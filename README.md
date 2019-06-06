## traceroute-mac
This script can be used to find a user specified MAC with traceroute.

### Usage

1. Enter the MAC address of the device.

2. Enter the IP of the Layer 3 switch/router.

```
Please enter the MAC address you would like to search. Must be HHHH.HHHH.HHHH format: 0000.0C00.0000 
Please enter the IP of the switch you would like to search: 192.168.2.1
```
The script will perform a L2 traceroute to find the switch and the port the device is connected to:
```
MAC 0000.0c00.0000 has been found!

Switch: switch1 (192.168.1.1)
Interface: Gi1/0/1
VLAN: 1
```
### Requirements

-Python 3

-Netmiko

-Cisco Discovery Protocol (CDP) enable on ALL switches and routers

-Cisco IOS that supports the "traceroute mac" command
