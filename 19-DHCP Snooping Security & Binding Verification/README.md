# 🔐 NetZero Lab 19 — DHCP Snooping Security & Binding Verification

## 📌 Overview

**NetZero Lab 19** demonstrates the implementation and verification of **DHCP Snooping** as a Layer 2 network security mechanism.

The lab builds upon the DHCP and Layer 2 security concepts covered in previous NetZero labs. A Cisco router is configured as a DHCP server, while a Cisco Catalyst 2960 switch is configured to distinguish between **trusted and untrusted DHCP interfaces**.

The switch dynamically builds a **DHCP Snooping Binding Table** containing the legitimate client MAC addresses, IP addresses, VLAN information, and switch interfaces.

This lab also demonstrates DHCP rate limiting on untrusted ports and verifies end-to-end connectivity after DHCP Snooping is enabled.

> **Note:** IP Source Guard was initially planned for this lab, but the Packet Tracer 2960 IOS used in this environment does not support the `ip verify source` command. Therefore, IP Source Guard was not included as an implemented feature.

---

## 🎯 Objectives

* Configure a Cisco router as a DHCP server.
* Configure DHCP address exclusions.
* Enable DHCP Snooping on a Cisco switch.
* Enable DHCP Snooping for VLAN 1.
* Configure trusted and untrusted switch ports.
* Configure DHCP rate limiting on client-facing ports.
* Disable DHCP Option 82 for Packet Tracer compatibility.
* Generate DHCP Snooping bindings from legitimate DHCP clients.
* Verify the DHCP Snooping Binding Table.
* Test client-to-router and client-to-client connectivity.
* Understand how DHCP Snooping protects against unauthorized DHCP activity.

---

## 🧰 Technologies & Tools

* **Cisco Packet Tracer**
* Cisco Router
* Cisco Catalyst 2960 Switch
* DHCP
* DHCP Snooping
* Layer 2 Security
* VLAN 1
* Ethernet
* ICMP
* Network troubleshooting and verification

---

## 🖥️ Network Topology

```text
                       ┌─────────────────┐
                       │       R1        │
                       │   DHCP Server   │
                       │ 192.168.19.1/24│
                       └────────┬────────┘
                                │
                              Fa0/1
                              TRUSTED
                                │
                       ┌────────┴────────┐
                       │      SW1        │
                       │     2960        │
                       │ DHCP Snooping   │
                       └───────┬─┬───────┘
                               │ │
                         Fa0/2 │ │ Fa0/3
                       UNTRUSTED│ │UNTRUSTED
                               │ │
                          ┌────┘ └────┐
                          │           │
                       ┌──┴───┐   ┌──┴───┐
                       │ PC1  │   │ PC2  │
                       │DHCP  │   │DHCP  │
                       └──────┘   └──────┘
```

---

## 🔌 Device & Port Connections

| Device | Interface | Connected To | Purpose               |
| ------ | --------- | ------------ | --------------------- |
| R1     | G0/0      | SW1 Fa0/1    | DHCP server/uplink    |
| SW1    | Fa0/1     | R1 G0/0      | Trusted DHCP port     |
| SW1    | Fa0/2     | PC1          | Untrusted client port |
| SW1    | Fa0/3     | PC2          | Untrusted client port |

---

## 🌐 IP Addressing Table

| Device | Interface | IP Address    | Subnet Mask   | Default Gateway | Method |
| ------ | --------- | ------------- | ------------- | --------------- | ------ |
| R1     | G0/0      | 192.168.19.1  | 255.255.255.0 | —               | Static |
| PC1    | Fa0       | 192.168.19.11 | 255.255.255.0 | 192.168.19.1    | DHCP   |
| PC2    | Fa0       | 192.168.19.12 | 255.255.255.0 | 192.168.19.1    | DHCP   |

### Network Information

```text
Network:        192.168.19.0/24
Gateway:        192.168.19.1
DHCP Pool:      NETZERO-LAB19
DHCP Range:     192.168.19.11 – 192.168.19.254
Excluded:       192.168.19.1 – 192.168.19.10
DNS Server:     8.8.8.8
VLAN:           1
```

---

# ⚙️ Configuration

## 1️⃣ Configure R1 as DHCP Server

### Configure Router Interface

```cisco
enable
configure terminal

hostname R1

interface gigabitEthernet 0/0
ip address 192.168.19.1 255.255.255.0
no shutdown
exit
```

### Configure DHCP Exclusions

The first ten addresses were reserved for infrastructure:

```cisco
ip dhcp excluded-address 192.168.19.1
ip dhcp excluded-address 192.168.19.2
ip dhcp excluded-address 192.168.19.3
ip dhcp excluded-address 192.168.19.4
ip dhcp excluded-address 192.168.19.5
ip dhcp excluded-address 192.168.19.6
ip dhcp excluded-address 192.168.19.7
ip dhcp excluded-address 192.168.19.8
ip dhcp excluded-address 192.168.19.9
ip dhcp excluded-address 192.168.19.10
```

### Configure DHCP Pool

