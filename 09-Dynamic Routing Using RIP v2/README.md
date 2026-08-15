# Lab 9 — Dynamic Routing Using RIP v2

## 📌 Objective

To configure and verify **RIP Version 2 (RIPv2)** on two Cisco routers and establish communication between two different LAN networks using dynamic routing.

---

## 🖥️ Network Topology

```text
PC0 ── Switch0 ── Router0 ───── Router1 ── Switch1 ── PC1
                  |              |
              LAN 1           LAN 2
```

---

## 🌐 IP Addressing

| Device  | Interface | IP Address   | Subnet Mask     | Default Gateway |
| ------- | --------- | ------------ | --------------- | --------------- |
| PC0     | NIC       | 192.168.1.10 | 255.255.255.0   | 192.168.1.1     |
| Router0 | G0/0      | 192.168.1.1  | 255.255.255.0   | —               |
| Router0 | G0/1      | 10.0.0.1     | 255.255.255.252 | —               |
| Router1 | G0/0      | 10.0.0.2     | 255.255.255.252 | —               |
| Router1 | G0/1      | 192.168.2.1  | 255.255.255.0   | —               |
| PC1     | NIC       | 192.168.2.10 | 255.255.255.0   | 192.168.2.1     |

---

## ⚙️ Router0 Configuration

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

router rip
version 2
no auto-summary
network 192.168.1.0
network 10.0.0.0
exit

end
```

---

## ⚙️ Router1 Configuration

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

router rip
version 2
no auto-summary
network 10.0.0.0
network 192.168.2.0
exit

end
```

---

## 🔍 Router Interface Verification

### Router0

```text
show ip interface brief
```

Expected:

```text
GigabitEthernet0/0    192.168.1.1    YES manual    up    up
GigabitEthernet0/1    10.0.0.1       YES manual    up    up
```

### Router1

```text
show ip interface brief
```

Expected:

```text
GigabitEthernet0/0    10.0.0.2       YES manual    up    up
GigabitEthernet0/1    192.168.2.1    YES manual    up    up
```

---

## 🔄 RIP Verification

Use:

```text
show ip protocols
```

### Router0

```text
Routing Protocol is "rip"
Default version control: send version 2, receive 2

Routing for Networks:
    10.0.0.0
    192.168.1.0
```

### Router1

```text
Routing Protocol is "rip"
Default version control: send version 2, receive 2

Routing for Networks:
    10.0.0.0
    192.168.2.0
```

---

## 🛣️ Routing Table Verification

Check the routing table using:

```text
show ip route
```

On Router0, the remote network should be learned through RIP:

```text
R    192.168.2.0/24 [120/1] via 10.0.0.2
```

On Router1:

```text
R    192.168.1.0/24 [120/1] via 10.0.0.1
```

`R` indicates that the route was learned dynamically through **RIP**.

---

## 📡 Connectivity Testing

### Router0 → Router1

```text
ping 10.0.0.2
```

Result:

```text
Packets: Sent = 4, Received = 4, Lost = 0
```

### Final PC-to-PC Test

From **PC0**:

```text
ping 192.168.2.10
```

Result:

```text
Packets: Sent = 4
Received = 4
Lost = 0
```

✅ **End-to-end connectivity successfully established.**

---

## 🎯 Skills Learned

* IPv4 Addressing
* Subnetting
* Cisco Router Configuration
* Cisco IOS Commands
* Router Interface Configuration
* `no shutdown`
* Router-to-Router Connectivity
* Dynamic Routing
* RIP Version 2
* `no auto-summary`
* RIP Network Advertisement
* Routing Table Verification
* `show ip route`
* `show ip protocols`
* Ping and Connectivity Testing
* Troubleshooting Network Connectivity

---

## 🛠️ Tools Used

* Cisco Packet Tracer
* Cisco 1941 Routers
* Cisco 2960 Switches
* PCs
* Cisco IOS CLI

---
