# 🔐 NetZero Lab 17 — DHCP Snooping

## 📌 Overview

**NetZero Lab 17** demonstrates the configuration and verification of **DHCP Snooping** on a Cisco Layer 2 switch using Cisco Packet Tracer.

DHCP Snooping is a network security feature designed to protect LAN environments from **rogue or unauthorized DHCP servers**. It establishes a trust boundary between legitimate DHCP infrastructure and client-facing switch ports.

In this lab:

* **R1** acts as the legitimate DHCP server.
* **SW1** is configured with DHCP Snooping.
* **Fa0/1** is configured as a trusted DHCP server-facing port.
* **Fa0/2** and **Fa0/3** remain untrusted client-facing ports.
* DHCP Snooping dynamically creates a **binding table** containing legitimate client IP-to-MAC mappings.

---

## 🎯 Objectives

The objectives of this lab are to:

* Understand the purpose of DHCP Snooping.
* Configure a Cisco router as a DHCP server.
* Enable DHCP Snooping globally on a switch.
* Enable DHCP Snooping for VLAN 1.
* Configure the legitimate DHCP server-facing port as trusted.
* Keep client-facing ports untrusted.
* Disable DHCP Option 82 insertion for Packet Tracer compatibility.
* Verify DHCP Snooping operation.
* Verify dynamically learned DHCP bindings.
* Confirm that DHCP clients successfully obtain valid IP addresses.

---

## 🧠 What is DHCP Snooping?

**DHCP Snooping** is a Layer 2 security mechanism that filters DHCP messages based on the trust level of switch ports.

By default, switch ports are considered **untrusted**.

Only ports connected toward a legitimate DHCP server or trusted DHCP infrastructure should be configured as trusted.

### Without DHCP Snooping

```text
                DHCP Server
                     |
                     |
                    SW1
                  /    \
                 /      \
               PC1      Rogue DHCP
```

A rogue DHCP server could potentially respond to client DHCP requests.

### With DHCP Snooping

```text
              Legitimate DHCP Server
                       |
                    Fa0/1
                   TRUSTED
                       |
                   ┌───────┐
                   │  SW1  │
                   └───────┘
                    /     \
                Fa0/2     Fa0/3
              UNTRUSTED  UNTRUSTED
                  |          |
                 PC1        PC2
```

DHCP server responses are expected to enter through the trusted interface.

---

# 🏗️ Network Topology

```text
                         R1
                  DHCP Server
                192.168.17.1
                       |
                       |
                    Fa0/1
                   TRUSTED
                       |
                  ┌─────────┐
                  │   SW1   │
                  │ 2960    │
                  └─────────┘
                    /     \
                   /       \
              Fa0/2        Fa0/3
            UNTRUSTED    UNTRUSTED
                |            |
               PC1          PC2
```

---

## 🖥️ Devices Used

| Device           | Interface     | Role                     |
| ---------------- | ------------- | ------------------------ |
| Cisco Router R1  | G0/0          | DHCP Server              |
| Cisco Switch SW1 | Fa0/1         | Trusted DHCP Server Port |
| Cisco Switch SW1 | Fa0/2         | Untrusted Client Port    |
| Cisco Switch SW1 | Fa0/3         | Untrusted Client Port    |
| PC1              | FastEthernet0 | DHCP Client              |
| PC2              | FastEthernet0 | DHCP Client              |

---

# 🌐 IP Addressing

| Device | IP Address    | Subnet Mask   | Default Gateway |
| ------ | ------------- | ------------- | --------------- |
| R1     | 192.168.17.1  | 255.255.255.0 | —               |
| PC1    | 192.168.17.11 | 255.255.255.0 | 192.168.17.1    |
| PC2    | 192.168.17.12 | 255.255.255.0 | 192.168.17.1    |

### DHCP Configuration

```text
Network:       192.168.17.0/24
DHCP Pool:     NETZERO-LAB17
Default GW:    192.168.17.1
DNS Server:    8.8.8.8
Excluded:      192.168.17.1 – 192.168.17.10
```

---

# ⚙️ Configuration

## 1. Configure R1 as DHCP Server

```cisco
enable
configure terminal

interface gigabitEthernet 0/0
ip address 192.168.17.1 255.255.255.0
no shutdown
exit

ip dhcp excluded-address 192.168.17.1 192.168.17.10

ip dhcp pool NETZERO-LAB17
network 192.168.17.0 255.255.255.0
default-router 192.168.17.1
dns-server 8.8.8.8
exit

end
```