```cisco
ip dhcp pool NETZERO-LAB19
network 192.168.19.0 255.255.255.0
default-router 192.168.19.1
dns-server 8.8.8.8
exit
```

Save the configuration:

```cisco
end
write memory
```

---

# 2️⃣ Verify R1 DHCP Configuration

### Verify Interface Status

```cisco
show ip interface brief
```

Important result:

```text
GigabitEthernet0/0     192.168.19.1    YES manual up    up
```

### Verify DHCP Pool

```cisco
show ip dhcp pool
```

Final verification:

```text
Pool NETZERO-LAB19

Total addresses                : 254
Leased addresses               : 0
Excluded addresses             : 10
```

### Verify DHCP Configuration

```cisco
show running-config | section dhcp
```

Final configuration:

```text
ip dhcp excluded-address 192.168.19.1
ip dhcp excluded-address 192.168.19.2
ip dhcp excluded-address 192.168.19.3
ip dhcp excluded-address 192.168.19.4
ip dhcp excluded-address 192.168.19.5
ip dhcp excluded-address 192.168.19.6
ip dhcp excluded-address 192.168.19.7
ip dhcp excluded-address 192.168.19.8
ip dhcp excluded-address 192.168.19.9
ip dhcp excluded-address 192.168.19.10

ip dhcp pool NETZERO-LAB19
 network 192.168.19.0 255.255.255.0
 default-router 192.168.19.1
 dns-server 8.8.8.8
```

---

# 3️⃣ Configure PC1 and PC2 for DHCP

On each PC:

```text
Desktop
   ↓
IP Configuration
   ↓
DHCP
```

### PC1

```text
IPv4 Address:    192.168.19.11
Subnet Mask:     255.255.255.0
Default Gateway: 192.168.19.1
```

### PC2

```text
IPv4 Address:    192.168.19.12
Subnet Mask:     255.255.255.0
Default Gateway: 192.168.19.1
```

Both clients successfully received their addresses from the R1 DHCP server.

---

# 4️⃣ Configure DHCP Snooping on SW1

Enter configuration mode:

```cisco
enable
configure terminal
```

Enable DHCP Snooping:

```cisco
ip dhcp snooping
ip dhcp snooping vlan 1
```

### Configure R1-facing interface as Trusted

```cisco
interface fastEthernet 0/1
ip dhcp snooping trust
exit
```

### Configure PC1-facing interface

```cisco
interface fastEthernet 0/2
ip dhcp snooping limit rate 10
exit
```

### Configure PC2-facing interface

```cisco
interface fastEthernet 0/3
ip dhcp snooping limit rate 10
exit
```

Save configuration:

```cisco
end
write memory
```

---

# 5️⃣ DHCP Option 82 Adjustment

Initially, DHCP Option 82 was enabled.

In the Packet Tracer environment, DHCP renewal failed while Option 82 was enabled.

The following command was used:

```cisco
configure terminal
no ip dhcp snooping information option
end
```

After disabling Option 82, DHCP renewal succeeded.

Final configuration:

```text
Insertion of option 82 is disabled
```

This demonstrates an important troubleshooting consideration when working with simulated Cisco IOS environments.

---

# 6️⃣ Verify DHCP Snooping

Run:

```cisco
show ip dhcp snooping
```

Final verified configuration:

```text
Switch DHCP snooping is enabled

DHCP snooping is configured on following VLANs:

1

Insertion of option 82 is disabled
Option 82 on untrusted port is not allowed
Verification of hwaddr field is enabled

Interface                  Trusted    Rate limit (pps)

FastEthernet0/2            no         10
FastEthernet0/1            yes        unlimited
FastEthernet0/3            no         10
```

### Port Security Roles

```text
Fa0/1 → TRUSTED
Fa0/2 → UNTRUSTED
Fa0/3 → UNTRUSTED
```

The switch therefore accepts legitimate DHCP server traffic through the trusted router-facing interface while treating client-facing ports as untrusted.

---

# 7️⃣ DHCP Snooping Binding Table

After renewing the DHCP leases on PC1 and PC2, SW1 dynamically learned the client bindings.

Command:

```cisco
show ip dhcp snooping binding
```

### Verified Output

```text
MacAddress          IpAddress        Lease(sec)  Type           VLAN  Interface

00:90:0C:E9:0A:EB   192.168.19.11    86400       dhcp-snooping  1     FastEthernet0/2

00:05:5E:04:25:96   192.168.19.12    86400       dhcp-snooping  1     FastEthernet0/3

Total number of bindings: 2
```

### Binding Analysis

| Client | MAC Address         | IP Address      | VLAN | Interface |     Lease |
| ------ | ------------------- | --------------- | ---: | --------- | --------: |
| PC1    | `00:90:0C:E9:0A:EB` | `192.168.19.11` |    1 | Fa0/2     | 86400 sec |
| PC2    | `00:05:5E:04:25:96` | `192.168.19.12` |    1 | Fa0/3     | 86400 sec |

This confirms that SW1 has successfully associated each legitimate DHCP client with its IP address, MAC address, VLAN, and physical interface.

---

# 🧪 Connectivity Testing

## PC1 → R1

