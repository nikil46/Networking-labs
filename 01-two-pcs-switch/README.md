# Lab 1: Two PCs Connected Through a Switch

## Objective

To connect two PCs using a Cisco 2960 switch and verify communication between them using the ping command.

## Network Topology

PC0 ─── Switch0 ─── PC1

## Devices Used

- 2 × PCs
- 1 × Cisco 2960 Switch
- Copper Straight-Through cables

## IP Addressing

| Device | IP Address | Subnet Mask |
|---|---|---|
| PC0 | 192.168.1.1 | 255.255.255.0 |
| PC1 | 192.168.1.2 | 255.255.255.0 |

## Configuration

PC0:
- IP Address: 192.168.1.1
- Subnet Mask: 255.255.255.0

PC1:
- IP Address: 192.168.1.2
- Subnet Mask: 255.255.255.0

## Testing

From PC0, the following command was used:

ping 192.168.1.2

The ping was successful with 4 replies and 0% packet loss.

## Result

The two PCs successfully communicated through the Cisco 2960 switch.

## Key Learning

A network switch connects devices within a LAN and forwards Ethernet frames between them.
