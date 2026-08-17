# 🌐 NetZero Lab 11 — EIGRP Dynamic Routing

## 📌 Overview

This lab demonstrates **EIGRP (Enhanced Interior Gateway Routing Protocol)** using Cisco Packet Tracer.

Three Cisco routers are connected in a chain, with a LAN on each end. EIGRP is configured to dynamically exchange routing information between the routers, allowing devices on different networks to communicate without manually configured static routes.

---

## 🎯 Objectives

* Configure IPv4 addresses on routers and PCs
* Configure router interfaces
* Enable EIGRP dynamic routing
* Establish EIGRP neighbor relationships
* Verify dynamically learned routes
* Test end-to-end connectivity
* Use `tracert` to verify the routing path
* Understand EIGRP routing-table entries

---

## 🖥️ Topology

```text
PC0
 |
 |
Switch0
 |
 |
Router0
 |
 | 10.0.0.0/30
 |
Router1
 |
 | 10.0.0.4/30
 |
Router2
 |
 |
Switch1
 |
 |
PC1
```

### Devices Used

* 3 × Cisco 1941 Routers
* 2 × Cisco 2960 Switches
* 2 × PCs
* Copper Straight-Through cables

---

## 🗺️ IP Addressing Scheme

| Device  | Interface | IP Address      | Subnet Mask       |
| ------- | --------- | --------------- | ----------------- |
| PC0     | NIC       | `192.168.10.10` | `255.255.255.0`   |
| Router0 | G0/0      | `192.168.10.1`  | `255.255.255.0`   |
| Router0 | G0/1      | `10.0.0.1`      | `255.255.255.252` |
| Router1 | G0/0      | `10.0.0.2`      | `255.255.255.252` |
| Router1 | G0/1      | `10.0.0.5`      | `255.255.255.252` |
| Router2 | G0/0      | `10.0.0.6`      | `255.255.255.252` |
| Router2 | G0/1      | `192.168.20.1`  | `255.255.255.0`   |
| PC1     | NIC       | `192.168.20.10` | `255.255.255.0`   |

### Default Gateways

```text
PC0 → 192.168.10.1
PC1 → 192.168.20.1
```

---

# ⚙️ Router Configuration

## 🔹 Router0 Configuration

```text
enable
configure terminal

interface gigabitEthernet 0/0
ip address 192.168.10.1 255.255.255.0
no shutdown
exit

interface gigabitEthernet 0/1
ip address 10.0.0.1 255.255.255.252
no shutdown
exit

router eigrp 100
no auto-summary
network 192.168.10.0
network 10.0.0.0
end
```

---

## 🔹 Router1 Configuration

```text
enable
configure terminal

interface gigabitEthernet 0/0
ip address 10.0.0.2 255.255.255.252
no shutdown
exit

interface gigabitEthernet 0/1
ip address 10.0.0.5 255.255.255.252
no shutdown
exit

router eigrp 100
no auto-summary
network 10.0.0.0
end
```

---

## 🔹 Router2 Configuration

```text
enable
configure terminal

interface gigabitEthernet 0/0
ip address 10.0.0.6 255.255.255.252
no shutdown
exit

interface gigabitEthernet 0/1
ip address 192.168.20.1 255.255.255.0
no shutdown
exit

router eigrp 100
no auto-summary
network 10.0.0.0
network 192.168.20.0
end
```

---

# 💻 PC Configuration

## PC0

Configure under:

**PC0 → Desktop → IP Configuration**

```text
IP Address:       192.168.10.10
Subnet Mask:      255.255.255.0
Default Gateway:  192.168.10.1
```

## PC1

```text
IP Address:       192.168.20.10
Subnet Mask:      255.255.255.0
Default Gateway:  192.168.20.1
```

---

# 🔍 Verification

## 1. Verify Router Interfaces

Command:

```text
show ip interface brief
```

Expected result:

```text
GigabitEthernet0/0    up    up
GigabitEthernet0/1    up    up
```

All configured router interfaces were successfully verified as:

**Status: UP**

**Protocol: UP**

---

## 2. Verify EIGRP Neighbors

