# NetZero Lab 20 — IP Source Guard

## 📌 Overview

This lab explores **IP Source Guard (IPSG)** as a network security mechanism used to prevent IP address spoofing on untrusted switch ports.

IP Source Guard is designed to work with the **DHCP Snooping binding database**. The switch can use the learned IP-MAC-port binding to validate traffic received from client ports.

> **Packet Tracer Limitation:**
> The Cisco 2960 switch IOS used in this lab does not support the `ip verify source` command. Therefore, the IP Source Guard configuration could not be enabled or demonstrated in Packet Tracer. The DHCP Snooping prerequisite was successfully configured and verified.

---

## 🎯 Objectives

* Configure a router as a DHCP server.
* Enable DHCP Snooping on the access switch.
* Configure the DHCP-server-facing port as trusted.
* Configure client ports as untrusted.
* Disable DHCP Option 82 for Packet Tracer compatibility.
* Obtain a DHCP address on a client.
* Verify the DHCP Snooping binding database.
* Attempt to configure IP Source Guard.
* Identify the Packet Tracer IOS limitation.

---

## 🏗️ Network Topology

```text
                 ┌─────────────────┐
                 │       R1        │
                 │  DHCP Server    │
                 │ 192.168.20.1/24 │
                 └────────┬────────┘
                          │
                       Fa0/1
                       TRUSTED
                          │
                 ┌────────┴────────┐
                 │       SW1       │
                 │      2960       │
                 └───────┬─────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
            Fa0/2                 Fa0/3
          UNTRUSTED              UNTRUSTED
              │                     │
            PC1                   PC2
```

---

## 🌐 IP Addressing

| Device | Interface | IP Address         | Configuration |
| ------ | --------- | ------------------ | ------------- |
| R1     | G0/0      | `192.168.20.1/24`  | Static        |
| PC1    | NIC       | `192.168.20.11/24` | DHCP          |
| PC2    | NIC       | DHCP               | DHCP          |
| SW1    | Fa0/1     | —                  | Trusted       |
| SW1    | Fa0/2     | —                  | Untrusted     |
| SW1    | Fa0/3     | —                  | Untrusted     |

---

# 🔧 1. Router Configuration

R1 was configured as the DHCP server.

```text
enable
configure terminal

hostname R1

interface gigabitEthernet 0/0
 ip address 192.168.20.1 255.255.255.0
 no shutdown
exit

ip dhcp excluded-address 192.168.20.1 192.168.20.10

ip dhcp pool NETZERO-LAB20
 network 192.168.20.0 255.255.255.0
 default-router 192.168.20.1
 dns-server 8.8.8.8
exit

end
```

---

# 🔧 2. Verify Router Interface

Command:

```text
show ip interface brief
```

Result:

```text
Interface              IP-Address      Status    Protocol
GigabitEthernet0/0     192.168.20.1    up        up
GigabitEthernet0/1     unassigned      administratively down
Vlan1                  unassigned      administratively down
```

The DHCP server interface was confirmed **up/up**.

---

# 🔧 3. Verify DHCP Pool

Command:

```text
show ip dhcp pool
```

Result:

```text
Pool NETZERO-LAB20 :

Total addresses                : 254
Leased addresses               : 1
Excluded addresses             : 1

Current index
192.168.20.1
```

The router successfully leased an address to the client.

---

# 🔐 4. Configure DHCP Snooping

On SW1:

```text
enable
configure terminal

ip dhcp snooping
ip dhcp snooping vlan 1

no ip dhcp snooping information option
```

### Configure trusted DHCP-server port

```text
interface fastEthernet 0/1
 ip dhcp snooping trust
exit
```

### Configure client ports

```text
interface range fastEthernet 0/2 - 3
 ip dhcp snooping limit rate 10
exit

end
```

---

# 🔍 5. Verify DHCP Snooping

Command:

```text
show ip dhcp snooping
```

Important configuration:

```text
Switch DHCP snooping is enabled

DHCP snooping is configured on following VLANs:
1

Insertion of option 82 is disabled

Interface                  Trusted    Rate limit (pps)

FastEthernet0/3            no         10
FastEthernet0/2            no         10
FastEthernet0/1            yes        unlimited
```

### Security configuration

| Port  | Role      | Rate Limit |
| ----- | --------- | ---------: |
| Fa0/1 | Trusted   |  Unlimited |
| Fa0/2 | Untrusted |     10 pps |
| Fa0/3 | Untrusted |     10 pps |

---

# 📋 6. DHCP Snooping Binding

Command:

```text
show ip dhcp snooping binding
```

Verified binding:

```text
MacAddress          IpAddress        Lease(sec)  Type           VLAN  Interface

00:90:2B:C3:5B:77   192.168.20.11    86400       dhcp-snooping  1     FastEthernet0/2

Total number of bindings: 1
```

### Binding interpretation

```text
MAC Address  →  00:90:2B:C3:5B:77
IP Address   →  192.168.20.11
VLAN         →  1
Port         →  Fa0/2
Lease        →  86400 seconds
```

This confirms that DHCP Snooping successfully learned the legitimate IP-MAC-port association.

---

# 🧪 7. Connectivity Test

From PC1:

```text
ping 192.168.20.1
```

Result:

```text
Pinging 192.168.20.1 with 32 bytes of data:

Reply from 192.168.20.1: bytes=32 time<1ms TTL=255
Reply from 192.168.20.1: bytes=32 time<1ms TTL=255
Reply from 192.168.20.1: bytes=32 time<1ms TTL=255
Reply from 192.168.20.1: bytes=32 time<1ms TTL=255

Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
```

### Result

**PC1 successfully communicated with the DHCP gateway.**

---

# 🛡️ 8. IP Source Guard Configuration Attempt

The intended IP Source Guard configuration was:

```text
interface FastEthernet0/2
 ip verify source
```

However, Packet Tracer returned:

```text
SW1(config-if)#ip verify source
                  ^
% Invalid input detected at '^' marker.
```

The command was therefore **not accepted by the Cisco 2960 IOS image used in Packet Tracer**.

The running configuration confirmed that the command was not installed.

---

# ⚠️ 9. Packet Tracer Limitation

The following verification command was also unavailable:

```text
show ip verify source
```

Packet Tracer returned:

```text
% Invalid input detected at '^' marker.
```

Therefore, IP Source Guard could not be fully implemented in this simulation.

This is documented as a **simulator/platform limitation**, not as a network configuration failure.

---

# 📊 10. Final Verification

| Feature                 | Status            |
| ----------------------- | ----------------- |
| R1 G0/0                 | ✅ Up/Up           |
| DHCP Server             | ✅ Working         |
| DHCP Pool               | ✅ Configured      |
| DHCP Snooping           | ✅ Enabled         |
| DHCP Snooping VLAN 1    | ✅ Enabled         |
| Trusted DHCP Port       | ✅ Fa0/1           |
| Untrusted Client Ports  | ✅ Fa0/2, Fa0/3    |
| DHCP Rate Limiting      | ✅ 10 pps          |
| DHCP Binding            | ✅ Learned         |
| PC1 DHCP Address        | ✅ `192.168.20.11` |
| PC1 → R1 Ping           | ✅ 4/4             |
| IP Source Guard         | ⚠️ Unsupported    |
| `show ip verify source` | ⚠️ Unsupported    |

---

# 🧠 Skills Learned

* DHCP Snooping
* DHCP trust boundaries
* Trusted vs. untrusted switch ports
* DHCP binding databases
* DHCP security
* IP address spoofing concepts
* IP Source Guard concepts
* Switch security configuration
* Packet Tracer IOS limitations
* Network troubleshooting and verification

---

# 🔑 Key Takeaway

**IP Source Guard relies on trusted DHCP Snooping information to validate the source IP address of devices connected to untrusted switch ports.**

The lab successfully established the required **DHCP Snooping foundation and binding database**, while the actual IP Source Guard command was unavailable in the selected Packet Tracer IOS image.

