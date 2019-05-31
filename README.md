# DevNet-traceroute
This script can be used to find a user specified MAC with traceroute.

# Usage

1. Enter the MAC address of the device.

2. Enter the IP of the L3 switch/router.

```
Please enter the MAC address you would like to search. Must be HHHH.HHHH.HHHH format: 0000.0C00.0000 

Please enter the IP of the switch you would like to search: 192.168.2.1
```
The script will perform a L2 traceroute to find the switch and the port the device is connected to:
```
MAC HAS BEEN FOUND!

Switch: switch1 (192.168.1.1)
Interface: Gi1/0/1
VLAN: 1
```