---

## 2. Verify R1

```cisco
show ip interface brief
```

Expected:

```text
GigabitEthernet0/0     192.168.17.1    YES manual up up
```

Verify the DHCP pool:

```cisco
show ip dhcp pool
```

Expected pool:

```text
Pool NETZERO-LAB17
Network 192.168.17.0 /24
```

---

# 🔐 3. Enable DHCP Snooping on SW1

```cisco
enable
configure terminal

ip dhcp snooping
ip dhcp snooping vlan 1

interface fastEthernet 0/1
ip dhcp snooping trust
exit

end
```

---

# ⚙️ 4. Disable DHCP Option 82

During testing in Cisco Packet Tracer, DHCP renewal initially failed while Option 82 insertion was enabled.

Therefore, Option 82 insertion was disabled:

```cisco
enable
configure terminal

no ip dhcp snooping information option

end
```

After this adjustment, DHCP clients successfully renewed their addresses and DHCP Snooping populated the binding table.

---

# 🔎 Verification

## DHCP Snooping Status

Command:

```cisco
show ip dhcp snooping
```

### Verified Result

```text
Switch DHCP snooping is enabled

DHCP snooping is configured on following VLANs:

1

Insertion of option 82 is disabled
Option 82 on untrusted port is not allowed
Verification of hwaddr field is enabled

Interface                  Trusted
-----------------------    -------
FastEthernet0/2            no
FastEthernet0/3            no
FastEthernet0/1            yes
```

### Interpretation

| Interface | Status      | Purpose                           |
| --------- | ----------- | --------------------------------- |
| Fa0/1     | ✅ Trusted   | Legitimate DHCP server connection |
| Fa0/2     | ❌ Untrusted | PC1 client port                   |
| Fa0/3     | ❌ Untrusted | PC2 client port                   |

This establishes the DHCP Snooping trust boundary.

---

# 📋 DHCP Snooping Binding Table

Command:

```cisco
show ip dhcp snooping binding
```

### Verified Result

```text
MacAddress          IpAddress        Lease(sec)  Type
------------------  ---------------  ----------  -------------
00:D0:FF:25:99:99   192.168.17.11    86400       dhcp-snooping
00:09:7C:83:54:9D   192.168.17.12    86400       dhcp-snooping

Total number of bindings: 2
```

### Binding Analysis

```text
PC1
MAC: 00:D0:FF:25:99:99
IP:  192.168.17.11
Port: Fa0/2
VLAN: 1
```

```text
PC2
MAC: 00:09:7C:83:54:9D
IP: 192.168.17.12
Port: Fa0/3
VLAN: 1
```

The switch successfully learned **two legitimate DHCP bindings**.

---

# 💻 DHCP Client Verification

## PC1

```text
IPv4 Address : 192.168.17.11
Subnet Mask  : 255.255.255.0
Gateway      : 192.168.17.1
DNS          : 8.8.8.8
```

## PC2

```text
IPv4 Address : 192.168.17.12
Subnet Mask  : 255.255.255.0
Gateway      : 192.168.17.1
DNS          : 8.8.8.8
```

Both PCs successfully obtained their addresses through DHCP.

---

# 🧪 DHCP Renewal Test

Initially, DHCP renewal failed after DHCP Snooping was enabled:

```text
DHCP request failed.
```

After disabling DHCP Option 82 insertion:

```cisco
no ip dhcp snooping information option
```

DHCP renewal succeeded.

### PC1

```text
C:\>ipconfig /renew

IP Address......................: 192.168.17.11
Subnet Mask.....................: 255.255.255.0
Default Gateway.................: 192.168.17.1
DNS Server......................: 8.8.8.8
```

### PC2

```text
C:\>ipconfig /renew

IP Address......................: 192.168.17.12
Subnet Mask.....................: 255.255.255.0
Default Gateway.................: 192.168.17.1
DNS Server......................: 8.8.8.8
```

---

# 🔍 MAC Address Table

Command:

```cisco
show mac address-table
```

The switch successfully learned the MAC address of the directly connected DHCP infrastructure.

The DHCP Snooping binding table provides the more important security verification for this lab because it associates the learned client IP addresses with their MAC addresses, VLAN, and switch interfaces.

---

# 🧠 Key Concepts Learned

### 1. Trusted Ports

A trusted port is allowed to receive legitimate DHCP server messages.

In this lab:

