# NetZero Lab 10 – OSPF Single-Area Routing

## Objective

The objective of this lab is to configure **OSPF (Open Shortest Path First)** in **Area 0** between two Cisco routers and verify dynamic routing and end-to-end connectivity between two different LAN networks.

This lab demonstrates how OSPF automatically exchanges routing information between routers without manually configuring static routes.

---

## Network Topology

```text
PC0
 |
Switch0
 |
Router0 (R1)
 | G0/1
 | 10.0.0.1/30
 |
 | 10.0.0.2/30
 | G0/0
Router1 (R2)
 |
Switch1
 |
PC1
```

Both routers participate in **OSPF Area 0**.

---

## IP Addressing Table

| Device  | Interface | IP Address   | Subnet Mask     |
| ------- | --------- | ------------ | --------------- |
| PC0     | NIC       | 192.168.1.10 | 255.255.255.0   |
| Router0 | G0/0      | 192.168.1.1  | 255.255.255.0   |
| Router0 | G0/1      | 10.0.0.1     | 255.255.255.252 |
| Router1 | G0/0      | 10.0.0.2     | 255.255.255.252 |
| Router1 | G0/1      | 192.168.2.1  | 255.255.255.0   |
| PC1     | NIC       | 192.168.2.10 | 255.255.255.0   |

---

## PC Configuration

### PC0

```text
IP Address:      192.168.1.10
Subnet Mask:     255.255.255.0
Default Gateway: 192.168.1.1
```

### PC1

```text
IP Address:      192.168.2.10
Subnet Mask:     255.255.255.0
Default Gateway: 192.168.2.1
```

---

# Router Configuration

## Router0 (R1)

```text
enable
configure terminal

interface gigabitEthernet 0/0
ip address 192.168.1.1 255.255.255.0
no shutdown
exit

interface gigabitEthernet 0/1
ip address 10.0.0.1 255.255.255.252
no shutdown
exit

router ospf 1
router-id 1.1.1.1
network 192.168.1.0 0.0.0.255 area 0
network 10.0.0.0 0.0.0.3 area 0
exit

end
write memory
```

---

## Router1 (R2)

```text
enable
configure terminal

interface gigabitEthernet 0/0
ip address 10.0.0.2 255.255.255.252
no shutdown
exit

interface gigabitEthernet 0/1
ip address 192.168.2.1 255.255.255.0
no shutdown
exit

router ospf 1
router-id 2.2.2.2
network 10.0.0.0 0.0.0.3 area 0
network 192.168.2.0 0.0.0.255 area 0
exit

end
write memory
```

---

# OSPF Verification

The following commands were used to verify the OSPF configuration.

## Check OSPF Neighbor

```text
show ip ospf neighbor
```

The routers successfully formed an OSPF adjacency.

Example neighbor information:

```text
Neighbor ID     State
2.2.2.2         FULL
```

---

## Check Routing Protocol

```text
show ip protocols
```

Output confirmed:

```text
Routing Protocol is "ospf 1"
```

Both routers were configured in **Area 0**.

---

## Check OSPF Routes

```text
show ip route ospf
```

Router0 learned the remote LAN through OSPF:

```text
O 192.168.2.0/24 via 10.0.0.2
```

Router1 learned the remote LAN through OSPF:

```text
O 192.168.1.0/24 via 10.0.0.1
```

The `O` route code indicates that the route was learned dynamically through OSPF.

---

# Connectivity Testing

## PC0 to PC1

Command:

```text
ping 192.168.2.10
```

Result:

```text
Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
```

---

## PC1 to PC0

Command:

```text
ping 192.168.1.10
```

Result:

```text
Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
```

Successful ping results confirmed that OSPF dynamically exchanged routes between the two routers.

---

# Routing Table Verification

Router0 routing table contained:

```text
C 192.168.1.0/24
C 10.0.0.0/30
O 192.168.2.0/24 via 10.0.0.2
```

Router1 routing table contained:

```text
C 192.168.2.0/24
C 10.0.0.0/30
O 192.168.1.0/24 via 10.0.0.1
```

This confirmed that the remote networks were learned dynamically using OSPF.

---

# Skills Learned

* Configuring OSPF version 2
* Configuring OSPF Area 0
* Assigning OSPF router IDs
* Using wildcard masks in OSPF network statements
* Forming OSPF neighbor relationships
* Understanding dynamic routing
* Verifying OSPF routes in the routing table
* Testing end-to-end connectivity using ping
* Troubleshooting OSPF configurations

---

# Tools Used

* Cisco Packet Tracer
* Cisco 1941 Routers
* Cisco 2960 Switches
* PCs
* Cisco IOS CLI

---

# Result

The OSPF single-area routing configuration was successfully completed.

* OSPF neighbors formed successfully.
* Dynamic routes were exchanged between Router0 and Router1.
* Both LAN networks were reachable.
* Ping tests succeeded in both directions with **4 packets sent, 4 packets received, and 0 packets lost**.
