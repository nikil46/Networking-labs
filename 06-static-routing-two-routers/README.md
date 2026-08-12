``markdown
# NetZero Lab 6 — Static Routing Between Two Routers

## 📌 Objective

To configure and verify static routing between two different networks using two Cisco routers in Cisco Packet Tracer.

The lab demonstrates how routers communicate between different LANs using manually configured static routes.

---

## 🛠️ Tools Used

- Cisco Packet Tracer
- 2 × Cisco 1941 Routers
- 2 × Cisco 2960 Switches
- 2 × PCs
- Copper Straight-Through Cables

---

## 🌐 Network Topology

```text
PC0 ── Switch0 ── Router0 ───── Router1 ── Switch1 ── PC1
                    |              |
                 LAN 1          LAN 2
````

### Network Structure

```text
PC0
 |
Switch0
 |
Router0
 | G0/0 = 192.168.1.1
 | G0/1 = 10.0.0.1
 |
 | 10.0.0.0/24
 |
 | G0/1 = 10.0.0.2
Router1
 | G0/0 = 192.168.2.1
 |
Switch1
 |
PC1
```

---

## 📋 IP Addressing Table

| Device  | Interface          | IP Address   | Subnet Mask   | Default Gateway |
| ------- | ------------------ | ------------ | ------------- | --------------- |
| PC0     | FastEthernet0      | 192.168.1.10 | 255.255.255.0 | 192.168.1.1     |
| Router0 | GigabitEthernet0/0 | 192.168.1.1  | 255.255.255.0 | —               |
| Router0 | GigabitEthernet0/1 | 10.0.0.1     | 255.255.255.0 | —               |
| Router1 | GigabitEthernet0/1 | 10.0.0.2     | 255.255.255.0 | —               |
| Router1 | GigabitEthernet0/0 | 192.168.2.1  | 255.255.255.0 | —               |
| PC1     | FastEthernet0      | 192.168.2.10 | 255.255.255.0 | 192.168.2.1     |

---

# ⚙️ Router Configuration

## Router0 Configuration

```text
enable
configure terminal

hostname Router0

interface gigabitEthernet 0/0
ip address 192.168.1.1 255.255.255.0
no shutdown
exit

interface gigabitEthernet 0/1
ip address 10.0.0.1 255.255.255.0
no shutdown
exit

end
```

### Configure Static Route on Router0

Router0 needs a route to the `192.168.2.0/24` network through Router1.

```text
enable
configure terminal

ip route 192.168.2.0 255.255.255.0 10.0.0.2

end
```

---

# Router1 Configuration

```text
enable
configure terminal

hostname Router1

interface gigabitEthernet 0/0
ip address 192.168.2.1 255.255.255.0
no shutdown
exit

interface gigabitEthernet 0/1
ip address 10.0.0.2 255.255.255.0
no shutdown
exit

end
```

### Configure Static Route on Router1

Router1 needs a route to the `192.168.1.0/24` network through Router0.

```text
enable
configure terminal

ip route 192.168.1.0 255.255.255.0 10.0.0.1

end
```

---

# 💻 PC Configuration

## PC0

```text
IP Address:       192.168.1.10
Subnet Mask:      255.255.255.0
Default Gateway:  192.168.1.1
```

## PC1

```text
IP Address:       192.168.2.10
Subnet Mask:      255.255.255.0
Default Gateway:  192.168.2.1
```

---

# 🔍 Verification Commands

## Check Router0 Interfaces

```text
show ip interface brief
```

Expected:

```text
GigabitEthernet0/0    192.168.1.1    up    up
GigabitEthernet0/1    10.0.0.1       up    up
```

## Check Router1 Interfaces

```text
show ip interface brief
```

Expected:

```text
GigabitEthernet0/0    192.168.2.1    up    up
GigabitEthernet0/1    10.0.0.2       up    up
```

---

# 🛣️ Verify Static Routes

## Router0

```text
show ip route
```

Expected static route:

```text
S    192.168.2.0/24 [1/0] via 10.0.0.2
```

## Router1

```text
show ip route
```

Expected static route:

```text
S    192.168.1.0/24 [1/0] via 10.0.0.1
```

The letter `S` indicates that the route was manually configured as a static route.

---

# 🧪 Connectivity Testing

## PC0 → Router0

From PC0:

```text
ping 192.168.1.1
```

Result:

```text
Sent = 4
Received = 4
Lost = 0
```

## PC1 → Router1

From PC1:

```text
ping 192.168.2.1
```

Result:

```text
Sent = 4
Received = 4
Lost = 0
```

## PC0 → PC1

Final end-to-end connectivity test:

```text
ping 192.168.2.10
```

### ✅ Final Result

```text
Sent = 4
Received = 4
Lost = 0
```

This confirms successful communication between the two different LANs through Router0 and Router1 using static routing.

---

# 🧠 Skills Learned

* IPv4 Addressing
* Subnet Mask Configuration
* Default Gateway Configuration
* Cisco Router Interface Configuration
* `no shutdown` Command
* Router-to-Router Communication
* Static Routing
* Next-Hop Configuration
* Routing Table Verification
* `show ip route`
* `show ip interface brief`
* Ping Testing
* End-to-End Network Connectivity
* Basic Network Troubleshooting
