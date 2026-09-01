# 🌐 NetZero Lab 15 — Spanning Tree Protocol (STP) Loop Prevention

## 📌 Overview

**NetZero Lab 15** demonstrates the implementation and verification of **Spanning Tree Protocol (STP)** in a redundant Layer-2 switched network.

The lab uses a **triangle topology** between three switches. While the redundant links provide network resilience, they can create Layer-2 switching loops. STP automatically identifies the redundant path and places one port into a **Blocking** state to create a loop-free logical topology.

This lab focuses on understanding:

* Root Bridge election
* Root Port selection
* Alternate Port selection
* STP port states
* Path cost
* Layer-2 loop prevention
* Redundant network paths
* STP verification using Cisco IOS commands

---

## 🎯 Objectives

By completing this lab, the following concepts were demonstrated:

1. Understand the purpose of STP.
2. Configure and observe STP in a redundant topology.
3. Identify the Root Bridge.
4. Identify the Root Port.
5. Identify an Alternate Port.
6. Verify the Blocking and Forwarding states.
7. Understand how STP prevents Layer-2 loops.
8. Analyze STP path cost and port roles.
9. Verify STP operation using Cisco IOS commands.
10. Save the final switch configuration.

---

## 🏗️ Network Topology

The lab uses three switches connected in a triangular topology:

```text
                    +-------------+
                    |     SW1     |
                    | Root Bridge |
                    +-------------+
                     /           \
                    /             \
                   /               \
                  /                 \
          +-------------+     +-------------+
          |     SW2     |-----|     SW3     |
          +-------------+     +-------------+
                                  |
                              Fa0/2
                              BLOCKED
```

### Logical STP Topology

Although all three physical links remain connected, STP logically blocks the redundant path:

```text
                    SW1
                 ROOT BRIDGE
                  /       \
             FWD /         \ FWD
                /           \
              SW2-----------SW3
                           /
                     Fa0/2
                       BLK
```

The blocked port prevents Ethernet frames from continuously circulating around the triangle.

---

## 🧰 Technologies & Tools

| Technology          | Purpose                               |
| ------------------- | ------------------------------------- |
| Cisco Packet Tracer | Network simulation                    |
| Cisco IOS           | Switch configuration and verification |
| STP                 | Layer-2 loop prevention               |
| IEEE 802.1D         | Classic Spanning Tree Protocol        |
| Ethernet            | Layer-2 connectivity                  |

---

## 🖥️ Devices Used

| Device | Role                    |
| ------ | ----------------------- |
| SW1    | Root Bridge             |
| SW2    | Intermediate Switch     |
| SW3    | STP verification switch |

---

# ⚙️ STP Configuration

STP is enabled by default on the Cisco switches used in this lab.

The lab primarily focuses on **observing and analyzing the STP election process and resulting port roles**, rather than manually configuring STP priorities.

### Check STP status

```bash
show spanning-tree
```

This command displays:

* Root Bridge information
* Bridge ID
* Root Path Cost
* Root Port
* STP port roles
* STP port states

---

# 🔍 STP Verification

## SW3 — Spanning Tree Status

The following command was used:

```bash
SW3#show spanning-tree
```

The switch reported:

```text
Root ID    Priority    32769
           Address     0001.97A2.1964
           Cost        19
           Port        1(FastEthernet0/1)
```

### Interpretation

SW3 has identified the bridge with MAC address:

```text
0001.97A2.1964
```

as the **Root Bridge**.

SW3 reaches the Root Bridge through:

```text
Fa0/1
```

with a root path cost of:

```text
19
```

---

# 🚦 STP Port Roles on SW3

The original STP output showed:

```text
Interface        Role Sts Cost      Prio.Nbr Type
---------------- ---- --- --------- -------- --------------------------------
Fa0/2            Altn BLK 19        128.2    P2p
```

This confirms:

```text
Fa0/2 = Alternate Port
State  = Blocking
```

Therefore, **SW3 Fa0/2 is the blocked redundant path**.

---

# 🔎 Detailed Port Verification

## Fa0/2 — Alternate Blocking Port

Command:

```bash
SW3#show spanning-tree interface fa0/2
```

Output:

```text
Vlan             Role Sts Cost      Prio.Nbr Type
---------------- ---- --- --------- -------- --------------------------------
VLAN0001         Altn BLK 19        128.2     P2p
```

### Result

| Parameter | Value          |
| --------- | -------------- |
| VLAN      | VLAN0001       |
| Role      | Alternate      |
| State     | Blocking       |
| Cost      | 19             |
| Port ID   | 128.2          |
| Type      | Point-to-Point |

### Meaning