### Router0

```text
show ip eigrp neighbors
```

Router0 successfully established an EIGRP neighbor with:

```text
10.0.0.2
```

### Router1

```text
show ip eigrp neighbors
```

Router1 successfully established EIGRP neighbors with:

```text
10.0.0.1
10.0.0.6
```

### Router2

```text
show ip eigrp neighbors
```

Router2 successfully established an EIGRP neighbor with:

```text
10.0.0.5
```

---

# 🛣️ Routing Table Verification

Command:

```text
show ip route
```

EIGRP routes are identified by:

```text
D
```

### Router0 learned:

```text
D 10.0.0.4/30 via 10.0.0.2
D 192.168.20.0/24 via 10.0.0.2
```

### Router1 learned:

```text
D 192.168.10.0/24 via 10.0.0.1
D 192.168.20.0/24 via 10.0.0.6
```

### Router2 learned:

```text
D 10.0.0.0/30 via 10.0.0.5
D 192.168.10.0/24 via 10.0.0.5
```

This confirms that routing information was exchanged dynamically using EIGRP.

---

# 🧪 Connectivity Testing

## PC0 → PC1

Command:

```text
ping 192.168.20.10
```

Final result:

```text
Packets: Sent = 4, Received = 4, Lost = 0
```

### Result

**100% successful connectivity**

---

## PC1 → PC0

Command:

```text
ping 192.168.10.10
```

Final result:

```text
Packets: Sent = 4, Received = 4, Lost = 0
```

### Result

**100% successful connectivity**

---

# 🔎 Traceroute Verification

From PC0:

```text
tracert 192.168.20.10
```

Observed path:

```text
1    192.168.10.1
2    10.0.0.2
3    10.0.0.6
4    192.168.20.10
```

This confirms that packets traveled through:

```text
PC0
 ↓
Router0
 ↓
Router1
 ↓
Router2
 ↓
PC1
```

---

# 📊 Final Verification Summary

| Test                    | Result          |
| ----------------------- | --------------- |
| Router interfaces       | ✅ UP/UP         |
| Router0 EIGRP neighbor  | ✅ Established   |
| Router1 EIGRP neighbors | ✅ 2 Established |
| Router2 EIGRP neighbor  | ✅ Established   |
| EIGRP routes            | ✅ Learned       |
| PC0 → PC1 ping          | ✅ 4/4           |
| PC1 → PC0 ping          | ✅ 4/4           |
| Traceroute              | ✅ Successful    |
| Packet loss             | ✅ 0%            |

---

# 🧠 Key Concepts Learned

* EIGRP Dynamic Routing
* Autonomous System (AS) Number
* EIGRP Neighbor Adjacency
* IPv4 Addressing
* Subnetting
* `/30` point-to-point networks
* `/24` LAN networks
* Dynamic Route Advertisement
* Routing Tables
* EIGRP Route Code `D`
* Next-Hop Routing
* End-to-End Connectivity
* Traceroute Analysis

---

# 🛠️ Important Cisco Commands

```text
show ip interface brief
```

```text
show ip eigrp neighbors
```

```text
show ip route
```

```text
show ip protocols
```

```text
ping <destination-ip>
```

```text
tracert <destination-ip>
```

---

# 💡 EIGRP vs Static Routing

In previous NetZero labs, static routes were manually configured.

With EIGRP:

```text
Router0 ── EIGRP ── Router1 ── EIGRP ── Router2
```

Routers automatically exchange routing information.

This makes EIGRP more suitable for larger networks where manually maintaining static routes would become difficult.

---

# 🎓 Skills Demonstrated

* Cisco IOS Configuration
* Router Interface Configuration
* IPv4 Network Design
* Subnetting
* Dynamic Routing
* EIGRP Configuration
* EIGRP Neighbor Verification
* Routing Table Analysis
* Network Troubleshooting
* Ping Testing
* Traceroute Analysis
* Cisco Packet Tracer

---

# 🧰 Tools Used

* **Cisco Packet Tracer**
* Cisco 1941 Routers
* Cisco 2960 Switches
* PCs
* Cisco IOS CLI

---
