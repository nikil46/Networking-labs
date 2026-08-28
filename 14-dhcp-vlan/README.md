# 🚀 NetZero Lab 14 — DHCP Server Configuration with VLAN 10

## 📌 Overview

This lab demonstrates how to configure a **Cisco router as a DHCP server** and provide automatic IPv4 addressing to a client through a Layer 2 switch.

The lab uses **VLAN 10** to connect the client and router interface. The router dynamically assigns IP addresses, subnet masks, default gateway, and DNS information to the PC.

This lab also includes practical troubleshooting of DHCP connectivity using MAC address tables, VLAN verification, interface status, and DHCP lease verification.

---

## 🎯 Objectives

* Configure a Cisco router as a DHCP server.
* Create a DHCP address pool.
* Configure excluded IP addresses.
* Configure default gateway and DNS server information.
* Configure VLAN 10 on the switch.
* Assign access ports to VLAN 10.
* Verify Layer 2 MAC address learning.
* Verify DHCP address assignment.
* Test connectivity between the PC and router.
* Troubleshoot DHCP failures using Cisco IOS commands.

---

## 🗺️ Network Topology

```text
                    VLAN 10
                      
        PC0 ---------------- SW1
         |                   |
         | Fa0/2             | Fa0/1
         |                   |
         +-------------------+
                             |
                             |
                            R1
                         G0/0
                      192.168.10.1
                             |
                        DHCP Server
```

### Physical Connections

```text
PC0 FastEthernet0  →  SW1 Fa0/2
R1 G0/0            →  SW1 Fa0/1
```

---

# 📋 IP Addressing Table

| Device | Interface     | IP Address   | Subnet Mask   | VLAN | Role                  |
| ------ | ------------- | ------------ | ------------- | ---- | --------------------- |
| R1     | G0/0          | 192.168.10.1 | 255.255.255.0 | 10   | DHCP Server / Gateway |
| PC0    | FastEthernet0 | DHCP         | 255.255.255.0 | 10   | DHCP Client           |
| SW1    | Fa0/1         | N/A          | N/A           | 10   | Connection to R1      |
| SW1    | Fa0/2         | N/A          | N/A           | 10   | Connection to PC0     |

### DHCP Address Range

```text
Network:        192.168.10.0/24
Default Gateway: 192.168.10.1
Excluded Range:  192.168.10.1 - 192.168.10.10
Available Range: 192.168.10.11 - 192.168.10.254
DNS Server:      8.8.8.8
```

---

# 🔧 Step 1 — Configure R1 Interface

Enter privileged mode:

```bash
enable
```

Enter configuration mode:

```bash
configure terminal
```

Configure the router interface:

```bash
interface gigabitEthernet 0/0
ip address 192.168.10.1 255.255.255.0
no shutdown
exit
```

Verify:

```bash
show ip interface brief
```

Expected:

```text
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     192.168.10.1    YES manual up                    up
```

---

# 🔧 Step 2 — Configure VLAN 10 on SW1

On SW1:

```bash
enable
configure terminal
```

Create VLAN 10:

```bash
vlan 10
name NETZERO-DHCP
exit
```

---

# 🔧 Step 3 — Configure SW1 Port Connected to R1

R1 is connected to **Fa0/1**.

Configure the port as an access port in VLAN 10:

```bash
interface fastEthernet 0/1
switchport mode access
switchport access vlan 10
exit
```

---

# 🔧 Step 4 — Configure SW1 Port Connected to PC0

PC0 is connected to **Fa0/2**.

```bash
interface fastEthernet 0/2
switchport mode access
switchport access vlan 10
exit
```

Exit configuration mode:

```bash
end
```

---

# 🔧 Step 5 — Verify VLAN Configuration

Run:

```bash
show vlan brief
```

Expected:

```text
10   NETZERO-DHCP    active    Fa0/1, Fa0/2
```

This confirms that both the router connection and PC connection belong to VLAN 10.

---

# 🔧 Step 6 — Configure DHCP on R1

Enter configuration mode:

```bash
enable
configure terminal
```

Exclude the router/gateway and reserved addresses:

```bash
ip dhcp excluded-address 192.168.10.1 192.168.10.10
```

Create the DHCP pool:

