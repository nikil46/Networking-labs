 Lab 7 — NAT & PAT Configuration

## 📌 Objective

Configure and verify **NAT (Network Address Translation)** and **PAT (Port Address Translation)** using Cisco Packet Tracer.

The lab demonstrates how a private network can communicate through a router by translating private IP addresses into an address on the router's outside interface.

---

## 🛠️ Tools Used

* Cisco Packet Tracer
* Cisco 1941 Routers × 2
* Cisco 2960 Switch
* PC
* Server

---

## 🗺️ Network Topology

```text
PC0
 |
Switch
 |
R1
 |
R2
 |
Server
```

### IP Addressing

| Device | Interface    | IP Address   | Subnet Mask     |
| ------ | ------------ | ------------ | --------------- |
| PC0    | FastEthernet | 192.168.1.10 | 255.255.255.0   |
| R1     | G0/0         | 192.168.1.1  | 255.255.255.0   |
| R1     | G0/1         | 10.0.0.1     | 255.255.255.252 |
| R2     | G0/0         | 10.0.0.2     | 255.255.255.252 |
| R2     | G0/1         | 192.168.2.1  | 255.255.255.0   |
| Server | FastEthernet | 192.168.2.10 | 255.255.255.0   |

---

# ⚙️ Router Configuration

## R1 Configuration

```text
enable
configure terminal

interface gigabitEthernet 0/0
ip address 192.168.1.1 255.255.255.0
ip nat inside
no shutdown
exit

interface gigabitEthernet 0/1
ip address 10.0.0.1 255.255.255.252
ip nat outside
no shutdown
exit

ip route 192.168.2.0 255.255.255.0 10.0.0.2

access-list 1 permit 192.168.1.0 0.0.0.255

ip nat inside source list 1 interface gigabitEthernet 0/1 overload

end
```

---

## R2 Configuration

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

ip route 192.168.1.0 255.255.255.0 10.0.0.1

end
```

---

# 🔀 NAT Configuration

### Configure NAT Inside

```text
interface gigabitEthernet 0/0
ip nat inside
```

### Configure NAT Outside

```text
interface gigabitEthernet 0/1
ip nat outside
```

### Create NAT Access List

```text
access-list 1 permit 192.168.1.0 0.0.0.255
```

### Configure PAT / NAT Overload

```text
ip nat inside source list 1 interface gigabitEthernet 0/1 overload
```

---

# 🔎 NAT Verification

Command used:

```text
show ip nat translations
```

Example translation observed:

```text
Inside Global    Inside Local
10.0.0.1:44      192.168.1.10:44
```

This confirms that the private IP address:

```text
192.168.1.10
```

was translated to:

```text
10.0.0.1
```

using PAT.

---

# 📊 NAT Statistics

Command:

```text
show ip nat statistics
```

Verified:

```text
Outside Interface: GigabitEthernet0/1
Inside Interface: GigabitEthernet0/0
```

NAT traffic was successfully processed during connectivity testing.

---

# 🧪 Connectivity Testing

### Test 1 — PC to R1

```text
ping 192.168.1.1
```

Result:

```text
Sent = 4
Received = 4
Lost = 0
```

### Test 2 — PC to R2

```text
ping 10.0.0.2
```

Result:

```text
Sent = 4
Received = 4
Lost = 0
```

### Test 3 — PC to Server

```text
ping 192.168.2.10
```

Result:

```text
Sent = 4
Received = 4
Lost = 0
```

---

# 💾 Save Configuration

R1:

```text
copy running-config startup-config
```

R2:

```text
copy running-config startup-config
```

---

# 🧠 Key Concepts Learned

* NAT (Network Address Translation)
* PAT (Port Address Translation)
* NAT Overload
* Inside and Outside NAT Interfaces
* Private IPv4 Address Translation
* Static Routing
* IPv4 Addressing
* Cisco IOS Configuration
* NAT Verification
* Network Troubleshooting
* End-to-End Connectivity Testing

---

# 🏆 Lab Result

**NetZero Lab 7 — Successfully Completed ✅**

NAT/PAT was configured successfully and end-to-end connectivity was verified with:

```text
Sent = 4
Received = 4
Lost = 0
```