```text
ping 192.168.19.1
```

Result:

```text
Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
```

✅ Successful.

---

## PC2 → R1

```text
ping 192.168.19.1
```

Result:

```text
Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
```

✅ Successful.

---

## PC1 → PC2

```text
ping 192.168.19.12
```

Result:

```text
Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
```

✅ Successful.

---

## PC2 → PC1

```text
ping 192.168.19.11
```

Result:

```text
Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
```

✅ Successful.

---

# 🛠️ Troubleshooting

## Issue 1 — DHCP Pool Exclusion

Initially, the DHCP pool showed:

```text
Excluded addresses : 0
```

The DHCP exclusion was corrected by explicitly excluding `.1` through `.10`.

Final result:

```text
Excluded addresses : 10
```

---

## Issue 2 — DHCP Renewal Failed

After enabling DHCP Snooping, DHCP renewal initially failed:

```text
DHCP request failed.
```

Investigation showed that DHCP Option 82 was enabled.

Option 82 was disabled:

```cisco
no ip dhcp snooping information option
```

After this change, DHCP renewal succeeded and the switch learned both DHCP bindings.

---

## Issue 3 — Empty DHCP Snooping Binding Table

Initially:

```text
Total number of bindings: 0
```

The clients had received their DHCP addresses before DHCP Snooping was enabled.

After releasing and renewing the DHCP leases:

```text
Total number of bindings: 2
```

This confirmed successful DHCP Snooping operation.

---

## Issue 4 — IP Source Guard Command Unsupported

The command:

```cisco
ip verify source
```

was attempted on the client interfaces but returned:

```text
% Invalid input detected
```

The verification command:

```cisco
show ip verify source
```

was also unsupported.

### Conclusion

The Packet Tracer 2960 IOS used in this lab does not provide the required IP Source Guard command support.

Therefore, IP Source Guard was **not included as an implemented feature** in the final lab.

This is documented intentionally rather than treating an unsupported Packet Tracer feature as successfully configured.

---

## Issue 5 — DHCP Snooping Statistics Command Unsupported

The following command was attempted:

```cisco
show ip dhcp snooping statistics
```

Packet Tracer returned:

```text
% Invalid input detected
```

This command is therefore not supported by the IOS image used in this simulation.

The DHCP Snooping functionality itself was successfully verified through:

```cisco
show ip dhcp snooping
show ip dhcp snooping binding
```

---

# 🔍 Final Verification Checklist

| Verification              | Result                              |
| ------------------------- | ----------------------------------- |
| R1 G0/0 up/up             | ✅                                   |
| R1 DHCP Server            | ✅                                   |
| DHCP Pool configured      | ✅                                   |
| DHCP exclusions `.1–.10`  | ✅                                   |
| PC1 received DHCP address | ✅                                   |
| PC2 received DHCP address | ✅                                   |
| DHCP Snooping enabled     | ✅                                   |
| VLAN 1 Snooping enabled   | ✅                                   |
| Fa0/1 trusted             | ✅                                   |
| Fa0/2 untrusted           | ✅                                   |
| Fa0/3 untrusted           | ✅                                   |
| DHCP rate limiting        | ✅ 10 pps                            |
| Option 82 disabled        | ✅                                   |
| PC1 DHCP binding          | ✅                                   |
| PC2 DHCP binding          | ✅                                   |
| Total bindings            | ✅ 2                                 |
| PC1 → R1                  | ✅ 4/4                               |
| PC2 → R1                  | ✅ 4/4                               |
| PC1 → PC2                 | ✅ 4/4                               |
| PC2 → PC1                 | ✅ 4/4                               |
| IP Source Guard           | ⚠️ Unsupported by Packet Tracer IOS |
| DHCP Snooping Statistics  | ⚠️ Unsupported by Packet Tracer IOS |

---

# 🧠 Key Concepts Learned

### DHCP Snooping

DHCP Snooping helps protect a Layer 2 network against unauthorized DHCP servers by identifying trusted and untrusted interfaces.

### Trusted Interface

The interface connected toward the legitimate DHCP server is configured as trusted:

```cisco
ip dhcp snooping trust
```

In this lab:

```text
Fa0/1 → R1 → Trusted
```

### Untrusted Interface

Client-facing interfaces remain untrusted:

```text
Fa0/2 → PC1
Fa0/3 → PC2
```

### DHCP Binding Table

The switch dynamically records:

```text
MAC Address
IP Address
VLAN
Interface
Lease
```

This information can later be used by other Layer 2 security mechanisms.

### DHCP Rate Limiting

The client-facing interfaces were configured with:

```cisco
ip dhcp snooping limit rate 10
```

This limits the rate of DHCP messages accepted on those ports.

---

# 💼 Skills Demonstrated

* Cisco IOS configuration
* DHCP server configuration
* DHCP address management
* DHCP Snooping
* Layer 2 security
* Trusted/untrusted interfaces
* DHCP binding table analysis
* DHCP rate limiting
* VLAN security
* Network troubleshooting
* Packet Tracer simulation
* Connectivity testing
* Command-line verification
* Security feature compatibility analysis

---


