# 🔐 NetZero Lab 18 — Dynamic ARP Inspection (DAI)

## 📌 Overview

**NetZero Lab 18** demonstrates the configuration and verification of **Dynamic ARP Inspection (DAI)** using Cisco switches in Cisco Packet Tracer.

Dynamic ARP Inspection is a Layer 2 security feature designed to protect a switched network from **ARP spoofing and ARP poisoning attacks**.

DAI validates ARP packets received on untrusted switch ports by comparing the information in the ARP packet against the **DHCP Snooping Binding Database**.

This lab builds directly upon:

* **NetZero Lab 16 — Port Security**
* **NetZero Lab 17 — DHCP Snooping**
* **NetZero Lab 18 — Dynamic ARP Inspection**

---

## 🎯 Objectives

The objectives of this lab were to:

* Configure DHCP Snooping.
* Configure Dynamic ARP Inspection.
* Establish trusted and untrusted switch ports.
* Use the DHCP Snooping binding database for ARP validation.
* Verify DAI operation.
* Verify ARP information from the end device.
* Understand how DAI protects against ARP spoofing.

---

## 🏗️ Network Topology

```text
                    ┌─────────────────┐
                    │       R1        │
                    │ DHCP Server     │
                    │ 192.168.18.1    │
                    └────────┬────────┘
                             │
                         G0/0 │
                             │
                         Fa0/1
                    ┌────────┴────────┐
                    │       SW1       │
                    │     2960        │
                    └───────┬───┬─────┘
                            │   │
                         Fa0/2 Fa0/3
                            │   │
                         ┌──┘   └──┐
                         │         │
                      ┌──┴──┐   ┌──┴──┐
                      │ PC1 │   │ PC2 │
                      └─────┘   └─────┘
```

---

## 🌐 IP Addressing

| Device | Interface | IP Address         | Role                  |
| ------ | --------- | ------------------ | --------------------- |
| R1     | G0/0      | `192.168.18.1/24`  | DHCP Server / Gateway |
| SW1    | Fa0/1     | —                  | Trusted Uplink        |
| PC1    | NIC       | `192.168.18.11/24` | DHCP Client           |
| PC2    | NIC       | DHCP               | DHCP Client           |

**Network:** `192.168.18.0/24`
**Default Gateway:** `192.168.18.1`

---

# ⚙️ Configuration

## 1. Configure R1 as DHCP Server

```cisco
enable
configure terminal

hostname R1

interface gigabitEthernet 0/0
ip address 192.168.18.1 255.255.255.0
no shutdown
exit

ip dhcp excluded-address 192.168.18.1 192.168.18.10

ip dhcp pool NETZERO-LAB18
network 192.168.18.0 255.255.255.0
default-router 192.168.18.1
dns-server 8.8.8.8
exit

end
write memory
```

### Verification

```cisco
show ip interface brief
```

Expected:

```text
GigabitEthernet0/0    192.168.18.1    YES manual    up    up
```

---

# 🔒 2. Configure DHCP Snooping on SW1

```cisco
enable
configure terminal

hostname SW1

interface fastEthernet 0/1
switchport mode access
exit

interface range fastEthernet 0/2 - 3
switchport mode access
exit

ip dhcp snooping
ip dhcp snooping vlan 1

interface fastEthernet 0/1
ip dhcp snooping trust
exit

end
write memory
```

---

# 🛠️ 3. Disable DHCP Option 82

During the lab, Packet Tracer's DHCP Option 82 behavior prevented DHCP clients from successfully obtaining addresses.

The following command was used:

```cisco
enable
configure terminal

no ip dhcp snooping information option

end
write memory
```

### Verification

```cisco
show ip dhcp snooping
```

Expected:

```text
Switch DHCP snooping is enabled

DHCP snooping is configured on following VLANs:

1

Insertion of option 82 is disabled
Option 82 on untrusted port is not allowed
```

The R1-facing port should appear as trusted:

```text
FastEthernet0/1    yes
```

---

# 🛡️ 4. Configure Dynamic ARP Inspection

Enable DAI for VLAN 1:

```cisco
enable
configure terminal

ip arp inspection vlan 1
```

Initially, DAI showed:

```text
Vlan 1 Configuration Enabled Operation Inactive
```

