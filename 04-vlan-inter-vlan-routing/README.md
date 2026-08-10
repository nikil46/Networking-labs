markdown
# Lab 4 – VLANs and Inter-VLAN Routing

## Objective

Configure VLANs on a Cisco switch and enable communication between different VLANs using Router-on-a-Stick (Inter-VLAN Routing).

## Network Topology

PC0 → Switch0 → Router0
PC1 → Switch0

- PC0 belongs to VLAN 10 (SALES)
- PC1 belongs to VLAN 20 (IT)
- Router0 provides Inter-VLAN Routing

## IP Addressing

| Device | VLAN | Interface | IP Address | Subnet Mask | Default Gateway |
|---|---|---|---|---|---|
| PC0 | VLAN 10 | FastEthernet | 192.168.10.10 | 255.255.255.0 | 192.168.10.1 |
| PC1 | VLAN 20 | FastEthernet | 192.168.20.10 | 255.255.255.0 | 192.168.20.1 |
| Router0 | VLAN 10 | G0/0.10 | 192.168.10.1 | 255.255.255.0 | - |
| Router0 | VLAN 20 | G0/0.20 | 192.168.20.1 | 255.255.255.0 | - |

## VLAN Configuration

### VLANs Created

| VLAN ID | VLAN Name | Switch Port |
|---|---|---|
| 10 | SALES | Fa0/1 |
| 20 | IT | Fa0/2 |

## Switch0 Configuration

enable
configure terminal

vlan 10
name SALES
exit

vlan 20
name IT
exit

interface fastEthernet 0/1
switchport mode access
switchport access vlan 10
exit

interface fastEthernet 0/2
switchport mode access
switchport access vlan 20
exit

interface fastEthernet 0/24
switchport mode trunk
exit

end

## Router0 Configuration

Router0 was configured using Router-on-a-Stick.

enable
configure terminal

interface gigabitEthernet 0/0
no shutdown
exit

interface gigabitEthernet 0/0.10
encapsulation dot1Q 10
ip address 192.168.10.1 255.255.255.0
exit

interface gigabitEthernet 0/0.20
encapsulation dot1Q 20
ip address 192.168.20.1 255.255.255.0
exit

end

## VLAN Verification

Command:
show vlan brief


Result:
VLAN Name       Status    Ports
10   SALES      active    Fa0/1
20   IT         active    Fa0/2

This confirms that VLAN 10 (SALES) is assigned to Fa0/1 and VLAN 20 (IT) is assigned to Fa0/2.

## Trunk Verification

Command:
show interfaces trunk

Result:

Fa0/24 is configured as a trunk port between Switch0 and Router0.

## Router Interface Verification

Command:
show ip interface brief

Result:
GigabitEthernet0/0       unassigned      up    up
GigabitEthernet0/0.10    192.168.10.1    up    up
GigabitEthernet0/0.20    192.168.20.1    up    up

Both router subinterfaces are operational.

## Connectivity Testing

### Initial VLAN Isolation Test

Before configuring Inter-VLAN Routing, PC0 attempted to communicate with PC1.

Command:
ping 192.168.20.10


Result:
Sent = 4
Received = 0
Lost = 4

This confirmed that VLAN 10 and VLAN 20 were isolated from each other.

### PC0 to PC1

After configuring Router-on-a-Stick:

Command:
ping 192.168.20.10


Result:
Sent = 4
Received = 4
Lost = 0

Success: 100%

### PC1 to PC0

Command:
ping 192.168.10.10


Result:
Sent = 4
Received = 4
Lost = 0


Success: 100%

## Result

Successfully created VLAN 10 and VLAN 20 on a Cisco switch and configured Router-on-a-Stick to enable communication between the two different VLANs.

PC0 and PC1 successfully communicated across different VLANs with:

Sent = 4
Received = 4
Lost = 0

## Skills Learned

* VLAN creation and configuration
* VLAN naming
* Access port configuration
* VLAN assignment
* VLAN isolation
* Trunk port configuration
* IEEE 802.1Q VLAN tagging
* Router subinterface configuration
* Router-on-a-Stick
* Inter-VLAN routing
* Default gateway configuration
* Cisco IOS commands
* Network troubleshooting
* Connectivity testing using ping

## Tools Used

* Cisco Packet Tracer
* Cisco 1941 Router
* Cisco 2960 Switch
* End Devices (PCs)

## Status 
Completed ✅