```bash
ip dhcp pool NETZERO-LAB14
network 192.168.10.0 255.255.255.0
default-router 192.168.10.1
dns-server 8.8.8.8
exit
```

Exit:

```bash
end
```

---

# 📦 DHCP Configuration Summary

The final DHCP configuration is:

```text
ip dhcp excluded-address 192.168.10.1 192.168.10.10

ip dhcp pool NETZERO-LAB14
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 dns-server 8.8.8.8
```

---

# 🔍 Step 7 — Verify DHCP Configuration

Run:

```bash
show running-config | section dhcp
```

Expected:

```text
ip dhcp excluded-address 192.168.10.1 192.168.10.10

ip dhcp pool NETZERO-LAB14
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 dns-server 8.8.8.8
```

---

# 🔍 Step 8 — Verify DHCP Pool

Run:

```bash
show ip dhcp pool NETZERO-LAB14
```

Important information:

```text
Pool NETZERO-LAB14
Network: 192.168.10.0/24
Default Router: 192.168.10.1
```

Before a client receives an address:

```text
Leased addresses: 0
```

After successful DHCP assignment, the leased address count should increase.

---

# 💻 Step 9 — Configure PC0 as DHCP Client

Open:

```text
PC0 → Desktop → IP Configuration
```

Select:

```text
DHCP
```

Alternatively, use the PC command prompt:

```bash
ipconfig /release
ipconfig /renew
```

Then verify:

```bash
ipconfig
```

Expected configuration:

```text
IP Address:       192.168.10.x
Subnet Mask:      255.255.255.0
Default Gateway:  192.168.10.1
DNS Server:       8.8.8.8
```

The exact IP address depends on the DHCP lease.

---

# 🔎 Step 10 — Verify DHCP Lease on R1

Run:

```bash
show ip dhcp binding
```

After successful DHCP assignment, R1 should display the dynamically assigned address and client information.

Example:

```text
IP address       Client-ID/              Lease expiration
                 Hardware address

192.168.10.11    <client information>    ...
```

---

# 🔎 Step 11 — Verify MAC Address Learning

On SW1:

```bash
show mac address-table dynamic
```

The final lab verification showed:

```text
Vlan    Mac Address       Type        Ports
----    -----------       --------    -----
10      0001.97e4.8a9a    DYNAMIC     Fa0/2
10      00e0.b0dc.5701    DYNAMIC     Fa0/1
```

### MAC Address Mapping

| Device  | MAC Address      | Switch Port |
| ------- | ---------------- | ----------- |
| PC0     | `0001.97e4.8a9a` | Fa0/2       |
| R1 G0/0 | `00e0.b0dc.5701` | Fa0/1       |

This confirms that both PC0 and R1 are correctly connected through **VLAN 10**.

---

# 🧪 Step 12 — Test Connectivity

From PC0:

```bash
ping 192.168.10.1
```

Expected:

```text
Reply from 192.168.10.1
```

A successful test should show:

```text
Sent = 4
Received = 4
Lost = 0
```

This confirms connectivity between the DHCP client and router gateway.

---

# 🛠️ DHCP Troubleshooting Performed

During this lab, DHCP initially failed:

```text
C:\>ipconfig /renew

DHCP request failed.
```

The issue was investigated systematically rather than changing random configurations.

### 1. Checked R1 interface

```bash
show ip interface brief
```

Result:

```text
GigabitEthernet0/0     192.168.10.1    YES manual up up
```

This confirmed that R1's gateway interface was operational.

---

### 2. Checked DHCP configuration

```bash
show running-config | section dhcp
```

Configuration:

```text
ip dhcp excluded-address 192.168.10.1 192.168.10.10

ip dhcp pool NETZERO-LAB14
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 dns-server 8.8.8.8
```

---

### 3. Checked DHCP bindings

```bash
show ip dhcp binding
```

Initially:

```text
No DHCP leases
```

This confirmed that the PC was not receiving an address.

---

### 4. Checked VLAN configuration

Initially, SW1 ports were in VLAN 1.

The DHCP network required VLAN 10.

The ports were therefore configured as:

```text
Fa0/1 → VLAN 10
Fa0/2 → VLAN 10
```

---

### 5. Verified switch MAC learning

After correcting the VLAN configuration:

```bash
show mac address-table dynamic
```

Final result:

```text
Vlan    Mac Address       Type        Ports
10      0001.97e4.8a9a    DYNAMIC     Fa0/2
10      00e0.b0dc.5701    DYNAMIC     Fa0/1
```

This confirmed that both endpoints were visible to the switch.

---

### 6. Recreated the DHCP Pool

The DHCP pool was removed and recreated to eliminate any possible Packet Tracer DHCP state/configuration issue:

```bash
no ip dhcp pool NETZERO-LAB14

no ip dhcp excluded-address 192.168.10.1 192.168.10.10

ip dhcp excluded-address 192.168.10.1 192.168.10.10

ip dhcp pool NETZERO-LAB14
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 dns-server 8.8.8.8
exit
```

This restored a clean DHCP configuration.

---

# 📊 Verification Commands

### R1

```bash
show ip interface brief
show running-config | section dhcp
show ip dhcp pool NETZERO-LAB14
show ip dhcp binding
show ip dhcp conflict
show ip arp
show interfaces gigabitEthernet 0/0
```

### SW1

```bash
show vlan brief
show interfaces status
show interfaces fa0/1 status
show interfaces fa0/2 status
show interfaces fa0/1 switchport
show interfaces fa0/2 switchport
show mac address-table dynamic
```

### PC0

```bash
ipconfig
ipconfig /all
ipconfig /release
ipconfig /renew
ping 192.168.10.1
```

---

# ✅ Final Verification Checklist

| Test                 | Expected Result   | Status |
| -------------------- | ----------------- | ------ |
| R1 G0/0 configured   | `192.168.10.1/24` | ✅      |
| R1 G0/0 operational  | Up/Up             | ✅      |
| VLAN 10 created      | `NETZERO-DHCP`    | ✅      |
| R1 port in VLAN 10   | Fa0/1             | ✅      |
| PC0 port in VLAN 10  | Fa0/2             | ✅      |
| PC0 MAC learned      | Fa0/2             | ✅      |
| R1 MAC learned       | Fa0/1             | ✅      |
| DHCP pool created    | `NETZERO-LAB14`   | ✅      |
| DHCP network         | `192.168.10.0/24` | ✅      |
| Gateway              | `192.168.10.1`    | ✅      |
| DNS                  | `8.8.8.8`         | ✅      |
| PC0 receives DHCP IP | `192.168.10.x`    | ✅      |
| DHCP binding created | Yes               | ✅      |
| Gateway ping         | Successful        | ✅      |

---

# 🧠 Skills Learned

### Networking

* IPv4 addressing
* Subnetting
* VLAN configuration
* Access port configuration
* Layer 2 switching
* MAC address learning
* Default gateway configuration

### DHCP

* DHCP server configuration
* DHCP address pools
* DHCP excluded addresses
* DHCP client configuration
* DHCP lease verification
* DHCP troubleshooting

### Cisco IOS

* `show ip interface brief`
* `show running-config`
* `show ip dhcp pool`
* `show ip dhcp binding`
* `show ip dhcp conflict`
* `show vlan brief`
* `show interfaces status`
* `show mac address-table dynamic`

### Troubleshooting

* Identifying incorrect VLAN assignments
* Mapping MAC addresses to switch ports
* Verifying physical interface status
* Checking Layer 2 connectivity
* Isolating DHCP-specific problems
* Systematic network troubleshooting

---

# 💡 Key Learning

A DHCP problem is not always caused by the DHCP configuration itself.

The DHCP process depends on the complete path:

```text
DHCP Client
     ↓
Switch Port
     ↓
Correct VLAN
     ↓
Router Interface
     ↓
DHCP Server/Pool
     ↓
DHCP Offer
     ↓
Client receives IP
```

In this lab, checking the **MAC address table** was particularly useful because it showed whether PC0 and R1 were actually being learned on the expected VLAN and ports.

---

# 🏁 Lab Result

**NetZero Lab 14 — DHCP Server Configuration**

### Status: ✅ COMPLETED

The Cisco router successfully provides DHCP services to PC0 through VLAN 10.

PC0 can dynamically obtain an IPv4 address from the `NETZERO-LAB14` DHCP pool and communicate with the router gateway at:

```text
192.168.10.1
```

