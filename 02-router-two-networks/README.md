# NetZero Lab 2 – Router + Two Different Networks

## Objective

To configure a router to connect two different IP networks and verify communication between devices using Cisco Packet Tracer.

## Topology

PC0 → Switch0 → Router0 → Switch1 → PC1

## Network 1

- Network: `192.168.1.0/24`
- PC0 IP Address: `192.168.1.10`
- Subnet Mask: `255.255.255.0`
- Default Gateway: `192.168.1.1`

## Network 2

- Network: `192.168.2.0/24`
- PC1 IP Address: `192.168.2.10`
- Subnet Mask: `255.255.255.0`
- Default Gateway: `192.168.2.1`

## Router Configuration

### GigabitEthernet 0/0

- IP Address: `192.168.1.1`
- Subnet Mask: `255.255.255.0`
- Status: Up/Up

### GigabitEthernet 0/1

- IP Address: `192.168.2.1`
- Subnet Mask: `255.255.255.0`
- Status: Up/Up

## Verification

Connectivity was tested using the `ping` command.

### PC0 to Router

```text
ping 192.168.1.1
```

Result:

```text
Sent = 4
Received = 4
Lost = 0
```

### PC0 to PC1

```text
ping 192.168.2.10
```

Final result:

```text
Sent = 4
Received = 4
Lost = 0
```

## Result

Successfully configured a router to connect two different networks and verified communication between PC0 and PC1.

## Skills Learned

- IPv4 addressing
- Subnetting (`/24`)
- Default gateway configuration
- Router interface configuration
- `no shutdown` command
- Basic router configuration
- Connectivity testing using `ping`
- Communication between different networks

## Tools Used

- Cisco Packet Tracer
- Cisco 1941 Router
- Cisco 2960 Switch
- End Devices (PCs)

## Status

**Completed ✅**
