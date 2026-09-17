# 🔐 NetZero Lab 22 — PortFast & BPDU Guard

## 📌 Overview

This lab demonstrates the configuration of **Spanning Tree Protocol (STP) PortFast** and **BPDU Guard** on Cisco switch access ports.

PortFast allows end-device ports to transition directly to the forwarding state, reducing the time required for a host to obtain network connectivity.

BPDU Guard protects PortFast-enabled access ports by shutting down the port if an unexpected **Bridge Protocol Data Unit (BPDU)** is received.

These features are commonly used together to improve **Layer 2 network security and STP stability**.

---

## 🎯 Objectives

* Configure switch ports as access ports.
* Enable STP PortFast on end-device interfaces.
* Enable BPDU Guard on access ports.
* Verify PortFast operation.
* Verify BPDU Guard configuration.
* Verify STP forwarding state.
* Understand protection against unauthorized switch connections.
* Test and document Cisco Packet Tracer command limitations.

---

## 🖥️ Topology

```text
                 +------+
                 | SW1  |
                 +------+
                  |    |
               Fa0/1  Fa0/2
                  |    |
                 PC1  PC2
```

### Devices Used

* Cisco 2960 Switch — SW1
* PC1
* PC2
* Cisco Packet Tracer

---

## 📋 Port Configuration

| Switch Port | Connected Device | Mode   | PortFast | BPDU Guard |
| ----------- | ---------------- | ------ | -------- | ---------- |
| Fa0/1       | PC1              | Access | Enabled  | Enabled    |
| Fa0/2       | PC2              | Access | Enabled  | Enabled    |

---

# ⚙️ Configuration

## 1. Configure Access Ports

```cisco
enable
configure terminal

interface range fastEthernet0/1-2
switchport mode access
exit
```

This ensures that Fa0/1 and Fa0/2 operate as Layer 2 access ports.

---

## 2. Enable PortFast

```cisco
interface range fastEthernet0/1-2
spanning-tree portfast
exit
```

PortFast allows the access ports to transition quickly to the forwarding state.

### Verification

```cisco
show spanning-tree interface fa0/1 detail
```

Output confirmed:

```text
Port 1 (FastEthernet0/1) of VLAN0001 is designated forwarding

The port is in the portfast mode
```

Similarly, Fa0/2 showed:

```text
Port 2 (FastEthernet0/2) of VLAN0001 is designated forwarding

The port is in the portfast mode
```

---

## 3. Enable BPDU Guard

```cisco
interface range fastEthernet0/1-2
spanning-tree bpduguard enable
exit

end
```

BPDU Guard is configured individually on Fa0/1 and Fa0/2.

---

# 🔍 Verification

## PortFast Verification

Command:

```cisco
show spanning-tree interface fa0/1 detail
```

Result:

```text
Port 1 (FastEthernet0/1) of VLAN0001 is designated forwarding

Number of transitions to forwarding state: 1

The port is in the portfast mode
```

✅ PortFast is operational on Fa0/1.

---

Command:

```cisco
show spanning-tree interface fa0/2 detail
```

Result:

```text
Port 2 (FastEthernet0/2) of VLAN0001 is designated forwarding

Number of transitions to forwarding state: 1

The port is in the portfast mode
```

✅ PortFast is operational on Fa0/2.

---

# 🔎 STP Summary

Command:

```cisco
show spanning-tree summary
```

Observed:

```text
Switch is in pvst mode

Root bridge for: default

Portfast Default             is disabled
PortFast BPDU Guard Default  is disabled
Portfast BPDU Filter Default is disabled
```

### Important Note

`PortFast BPDU Guard Default is disabled` refers to the **global/default BPDU Guard setting**.

BPDU Guard was still configured directly on Fa0/1 and Fa0/2.

---

# 🧾 Running Configuration

Command:

```cisco
show running-config
```

Relevant configuration:

```cisco
interface FastEthernet0/1
 switchport mode access
 spanning-tree portfast
 spanning-tree bpduguard enable

interface FastEthernet0/2
 switchport mode access
 spanning-tree portfast
 spanning-tree bpduguard enable
```

This confirms that both access ports have:

* Access mode
* PortFast
* BPDU Guard

configured.

---

# 🔌 Interface Verification

Command:

```cisco
show interfaces fa0/1 status
```

Observed:

```text
Port      Name               Status       Vlan       Duplex  Speed Type

Fa0/1                        connected    1          a-full  a-100 10/100BaseTX
```

### Result

✅ Fa0/1 is connected and operational.

---

# ⚠️ Packet Tracer Limitation

The following command was attempted:

```cisco
show err-disabled
```

Packet Tracer returned:

```text
% Invalid input detected at '^' marker.
```

This command is not supported by the simulated switch IOS in this Packet Tracer environment.

Therefore, BPDU Guard status was verified through:

```cisco
show running-config
```

and the configured interface settings.

---

# 🧠 How PortFast + BPDU Guard Works

```text
             End Device
                 |
                 |
          +-------------+
          | Access Port |
          +-------------+
                 |
          ┌──────┴──────┐
          │             │
       PortFast      BPDU Guard
          │             │
          ▼             ▼
   Fast Forwarding   BPDU Protection
```

### PortFast

PortFast is designed for ports connected to end devices such as:

* PCs
* Printers
* Servers
* Other non-switch devices

It allows the port to move rapidly into the forwarding state.

### BPDU Guard

BPDU Guard protects a PortFast-enabled port from receiving BPDUs.

If a switch is accidentally or maliciously connected to such a port and sends BPDUs, BPDU Guard can place the interface into an **err-disabled** state.

---

# 🛡️ Security Benefits

PortFast + BPDU Guard helps:

* Prevent unauthorized switches from affecting STP.
* Reduce the possibility of Layer 2 topology manipulation.
* Protect the STP topology.
* Reduce unnecessary STP convergence delays on host ports.
* Improve access-layer security.

---

# 🧪 Verification Summary

| Test                      | Result                            |
| ------------------------- | --------------------------------- |
| Fa0/1 access mode         | ✅ Verified                        |
| Fa0/2 access mode         | ✅ Verified                        |
| PortFast Fa0/1            | ✅ Verified                        |
| PortFast Fa0/2            | ✅ Verified                        |
| BPDU Guard Fa0/1          | ✅ Configured                      |
| BPDU Guard Fa0/2          | ✅ Configured                      |
| Fa0/1 forwarding          | ✅ Verified                        |
| Fa0/2 forwarding          | ✅ Verified                        |
| PVST mode                 | ✅ Verified                        |
| Interface Fa0/1 connected | ✅ Verified                        |
| `show err-disabled`       | ⚠️ Not supported in Packet Tracer |

---

# 🧠 Key Commands Learned

### PortFast

```cisco
spanning-tree portfast
```

### BPDU Guard

```cisco
spanning-tree bpduguard enable
```

### Verification

```cisco
show spanning-tree interface fa0/1 detail
show spanning-tree interface fa0/2 detail
show spanning-tree summary
show interfaces fa0/1 status
show running-config
```

---

# 📚 Skills Demonstrated

* Cisco IOS configuration
* Spanning Tree Protocol (STP)
* PVST
* PortFast
* BPDU Guard
* Access-port security
* Layer 2 network security
* STP verification
* Cisco Packet Tracer troubleshooting

---

# 🎓 Key Learning

> **PortFast provides fast forwarding for end-device ports, while BPDU Guard protects those ports from unexpected STP BPDUs.**

Using both features together provides a practical Layer 2 security mechanism at the network access layer.

---