```text
Fa0/1 → Trusted
```

because it connects to R1.

### 2. Untrusted Ports

Client-facing ports remain untrusted:

```text
Fa0/2 → Untrusted
Fa0/3 → Untrusted
```

This prevents unauthorized DHCP server traffic from being treated as legitimate.

### 3. DHCP Snooping Binding Table

The switch dynamically records:

```text
MAC Address
     ↓
IP Address
     ↓
VLAN
     ↓
Switch Port
     ↓
Lease Information
```

This information can later be used by other Cisco security features such as **Dynamic ARP Inspection (DAI)** and **IP Source Guard**.

### 4. Option 82

DHCP Option 82 allows network devices to insert relay-agent information into DHCP messages.

In this Packet Tracer lab, Option 82 insertion caused DHCP renewal issues, so it was disabled for compatibility.

---

# 🛡️ Security Benefits

DHCP Snooping helps protect against:

* Rogue DHCP servers
* Unauthorized DHCP offers
* Incorrect default gateways
* Malicious DNS server assignments
* Certain DHCP-based network attacks

It also creates a trusted database that can support additional Layer 2 security mechanisms.

---

# 🧰 Important Commands

| Command                                  | Purpose                            |
| ---------------------------------------- | ---------------------------------- |
| `show ip dhcp snooping`                  | Verify DHCP Snooping configuration |
| `show ip dhcp snooping binding`          | Display learned DHCP bindings      |
| `show ip dhcp pool`                      | Verify DHCP pool                   |
| `show ip interface brief`                | Verify router interfaces           |
| `show mac address-table`                 | Display learned MAC addresses      |
| `ip dhcp snooping`                       | Enable DHCP Snooping               |
| `ip dhcp snooping vlan 1`                | Enable Snooping for VLAN 1         |
| `ip dhcp snooping trust`                 | Configure trusted interface        |
| `no ip dhcp snooping information option` | Disable Option 82 insertion        |

---

# 🧪 Troubleshooting Performed

### Problem

After enabling DHCP Snooping:

```text
DHCP request failed.
```

The PCs could no longer renew their DHCP leases.

### Investigation

Verified:

```text
DHCP Snooping → Enabled
VLAN 1 → Enabled
Fa0/1 → Trusted
Fa0/2 → Untrusted
Fa0/3 → Untrusted
```

The DHCP Snooping binding table initially contained:

```text
Total number of bindings: 0
```

### Solution

Disabled DHCP Option 82 insertion:

```cisco
no ip dhcp snooping information option
```

### Final Result

DHCP renewal succeeded and the switch learned:

```text
Total number of bindings: 2
```

This demonstrated practical troubleshooting rather than simply configuring the feature.

---

# ✅ Final Verification Checklist

* [x] R1 configured as DHCP server
* [x] DHCP pool `NETZERO-LAB17` created
* [x] R1 G0/0 configured with `192.168.17.1/24`
* [x] DHCP Snooping enabled
* [x] DHCP Snooping enabled on VLAN 1
* [x] Fa0/1 configured as trusted
* [x] Fa0/2 remains untrusted
* [x] Fa0/3 remains untrusted
* [x] DHCP Option 82 disabled for Packet Tracer compatibility
* [x] PC1 received `192.168.17.11`
* [x] PC2 received `192.168.17.12`
* [x] DHCP Snooping binding table populated
* [x] Total DHCP bindings: **2**
* [x] DHCP renewal successfully tested
* [x] Lab completed successfully

---

# 📚 Skills Demonstrated

```text
Cisco IOS
   │
   ├── DHCP Server Configuration
   ├── DHCP Snooping
   ├── VLAN Security
   ├── Trusted / Untrusted Ports
   ├── DHCP Binding Tables
   ├── Layer 2 Security
   ├── Network Troubleshooting
   └── Packet Tracer Verification
```

---

# 🚀 Real-World Relevance

DHCP Snooping is commonly used in enterprise switching environments as part of a broader **Layer 2 security strategy**.

It is especially valuable in networks where unauthorized devices could attempt to provide DHCP services.

DHCP Snooping also provides a foundation for technologies such as:

```text
DHCP Snooping
      │
      ├── Dynamic ARP Inspection (DAI)
      │
      └── IP Source Guard
```

These mechanisms can work together to improve protection against spoofing and unauthorized Layer 2 activity.

---

# 🏁 Lab Status

**NetZero Lab 17 — COMPLETED ✅**

