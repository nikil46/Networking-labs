# 🔐 NetZero Lab 16 — Cisco Switch Port Security

## 📌 Overview

**NetZero Lab 16** demonstrates how to secure a Cisco switch access port using **Port Security**.

The lab focuses on restricting a switch port to a single authorized MAC address and demonstrating how the switch reacts when an unauthorized device attempts to access the secured port.

The lab covers:

* Port Security configuration
* Sticky MAC address learning
* Maximum MAC address limitation
* Security violation detection
* Shutdown violation mode
* Secure-shutdown state
* Port recovery
* Re-testing an unauthorized device
* Restoring the authorized device
* Configuration verification

---

## 🎯 Objectives

By completing this lab, the following networking concepts were practiced:

* Configure Cisco switch Port Security
* Restrict a switch port to one MAC address
* Dynamically learn an authorized MAC using sticky learning
* Configure violation mode as `shutdown`
* Detect an unauthorized MAC address
* Verify the Port Security violation counter
* Recover a shutdown interface
* Restore the authorized device
* Verify the final secure state
* Save the configuration

---

## 🧰 Technologies & Tools

| Technology                 | Purpose                                       |
| -------------------------- | --------------------------------------------- |
| Cisco Packet Tracer        | Network simulation                            |
| Cisco Catalyst 2960 Switch | Layer 2 switching                             |
| PC0                        | Unauthorized device used for security testing |
| PC1                        | Authorized device                             |
| Ethernet                   | End-device connectivity                       |
| Port Security              | Layer 2 access-port security                  |

---

## 🖥️ Network Topology

```text
                 ┌─────────────────┐
                 │      SW1        │
                 │  Cisco 2960     │
                 │                 │
                 │     Fa0/1       │
                 └────────┬────────┘
                          │
                ┌─────────┴─────────┐
                │                   │
             Authorized          Unauthorized
                PC1                  PC0
          MAC: 0060.4743.61C3   MAC: 0090.2153.4B57
```

### Port Assignment

| Device | Switch Port | Role                     |
| ------ | ----------- | ------------------------ |
| PC1    | Fa0/1       | Authorized device        |
| PC0    | Fa0/1       | Unauthorized test device |

---

# ⚙️ Configuration

## Step 1 — Enter Privileged EXEC Mode

```text
enable
```

## Step 2 — Enter Global Configuration Mode

```text
configure terminal
```

## Step 3 — Select the Access Port

```text
interface fa0/1
```

## Step 4 — Configure Port Security

The port was configured to allow only **one MAC address**:

```text
switchport mode access
switchport port-security
switchport port-security maximum 1
```

## Step 5 — Enable Sticky MAC Learning

```text
switchport port-security mac-address sticky
```

## Step 6 — Configure Violation Mode

The violation mode was configured as `shutdown`:

```text
switchport port-security violation shutdown
```

## Step 7 — Exit Configuration Mode

```text
exit
end
```

---

# 🔒 Final Port Security Configuration

The effective Port Security configuration on `Fa0/1` is:

```text
interface FastEthernet0/1
 switchport mode access
 switchport port-security
 switchport port-security maximum 1
 switchport port-security mac-address sticky
 switchport port-security violation shutdown
```

The authorized sticky MAC learned during the lab was:

```text
0060.4743.61C3
```

---

# 🔍 Verification — Authorized Device

After connecting PC1 to `Fa0/1`, Port Security was verified using:

```text
show port-security interface fa0/1
```

### Expected/Final Result

```text
Port Security              : Enabled
Port Status                : Secure-up
Violation Mode             : Shutdown
Aging Time                 : 0 mins
Aging Type                 : Absolute
SecureStatic Address Aging : Disabled
Maximum MAC Addresses      : 1
Total MAC Addresses        : 1
Configured MAC Addresses   : 0
Sticky MAC Addresses       : 1
Last Source Address:Vlan   : 0060.4743.61C3:1
Security Violation Count   : 0
```

### Interpretation

* **Port Security:** Enabled
* **Port Status:** Secure-up
* **Maximum MAC Addresses:** 1
* **Sticky MAC Addresses:** 1
* **Authorized MAC:** `0060.4743.61C3`
* **Security Violations:** 0

This confirms that PC1 is successfully authorized.

---

# 🚨 Security Violation Test

To test Port Security, PC1 was disconnected from `Fa0/1` and PC0 was connected to the same secured port.

PC0 has a different MAC address:

```text
0090.2153.4B57
```

Traffic was generated from PC0 to force the device to transmit frames through the secured port.

The switch detected the unauthorized MAC address.

Verification command:

```text
show port-security interface fa0/1
```

### Violation Result

```text
Port Status                : Secure-shutdown
Violation Mode             : Shutdown
Maximum MAC Addresses      : 1
Sticky MAC Addresses       : 1
Last Source Address:Vlan   : 0090.2153.4B57:1
Security Violation Count   : 1
```

### 🔴 Result

The security violation was successfully detected.

The switch:

1. Detected an unauthorized source MAC.
2. Compared it against the permitted sticky MAC.
3. Registered a security violation.
4. Incremented the violation counter to `1`.
5. Placed `Fa0/1` into `Secure-shutdown`.

---

# ♻️ Port Recovery

After the violation, `Fa0/1` was manually recovered using:

```text
enable
configure terminal
interface fa0/1
shutdown
no shutdown
exit
end
```

The interface was then verified:

```text
show interfaces status
```

Result:

```text
Fa0/1    connected    1    a-full    a-100
```

Port Security was also verified:

