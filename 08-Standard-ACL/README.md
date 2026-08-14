# NetZero Lab 8 — Standard ACL (Access Control List)

## 📌 Objective

Configure a network using two routers and implement a **Standard Access Control List (ACL)** to control traffic between two different LAN networks.

The objective is to allow normal network communication while specifically blocking traffic originating from **PC0 (192.168.1.10)** from reaching the **192.168.2.0/24 network**.

---

## 🖥️ Network Topology

```text
PC0
 |
Switch0
 |
Router0
 |
 | 10.0.0.0/30
 |
Router1
 |
Switch1
 |
PC1
```

---

## 🌐 IP Addressing

| Device  | Interface    | IP Address   | Subnet Mask     |
| ------- | ------------ | ------------ | --------------- |
| PC0     | FastEthernet | 192.168.1.10 | 255.255.255.0   |
| Router0 | G0/0         | 192.168.1.1  | 255.255.255.0   |
| Router0 | G0/1         | 10.0.0.1     | 255.255.255.252 |
| Router1 | G0/0         | 10.0.0.2     | 255.255.255.252 |
| Router1 | G0/1         | 192.168.2.1  | 255.255.255.0   |
| PC1     | FastEthernet | 192.168.2.10 | 255.255.255.0   |

---

## 🔧 PC Configuration

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

ip route 192.168.2.0 255.255.255.0 10.0.0.2

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

ip route 192.168.1.0 255.255.255.0 10.0.0.1

end
```

---

## 🔐 Standard ACL Configuration

A Standard ACL was created to block traffic originating from PC0.

```text
enable
configure terminal

access-list 10 deny host 192.168.1.10
access-list 10 permit any
```

### Apply ACL to Router1 G0/1

```text
interface gigabitEthernet 0/1
ip access-group 10 out
exit

end
```

The ACL was applied **outbound on Router1 G0/1** so that traffic destined for the `192.168.2.0/24` network from PC0 is blocked.

---

## 🔍 ACL Verification

Command:

```text
show access-lists
```

Expected output:

```text
Standard IP access list 10
    10 deny host 192.168.1.10
    20 permit any
```

Verify interface ACL:

```text
show ip interface gigabitEthernet 0/1
```

The interface should show:

```text
Outgoing access list is 10
```

---

## 🧪 Connectivity Testing

### Before ACL

PC0 → PC1:

```text
ping 192.168.2.10
```

Result:

```text
Packets: Sent = 4, Received = 4, Lost = 0
```

✅ Connectivity successfully established before applying the ACL.

### After ACL

PC0 → PC1:

```text
ping 192.168.2.10
```

Result:

```text
Packets: Sent = 4, Received = 0, Lost = 4
```

❌ PC0 traffic successfully blocked by the ACL.

### Reverse Connectivity Test

PC1 → PC0:

```text
ping 192.168.1.10
```

Result:

```text
Packets: Sent = 4, Received = 4, Lost = 0
```

✅ PC1 can still communicate with PC0.

---

## 📊 Final ACL Behavior

```text
PC0 (192.168.1.10)
        |
        | ❌ BLOCKED
        ↓
Router1 → PC1 (192.168.2.10)


PC1 (192.168.2.10)
        |
        | ✅ ALLOWED
        ↓
Router1 → PC0 (192.168.1.10)
```

---

## 🧠 Skills Learned

* Standard Access Control Lists (ACL)
* IPv4 addressing
* Subnetting
* Static routing
* Cisco IOS configuration
* ACL `deny` statements
* ACL `permit` statements
* Applying ACLs to router interfaces
* Inbound vs outbound ACL concepts
* ACL troubleshooting
* `show access-lists`
* `show ip interface`
* Ping-based connectivity testing
* Network traffic filtering

---

## 🛠️ Tools Used

* Cisco Packet Tracer
* Cisco 1941 Routers
* Cisco 2960 Switches
* PCs
* Cisco IOS CLI