This occurred because the R1-facing interface was not yet trusted for DAI.

---

# 🔐 5. Trust the R1-Facing Interface

Configure Fa0/1 as a trusted DAI interface:

```cisco
interface fastEthernet 0/1
ip arp inspection trust
exit

end
write memory
```

The resulting trust model is:

| Interface | Connected Device | DHCP Snooping | DAI       |
| --------- | ---------------- | ------------- | --------- |
| Fa0/1     | R1               | Trusted       | Trusted   |
| Fa0/2     | PC1              | Untrusted     | Untrusted |
| Fa0/3     | PC2              | Untrusted     | Untrusted |

This is an important security principle:

> **Trust infrastructure-facing ports and keep end-user ports untrusted.**

---

# 🔍 Verification

## 1. Verify DHCP Snooping Binding

Command:

```cisco
show ip dhcp snooping binding
```

Observed result:

```text
MacAddress          IpAddress        Lease(sec)  Type
------------------  ---------------  ----------  -------------
00:01:42:75:55:11   192.168.18.11    86400       dhcp-snooping
```

The binding was associated with:

```text
VLAN       : 1
Interface  : FastEthernet0/2
IP Address : 192.168.18.11
MAC Address: 00:01:42:75:55:11
```

This confirms that DHCP Snooping successfully learned the legitimate DHCP assignment.

---

## 2. Verify Dynamic ARP Inspection

Command:

```cisco
show ip arp inspection
```

Observed:

```text
Source Mac Validation      : Disabled
Destination Mac Validation : Disabled
IP Address Validation     : Disabled

Vlan     Configuration    Operation
----     -------------    ---------
1        Enabled          Active
```

### Result

```text
VLAN 1 → Enabled / Active
```

This confirms that DAI is operational on VLAN 1.

---

## 3. Verify DAI Interfaces

Command:

```cisco
show ip arp inspection interfaces
```

Important result:

```text
Interface     Trust State
-----------   -----------
Fa0/1         Trusted
Fa0/2         Untrusted
Fa0/3         Untrusted
```

This confirms the intended security configuration.

---

## 4. Verify DAI Statistics

Command:

```cisco
show ip arp inspection statistics
```

Observed:

```text
Vlan      Forwarded        Dropped     DHCP Drops     ACL Drops
----      ---------        -------     -----------    ---------
1              0              0              0             0

Vlan   DHCP Permits    ACL Permits   Source MAC Failures
----   ------------    -----------   -------------------
1              0              0                     0

Vlan   Dest MAC Failures   IP Validation Failures
----   -----------------   ----------------------
1                   0                        0
```

The zero counters indicate that no ARP packets were recorded as forwarded or dropped by the DAI statistics mechanism during the test.

> **Packet Tracer Note:** DAI statistics may remain at zero during normal simulated ARP activity. Therefore, the DAI operational state, interface trust configuration, DHCP Snooping binding, and ARP table were used as the primary verification evidence.

---

## 5. Verify ARP Table on PC1

Command:

```text
arp -a
```

Observed:

```text
Internet Address      Physical Address      Type
192.168.18.1          0001.6375.e401        dynamic
```

This confirms that PC1 successfully learned the MAC address of the default gateway through ARP.

---

# 🧪 Connectivity Verification

PC1 was tested against the default gateway:

```text
ping 192.168.18.1
```

Expected result:

```text
Packets: Sent = 4, Received = 4, Lost = 0
```

Successful connectivity confirms that legitimate traffic continues to operate while DAI is enabled.

---

# 🔐 Security Concept

### What problem does DAI solve?

ARP does not inherently authenticate the sender of an ARP message.

An attacker could potentially send a forged ARP message such as:

```text
192.168.18.1 → Attacker's MAC Address
```

A victim may then incorrectly associate the gateway's IP address with the attacker's MAC address.

This technique can be used for:

* ARP spoofing
* ARP poisoning
* Man-in-the-Middle attacks
* Traffic interception

### How DAI helps

DAI inspects ARP packets arriving on **untrusted ports**.

The switch compares the ARP information against trusted information such as the DHCP Snooping binding database.

