# Lab 3 – Connecting Two Routers

## Objective

Configure two routers to connect two different networks and verify end-to-end communication between PCs.

## Network Topology

PC0 → Switch0 → Router0 → Router1 → Switch1 → PC1

## IP Addressing

| Device | Interface | IP Address | Subnet Mask |
|---|---|---|---|
| PC0 | FastEthernet | 192.168.1.10 | 255.255.255.0 |
| Router0 | GigabitEthernet0/0 | 192.168.1.1 | 255.255.255.0 |
| Router0 | GigabitEthernet0/1 | 10.0.0.1 | 255.255.255.252 |
| Router1 | GigabitEthernet0/0 | 10.0.0.2 | 255.255.255.252 |
| Router1 | GigabitEthernet0/1 | 192.168.2.1 | 255.255.255.0 |
| PC1 | FastEthernet | 192.168.2.10 | 255.255.255.0 |

## Router Configuration

### Router0

``text
interface gigabitEthernet 0/0
ip address 192.168.1.1 255.255.255.0
no shutdown

interface gigabitEthernet 0/1
ip address 10.0.0.1 255.255.255.252
no shutdown

ip route 192.168.2.0 255.255.255.0 10.0.0.2

Router1
interface gigabitEthernet 0/0
ip address 10.0.0.2 255.255.255.252
no shutdown

interface gigabitEthernet 0/1
ip address 192.168.2.1 255.255.255.0
no shutdown

ip route 192.168.1.0 255.255.255.0 10.0.0.1

Connectivity Testing
PC0 to PC1
ping 192.168.2.10

Result:
Sent = 4
Received = 4
Lost = 0

PC1 to PC0
ping 192.168.1.10

Result:
Sent = 4
Received = 4
Lost = 0

Result
Successfully configured two routers to connect two different networks and verified end-to-end communication between PC0 and PC1.

Skills Learned
IPv4 addressing
Subnetting
Router interface configuration
Static routing
no shutdown command
Default gateway configuration
Router-to-router communication
Connectivity testing using ping
Basic Cisco IOS commands

Tools Used
Cisco Packet Tracer
Cisco 1941 Routers
Cisco 2960 Switches
End Devices (PCs)

Status
Completed ✅
