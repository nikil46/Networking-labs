markdown
# NetZero Lab 5 — DHCP Configuration

## 📌 Lab Overview

This lab demonstrates how to configure a Cisco router as a DHCP server and automatically assign IP addresses to PCs in a local network.

The router provides:

- IP addresses
- Subnet masks
- Default gateway
- DNS server information

The PCs obtain their network configuration automatically using DHCP.

---

## 🎯 Objectives

- Configure a Cisco router as a DHCP server
- Create a DHCP pool
- Configure the network address
- Configure the default gateway
- Configure a DNS server
- Exclude specific IP addresses from the DHCP pool
- Configure PCs to obtain IP addresses automatically
- Verify DHCP operation
- Test network connectivity

---

## 🛠️ Tools Used

- Cisco Packet Tracer
- Cisco 1941 Router
- Cisco 2960 Switch
- 2 PCs
- Copper Straight-Through Cables

---

## 🌐 Network Topology

```text
                 ┌─────────────────┐
                 │   Cisco 1941    │
                 │     Router      │
                 │ 192.168.10.1    │
                 │   DHCP Server   │
                 └────────┬────────┘
                          │
                          │
                 ┌────────┴────────┐
                 │   Cisco 2960    │
                 │     Switch      │
                 └───────┬─┬───────┘
                         │ │
                    ┌────┘ └────┐
                    │           │
                 ┌──┴──┐     ┌──┴──┐
                 │ PC0 │     │ PC1 │
                 │ DHCP│     │ DHCP│
                 └─────┘     └─────┘
````

---

## 📋 IP Addressing

| Device  | Interface          | IP Address   | Method |
| ------- | ------------------ | ------------ | ------ |
| Router0 | GigabitEthernet0/0 | 192.168.10.1 | Static |
| PC0     | FastEthernet0      | 192.168.10.x | DHCP   |
| PC1     | FastEthernet0      | 192.168.10.x | DHCP   |

### Network

```text
Network: 192.168.10.0/24
Subnet Mask: 255.255.255.0
Default Gateway: 192.168.10.1
DNS Server: 8.8.8.8
```

---

# ⚙️ Router Configuration

## Step 1 — Enter Privileged EXEC Mode

```text
enable
```

## Step 2 — Enter Global Configuration Mode

```text
configure terminal
```

## Step 3 — Configure Router Interface

```text
interface gigabitEthernet 0/0
ip address 192.168.10.1 255.255.255.0
no shutdown
exit
```

## Step 4 — Exclude IP Addresses

The first 10 IP addresses are excluded from DHCP so they can be reserved for network devices.

```text
ip dhcp excluded-address 192.168.10.1 192.168.10.10
```

## Step 5 — Create DHCP Pool

```text
ip dhcp pool NETZERO
network 192.168.10.0 255.255.255.0
default-router 192.168.10.1
dns-server 8.8.8.8
exit
```

## Step 6 — Exit Configuration Mode

```text
end
```

## Step 7 — Save Configuration

```text
copy running-config startup-config
```

When prompted:

```text
Destination filename [startup-config]?
```

Press:

```text
Enter
```

---

# 🔍 DHCP Verification

## Verify DHCP Pool

```text
show ip dhcp pool
```

Expected configuration:

```text
Pool NETZERO
Network: 192.168.10.0
Subnet Mask: 255.255.255.0
```

The DHCP pool provides addresses from:

```text
192.168.10.1 - 192.168.10.254
```

with the reserved addresses excluded.

---

## Verify DHCP Bindings

```text
show ip dhcp binding
```

This command displays the IP addresses leased to client devices.

---

## Verify Router Interfaces

```text
show ip interface brief
```

Expected result:

```text
GigabitEthernet0/0    192.168.10.1    up    up
```

---

# 💻 PC Configuration

## PC0

Go to:

```text
PC0
→ Desktop
→ IP Configuration
→ DHCP
```

PC0 automatically receives an IP address from the router.

---

## PC1

Go to:

```text
PC1
→ Desktop
→ IP Configuration
→ DHCP
```

PC1 automatically receives an IP address from the router.

---

# 🧪 Connectivity Testing

## Test 1 — PC0 to Router

From PC0 Command Prompt:

```text
ping 192.168.10.1
```

Result:

```text
Sent = 4
Received = 4
Lost = 0
```

---

## Test 2 — PC1 to Router

From PC1 Command Prompt:

```text
ping 192.168.10.1
```

Result:

```text
Sent = 4
Received = 4
Lost = 0
```

---

## Test 3 — PC0 to PC1

From PC0 Command Prompt:

```text
ping <PC1-IP-address>
```

Result:

```text
Sent = 4
Received = 4
Lost = 0
```

This confirms successful communication between both PCs.

---

# ✅ Final Verification

| Verification                       | Result |
| ---------------------------------- | ------ |
| Router interface configured        | ✅      |
| Router interface UP/UP             | ✅      |
| DHCP pool created                  | ✅      |
| DHCP excluded addresses configured | ✅      |
| PC0 receives IP automatically      | ✅      |
| PC1 receives IP automatically      | ✅      |
| PC0 → Router connectivity          | ✅      |
| PC1 → Router connectivity          | ✅      |
| PC0 → PC1 connectivity             | ✅      |
| Packet Loss                        | 0%     |

---

# 🧠 Skills Learned

* DHCP configuration
* Cisco IOS commands
* IPv4 addressing
* Subnetting
* DHCP address pools
* IP address reservation/exclusion
* Default gateway configuration
* DNS configuration
* Automatic IP assignment
* Network connectivity testing
* Router interface configuration
* Basic network troubleshooting