`Altn BLK` means **Alternate Blocking**.

Fa0/2 provides a redundant path toward the Root Bridge, but STP prevents it from forwarding traffic under normal conditions.

---

# 🔎 Fa0/1 — Root Forwarding Port

Command:

```bash
SW3#show spanning-tree interface fa0/1
```

Output:

```text
Vlan             Role Sts Cost      Prio.Nbr Type
---------------- ---- --- --------- -------- --------------------------------
VLAN0001         Root FWD 19        128.1     P2p
```

### Result

| Parameter | Value          |
| --------- | -------------- |
| VLAN      | VLAN0001       |
| Role      | Root           |
| State     | Forwarding     |
| Cost      | 19             |
| Port ID   | 128.1          |
| Type      | Point-to-Point |

### Meaning

`Root FWD` means **Root Port in Forwarding state**.

Fa0/1 is the preferred path from SW3 toward the Root Bridge.

---

# 🧠 Why Did STP Block Fa0/2?

The three switches form a physical Layer-2 triangle:

```text
        SW1
       /   \
      /     \
    SW2-----SW3
```

Without STP, this topology could create a switching loop.

For example:

```text
SW1 → SW2 → SW3 → SW1 → SW2 → SW3 → ...
```

Broadcast and unknown-unicast frames could circulate repeatedly.

This can lead to:

* Broadcast storms
* MAC table instability
* Excessive network traffic
* Network degradation
* Complete Layer-2 network failure

STP solves this by calculating a loop-free logical topology.

In this lab, SW3's:

```text
Fa0/1
```

was selected as the preferred path toward the Root Bridge.

The redundant:

```text
Fa0/2
```

was therefore placed into:

```text
Alternate / Blocking
```

state.

---

# 🌳 STP Logical Topology

### Physical topology

```text
             SW1
            /   \
           /     \
          /       \
        SW2-------SW3
```

### STP logical topology

```text
             SW1
          ROOT BRIDGE
            /     \
           /       \
        FWD         FWD
         /           \
       SW2           SW3
                       |
                     BLK
                       X
                     Fa0/2
```

STP has effectively transformed the physical triangle into a **loop-free tree**.

---

# 📊 STP Port Summary

| Switch | Port  | Role      | State      | Function                         |
| ------ | ----- | --------- | ---------- | -------------------------------- |
| SW3    | Fa0/1 | Root      | Forwarding | Best path toward Root Bridge     |
| SW3    | Fa0/2 | Alternate | Blocking   | Redundant path / loop prevention |

---

# 🔄 What Happens if the Active Path Fails?

One of the major advantages of having a redundant topology is **resiliency**.

The blocked path is not physically disconnected. STP keeps it available as an alternate path.

Conceptually:

```text
Normal Operation

SW3 Fa0/1
    ↓
Forwarding
    ↓
Root Bridge
```

If the active path fails:

```text
Fa0/1
  X
FAILURE
  ↓
STP recalculates
  ↓
Alternate path can become active
  ↓
Fa0/2
```

This allows the network to recover from certain link or device failures while maintaining Layer-2 connectivity.

---

# 🧪 Commands Used

### Display complete STP information

```bash
show spanning-tree
```

### Verify a specific STP interface

```bash
show spanning-tree interface fa0/1
```

```bash
show spanning-tree interface fa0/2
```

### Save configuration

```bash
copy running-config startup-config
```

---

# 🎓 Key Learning Outcomes

After completing NetZero Lab 15, the following STP concepts were demonstrated:

### 1. Root Bridge

STP elects a Root Bridge based on the lowest Bridge ID.

### 2. Root Port

Each non-root switch selects the best path toward the Root Bridge.

In this lab:

```text
SW3 Fa0/1 = Root Port
```

### 3. Alternate Port

A redundant path can become an Alternate Port.

In this lab:

```text
SW3 Fa0/2 = Alternate Port
```

### 4. Blocking State

The Alternate Port is placed into Blocking state to prevent a Layer-2 loop.

```text
Fa0/2 = BLK
```

### 5. Forwarding State

The Root Port continues forwarding traffic.

```text
Fa0/1 = FWD
```

### 6. Redundancy

The physical redundant connection remains available for network resilience.

---

# 🚀 Conclusion

**NetZero Lab 15** successfully demonstrated how **Spanning Tree Protocol** prevents Layer-2 loops in a redundant switched network.

The three-switch triangle provides physical redundancy, while STP creates a loop-free logical topology by selecting the best forwarding path and blocking the redundant path.

The final verification on SW3 confirmed:

```text
Fa0/1 → Root → Forwarding
Fa0/2 → Alternate → Blocking
```