```text
show port-security interface fa0/1
```

The port returned to:

```text
Port Status : Secure-up
```

---

# 🔁 Re-Test of Unauthorized Device

PC0 was connected to the secured port again and traffic was generated.

The switch once again detected PC0's unauthorized MAC address:

```text
0090.2153.4B57
```

The resulting state was:

```text
Port Status                : Secure-shutdown
Security Violation Count   : 1
Last Source Address:Vlan   : 0090.2153.4B57:1
```

This confirmed that **Port Security remained active after interface recovery**.

---

# ✅ Restoration of Authorized Device

PC0 was disconnected and PC1 was reconnected to `Fa0/1`.

The original authorized MAC address was:

```text
0060.4743.61C3
```

After generating traffic from PC1, the port was verified again.

### Final Verification

```text
Port Status                : Secure-up
Maximum MAC Addresses      : 1
Sticky MAC Addresses       : 1
Last Source Address:Vlan   : 0060.4743.61C3:1
Security Violation Count   : 0
```

This confirms that the authorized PC1 device was successfully restored.

---

# 🧪 Verification Commands

The following commands were used throughout the lab:

### Check MAC Address Table

```text
show mac address-table
```

### Check Interface Status

```text
show interfaces status
```

### Check Interface Details

```text
show interfaces fa0/1
```

### Check Port Security

```text
show port-security interface fa0/1
```

### Check Interface Configuration

```text
show running-config interface fa0/1
```

### Save Configuration

```text
copy running-config startup-config
```

---

# 📊 Test Results

| Test                         | Expected Result           | Status   |
| ---------------------------- | ------------------------- | -------- |
| PC1 connected                | Secure-up                 | ✅ Passed |
| Sticky MAC learned           | `0060.4743.61C3`          | ✅ Passed |
| Maximum MAC addresses        | 1                         | ✅ Passed |
| PC0 connected                | Unauthorized MAC detected | ✅ Passed |
| Security violation           | Counter = 1               | ✅ Passed |
| Violation mode               | Shutdown                  | ✅ Passed |
| Port shutdown                | Secure-shutdown           | ✅ Passed |
| Interface recovery           | Secure-up                 | ✅ Passed |
| Unauthorized PC tested again | Violation detected        | ✅ Passed |
| PC1 restored                 | Secure-up                 | ✅ Passed |
| Final violation count        | 0                         | ✅ Passed |

---

# 🧠 Key Concepts Learned

## 1. Port Security

Port Security is a Layer 2 switch security feature that controls which MAC addresses are allowed to communicate through a switch port.

---

## 2. Sticky MAC Address

Sticky MAC learning allows the switch to dynamically learn the MAC address of a connected device and treat it as a secure address.

In this lab:

```text
0060.4743.61C3
```

was the authorized sticky MAC address.

---

## 3. Maximum MAC Address Limit

The port was configured to allow only:

```text
Maximum MAC Addresses : 1
```

Therefore, a second different MAC address causes a security violation.

---

## 4. Shutdown Violation Mode

The port was configured with:

```text
switchport port-security violation shutdown
```

When an unauthorized MAC address was detected, the switch placed the interface into:

```text
Secure-shutdown
```

This provides strong protection against unauthorized devices being connected to the access port.

---

## 5. Security Violation Counter

The command:

```text
show port-security interface fa0/1
```

can be used to identify security violations.

During the test:

```text
Security Violation Count : 1
```

confirmed that the unauthorized PC had triggered Port Security.

---

# 💼 Real-World Applications

Port Security can be used in enterprise networks to:

* Prevent unauthorized devices from accessing wired networks
* Restrict access to sensitive switch ports
* Reduce the risk of rogue devices
* Limit the number of devices connected to an access port
* Protect against unauthorized MAC addresses
* Improve Layer 2 network security
* Enforce endpoint access policies

Typical deployment scenarios include:

* Office access ports
* University/college networks
* Server rooms
* Network labs
* Data centers
* Enterprise wired LANs

---

# ⚠️ Important Operational Consideration

Using:

```text
switchport port-security violation shutdown
```

provides strong protection, but it can also cause legitimate devices to lose connectivity if their MAC address changes or if an unauthorized device is connected.

In production networks, administrators should therefore combine Port Security with proper endpoint management, monitoring, and documented recovery procedures.

---
```

---

# 🏁 Conclusion

**NetZero Lab 16** successfully demonstrated Cisco switch Port Security using sticky MAC learning and shutdown violation mode.

The lab successfully showed the complete security lifecycle:

```text
Authorized Device
       ↓
Sticky MAC Learning
       ↓
Unauthorized Device
       ↓
MAC Violation Detected
       ↓
Security Violation Count = 1
       ↓
Port → Secure-shutdown
       ↓
Interface Recovery
       ↓
Authorized Device Restored
       ↓
Port → Secure-up
```

The final state confirmed that **PC1's MAC address ****0060.4743.61C3**** was authorized**, while unauthorized devices were successfully blocked.

---

## 🚀 NetZero Networking Series

This lab is part of the **NetZero Networking Lab Series**, a hands-on Cisco networking project focused on building practical networking, switching, routing, security, and infrastructure skills through Cisco Packet Tracer.

### Skills demonstrated so far

* Basic Switching
* VLANs
* Inter-VLAN Routing
* Static Routing
* DHCP
* NAT/PAT
* ACLs
* RIP
* OSPF
* EIGRP
* Layer 3 Switching
* EtherChannel/LACP
* **Switch Port Security 🔐**

---