```text
                DHCP Server
                     │
                     ▼
              DHCP Snooping
                     │
                     ▼
           Binding Database
                     │
                     ▼
        Dynamic ARP Inspection
                     │
          ┌──────────┴──────────┐
          │                     │
       Valid ARP            Invalid ARP
          │                     │
          ▼                     ▼
       Forward                Drop
```

---

# 🔗 Relationship Between Labs

NetZero's Layer 2 security progression is now:

```text
Lab 16
Port Security
     │
     ▼
Controls which MAC addresses
can use a switch port
     │
     ▼
Lab 17
DHCP Snooping
     │
     ▼
Builds trusted DHCP bindings
     │
     ▼
Lab 18
Dynamic ARP Inspection
     │
     ▼
Validates ARP traffic
     │
     ▼
Lab 19
IP Source Guard
```

This creates a progressively stronger Layer 2 security architecture.

---

# 🧰 Troubleshooting

### Issue 1 — DHCP clients received APIPA addresses

PCs initially failed to obtain DHCP addresses.

Example APIPA address:

```text
169.254.x.x
```

### Solution

DHCP Option 82 was disabled:

```cisco
no ip dhcp snooping information option
```

After renewing DHCP, PC1 successfully received:

```text
192.168.18.11
```

---

### Issue 2 — DAI showed Inactive

Initial output:

```text
Vlan 1 Configuration Enabled Operation Inactive
```

### Solution

The R1-facing interface was configured as trusted:

```cisco
interface fastEthernet 0/1
ip arp inspection trust
```

DAI then changed to:

```text
VLAN 1 → Enabled / Active
```

---

### Issue 3 — DAI statistics remained zero

The command:

```cisco
show ip arp inspection statistics
```

returned zero counters.

This was not treated as a configuration failure because Packet Tracer does not always simulate or increment DAI statistics during ordinary ARP activity.

The configuration was instead verified using:

* DAI operational state
* DAI interface trust state
* DHCP Snooping binding database
* PC ARP table
* End-to-end connectivity

---

# 📋 Final Verification Checklist

| Verification                 | Result |
| ---------------------------- | ------ |
| R1 G0/0 up/up                | ✅      |
| DHCP Server configured       | ✅      |
| DHCP Snooping enabled        | ✅      |
| DHCP Snooping VLAN 1 enabled | ✅      |
| DHCP binding learned         | ✅      |
| R1-facing port trusted       | ✅      |
| DAI enabled on VLAN 1        | ✅      |
| DAI operational state Active | ✅      |
| Fa0/1 trusted                | ✅      |
| Fa0/2 untrusted              | ✅      |
| Fa0/3 untrusted              | ✅      |
| PC1 received DHCP address    | ✅      |
| Gateway ARP entry learned    | ✅      |
| Connectivity verified        | ✅      |

---

# 🧠 Key Skills Learned

* Dynamic ARP Inspection (DAI)
* DHCP Snooping
* Layer 2 network security
* ARP spoofing prevention
* Trusted and untrusted switch ports
* DHCP Snooping binding database
* Cisco IOS security configuration
* ARP table verification
* Packet Tracer troubleshooting
* Layer 2 attack mitigation

---

# 🚀 Real-World Relevance

DAI is commonly used as part of a broader enterprise Layer 2 security strategy.

A typical secure access-layer design can combine:

```text
Port Security
      +
DHCP Snooping
      +
Dynamic ARP Inspection
      +
IP Source Guard
      +
STP Security
```

Together, these mechanisms help protect the access layer against unauthorized devices, DHCP attacks, ARP spoofing, IP/MAC spoofing, and certain Layer 2 attacks.

---


---

# 🎓 Conclusion

**NetZero Lab 18 successfully demonstrated Dynamic ARP Inspection using Cisco Packet Tracer.**

The lab established a security relationship between **DHCP Snooping and DAI**, where DHCP Snooping creates trusted IP-to-MAC bindings and DAI uses those bindings to validate ARP traffic on untrusted interfaces.

The final configuration successfully achieved:

```text
DHCP Snooping       → Enabled
DHCP Binding        → Learned
DAI VLAN 1          → Active
R1 Interface        → Trusted
PC Interfaces       → Untrusted
ARP Gateway Entry   → Learned
Connectivity        → Successful
```

This lab strengthens the NetZero networking portfolio by demonstrating practical **Cisco Layer 2 security and ARP spoofing mitigation**.

